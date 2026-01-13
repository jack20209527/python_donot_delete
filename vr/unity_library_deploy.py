#!/usr/bin/env python3

"""
/Users/sun2022/pro/pro_android_unity/yzgame/yzgame/good3
Unity Library 部署脚本
功能：将新生成的 unityLibrary 部署到项目工程中，并合并旧库的自定义内容。

执行步骤：
0. 如果已经存在 unityLibrary2 了，就先给这个删掉
1. 重命名原有的 unityLibrary 为 unityLibrary2（备份）
2. 拷贝新的 unityLibrary 到目标目录
3. 整理libs文件:
    (1)在新拷贝过来的的unityLibrary中，删除unitylibrary-debug.aar和rtmp-client-3.2.0.aar
    (2)保留unity-classes.jar不动
    (3)剪切其余的jar文件和aar文件到我给你的original_app_libs_dir这个变量指定的目录下，也就是可以先给original_app_libs_dir路径下的你需要剪切的文件删除，再给需要剪切的文件拷贝过来
4. 给 library2 中的 build.gradle的全部内容 整体拷贝到 library中的build.gradle文件中
5. 替换新库 unityLibrary AndroidManifest.xml 文件：删除原文件，从 android_manifest_xml_path 拷贝新文件
6. 替换 com 包内容：删除新库 com/ 下所有内容，拷贝旧库 com/ 下所有内容到新库

"""

import os
import sys
import shutil

# 导入 FileUtils 中的工具函数
from utils.FileUtils import (
    copy_file_to_folder,
    copy_new_folder_into_existing_folder,
    rename_folder,
    delete_folder
)

#==================================================
is_online_old_manifest_config = 1 # 1: 线上配置配置，干净的没有蓝牙的配置；   0: 新配置，有蓝牙配置，

android_manifest_xml_path = "/Users/sun2022/Downloads/公司/configs/manifest_online/AndroidManifest.xml"
if (is_online_old_manifest_config != 1) :
    android_manifest_xml_path = "/Users/sun2022/Downloads/公司/configs/manifest_new_all/AndroidManifest.xml"

# ==================== 配置路径 ====================
# 配置的时候，注意最后面的斜杠，保持原样吧
# 原有库的父目录
original_library_dir = "/Users/sun2022/pro/pico_pro/yz_test_branch/yzandroid/"
# 原有的 unityLibrary 路径
original_library_path = "/Users/sun2022/pro/pico_pro/yz_test_branch/yzandroid/unityLibrary"
# app 中的 libs，需要覆盖一些 aar
original_app_libs_dir = "/Users/sun2022/pro/pico_pro/yz_test_branch/yzandroid/app/libs/"

# # 原有库的父目录
# original_library_dir = "/Users/sun2022/Downloads/local_android/yzandroid/"
# # 原有的 unityLibrary 路径
# original_library_path = "/Users/sun2022/Downloads/local_android/yzandroid/unityLibrary"
# # app 中的 libs，需要覆盖一些 aar
# original_app_libs_dir = "/Users/sun2022/Downloads/local_android/yzandroid/app/libs/"

# # 原有库的父目录
# original_library_dir = "/Users/sun2022/pro/pico_pro/yz_main/yzandroid/"
# # 原有的 unityLibrary 路径
# original_library_path = "/Users/sun2022/pro/pico_pro/yz_main/yzandroid/unityLibrary"
# # app 中的 libs，需要覆盖一些 aar
# original_app_libs_dir = "/Users/sun2022/pro/pico_pro/yz_main/yzandroid/app/libs/"

# 新生成的 unityLibrary 路径
new_library_path = "/Users/sun2022/pro/pro_android_unity/yzgame/yzgame/good3/unityLibrary"

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


