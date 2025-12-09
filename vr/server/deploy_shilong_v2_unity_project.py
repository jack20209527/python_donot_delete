#!/usr/bin/env python3
"""
Unity Library 部署脚本
功能：将新生成的 unityLibrary 部署到项目工程中，并合并旧库的自定义内容。

执行步骤：
1. 重命名原有的 unityLibrary 为 unityLibrary2（备份）
2. 拷贝新的 unityLibrary 到目标目录
3. 清空新库 libs 文件夹中的所有文件和文件夹
4. 合并 build.gradle 文件：将旧库的 android{} 闭包及以上的代码替换到新库中
5. 注释新库 AndroidManifest.xml 中的 <activity>...</activity> 标签
6. 替换 com 包内容：删除新库 com/ 下所有内容，拷贝旧库 com/ 下所有内容到新库
"""

import os
import re
import sys
import shutil

# 导入 FileUtils 中的工具函数
from utils.FileUtils import (
    copy_file_to_folder,
    copy_new_folder_into_existing_folder,
    rename_folder,
    delete_folder
)


# ==================== 配置路径 ====================
# 原有库的父目录
original_library_dir = "/Users/sun2022/pro/pico_pro/android_uniapp/android_shilong_v2/"
# 原有的 unityLibrary 路径
original_library_path = "/Users/sun2022/pro/pico_pro/android_uniapp/android_shilong_v2/unityLibrary"

# 新生成的 unityLibrary 路径
new_library_path = "/Users/sun2022/pro/pro_android_unity/yzgame/yzgame/good1/unityLibrary"
# ==================================================


def log_step(step_num: int, description: str):
    """打印步骤日志"""
    print(f"\n{'='*60}")
    print(f"📌 步骤 {step_num}: {description}")
    print(f"{'='*60}")


def log_success(message: str):
    """打印成功日志"""
    print(f"✅ {message}")


def log_error(message: str):
    """打印错误日志"""
    print(f"❌ {message}")


def log_info(message: str):
    """打印信息日志"""
    print(f"💡 {message}")


def extract_content_up_to_first_android_block(gradle_content: str) -> str:
    """
    从 build.gradle 内容中提取从文件开头到第一个 android {} 闭包结束的所有内容。

    算法：
    1. 找到第一个 'android {' 的位置
    2. 从该位置开始，通过计数大括号来找到对应的闭合 '}'
    3. 返回从文件开头到该闭合 '}' 的所有内容

    参数:
        gradle_content (str): build.gradle 的完整内容

    返回:
        str: 从文件开头到第一个 android {} 闭包结束的内容
    """
    # 找到第一个 'android {' 或 'android{' 的位置
    # 使用正则匹配 android 后面跟着可选空白和 {
    match = re.search(r'android\s*\{', gradle_content)

    if not match:
        return ""

    # 从 android { 的 { 位置开始计数
    start_brace_pos = match.end() - 1  # { 的位置

    # 计数大括号，找到匹配的闭合 }
    brace_count = 0
    end_pos = start_brace_pos

    for i in range(start_brace_pos, len(gradle_content)):
        char = gradle_content[i]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos = i
                break

    # 返回从开头到闭合 } 的内容（包括 }）
    return gradle_content[:end_pos + 1]


def extract_content_after_first_android_block(gradle_content: str) -> str:
    """
    从 build.gradle 内容中提取第一个 android {} 闭包结束之后的所有内容。

    参数:
        gradle_content (str): build.gradle 的完整内容

    返回:
        str: 第一个 android {} 闭包结束之后的内容
    """
    # 找到第一个 'android {' 或 'android{' 的位置
    match = re.search(r'android\s*\{', gradle_content)

    if not match:
        return gradle_content

    # 从 android { 的 { 位置开始计数
    start_brace_pos = match.end() - 1  # { 的位置

    # 计数大括号，找到匹配的闭合 }
    brace_count = 0
    end_pos = start_brace_pos

    for i in range(start_brace_pos, len(gradle_content)):
        char = gradle_content[i]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos = i
                break

    # 返回闭合 } 之后的内容
    return gradle_content[end_pos + 1:]


def comment_activity_block(manifest_content: str) -> str:
    """
    将 AndroidManifest.xml 内容中的 <activity>...</activity> 标签块用 XML 注释包裹。

    参数:
        manifest_content (str): AndroidManifest.xml 的完整内容

    返回:
        str: 处理后的 AndroidManifest.xml 内容
    """
    # 使用正则表达式匹配 <activity 开始到 </activity> 结束的内容
    # re.DOTALL 让 . 匹配换行符
    pattern = r'(<activity[^>]*>.*?</activity>)'

    def replace_with_comment(match):
        activity_block = match.group(1)
        # 用 XML 注释包裹
        return f"<!--\n{activity_block}\n-->"

    result = re.sub(pattern, replace_with_comment, manifest_content, flags=re.DOTALL)
    return result


