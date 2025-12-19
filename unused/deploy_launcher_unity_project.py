#!/usr/bin/env python3
"""
Unity Library 部署脚本
功能：将新生成的 unityLibrary 部署到项目工程中，并合并旧库的自定义内容。

执行步骤：
1. 重命名原有的 unityLibrary 为 unityLibrary2
2. 拷贝新的 unityLibrary 到目标目录
3. 合并 AndroidManifest.xml 中的 <activity> 标签内容
4. 拷贝 unityLibrary2 中的 com.draw.sdk 文件夹到新库
5. 拷贝 unityLibrary2 中的 com.unity3d.player 包下的所有文件到新库
6. 拷贝 unityLibrary2 中的 res/layout 文件夹到新库
7. 拷贝 unityLibrary2 中的 res/values/strings.xml 到新库
8. 清理新库的 libs 文件夹，只保留 unity-classes.jar，其他文件和文件夹都会被删除
9. 合并 build.gradle 文件：将旧库的 android{} 闭包及以上的代码替换到新库中。
    step9_merge_build_gradle() - 合并逻辑：
    从旧文件提取：开头 + android{} 闭包
    从新文件提取：android{} 闭包之后的内容
    合并：旧的头部和android闭包 + 新的android闭包之后的内容
"""

# 这个脚本是用来部署launcher工程的
# 路径: /Users/sun2022/pro/pro_android_unity/Android_Launcher_Unity

import os
import re
import sys

# 导入 FileUtils 中的工具函数
from utils.FileUtils import (
    copy_file_to_folder,
    copy_new_folder_into_existing_folder,
    rename_folder,
    delete_folder
)


# ==================== 配置路径 ====================
# 原有库的父目录
original_library_dir = "/Users/sun2022/Downloads/deploy_library/"
# 原有的 unityLibrary 路径
original_library_path = "/Users/sun2022/Downloads/deploy_library/unityLibrary"
# 新生成的 unityLibrary 路径
new_library_path = "/Users/sun2022/pro/pro_android_unity/unity_lib_source/yzgame1/good2/good5/unityLibrary"
# ================================================


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



def extract_activity_block(manifest_content: str) -> str:
    """
    从 AndroidManifest.xml 内容中提取 <activity>...</activity> 标签块。

    参数:
        manifest_content (str): AndroidManifest.xml 的完整内容

    返回:
        str: 提取的 activity 标签块内容（包括开始和结束标签行）
    """
    # 使用正则表达式匹配 <activity 开始到 </activity> 结束的内容
    # re.DOTALL 让 . 匹配换行符
    pattern = r'(<activity[^>]*>.*?</activity>)'
    match = re.search(pattern, manifest_content, re.DOTALL)

    if match:
        return match.group(1)
    else:
        return ""


def replace_activity_block(manifest_content: str, new_activity_block: str) -> str:
    """
    替换 AndroidManifest.xml 内容中的 <activity>...</activity> 标签块。

    参数:
        manifest_content (str): 原始 AndroidManifest.xml 的完整内容
        new_activity_block (str): 要替换的新 activity 标签块内容

    返回:
        str: 替换后的 AndroidManifest.xml 内容
    """
    pattern = r'<activity[^>]*>.*?</activity>'
    result = re.sub(pattern, new_activity_block, manifest_content, flags=re.DOTALL)
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


