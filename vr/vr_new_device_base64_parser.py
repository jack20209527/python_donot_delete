#!/usr/bin/env python3
"""
decode_b64.py
提取并解码 Base64 数据
"""

# 2025-12-15 21:11:37.623 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AWDtKgDUyo09n9gJu2f6iDxpWX8/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.624 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42,1C:69:A9:F6"},"data":"AWrtKgBiZaU9CwI7u8bGjjyuH38/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.626 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AXTtKgCH9bw9I7xzuym0lTwD3X4/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.657 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AX7tKgDQfdQ9MYKau7qmnTxbkX4/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.660 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AYjtKgAk7+s9KtS+uxO2pjziPH4/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.662 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AZLtKgAlqgE+51Lnu4OjsDx4330/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.691 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AZztKgBTOQ0+e5gJvFE+uzwien0/"},"message":"数据已经传递成功"},"unityID":""}
# 2025-12-15 21:11:37.694 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AabtKgDEwRg+7F8hvO2+xjz3C30/"},"message":"数据已经传递成功"},"unityID":""}

# 1. 原始日志文本（已包含）
LOG = r'''
I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AuW8gOWni+agoeWHhu+8jOivt+S/neaMgeiuvuWkh+mdmeatoi4uLg\u003d\u003d"},"message":"数据已经传递成功"},"unityID":""}
2025-12-18 20:01:53.647 14306-15147 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AuagoeWHhuWujOaIkA\u003d\u003d"},"message":"数据已经传递成功"},"unityID":""}
2025-12-18 20:01:53.647 14306-15147 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"A77Dyj5QOuk8mPpYu57v8Ly81Fm+L+VfPw\u003d\u003d"},"message":"数据已经传递成功"},"unityID":""}
'''

import re
import base64





def main():

    print(decode_base64("AuW8gOWni+agoeWHhu+8jOivt+S/neaMgeiuvuWkh+mdmeatoi4uLg\u003d\u003d"))



import re
import base64






def main():
    log_data = """
# 2025-12-15 21:11:37.662 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AZLtKgAlqgE+51Lnu4OjsDx4330/"},"message":"数据已经传递成功"},"unityID":""} 
# 2025-12-15 21:11:37.691 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AZztKgBTOQ0+e5gJvFE+uzwien0/"},"message":"数据已经传递成功"},"unityID":""} 
# 2025-12-15 21:11:37.694 19592-20273 BaseBluetoothManagerLog             uni.yizhizh.com                      I  sendToUnity ::{"action":25,"result":{"code":200,"data":{"device":{"connectState":10,"isPaired":false,"macAddress":"78:42:1C:69:A9:F6"},"data":"AabtKgDEwRg+7F8hvO2+xjz3C30/"},"message":"数据已经传递成功"},"unityID":""} 
Au"data":"AuagoeWHhuWujOaIkA=="

"data":"A77Dyj5QOuk8mPpYu57v8Ly81Fm+L+VfPw=="

"""

    # 提取 base64 字符串
    b64_list = extract_data_base64(log_data)

    print(f"✅ 找到 {len(b64_list)} 个 base64 字符串\n")
    print("-" * 80)

    # 解码并打印
    for idx, b64 in enumerate(b64_list, 1):
        decoded = decode_base64(b64)
        print(f"{idx} | Base64: {b64}")
        print(f"  | Decoded: {decoded}")
        print("-" * 80)

def extract_data_base64(log_text: str) -> list:

    base64_list = []

    # 匹配 "data":"base64string" 的模式
    # 支持 Unicode 转义的 = (\u003d)
    pattern = r'"data"\s*:\s*"([A-Za-z0-9+/=\u003d\\]+?)"'

    matches = re.findall(pattern, log_text)

    for match in matches:
        # 处理 Unicode 转义的 =（\u003d）
        decoded_match = match.replace('\\u003d', '=')
        base64_list.append(decoded_match)

    return base64_list

def decode_base64(b64: str) -> str:
    try:
        raw = base64.b64decode(b64, validate=True)
        ascii_str = raw.decode('utf-8', 'replace').replace('\n', '\\n')
        return ascii_str
    except Exception as e:
        return f"[ERR] {str(e)}"


if __name__ == '__main__':
    main()