def step1_rename_original_library() -> str:
    """
    步骤1: 重命名原有的 unityLibrary 为 unityLibrary2

    返回:
        str: 重命名后的路径，失败返回空字符串
    """
    log_step(1, "重命名原有的 unityLibrary 为 unityLibrary2")

    # 检查原有库是否存在
    if not os.path.exists(original_library_path):
        log_error(f"原有库不存在: {original_library_path}")
        return ""

    log_info(f"原有库路径: {original_library_path}")

    # 执行重命名
    new_path = rename_folder(original_library_path, "unityLibrary2")

    if new_path:
        log_success(f"重命名成功: {original_library_path} -> {new_path}")
        return new_path
    else:
        log_error("重命名失败")
        return ""


def step2_copy_new_library() -> bool:
    """
    步骤2: 拷贝新的 unityLibrary 到目标目录

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(2, "拷贝新的 unityLibrary 到目标目录")

    # 检查新库是否存在
    if not os.path.exists(new_library_path):
        log_error(f"新库不存在: {new_library_path}")
        return False

    log_info(f"新库路径: {new_library_path}")
    log_info(f"目标目录: {original_library_dir}")

    # 执行拷贝
    result = copy_new_folder_into_existing_folder(original_library_dir, new_library_path)

    if result:
        log_success("新库拷贝成功")
        return True
    else:
        log_error("新库拷贝失败")
        return False


def step3_clean_libs_folder() -> bool:
    """
    步骤3: 清空新库 libs 文件夹中的所有文件和文件夹（保留 unity-classes.jar）

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(3, "清空新库 libs 文件夹（保留 unity-classes.jar）")

    # 需要保留的文件
    keep_files = ["unity-classes.jar"]

    # 构造路径
    libs_path = os.path.join(original_library_dir, "unityLibrary/libs")

    log_info(f"libs 文件夹路径: {libs_path}")
    log_info(f"保留文件: {keep_files}")

    # 检查 libs 文件夹是否存在
    if not os.path.exists(libs_path):
        log_error(f"libs 文件夹不存在: {libs_path}")
        return False

    try:
        deleted_count = 0
        skipped_count = 0
        for item in os.listdir(libs_path):
            item_path = os.path.join(libs_path, item)

            # 检查是否需要保留
            if item in keep_files:
                print(f"  ⏭️ 保留文件: {item}")
                skipped_count += 1
                continue

            # 删除文件或文件夹
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"  🗑️ 删除文件: {item}")
                deleted_count += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"  🗑️ 删除文件夹: {item}")
                deleted_count += 1

        log_success(f"libs 文件夹清理完成，删除 {deleted_count} 个，保留 {skipped_count} 个")
        return True

    except Exception as e:
        log_error(f"清空 libs 文件夹时发生错误: {e}")
        return False


def step4_merge_build_gradle(unity_library2_path: str) -> bool:
    """
    步骤4: 合并 build.gradle 文件
    将旧库（unityLibrary2）的 android{} 闭包及以上的代码替换到新库（unityLibrary）中

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(4, "合并 build.gradle 文件")

    # 构造文件路径
    old_gradle_path = os.path.join(unity_library2_path, "build.gradle")
    new_gradle_path = os.path.join(original_library_dir, "unityLibrary/build.gradle")

    log_info(f"旧 build.gradle: {old_gradle_path}")
    log_info(f"新 build.gradle: {new_gradle_path}")

    # 检查文件是否存在
    if not os.path.exists(old_gradle_path):
        log_error(f"旧 build.gradle 不存在: {old_gradle_path}")
        return False

    if not os.path.exists(new_gradle_path):
        log_error(f"新 build.gradle 不存在: {new_gradle_path}")
        return False

    try:
        # 读取旧 build.gradle
        with open(old_gradle_path, 'r', encoding='utf-8') as f:
            old_gradle_content = f.read()

        # 读取新 build.gradle
        with open(new_gradle_path, 'r', encoding='utf-8') as f:
            new_gradle_content = f.read()

        # 提取旧文件中从开头到第一个 android {} 闭包结束的内容
        old_header_and_android = extract_content_up_to_first_android_block(old_gradle_content)

        if not old_header_and_android:
            log_error("无法从旧 build.gradle 中提取 android {} 闭包")
            return False

        log_info("成功提取旧 build.gradle 中的 android {} 闭包及以上内容")

        # 提取新文件中第一个 android {} 闭包之后的内容
        new_after_android = extract_content_after_first_android_block(new_gradle_content)

        log_info("成功提取新 build.gradle 中 android {} 闭包之后的内容")

        # 合并：旧的头部和android闭包 + 新的android闭包之后的内容
        merged_content = old_header_and_android + new_after_android

        # 写入新 build.gradle
        with open(new_gradle_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)

        log_success("build.gradle 合并成功")
        return True

    except Exception as e:
        log_error(f"合并 build.gradle 时发生错误: {e}")
        return False


def step5_comment_activity_in_manifest() -> bool:
    """
    步骤5: 注释新库 AndroidManifest.xml 中的 <activity>...</activity> 标签

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(5, "注释 AndroidManifest.xml 中的 <activity> 标签")

    # 构造清单文件路径
    manifest_path = os.path.join(original_library_dir, "unityLibrary/src/main/AndroidManifest.xml")

    log_info(f"清单文件路径: {manifest_path}")

    # 检查文件是否存在
    if not os.path.exists(manifest_path):
        log_error(f"清单文件不存在: {manifest_path}")
        return False

    try:
        # 读取清单文件
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()

        # 注释 activity 标签块
        modified_content = comment_activity_block(manifest_content)

        # 写入清单文件
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        log_success("AndroidManifest.xml 中的 <activity> 标签已注释")
        return True

    except Exception as e:
        log_error(f"注释 AndroidManifest.xml 时发生错误: {e}")
        return False


