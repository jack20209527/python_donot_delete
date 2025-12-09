import cv2
import os
import argparse
from typing import List

def generate_video_cover(video_path: str, frame_index: int = 0) -> None:
    """
    生成视频封面并保存到视频同目录下

    Args:
        video_path: 视频文件路径
        frame_index: 截取的帧索引，0表示第一帧，-1表示最后一帧
    """
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        print(f"错误：视频文件不存在 - {video_path}")
        return

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"错误：无法打开视频 - {video_path}")
        return

    # 获取视频总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 处理帧索引
    if frame_index == -1:
        # 截取最后一帧
        target_frame = total_frames - 1
    elif frame_index < 0 or frame_index >= total_frames:
        # 索引超出范围，默认使用第一帧
        target_frame = 0
        print(f"警告：帧索引 {frame_index} 超出范围，使用第一帧")
    else:
        target_frame = frame_index

    # 设置视频位置到目标帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    # 读取帧
    ret, frame = cap.read()
    if not ret:
        print(f"错误：无法读取视频帧 - {video_path}")
        cap.release()
        return

    # 生成封面文件名
    video_dir = os.path.dirname(video_path)
    video_name = os.path.basename(video_path)
    video_name_without_ext = os.path.splitext(video_name)[0]
    cover_path = os.path.join(video_dir, f"{video_name_without_ext}_cover.jpg")

    # 保存封面
    cv2.imwrite(cover_path, frame)
    print(f"封面已生成：{cover_path}")

    # 释放资源
    cap.release()

def main(video_paths: List[str], frame_index: int = 0) -> None:
    """
    主函数，处理多个视频文件

    Args:
        video_paths: 视频文件路径列表
        frame_index: 截取的帧索引
    """
    for video_path in video_paths:
        generate_video_cover(video_path, frame_index)

if __name__ == "__main__":


    video_name = "8"
    # 直接定义视频路径列表
    video_paths = [

        f"/Users/sun2022/Downloads/1/video_left_{video_name}.mp4",
        f"/Users/sun2022/Downloads/1/video_right_{video_name}.mp4",
        # "/Users/sun2022/Downloads/1/video_left_3.mp4",
        # "/Users/sun2022/Downloads/1/video_right_3.mp4",
        # "/Users/sun2022/Downloads/1/left.mp4",
        # "/Users/sun2022/Downloads/1/right.mp4",
        # "/Users/sun2022/Downloads/1/video1_left.mp4",
        # "/Users/sun2022/Downloads/1/video1_right.mp4",
    ]
    frame_index = 0  # 可以调整为其他帧索引
    main(video_paths, frame_index)