def step0_cleanup_old_unity_library2() -> bool:
    """
    步骤0: 清理旧的 unityLibrary2 文件夹
    检查 original_library_dir 下是否存在 unityLibrary2 文件夹，如果存在则删除

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(0, "清理旧的 unityLibrary2 文件夹")

    # 构造 unityLibrary2 路径
    unity_library2_path = os.path.join(original_library_dir, "unityLibrary2")

    log_info(f"检查路径: {unity_library2_path}")

    # 检查文件夹是否存在
    if not os.path.exists(unity_library2_path):
        log_info("unityLibrary2 文件夹不存在，无需清理")
        return True

    # 文件夹存在，删除它
    try:
        log_info("正在删除 unityLibrary2 文件夹及其所有内容...")
        shutil.rmtree(unity_library2_path)
        log_success(f"unityLibrary2 文件夹已删除: {unity_library2_path}")
        return True
    except Exception as e:
        log_error(f"删除 unityLibrary2 文件夹失败: {e}")
        return False

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


def step3_organize_libs_folder() -> bool:
    """
    步骤3: 整理 libs 文件夹
    1. 删除 unitylibrary-debug.aar
    2. 保留 unity-classes.jar
    3. 剪切其余的 jar 和 aar 文件到 app/libs/

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(3, "整理 libs 文件夹")

    # 构造路径
    new_libs_path = os.path.join(original_library_dir, "unityLibrary/libs")

    log_info(f"新库 libs 文件夹路径: {new_libs_path}")
    log_info(f"app libs 目标路径: {original_app_libs_dir}")

    # 检查 libs 文件夹是否存在
    if not os.path.exists(new_libs_path):
        log_error(f"新库 libs 文件夹不存在: {new_libs_path}")
        return False

    # 检查 app/libs 目录是否存在，不存在则创建
    if not os.path.exists(original_app_libs_dir):
        try:
            os.makedirs(original_app_libs_dir)
            log_info(f"创建 app/libs 目录: {original_app_libs_dir}")
        except Exception as e:
            log_error(f"创建 app/libs 目录失败: {e}")
            return False

    try:
        # 需要保留的文件
        keep_files = ["unity-classes.jar"]
        # 需要删除的文件
        delete_files = ["unitylibrary-debug.aar", "rtmp-client-3.2.0.aar"]
        # 需要剪切的文件类型
        cut_extensions = [".jar", ".aar"]

        deleted_count = 0
        kept_count = 0
        cut_count = 0

        # 第一步：删除和保留文件，收集需要剪切的文件
        files_to_cut = []

        for item in os.listdir(new_libs_path):
            item_path = os.path.join(new_libs_path, item)

            # 跳过文件夹
            if os.path.isdir(item_path):
                continue

            # 检查是否需要删除
            if item in delete_files:
                try:
                    os.remove(item_path)
                    print(f"  🗑️ 删除文件: {item}")
                    deleted_count += 1
                except Exception as e:
                    log_error(f"删除文件 {item} 失败: {e}")
                    return False
                continue

            # 检查是否需要保留
            if item in keep_files:
                print(f"  ⏭️ 保留文件: {item}")
                kept_count += 1
                continue

            # 检查是否需要剪切（jar 或 aar 文件）
            if any(item.endswith(ext) for ext in cut_extensions):
                files_to_cut.append((item, item_path))

        log_info(f"删除了 {deleted_count} 个文件，保留了 {kept_count} 个文件")

        # 第二步：只删除 app/libs 中需要被覆盖的文件（同名文件）
        log_info("正在删除 app/libs 中需要被覆盖的文件...")
        old_files_deleted = 0

        for filename, _ in files_to_cut:
            old_file_path = os.path.join(original_app_libs_dir, filename)
            if os.path.exists(old_file_path):
                try:
                    os.remove(old_file_path)
                    print(f"  🗑️ 删除旧文件: {filename}")
                    old_files_deleted += 1
                except Exception as e:
                    log_error(f"删除旧文件 {filename} 失败: {e}")
                    return False

        log_info(f"已删除 {old_files_deleted} 个需要被覆盖的文件")

        # 第三步：剪切新的 jar 和 aar 文件到 app/libs
        log_info("正在剪切文件到 app/libs...")

        for filename, src_path in files_to_cut:
            dst_path = os.path.join(original_app_libs_dir, filename)
            try:
                shutil.move(src_path, dst_path)
                print(f"  ✂️ 剪切文件: {filename}")
                cut_count += 1
            except Exception as e:
                log_error(f"剪切文件 {filename} 失败: {e}")
                return False

        log_success(f"libs 文件夹整理完成，删除 {deleted_count} 个，保留 {kept_count} 个，剪切 {cut_count} 个")
        return True

    except Exception as e:
        log_error(f"整理 libs 文件夹时发生错误: {e}")
        return False