def step3_merge_android_manifest(unity_library2_path: str) -> bool:
    """
    步骤3: 合并 AndroidManifest.xml 中的 <activity> 标签内容

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(3, "合并 AndroidManifest.xml 中的 <activity> 标签内容")

    # 构造清单文件路径
    old_manifest_path = os.path.join(unity_library2_path, "src/main/AndroidManifest.xml")
    new_manifest_path = os.path.join(original_library_path, "src/main/AndroidManifest.xml")

    log_info(f"旧清单文件: {old_manifest_path}")
    log_info(f"新清单文件: {new_manifest_path}")

    # 检查文件是否存在
    if not os.path.exists(old_manifest_path):
        log_error(f"旧清单文件不存在: {old_manifest_path}")
        return False

    if not os.path.exists(new_manifest_path):
        log_error(f"新清单文件不存在: {new_manifest_path}")
        return False

    try:
        # 读取旧清单文件
        with open(old_manifest_path, 'r', encoding='utf-8') as f:
            old_manifest_content = f.read()

        # 读取新清单文件
        with open(new_manifest_path, 'r', encoding='utf-8') as f:
            new_manifest_content = f.read()

        # 提取旧清单中的 activity 标签块
        old_activity_block = extract_activity_block(old_manifest_content)

        if not old_activity_block:
            log_error("无法从旧清单文件中提取 <activity> 标签块")
            return False

        log_info("成功提取旧清单中的 <activity> 标签块")

        # 替换新清单中的 activity 标签块
        merged_content = replace_activity_block(new_manifest_content, old_activity_block)

        # 写入新清单文件
        with open(new_manifest_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)

        log_success("AndroidManifest.xml 合并成功")
        return True

    except Exception as e:
        log_error(f"合并 AndroidManifest.xml 时发生错误: {e}")
        return False


def step4_copy_draw_folder(unity_library2_path: str) -> bool:
    """
    步骤4: 拷贝 unityLibrary2 中的 com.draw.sdk 文件夹到新库

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(4, "拷贝 com.draw.sdk 文件夹到新库")

    # 构造路径 (com.draw.sdk 对应目录结构 com/draw/sdk)
    source_draw_path = os.path.join(unity_library2_path, "src/main/java/com/draw")
    target_com_path = os.path.join(original_library_dir, "unityLibrary/src/main/java/com")

    log_info(f"源 draw 文件夹: {source_draw_path}")
    log_info(f"目标 com 文件夹: {target_com_path}")

    # 检查源文件夹是否存在
    if not os.path.exists(source_draw_path):
        log_error(f"源 draw 文件夹不存在: {source_draw_path}")
        return False

    # 执行拷贝
    result = copy_new_folder_into_existing_folder(target_com_path, source_draw_path)

    if result:
        log_success("draw 文件夹拷贝成功")
        return True
    else:
        log_error("draw 文件夹拷贝失败")
        return False


def step5_copy_player_folder(unity_library2_path: str) -> bool:
    """
    步骤5: 拷贝 unityLibrary2 中的 com.unity3d.player 整个文件夹到新库（包括所有文件和子文件夹）

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(5, "拷贝 com.unity3d.player 整个文件夹到新库")

    # 构造路径 (com.unity3d.player 对应目录结构 com/unity3d/player)
    source_player_path = os.path.join(unity_library2_path, "src/main/java/com/unity3d/player")
    target_unity3d_path = os.path.join(original_library_dir, "unityLibrary/src/main/java/com/unity3d")

    log_info(f"源 player 文件夹: {source_player_path}")
    log_info(f"目标 unity3d 文件夹: {target_unity3d_path}")

    # 检查源文件夹是否存在
    if not os.path.exists(source_player_path):
        log_error(f"源 player 文件夹不存在: {source_player_path}")
        return False

    # 执行拷贝（拷贝整个 player 文件夹，包括所有文件和子文件夹）
    result = copy_new_folder_into_existing_folder(target_unity3d_path, source_player_path)

    if result:
        log_success("player 文件夹拷贝成功")
        return True
    else:
        log_error("player 文件夹拷贝失败")
        return False


def step6_copy_layout_folder(unity_library2_path: str) -> bool:
    """
    步骤6: 拷贝 unityLibrary2 中的 res/layout 文件夹到新库

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(6, "拷贝 res/layout 文件夹到新库")

    # 构造路径
    source_layout_path = os.path.join(unity_library2_path, "src/main/res/layout")
    target_res_path = os.path.join(original_library_dir, "unityLibrary/src/main/res")

    log_info(f"源 layout 文件夹: {source_layout_path}")
    log_info(f"目标 res 文件夹: {target_res_path}")

    # 检查源文件夹是否存在
    if not os.path.exists(source_layout_path):
        log_error(f"源 layout 文件夹不存在: {source_layout_path}")
        return False

    # 执行拷贝
    result = copy_new_folder_into_existing_folder(target_res_path, source_layout_path)

    if result:
        log_success("layout 文件夹拷贝成功")
        return True
    else:
        log_error("layout 文件夹拷贝失败")
        return False


