import subprocess
import platform
import re


def kill_port(port: int) -> str:
    """
    关闭占用指定端口的进程
    :param port: 要关闭的端口号（如 5000）
    :return: 执行结果信息
    """
    system = platform.system().lower()
    pid = None

    try:
        if system == "windows":
            # Windows系统：使用netstat命令查找PID
            cmd = f"netstat -ano | findstr :{port}"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=True
            )
            # 从输出中提取PID（示例输出：TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING       12345）
            pid_match = re.search(r"\s+(\d+)$", result.stdout.strip())
            if pid_match:
                pid = pid_match.group(1)
        else:
            # Mac/Linux系统：使用lsof命令查找PID（-t参数直接返回PID）
            cmd = f"lsof -t -i :{port}"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=True
            )
            pid = result.stdout.strip()

        if not pid:
            return f"端口 {port} 未被占用"

        # 强制终止进程
        if system == "windows":
            subprocess.run(
                f"taskkill /F /PID {pid}", shell=True, check=True
            )
        else:
            subprocess.run(
                f"kill -9 {pid}", shell=True, check=True
            )

        return f"成功关闭端口 {port} 的进程（PID: {pid}）"

    except subprocess.CalledProcessError as e:
        # 命令执行失败（如端口未被占用时，lsof会返回非零退出码）
        if "lsof" in str(e) or "findstr" in str(e):
            return f"端口 {port} 未被占用"
        return f"关闭端口失败：{e.stderr.strip() if e.stderr else str(e)}"
    except Exception as e:
        return f"执行出错：{str(e)}"

if __name__ == "__main__":

    kill_port (8888)
