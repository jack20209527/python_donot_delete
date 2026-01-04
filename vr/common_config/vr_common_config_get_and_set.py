#!/usr/bin/env python3
"""
通用配置管理脚本
功能：上传和获取服务器上的配置文件

使用方式：
    # 上传 launcher 配置
    python config_manager.py set launcher

    # 获取 launcher 配置
    python config_manager.py get launcher

    # 下载 launcher 配置中的所有图标
    python config_manager.py download launcher
"""

import os
import sys
import json
import requests
import importlib

# ==================== 配置 ====================
# https://linkprohub.top/vr/get_config?name=launcher_config
# 服务器地址
BASE_URL = "https://linkprohub.top"

# 接口地址（通用接口，需要 name 参数）
SET_CONFIG_URL = f"{BASE_URL}/vr/set_config_post"  # POST 方式，name 在 URL 参数中
GET_CONFIG_URL = f"{BASE_URL}/vr/get_config"       # GET 方式，name 在 URL 参数中

# ==================================================

def log_info(msg: str):
    print(f"💡 {msg}")


def log_success(msg: str):
    print(f"✅ {msg}")


def log_error(msg: str):
    print(f"❌ {msg}")


def load_config_module(config_name: str):
    """
    动态加载配置文件模块

    :param config_name: 配置名称，如 "launcher" 对应 config_content_launcher.py
    :return: 配置模块，失败返回 None
    """
    module_name = f"config_content_{config_name}"
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError as e:
        log_error(f"找不到配置文件: {module_name}.py")
        log_error(f"请确保文件存在: config_content_{config_name}.py")
        return None


def set_config(config_name: str):
    """
    上传配置文件到服务器

    :param config_name: 配置名称，如 "launcher"
    """
    print(f"\n{'='*50}")
    print(f"📤 上传配置: {config_name}")
    print(f"{'='*50}")

    # 加载配置模块
    module = load_config_module(config_name)
    if not module:
        return False

    # 获取配置数据
    config_data = getattr(module, "CONFIG_DATA", None)
    if config_data is None:
        log_error(f"配置模块中没有 CONFIG_DATA 变量")
        return False

    # 发送请求
    url = f"{SET_CONFIG_URL}?name={config_name}"
    log_info(f"请求地址: {url}")
    log_info(f"配置内容: {json.dumps(config_data, ensure_ascii=False)[:100]}...")

    try:
        response = requests.post(
            url,
            json=config_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        log_info(f"状态码: {response.status_code}")
        log_info(f"返回内容: {response.text}")

        if response.status_code == 200 and "success" in response.text.lower():
            log_success(f"配置 [{config_name}] 上传成功！")
            return True
        else:
            log_error(f"配置上传失败")
            return False

    except Exception as e:
        log_error(f"请求失败: {e}")
        return False


def get_config(config_name: str):
    """
    从服务器获取配置文件

    :param config_name: 配置名称，如 "launcher"
    :return: 配置内容（dict），失败返回 None
    """
    print(f"\n{'='*50}")
    print(f"📥 获取配置: {config_name}")
    print(f"{'='*50}")

    url = f"{GET_CONFIG_URL}?name={config_name}"
    log_info(f"请求地址: {url}")

    try:
        response = requests.get(url, timeout=30)

        log_info(f"状态码: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            if content and content != "{}":
                config = response.json()
                log_success(f"配置获取成功！")
                print(f"\n配置内容:\n{json.dumps(config, ensure_ascii=False, indent=2)}")
                return config
            else:
                log_info(f"配置文件为空或不存在")
                return {}
        else:
            log_error(f"获取配置失败")
            return None

    except Exception as e:
        log_error(f"请求失败: {e}")
        return None

def print_usage():
    """打印使用说明"""
    print("""
通用配置管理脚本
================

使用方式:
    python config_manager.py <命令> <配置名>

命令:
    set      上传配置到服务器
    get      从服务器获取配置
    download 下载配置中的所有图标

配置名:
    launcher    Launcher 配置 (对应 config_content_launcher.py)
    其他...     自定义配置 (对应 config_content_xxx.py)

示例:
    python config_manager.py set launcher      # 上传 launcher 配置
    python config_manager.py get launcher      # 获取 launcher 配置
    python config_manager.py download launcher # 下载 launcher 图标

添加新配置:
    1. 创建文件 config_content_xxx.py
    2. 在文件中定义 CONFIG_NAME 和 CONFIG_DATA 变量
    3. 使用 python config_manager.py set xxx 上传
""")


if __name__ == "__main__":

    # 1.这个输入的文件名config_content_launcher是本地用的，需要传入后边的launcher字符串
    # 2.这个launcher，就是对应服务器上的文件名，获取的时候，后边加上launcher就行了，因为这个配置文件中配置的文件名就是launcher
    #   https://linkprohub.top/vr/get_config?name=launcher
    #   https://linkprohub.top/vr/get_config?name=tester
    #   https://linkprohub.top/vr/get_config?name=select_scence
    #   https://linkprohub.top/vr/get_config?name=show_float_button

    # config_name = "launcher"
    # config_name = "tester"
    # config_name = "select_scence"
    config_name = "show_float_button"
    set_config(config_name)
    # get_config(config_name)