def step6_replace_com_folder(unity_library2_path: str) -> bool:
    """
    步骤6: 替换 com 包内容
    删除新库 com/ 下所有内容，拷贝旧库 com/ 下所有内容到新库

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(6, "替换 com 包内容")

    # 构造路径
    new_com_path = os.path.join(original_library_dir, "unityLibrary/src/main/java/com")
    old_com_path = os.path.join(unity_library2_path, "src/main/java/com")

    log_info(f"新库 com 文件夹: {new_com_path}")
    log_info(f"旧库 com 文件夹: {old_com_path}")

    # 检查路径是否存在
    if not os.path.exists(new_com_path):
        log_error(f"新库 com 文件夹不存在: {new_com_path}")
        return False

    if not os.path.exists(old_com_path):
        log_error(f"旧库 com 文件夹不存在: {old_com_path}")
        return False

    try:
        # 步骤6.1: 删除新库 com/ 下所有内容（不删除 com 文件夹本身）
        log_info("正在删除新库 com/ 下所有内容...")
        deleted_count = 0
        for item in os.listdir(new_com_path):
            item_path = os.path.join(new_com_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"  🗑️ 删除文件: {item}")
                deleted_count += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"  🗑️ 删除文件夹: {item}")
                deleted_count += 1
        log_info(f"已删除 {deleted_count} 个文件/文件夹")

        # 步骤6.2: 拷贝旧库 com/ 下所有内容到新库 com/
        log_info("正在拷贝旧库 com/ 下所有内容到新库...")
        copied_count = 0
        for item in os.listdir(old_com_path):
            src_path = os.path.join(old_com_path, item)
            dst_path = os.path.join(new_com_path, item)

            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"  📄 拷贝文件: {item}")
                copied_count += 1
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
                print(f"  📁 拷贝文件夹: {item}")
                copied_count += 1

        log_success(f"com 包内容替换完成，共拷贝 {copied_count} 个文件/文件夹")
        return True

    except Exception as e:
        log_error(f"替换 com 包内容时发生错误: {e}")
        return False


def main():
    """
    主函数：按顺序执行所有部署步骤
    """
    print("\n" + "="*60)
    print("🚀 Unity Library 部署脚本开始执行")
    print("="*60)

    print(f"\n📁 配置信息:")
    print(f"   原有库父目录: {original_library_dir}")
    print(f"   原有库路径: {original_library_path}")
    print(f"   新库路径: {new_library_path}")

    # 步骤1: 重命名原有库
    unity_library2_path = step1_rename_original_library()
    if not unity_library2_path:
        log_error("步骤1失败，脚本终止")
        sys.exit(1)

    # 步骤2: 拷贝新库
    if not step2_copy_new_library():
        log_error("步骤2失败，脚本终止")
        sys.exit(1)

    # 步骤3: 清空 libs 文件夹
    if not step3_clean_libs_folder():
        log_error("步骤3失败，脚本终止")
        sys.exit(1)

    # 步骤4: 合并 build.gradle
    if not step4_merge_build_gradle(unity_library2_path):
        log_error("步骤4失败，脚本终止")
        sys.exit(1)

    # 步骤5: 注释 AndroidManifest.xml 中的 activity 标签
    if not step5_comment_activity_in_manifest():
        log_error("步骤5失败，脚本终止")
        sys.exit(1)

    # 步骤6: 替换 com 包内容
    if not step6_replace_com_folder(unity_library2_path):
        log_error("步骤6失败，脚本终止")
        sys.exit(1)

    print("\n" + "="*60)
    print("🎉 Unity Library 部署完成！")
    print("="*60)
    print(f"\n📋 部署结果:")
    print(f"   ✅ 原有库已备份为: {unity_library2_path}")
    print(f"   ✅ 新库已部署到: {os.path.join(original_library_dir, 'unityLibrary')}")
    print(f"   ✅ 已清空 libs 文件夹")
    print(f"   ✅ 已合并 build.gradle 文件")
    print(f"   ✅ 已注释 AndroidManifest.xml 中的 <activity> 标签")
    print(f"   ✅ 已替换 com 包内容")


if __name__ == '__main__':
    main()
