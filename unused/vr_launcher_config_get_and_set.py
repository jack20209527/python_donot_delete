
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VR 配置文件上传脚本
用于向服务器 POST 请求更新 launcher_config.json 配置文件
"""
import os
import requests

ICON_DOWNLOAD_PATH = "/Users/sun2022/Downloads/logo"
# 服务器地址（本地测试用 localhost，线上改成你的服务器地址）
BASE_URL = "https://linkprohub.top"
# BASE_URL = "http://你的服务器IP:端口"

# 接口地址
SET_CONFIG_URL = f"{BASE_URL}/vr/set_config_post"
GET_CONFIG_URL = f"{BASE_URL}/vr/get_config"

# 要上传的配置内容
config_data = {
    "version": "1",
    "metadata": {
        "lastUpdated": "2025-12-8",
        "apiVersion": "v1"
    },
    "iconList": [
        {
            "appName": "3D视频",
            "packageName": "com.app.unit.converter",
            "activityName": "com.app.unit.converter.videoplaylist.VideoPlaylistActivity",
            "appType": 1,
            "isPreset": True,
            "presetFileName": "icon_3d_video_list_800_800.png",
            "iconInfo":
                {
                    "size": "800*800",
                    "url": "https://pub-2aef4031d227483ea5406094fa860a7e.r2.dev/yizhi/icon_3d_video_list_800_800.png",
                    "localPath": "",
                    "ext0": "",
                    "ext1": "",
                    "ext2": ""
                }
        },
        {
            "appName": "全景视频",
            "packageName": "com.yzkj.MobileGyroscope",
            "activityName": "UnityPlayerActivity",
            "appType": 1,
            "isPreset": True,
            "presetFileName": "icon_quan_jing_video_800_800.png",
            "iconInfo":
                {
                    "size": "800*800",
                    "url": "https://pub-2aef4031d227483ea5406094fa860a7e.r2.dev/yizhi/icon_quan_jing_video_800_800.png",
                    "localPath": "",
                    "ext0": "",
                    "ext1": "",
                    "ext2": ""
                }

        },
        {
            "appName": "爱奇艺VR",
            "packageName": "com.iqiyi.ivrcinema.cb",
            "activityName": "com.iqiyi.ivrcinema.activity.CbMainActivity",
            "appType": 1,
            "isPreset": True,
            "presetFileName": "icon_aiqiyi_800_800.png",
            "iconInfo":
                {
                    "size": "800*800",
                    "url": "https://pub-2aef4031d227483ea5406094fa860a7e.r2.dev/yizhi/icon_aiqiyi_800_800.png",
                    "localPath": "",
                    "ext0": "",
                    "ext1": "",
                    "ext2": ""
                }

        },
        {
            "appName": "艺值沉浸式展厅",
            "packageName": "Test",
            "activityName": "MainActivity",
            "appType": 1,
            "isPreset": True,
            "presetFileName": "icon_immersive_800_800.png",
            "iconInfo":
                {
                    "size": "800*800",
                    "url": "https://pub-2aef4031d227483ea5406094fa860a7e.r2.dev/yizhi/icon_immersive_800_800.png",
                    "localPath": "",
                    "ext0": "",
                    "ext1": "",
                    "ext2": ""
                }

        }
    ]
}

def set_config():
    """上传配置文件"""
    print("正在上传配置...")
    try:
        response = requests.post(SET_CONFIG_URL, json=config_data)
        print(f"状态码: {response.status_code}")
        print(f"返回内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")


def get_config():
    """获取配置文件"""
    print("正在获取配置...")
    try:
        response = requests.get(GET_CONFIG_URL)
        print(f"状态码: {response.status_code}")
        print(f"返回内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")


def download_all_icons_from_config():
    """
    从配置文件中获取所有图标 URL 并下载到本地
    """
    print("正在从配置中下载所有图标...")

    # 确保下载目录存在
    os.makedirs(ICON_DOWNLOAD_PATH, exist_ok=True)

    # 获取配置
    try:
        response = requests.get(GET_CONFIG_URL)
        if response.status_code != 200:
            print(f"获取配置失败，状态码: {response.status_code}")
            return

        config = response.json()
    except Exception as e:
        print(f"获取配置失败: {e}")
        return

    # 遍历 iconList，下载所有图标
    icon_list = config.get("iconList", [])
    total = 0
    success = 0

    for item in icon_list:
        app_name = item.get("appName", "unknown")
        icons = item.get("icons", [])

        for icon in icons:
            url = icon.get("url", "")
            if not url:
                continue

            total += 1
            # 从 URL 中提取文件名
            file_name = url.split("/")[-1]
            save_path = os.path.join(ICON_DOWNLOAD_PATH, file_name)

            print(f"\n[{app_name}] ", end="")
            if download_icon(url, save_path):
                success += 1

    print(f"\n下载完成！成功: {success}/{total}")
    print(f"保存路径: {ICON_DOWNLOAD_PATH}")

def download_icon(url, save_path):
    """
    下载单个图标
    :param url: 图标的 URL
    :param save_path: 保存的完整路径
    :return: 是否下载成功
    """
    try:
        print(f"正在下载: {url}")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {save_path}")
            return True
        else:
            print(f"下载失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"下载失败: {e}")
        return False



if __name__ == "__main__":
    # 上传配置
    set_config()

    # print("\n" + "=" * 50 + "\n")

    # 获取配置（验证是否上传成功）
    # get_config()

    # print("\n" + "=" * 50 + "\n")

    # 从服务器配置下载所有图标
    # download_all_icons_from_config()




