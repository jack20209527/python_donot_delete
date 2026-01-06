#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包名修改工具 - 配置文件
修改下面的配置后，运行 change_package.py 即可
"""

# ==================== 需要修改的配置 ====================

# 1. 选择第几套签名配置（1、2、3）
SIGN_CONFIG_INDEX = 2

# 2. Android 工程根目录路径
ANDROID_PROJECT_PATH = "/Users/sun2022/Downloads/local_android/yzandroid"

# 3. 待拷贝的 UniApp 资源文件夹路径
UNIAPP_SOURCE_PATH = "/Users/sun2022/Downloads/__UNI__0D35F8E"

# ==================== 以下是预置配置，一般不需要修改 ====================

# 签名配置列表（共3套）
SIGN_CONFIGS = [
    # 第1套：艺值字画商城
    {
        "name": "艺值字画商城",
        "package_name": "uni.yizhizh.com",
        "key_alias": "yizhizihua",
        "key_password": "yangyizhi",
        "store_file": "yizhizihua.keystore",
        "store_password": "yangyizhi",
        "keystore_source_path": "/Users/sun2022/Downloads/公司/yizhizihua.keystore",
        "dcloud_appkey": "614b26d2bb3cf002b0d3220190eb390b",
    },
    # 第2套：测试1
    {
        "name": "测试1",
        "package_name": "com.yizhi.tech",
        "key_alias": "yizhitech",
        "key_password": "20251218",
        "store_file": "yizhitech.keystore",
        "store_password": "20251218",
        "keystore_source_path": "/Users/sun2022/Downloads/公司/yizhitech.keystore",
        "dcloud_appkey": "555261490b6b6fbc1435fc49248d88a8",
    },
    # 第3套：测试2
    {
        "name": "测试2",
        "package_name": "com.yizhi.test",
        "key_alias": "yizhitest",
        "key_password": "20251219",
        "store_file": "yizhitest.keystore",
        "store_password": "20251219",
        "keystore_source_path": "/Users/sun2022/Downloads/公司/yizhitest.keystore",
        "dcloud_appkey": "b9313e28da4b79d9fc798469b343cd3d",
    },
]
