#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包名修改工具 - 主程序
功能：
1. 修改 build.gradle 中的包名（namespace 和 applicationId）
2. 拷贝 keystore 文件到 app 目录，修改签名配置
3. 拷贝 UniApp 资源文件夹到 assets/apps 目录
4. 修改 dcloud_control.xml 中的 appid
5. 修改 strings.xml 中的 app_name
6. 修改 AndroidManifest.xml 中的 dcloud_appkey

使用方法：
1. 先修改 package_config.py 中的配置
2. 运行此脚本：python3 change_package.py
"""

import os
import re
import shutil
from package_config import (
    SIGN_CONFIG_INDEX,
    ANDROID_PROJECT_PATH,
    UNIAPP_SOURCE_PATH,
    SIGN_CONFIGS,
)


def print_step(step_num, message):
    """打印步骤信息"""
    print("")
    print("=" * 60)
    print(f"步骤 {step_num}: {message}")
    print("=" * 60)


def print_success(message):
    """打印成功信息"""
    print(f"✅ {message}")


def print_error(message):
    """打印错误信息"""
    print(f"❌ {message}")


def print_info(message):
    """打印普通信息"""
    print(f"   {message}")


def get_current_config():
    """获取当前选择的签名配置"""
    # 检查序号是否有效
    if SIGN_CONFIG_INDEX < 1 or SIGN_CONFIG_INDEX > len(SIGN_CONFIGS):
        print_error(f"签名配置序号无效: {SIGN_CONFIG_INDEX}，有效范围: 1-{len(SIGN_CONFIGS)}")
        return None

    # 获取配置（序号从1开始，列表索引从0开始）
    config = SIGN_CONFIGS[SIGN_CONFIG_INDEX - 1]
    return config


def step1_modify_build_gradle(config):
    """
    步骤1：修改 build.gradle 中的包名
    - 修改 namespace
    - 修改 applicationId
    """
    print_step(1, "修改 build.gradle 中的包名")

    # build.gradle 文件路径
    build_gradle_path = os.path.join(ANDROID_PROJECT_PATH, "app", "build.gradle")

    # 检查文件是否存在
    if not os.path.exists(build_gradle_path):
        print_error(f"文件不存在: {build_gradle_path}")
        return False

    # 读取文件内容
    with open(build_gradle_path, "r", encoding="utf-8") as f:
        content = f.read()

    package_name = config["package_name"]
    print_info(f"新包名: {package_name}")

    # 修改 namespace
    # 匹配: namespace 'xxx' 或 namespace "xxx"
    old_content = content
    content = re.sub(
        r"namespace\s+['\"]([^'\"]+)['\"]",
        f"namespace '{package_name}'",
        content
    )
    if content != old_content:
        print_success("已修改 namespace")
    else:
        print_info("namespace 未找到或已是目标值")

    # 修改 applicationId
    # 匹配: applicationId "xxx" 或 applicationId 'xxx'
    old_content = content
    content = re.sub(
        r"applicationId\s+['\"]([^'\"]+)['\"]",
        f'applicationId "{package_name}"',
        content
    )
    if content != old_content:
        print_success("已修改 applicationId")
    else:
        print_info("applicationId 未找到或已是目标值")

    # 写回文件
    with open(build_gradle_path, "w", encoding="utf-8") as f:
        f.write(content)

    print_success("build.gradle 修改完成")
    return True


def step2_copy_keystore_and_modify_signing(config):
    """
    步骤2：拷贝 keystore 文件并修改签名配置
    - 拷贝 keystore 文件到 app 目录
    - 修改 build.gradle 中的 signingConfigs
    """
    print_step(2, "拷贝 keystore 并修改签名配置")

    # 1. 拷贝 keystore 文件
    keystore_source = config["keystore_source_path"]
    keystore_dest = os.path.join(ANDROID_PROJECT_PATH, "app", config["store_file"])

    # 检查源文件是否存在
    if not os.path.exists(keystore_source):
        print_error(f"keystore 源文件不存在: {keystore_source}")
        return False

    # 拷贝文件
    shutil.copy2(keystore_source, keystore_dest)
    print_success(f"已拷贝 keystore: {config['store_file']}")

    # 2. 修改 build.gradle 中的签名配置
    build_gradle_path = os.path.join(ANDROID_PROJECT_PATH, "app", "build.gradle")

    with open(build_gradle_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 构建新的签名配置
    new_signing_config = f"""signingConfigs {{
        config {{
            keyAlias '{config["key_alias"]}'
            keyPassword '{config["key_password"]}'
            storeFile file('{config["store_file"]}')
            storePassword '{config["store_password"]}'
            v1SigningEnabled true
            v2SigningEnabled true
        }}
    }}"""

    # 替换签名配置
    # 匹配 signingConfigs { ... } 块
    pattern = r"signingConfigs\s*\{[^}]*config\s*\{[^}]*\}[^}]*\}"

    old_content = content
    content = re.sub(pattern, new_signing_config, content, flags=re.DOTALL)

    if content != old_content:
        print_success("已修改 signingConfigs")
    else:
        print_info("signingConfigs 未找到或格式不匹配")

    # 写回文件
    with open(build_gradle_path, "w", encoding="utf-8") as f:
        f.write(content)

    print_success("签名配置修改完成")
    return True


def step3_copy_uniapp_resources():
    """
    步骤3：拷贝 UniApp 资源文件夹
    - 删除 assets/apps 目录下的所有内容
    - 拷贝 UniApp 文件夹到 assets/apps 目录
    """
    print_step(3, "拷贝 UniApp 资源文件夹")

    # 目标目录
    apps_dir = os.path.join(ANDROID_PROJECT_PATH, "app", "src", "main", "assets", "apps")

    # 检查源文件夹是否存在
    if not os.path.exists(UNIAPP_SOURCE_PATH):
        print_error(f"UniApp 源文件夹不存在: {UNIAPP_SOURCE_PATH}")
        return False

    # 获取 UniApp 文件夹名称（如 __UNI__0D35F8F）
    uniapp_folder_name = os.path.basename(UNIAPP_SOURCE_PATH)
    print_info(f"UniApp 文件夹名称: {uniapp_folder_name}")

    # 1. 删除 apps 目录下的所有内容
    if os.path.exists(apps_dir):
        # 遍历删除所有子文件夹和文件
        for item in os.listdir(apps_dir):
            item_path = os.path.join(apps_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print_info(f"已删除文件夹: {item}")
            else:
                os.remove(item_path)
                print_info(f"已删除文件: {item}")
        print_success("已清空 apps 目录")
    else:
        # 创建 apps 目录
        os.makedirs(apps_dir)
        print_info("已创建 apps 目录")

    # 2. 拷贝 UniApp 文件夹
    dest_path = os.path.join(apps_dir, uniapp_folder_name)
    shutil.copytree(UNIAPP_SOURCE_PATH, dest_path)
    print_success(f"已拷贝 UniApp 资源到: {dest_path}")

    return True


def step4_modify_dcloud_control():
    """
    步骤4：修改 dcloud_control.xml 中的 appid
    - 获取 UniApp 文件夹名称
    - 替换 dcloud_control.xml 中的 appid
    """
    print_step(4, "修改 dcloud_control.xml 中的 appid")

    # dcloud_control.xml 文件路径
    control_xml_path = os.path.join(
        ANDROID_PROJECT_PATH, "app", "src", "main", "assets", "data", "dcloud_control.xml"
    )

    # 检查文件是否存在
    if not os.path.exists(control_xml_path):
        print_error(f"文件不存在: {control_xml_path}")
        return False

    # 获取 UniApp 文件夹名称
    uniapp_folder_name = os.path.basename(UNIAPP_SOURCE_PATH)
    print_info(f"新的 appid: {uniapp_folder_name}")

    # 读取文件内容
    with open(control_xml_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换 appid
    # 匹配: appid="__UNI__XXXXXX"
    old_content = content
    content = re.sub(
        r'appid="([^"]*)"',
        f'appid="{uniapp_folder_name}"',
        content
    )

    if content != old_content:
        print_success(f"已将 appid 修改为: {uniapp_folder_name}")
    else:
        print_info("appid 未找到或已是目标值")

    # 写回文件
    with open(control_xml_path, "w", encoding="utf-8") as f:
        f.write(content)

    print_success("dcloud_control.xml 修改完成")
    return True


def step5_modify_app_name(config):
    """
    步骤5：修改 strings.xml 中的 app_name
    """
    print_step(5, "修改 strings.xml 中的 app_name")

    # strings.xml 文件路径
    strings_xml_path = os.path.join(
        ANDROID_PROJECT_PATH, "app", "src", "main", "res", "values", "strings.xml"
    )

    # 检查文件是否存在
    if not os.path.exists(strings_xml_path):
        print_error(f"文件不存在: {strings_xml_path}")
        return False

    # 获取 app 名称
    app_name = config["name"]
    print_info(f"新的 app_name: {app_name}")

    # 读取文件内容
    with open(strings_xml_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换 app_name
    # 匹配: <string name="app_name">xxx</string>
    old_content = content
    content = re.sub(
        r'(<string name="app_name">)[^<]*(</string>)',
        f'\\g<1>{app_name}\\g<2>',
        content
    )

    if content != old_content:
        print_success(f"已将 app_name 修改为: {app_name}")
    else:
        print_info("app_name 未找到或已是目标值")

    # 写回文件
    with open(strings_xml_path, "w", encoding="utf-8") as f:
        f.write(content)

    print_success("strings.xml 修改完成")
    return True


def step6_modify_manifest_appkey(config):
    """
    步骤6：修改 AndroidManifest.xml 中的 dcloud_appkey
    """
    print_step(6, "修改 AndroidManifest.xml 中的 dcloud_appkey")

    # AndroidManifest.xml 文件路径
    manifest_path = os.path.join(
        ANDROID_PROJECT_PATH, "app", "src", "main", "AndroidManifest.xml"
    )

    # 检查文件是否存在
    if not os.path.exists(manifest_path):
        print_error(f"文件不存在: {manifest_path}")
        return False

    # 获取 dcloud_appkey
    dcloud_appkey = config["dcloud_appkey"]
    print_info(f"新的 dcloud_appkey: {dcloud_appkey}")

    # 读取文件内容
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 替换 dcloud_appkey
    # 匹配: android:name="dcloud_appkey" 后面的 android:value="xxx"
    old_content = content

    # 使用正则匹配 meta-data 标签中的 dcloud_appkey
    pattern = r'(<meta-data[^>]*android:name="dcloud_appkey"[^>]*android:value=")[^"]*(")'
    replacement = f'\\g<1>{dcloud_appkey}\\g<2>'
    content = re.sub(pattern, replacement, content)

    # 如果上面的模式没匹配到，尝试另一种顺序
    if content == old_content:
        pattern = r'(<meta-data[^>]*android:value=")[^"]*("[^>]*android:name="dcloud_appkey")'
        replacement = f'\\g<1>{dcloud_appkey}\\g<2>'
        content = re.sub(pattern, replacement, content)

    if content != old_content:
        print_success(f"已将 dcloud_appkey 修改为: {dcloud_appkey}")
    else:
        print_info("dcloud_appkey 未找到或已是目标值")

    # 写回文件
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(content)

    print_success("AndroidManifest.xml 修改完成")
    return True


def main():
    """主函数"""
    print("")
    print("=" * 60)
    print("Android 包名修改工具")
    print("=" * 60)

    # 显示当前配置
    print("")
    print("当前配置:")
    print(f"  签名配置序号: {SIGN_CONFIG_INDEX}")
    print(f"  工程路径: {ANDROID_PROJECT_PATH}")
    print(f"  UniApp 资源路径: {UNIAPP_SOURCE_PATH}")

    # 获取签名配置
    config = get_current_config()
    if config is None:
        return

    print("")
    print(f"选择的签名配置: {config['name']}")
    print(f"  包名: {config['package_name']}")
    print(f"  keystore: {config['store_file']}")
    print(f"  dcloud_appkey: {config['dcloud_appkey']}")

    # 检查工程路径是否存在
    if not os.path.exists(ANDROID_PROJECT_PATH):
        print_error(f"工程路径不存在: {ANDROID_PROJECT_PATH}")
        return

    # 执行各步骤
    success = True

    # 步骤1：修改包名
    if not step1_modify_build_gradle(config):
        success = False

    # 步骤2：拷贝 keystore 并修改签名配置
    if not step2_copy_keystore_and_modify_signing(config):
        success = False

    # 步骤3：拷贝 UniApp 资源
    if not step3_copy_uniapp_resources():
        success = False

    # 步骤4：修改 dcloud_control.xml
    if not step4_modify_dcloud_control():
        success = False

    # 步骤5：修改 app_name
    if not step5_modify_app_name(config):
        success = False

    # 步骤6：修改 AndroidManifest.xml
    if not step6_modify_manifest_appkey(config):
        success = False

    # 打印结果
    print("")
    print("=" * 60)
    if success:
        print("✅ 所有步骤执行完成！")
    else:
        print("⚠️ 部分步骤执行失败，请检查上面的错误信息")
    print("=" * 60)
    print("")


if __name__ == "__main__":
    main()
