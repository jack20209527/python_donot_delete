import subprocess
import os

def split_vr_video(input_file, output_left, output_right):
    """
    将左右格式（Side-by-Side）的 VR 视频分割成左眼和右眼两个视频文件。

    :param input_file: 原始 VR 视频文件名 (e.g., "input_vr_video.mp4")
    :param output_left: 左眼视频输出文件名 (e.g., "output_left_eye.mp4")
    :param output_right: 右眼视频输出文件名 (e.g., "output_right_eye.mp4")
    :return: True 如果分割成功，否则返回 False
    """

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 '{input_file}' 不存在。")
        return False

    # ------------------------------------------------
    # 1. 导出左眼视频 (原视频的左半部分)
    # crop=iw/2:ih:0:0 
    # 宽度 (iw/2): 输入视频宽度的一半
    # 高度 (ih): 整个高度
    # 起始X (0): 最左边
    # 起始Y (0): 最上边
    # ------------------------------------------------

    # 构建左眼分割命令
    command_left = [
        "ffmpeg",
        "-i", input_file,
        "-filter:v", "crop=iw/2:ih:0:0",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
        output_left
    ]

    print(f"--- 正在导出左眼视频：{output_left} ---")
    try:
        # 使用 subprocess.run 执行命令
        # capture_output=True 和 text=True 用于捕获 FFmpeg 的输出，但通常对于长时间运行的视频任务，
        # 最好是让它直接打印到控制台，这里保持简单调用。
        subprocess.run(command_left, check=True)
        print("左眼视频导出成功。")
    except subprocess.CalledProcessError as e:
        print(f"错误：左眼视频导出失败。FFmpeg 返回错误码 {e.returncode}")
        return False
    except FileNotFoundError:
        print("错误：未找到 FFmpeg 命令。请确保 FFmpeg 已正确安装并配置到系统环境变量中。")
        return False

    # ------------------------------------------------
    # 2. 导出右眼视频 (原视频的右半部分)
    # crop=iw/2:ih:iw/2:0
    # 宽度 (iw/2): 输入视频宽度的一半
    # 高度 (ih): 整个高度
    # 起始X (iw/2): 视频中间点
    # 起始Y (0): 最上边
    # ------------------------------------------------

    # 构建右眼分割命令
    command_right = [
        "ffmpeg",
        "-i", input_file,
        "-filter:v", "crop=iw/2:ih:iw/2:0",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k",
        output_right
    ]

    print(f"\n--- 正在导出右眼视频：{output_right} ---")
    try:
        subprocess.run(command_right, check=True)
        print("右眼视频导出成功。")
    except subprocess.CalledProcessError as e:
        print(f"错误：右眼视频导出失败。FFmpeg 返回错误码 {e.returncode}")
        return False

    return True

# --- 主执行部分 ---
if __name__ == "__main__":
    # 设定文件名

    video_name = "8"
    INPUT_FILE_NAME = f"/Users/sun2022/Downloads/1/{video_name}.mp4" # 请将此替换为您要分割的 VR 视频文件名
    OUTPUT_LEFT = f"/Users/sun2022/Downloads/1/video_left_{video_name}.mp4"
    OUTPUT_RIGHT = f"/Users/sun2022/Downloads/1/video_right_{video_name}.mp4"

    # INPUT_FILE_NAME = "/Users/sun2022/Downloads/1/3.mp4" # 请将此替换为您要分割的 VR 视频文件名
    # OUTPUT_LEFT = "/Users/sun2022/Downloads/1/video_left_3.mp4"
    # OUTPUT_RIGHT = "/Users/sun2022/Downloads/1/video_right_3.mp4"

    print("--- VR 视频分割工具启动 ---")

    if split_vr_video(INPUT_FILE_NAME, OUTPUT_LEFT, OUTPUT_RIGHT):
        print(f"\n分割任务全部完成！\n已生成：{OUTPUT_LEFT} 和 {OUTPUT_RIGHT}")
    else:
        print("\n分割任务失败，请检查错误信息和 FFmpeg 安装情况。")