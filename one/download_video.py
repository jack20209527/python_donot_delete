#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频下载脚本
从提供的 URL 列表下载视频文件到指定目录
"""

import os
import sys
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

# 视频链接列表
VIDEO_URLS = [
    "https://mstream.app/video/1747787516776_250413_161404_333_9374_37.mp4",
    "https://mstream.app/video/1747787522758_250413_162544_300_6887_37.mp4",
    "https://mstream.app/video/1747787728224_250413_163713_287_6141_37.mp4",
    "https://mstream.app/video/1747787731713_250413_164153_018_3707_37.mp4",
    "https://mstream.app/video/1747787735675_250413_165330_476_4350_37.mp4",
    "https://mstream.app/video/1747787740024_250413_171501_349_5557_37.mp4",
    "https://mstream.app/video/1747787743078_250413_171845_794_5710_37.mp4",
    "https://mstream.app/video/1747787747605_250413_172227_789_1156_37.mp4",
    "https://mstream.app/video/1747787753154_250413_172857_135_4041_37.mp4",
    "https://mstream.app/video/1747787761762_250413_174656_495_6007_37.mp4",
    "https://mstream.app/video/1747787772068_250413_175022_873_9919_37.mp4",
    "https://mstream.app/video/1747787778461_250413_175839_722_4670_37.mp4",
    "https://mstream.app/video/1747787788108_250413_180317_651_14_37.mp4",
    "https://mstream.app/video/1747787800218_250413_181002_054_8480_37.mp4",
]

# 下载目录
DOWNLOAD_DIR = "/Users/sun2022/Downloads/videos"

# 请求头（模拟浏览器，避免被拒绝）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://mstream.app/',
}


def create_download_dir():
    """创建下载目录（如果不存在）"""
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
    print(f"✅ 下载目录已准备: {DOWNLOAD_DIR}")


def get_filename_from_url(url):
    """从 URL 中提取文件名"""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    return filename if filename else "video.mp4"


def download_video(url, output_path):
    """
    下载单个视频文件

    Args:
        url: 视频 URL
        output_path: 保存路径

    Returns:
        bool: 下载是否成功
    """
    try:
        print(f"\n📥 开始下载: {os.path.basename(output_path)}")
        print(f"   URL: {url}")

        # 发送 GET 请求，stream=True 用于大文件下载
        response = requests.get(url, headers=HEADERS, stream=True, timeout=30)
        response.raise_for_status()

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        if total_size > 0:
            print(f"   文件大小: {total_size / 1024 / 1024:.2f} MB")

        # 写入文件
        downloaded_size = 0
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # 显示进度
                    if total_size > 0:
                        percent = (downloaded_size / total_size) * 100
                        print(f"\r   进度: {percent:.1f}% ({downloaded_size / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB)", end='', flush=True)

        print()  # 换行
        print(f"✅ 下载完成: {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("视频下载脚本")
    print("=" * 60)

    # 创建下载目录
    create_download_dir()

    # 统计信息
    total = len(VIDEO_URLS)
    success_count = 0
    fail_count = 0
    skip_count = 0

    print(f"\n📋 共 {total} 个视频需要下载\n")

    # 遍历下载每个视频
    for index, url in enumerate(VIDEO_URLS, 1):
        print(f"\n[{index}/{total}] 处理中...")

        # 获取文件名
        filename = get_filename_from_url(url)
        output_path = os.path.join(DOWNLOAD_DIR, filename)

        # 检查文件是否已存在
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"⏭️  文件已存在，跳过: {filename} ({file_size / 1024 / 1024:.2f} MB)")
            skip_count += 1
            continue

        # 下载视频
        if download_video(url, output_path):
            success_count += 1
        else:
            fail_count += 1
            # 如果下载失败，删除可能的不完整文件
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass

        # 短暂延迟，避免请求过快
        if index < total:
            time.sleep(0.5)

    # 打印统计信息
    print("\n" + "=" * 60)
    print("下载完成统计")
    print("=" * 60)
    print(f"✅ 成功: {success_count}")
    print(f"⏭️  跳过: {skip_count}")
    print(f"❌ 失败: {fail_count}")
    print(f"📁 保存位置: {DOWNLOAD_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断下载")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 程序异常: {e}")
        sys.exit(1)

