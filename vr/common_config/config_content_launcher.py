#!/usr/bin/env python3
"""
Launcher 配置文件内容
文件名: launcher (对应服务器上的 launcher.json)
"""

# 配置文件名（不含 .json 后缀）
CONFIG_NAME = "launcher"

# 配置内容
CONFIG_DATA = {
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
            "iconInfo": {
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
            "iconInfo": {
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
            "iconInfo": {
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
            "iconInfo": {
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