def step7_copy_strings_xml(unity_library2_path: str) -> bool:
    """
    步骤7: 拷贝 unityLibrary2 中的 res/values/strings.xml 到新库

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(7, "拷贝 res/values/strings.xml 到新库")

    # 构造路径
    source_strings_path = os.path.join(unity_library2_path, "src/main/res/values/strings.xml")
    target_values_path = os.path.join(original_library_dir, "unityLibrary/src/main/res/values")

    log_info(f"源 strings.xml 文件: {source_strings_path}")
    log_info(f"目标 values 文件夹: {target_values_path}")

    # 检查源文件是否存在
    if not os.path.exists(source_strings_path):
        log_error(f"源 strings.xml 文件不存在: {source_strings_path}")
        return False

    # 执行拷贝
    result = copy_file_to_folder(source_strings_path, target_values_path)

    if result:
        log_success("strings.xml 文件拷贝成功")
        return True
    else:
        log_error("strings.xml 文件拷贝失败")
        return False


def step8_clean_libs_folder() -> bool:
    """
    步骤8: 清理新库 libs 文件夹，只保留 unity-classes.jar

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(8, "清理 libs 文件夹，只保留 unity-classes.jar")

    # 构造路径
    libs_path = os.path.join(original_library_dir, "unityLibrary/libs")
    keep_file = "unity-classes.jar"

    log_info(f"libs 文件夹路径: {libs_path}")
    log_info(f"保留的文件: {keep_file}")

    # 检查 libs 文件夹是否存在
    if not os.path.exists(libs_path):
        log_error(f"libs 文件夹不存在: {libs_path}")
        return False

    try:
        deleted_count = 0
        for item in os.listdir(libs_path):
            item_path = os.path.join(libs_path, item)

            # 跳过要保留的文件
            if item == keep_file:
                log_info(f"保留文件: {item}")
                continue

            # 删除其他文件或文件夹
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"  🗑️ 删除文件: {item}")
                deleted_count += 1
            elif os.path.isdir(item_path):
                import shutil
                shutil.rmtree(item_path)
                print(f"  🗑️ 删除文件夹: {item}")
                deleted_count += 1

        log_success(f"libs 文件夹清理完成，共删除 {deleted_count} 个文件/文件夹")
        return True

    except Exception as e:
        log_error(f"清理 libs 文件夹时发生错误: {e}")
        return False


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


def step9_merge_build_gradle(unity_library2_path: str) -> bool:
    """
    步骤9: 合并 build.gradle 文件
    将旧库（unityLibrary2）的 android{} 闭包及以上的代码替换到新库（unityLibrary）中

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(9, "合并 build.gradle 文件")

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

    # 步骤3: 合并 AndroidManifest.xml
    if not step3_merge_android_manifest(unity_library2_path):
        log_error("步骤3失败，脚本终止")
        sys.exit(1)

    # 步骤4: 拷贝 draw 文件夹
    if not step4_copy_draw_folder(unity_library2_path):
        log_error("步骤4失败，脚本终止")
        sys.exit(1)

    # 步骤5: 拷贝 player 文件夹
    if not step5_copy_player_folder(unity_library2_path):
        log_error("步骤5失败，脚本终止")
        sys.exit(1)

    # 步骤6: 拷贝 layout 文件夹
    if not step6_copy_layout_folder(unity_library2_path):
        log_error("步骤6失败，脚本终止")
        sys.exit(1)

    # 步骤7: 拷贝 strings.xml
    if not step7_copy_strings_xml(unity_library2_path):
        log_error("步骤7失败，脚本终止")
        sys.exit(1)

    # 步骤8: 清理 libs 文件夹
    if not step8_clean_libs_folder():
        log_error("步骤8失败，脚本终止")
        sys.exit(1)

    # 步骤9: 合并 build.gradle
    if not step9_merge_build_gradle(unity_library2_path):
        log_error("步骤9失败，脚本终止")
        sys.exit(1)

    print("\n" + "="*60)
    print("🎉 Unity Library 部署完成！")
    print("="*60)
    print(f"\n📋 部署结果:")
    print(f"   ✅ 原有库已备份为: {unity_library2_path}")
    print(f"   ✅ 新库已部署到: {os.path.join(original_library_dir, 'unityLibrary')}")
    print(f"   ✅ 已合并 AndroidManifest.xml 中的 <activity> 配置")
    print(f"   ✅ 已拷贝 com.draw.sdk 文件夹")
    print(f"   ✅ 已拷贝 com.unity3d.player 文件夹")
    print(f"   ✅ 已拷贝 res/layout 文件夹")
    print(f"   ✅ 已拷贝 res/values/strings.xml 文件")
    print(f"   ✅ 已清理 libs 文件夹，只保留 unity-classes.jar")
    print(f"   ✅ 已合并 build.gradle 文件")


if __name__ == '__main__':
    main()