def step4_replace_build_gradle(unity_library2_path: str) -> bool:
    """
    步骤4: 全量替换 build.gradle 文件
    将 unityLibrary2 的 build.gradle 完整内容拷贝到 unityLibrary 的 build.gradle

    参数:
        unity_library2_path (str): unityLibrary2 的路径

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(4, "全量替换 build.gradle 文件")

    # 构造文件路径
    old_gradle_path = os.path.join(unity_library2_path, "build.gradle")
    new_gradle_path = os.path.join(original_library_dir, "unityLibrary/build.gradle")

    log_info(f"源 build.gradle: {old_gradle_path}")
    log_info(f"目标 build.gradle: {new_gradle_path}")

    # 检查文件是否存在
    if not os.path.exists(old_gradle_path):
        log_error(f"源 build.gradle 不存在: {old_gradle_path}")
        return False

    if not os.path.exists(new_gradle_path):
        log_error(f"目标 build.gradle 不存在: {new_gradle_path}")
        return False

    try:
        # 读取源 build.gradle
        with open(old_gradle_path, 'r', encoding='utf-8') as f:
            old_gradle_content = f.read()

        # 直接写入目标 build.gradle（全量替换）
        with open(new_gradle_path, 'w', encoding='utf-8') as f:
            f.write(old_gradle_content)

        log_success("build.gradle 全量替换成功")
        return True

    except Exception as e:
        log_error(f"替换 build.gradle 时发生错误: {e}")
        return False


def step5_comment_activity_in_manifest() -> bool:
    """
    步骤5: 替换 AndroidManifest.xml 文件
    删除原有的 AndroidManifest.xml，从 android_manifest_xml_path 拷贝新文件

    返回:
        bool: 成功返回 True，失败返回 False
    """
    log_step(5, "替换 AndroidManifest.xml 文件")

    # 构造清单文件路径
    manifest_path = os.path.join(original_library_dir, "unityLibrary/src/main/AndroidManifest.xml")

    log_info(f"目标清单文件路径: {manifest_path}")
    log_info(f"源清单文件路径: {android_manifest_xml_path}")

    # 检查源文件是否存在
    if not os.path.exists(android_manifest_xml_path):
        log_error(f"源清单文件不存在: {android_manifest_xml_path}")
        return False

    # 检查目标文件是否存在，如果存在则删除
    if os.path.exists(manifest_path):
        try:
            log_info("正在删除原有的 AndroidManifest.xml 文件...")
            os.remove(manifest_path)
            print(f"  🗑️ 删除文件: {manifest_path}")
        except Exception as e:
            log_error(f"删除原有清单文件失败: {e}")
            return False

    try:
        # 拷贝新的清单文件
        log_info("正在拷贝新的 AndroidManifest.xml 文件...")
        shutil.copy2(android_manifest_xml_path, manifest_path)
        print(f"  📄 拷贝文件: {android_manifest_xml_path} -> {manifest_path}")
        log_success("AndroidManifest.xml 文件替换成功")
        return True

    except Exception as e:
        log_error(f"替换 AndroidManifest.xml 时发生错误: {e}")
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
    print(f"   app libs 目录: {original_app_libs_dir}")

    # 步骤0: 清理旧的 unityLibrary2
    if not step0_cleanup_old_unity_library2():
        log_error("步骤0失败，脚本终止")
        sys.exit(1)

    # 步骤1: 重命名原有库
    unity_library2_path = step1_rename_original_library()
    if not unity_library2_path:
        log_error("步骤1失败，脚本终止")
        sys.exit(1)

    # 步骤2: 拷贝新库
    if not step2_copy_new_library():
        log_error("步骤2失败，脚本终止")
        sys.exit(1)

    # 步骤3: 整理 libs 文件夹
    if not step3_organize_libs_folder():
        log_error("步骤3失败，脚本终止")
        sys.exit(1)

    # 步骤4: 全量替换 build.gradle
    if not step4_replace_build_gradle(unity_library2_path):
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
    print(f"   ✅ 已整理 libs 文件夹（删除 debug.aar，剪切其他到 app/libs）")
    print(f"   ✅ 已全量替换 build.gradle 文件")
    print(f"   ✅ 已替换 AndroidManifest.xml 文件")
    print(f"   ✅ 已替换 com 包内容")


if __name__ == '__main__':
    main()
