#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unity 蓝牙 SDK 打包脚本
将 unitybluetoothsdk + bluetoothlibrary + commonlibrary 打包成一个 fat AAR

使用方法:
    在 PyCharm 中直接运行，或者命令行执行:
    python3 build_unity_sdk.py

输出:
    unity_bluetooth_sdk_v{version}.aar
"""

import os
import shutil
import subprocess
import zipfile
import tempfile
from datetime import datetime

# ==================== 配置区域 ====================

# Android 工程根目录
ANDROID_PROJECT_PATH = "/Users/sun2022/Downloads/local_android/yzandroid"

# SDK 版本号
VERSION = "1.0.0"

# 输出目录（相对于 Android 工程根目录）
OUTPUT_DIR_NAME = "unity_sdk_output"

# 需要合并的模块列表（按依赖顺序）
MODULES = ["commonlibrary", "bluetoothlibrary", "myunitylibrary", "unitybluetoothsdk"]

# ==================== 配置区域结束 ====================


def get_output_dir():
    """获取输出目录的绝对路径"""
    return os.path.join(ANDROID_PROJECT_PATH, OUTPUT_DIR_NAME)


def run_command(cmd, cwd=None):
    """执行命令"""
    print(f"执行: {cmd}")
    print(f"工作目录: {cwd}")

    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False

    return True


def check_project():
    """检查 Android 工程是否存在"""
    print("\n=== 步骤 0: 检查工程 ===")

    if not os.path.exists(ANDROID_PROJECT_PATH):
        print(f"错误: Android 工程目录不存在: {ANDROID_PROJECT_PATH}")
        return False

    gradlew_path = os.path.join(ANDROID_PROJECT_PATH, "gradlew")
    if not os.path.exists(gradlew_path):
        print(f"错误: gradlew 不存在: {gradlew_path}")
        return False

    # 检查各模块是否存在
    for module in MODULES:
        module_path = os.path.join(ANDROID_PROJECT_PATH, module)
        if not os.path.exists(module_path):
            print(f"错误: 模块目录不存在: {module_path}")
            return False

    print(f"工程检查通过: {ANDROID_PROJECT_PATH}")
    return True


def build_modules():
    """编译所有模块"""
    print("\n=== 步骤 1: 编译模块 ===")

    for module in MODULES:
        print(f"\n编译 {module}...")
        cmd = f"./gradlew :{module}:assembleRelease"
        if not run_command(cmd, cwd=ANDROID_PROJECT_PATH):
            print(f"编译 {module} 失败")
            return False

    print("\n所有模块编译成功")
    return True


def merge_aars():
    """合并 AAR 文件"""
    print("\n=== 步骤 2: 合并 AAR ===")

    output_dir = get_output_dir()

    # 创建输出目录
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    merged_dir = os.path.join(temp_dir, "merged")
    os.makedirs(merged_dir)

    print(f"临时目录: {temp_dir}")

    # 解压并合并所有 AAR
    for module in MODULES:
        aar_path = os.path.join(
            ANDROID_PROJECT_PATH,
            module,
            "build",
            "outputs",
            "aar",
            f"{module}-release.aar"
        )

        if not os.path.exists(aar_path):
            print(f"找不到 AAR: {aar_path}")
            return False

        print(f"\n处理 {module}...")
        print(f"  AAR 路径: {aar_path}")

        # 解压 AAR
        module_dir = os.path.join(temp_dir, module)
        with zipfile.ZipFile(aar_path, 'r') as zip_ref:
            zip_ref.extractall(module_dir)

        # 合并 classes.jar
        classes_jar = os.path.join(module_dir, "classes.jar")
        if os.path.exists(classes_jar):
            # 解压 classes.jar 到合并目录
            classes_dir = os.path.join(merged_dir, "classes")
            os.makedirs(classes_dir, exist_ok=True)
            with zipfile.ZipFile(classes_jar, 'r') as zip_ref:
                zip_ref.extractall(classes_dir)
            print(f"  合并 classes.jar 完成")

        # 复制其他文件（AndroidManifest.xml, res, jni 等）
        for item in os.listdir(module_dir):
            src = os.path.join(module_dir, item)
            dst = os.path.join(merged_dir, item)

            if item == "classes.jar":
                continue
            elif item == "AndroidManifest.xml" and module == "unitybluetoothsdk":
                # 使用主模块的 AndroidManifest.xml
                shutil.copy2(src, dst)
                print(f"  使用 {module} 的 AndroidManifest.xml")
            elif os.path.isdir(src):
                if os.path.exists(dst):
                    # 合并目录
                    for sub_item in os.listdir(src):
                        sub_src = os.path.join(src, sub_item)
                        sub_dst = os.path.join(dst, sub_item)
                        if os.path.isdir(sub_src):
                            if os.path.exists(sub_dst):
                                shutil.copytree(sub_src, sub_dst, dirs_exist_ok=True)
                            else:
                                shutil.copytree(sub_src, sub_dst)
                        else:
                            shutil.copy2(sub_src, sub_dst)
                else:
                    shutil.copytree(src, dst)

    # 重新打包 classes.jar
    classes_dir = os.path.join(merged_dir, "classes")
    if os.path.exists(classes_dir):
        merged_classes_jar = os.path.join(merged_dir, "classes.jar")
        with zipfile.ZipFile(merged_classes_jar, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(classes_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, classes_dir)
                    zipf.write(file_path, arcname)

        # 删除临时 classes 目录
        shutil.rmtree(classes_dir)
        print(f"\n重新打包 classes.jar 完成")

    # 创建最终的 AAR
    output_aar = os.path.join(output_dir, f"unity_bluetooth_sdk_v{VERSION}.aar")
    with zipfile.ZipFile(output_aar, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(merged_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, merged_dir)
                zipf.write(file_path, arcname)

    # 清理临时目录
    shutil.rmtree(temp_dir)

    # 获取文件大小
    file_size = os.path.getsize(output_aar)
    file_size_mb = file_size / (1024 * 1024)

    print(f"\n合并完成!")
    print(f"  输出文件: {output_aar}")
    print(f"  文件大小: {file_size_mb:.2f} MB")

    return True


def copy_single_aars():
    """同时复制单独的 AAR 文件（备用）"""
    print("\n=== 步骤 3: 复制单独的 AAR（备用） ===")

    output_dir = get_output_dir()
    single_dir = os.path.join(output_dir, "single_aars")
    os.makedirs(single_dir, exist_ok=True)

    for module in MODULES:
        aar_path = os.path.join(
            ANDROID_PROJECT_PATH,
            module,
            "build",
            "outputs",
            "aar",
            f"{module}-release.aar"
        )

        if os.path.exists(aar_path):
            dst = os.path.join(single_dir, f"{module}-release.aar")
            shutil.copy2(aar_path, dst)
            print(f"  复制: {module}-release.aar")

    print(f"\n单独的 AAR 文件已复制到: {single_dir}")


def main():
    print("=" * 60)
    print("Unity 蓝牙 SDK 打包工具")
    print("=" * 60)
    print(f"版本: {VERSION}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Android 工程: {ANDROID_PROJECT_PATH}")
    print(f"输出目录: {get_output_dir()}")
    print("=" * 60)

    # 检查工程
    if not check_project():
        print("\n工程检查失败，退出")
        return

    # 编译模块
    if not build_modules():
        print("\n编译失败，退出")
        return

    # 合并 AAR
    if not merge_aars():
        print("\n合并失败，退出")
        return

    # 复制单独的 AAR（备用）
    copy_single_aars()

    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)
    print(f"\n输出目录: {get_output_dir()}")
    print(f"\n文件列表:")
    print(f"  1. unity_bluetooth_sdk_v{VERSION}.aar  (合并后的 fat AAR)")
    print(f"  2. single_aars/                        (单独的 AAR 文件)")
    print("\n给 Unity 团队使用时，推荐使用合并后的 fat AAR")
    print("=" * 60)


if __name__ == "__main__":
    main()
