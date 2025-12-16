#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decode_b64.py
提取并解码 Base64 数据
"""

import re
import base64

# 1. 原始日志文本（已包含）
LOG = r'''
2025-12-15 21:11:37.623 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AWDtKgDUyo09n9gJu2f6iDxpWX8/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.624 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42,1C:69:A9:F6"},"data":"AWrtKgBiZaU9CwI7u8bGjjyuH38/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.626 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AXTtKgCH9bw9I7xzuym0lTwD3X4/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.657 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AX7tKgDQfdQ9MYKau7qmnTxbkX4/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.660 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AYjtKgAk7+s9KtS+uxO2pjziPH4/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.662 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AZLtKgAlqgE+51Lnu4OjsDx4330/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.691 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AZztKgBTOQ0+e5gJvFE+uzwien0/"},"message":"数据已经传递成功"},"unityID":""}
2025-12-15 21:11:37.694 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AabtKgDEwRg+7F8hvO2+xjz3C30/"},"message":"数据已经传递成功"},"unityID":""}
'''

# 2. 提取并解码
def main():
    b64_list = re.findall(r'"data"\s*:\s*"([A-Za-z0-9+/=]+?)"', LOG)
    for idx, b64 in enumerate(b64_list, 1):
        try:
            raw = base64.b64decode(b64, validate=True)
        except Exception as e:
            print(f"{idx:>3} | [ERR] {e}")
            continue
        hex_str = raw.hex(' ').upper()
        ascii_str = raw.decode('utf-8', 'replace').replace('\n', '\\n')
        print(f"{idx:>3} | Hex : {hex_str}")
        print(f"    | Asc : {ascii_str}")
        print("-" * 80)

if __name__ == '__main__':
    main()