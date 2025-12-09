#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
from datetime import datetime
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import subprocess
import platform
import re

"""
自动化部署 Web 服务器

启动方式： python server.py
结束服务： 在终端按 Ctrl + C

访问地址：http://localhost:5000

"""
cur_port = 1802 # 当前端口号


# 获取当前脚本所在目录，能够自动获取如下的目录
# 工作目录: /Users/sun2022/pro/pro_python_work/python_donot_delete/vr/server
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 存储日志
logs = []



def add_log(message: str, level: str = "info"):
    """添加日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs.append({
        "time": timestamp,
        "message": message,
        "level": level
    })
    # 只保留最近 100 条日志
    if len(logs) > 100:
        logs.pop(0)
    print(f"[{timestamp}] [{level.upper()}] {message}")


def run_script(script_name: str, task_name: str):
    """在后台线程中运行脚本"""
    def execute():
        script_path = os.path.join(SCRIPT_DIR, script_name)
        
        if not os.path.exists(script_path):
            add_log(f"脚本不存在: {script_path}", "error")
            return
        
        add_log(f"开始执行: {task_name}", "info")
        
        try:
            # 执行脚本并捕获输出
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=SCRIPT_DIR
            )
            
            # 实时读取输出
            for line in process.stdout:
                line = line.strip()
                if line:
                    # 根据内容判断日志级别
                    if "❌" in line or "失败" in line or "错误" in line:
                        add_log(line, "error")
                    elif "✅" in line or "成功" in line or "完成" in line:
                        add_log(line, "success")
                    elif "📌" in line or "🚀" in line or "🎉" in line:
                        add_log(line, "info")
                    else:
                        add_log(line, "info")
            
            process.wait()
            
            if process.returncode == 0:
                add_log(f"✅ {task_name} 执行完成！", "success")
            else:
                add_log(f"❌ {task_name} 执行失败，返回码: {process.returncode}", "error")
                
        except Exception as e:
            add_log(f"❌ 执行出错: {str(e)}", "error")
    
    # 在新线程中执行，避免阻塞
    thread = threading.Thread(target=execute)
    thread.start()

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
# ==================== 路由 ====================

@app.route("/")
def index():
    """返回主页"""
    return send_file(os.path.join(SCRIPT_DIR, "index.html"))


@app.route("/api/deploy/integration", methods=["POST"])
def deploy_integration():
    """部署集成版本"""
    add_log("收到部署集成版本请求", "info")
    run_script("deploy_shilong_v2_unity_project.py", "部署集成版本")
    return jsonify({"status": "started", "message": "部署任务已启动"})


@app.route("/api/deploy/launcher", methods=["POST"])
def deploy_launcher():
    """部署 Launcher 版本"""
    add_log("收到部署 Launcher 版本请求", "info")
    # TODO: 添加 Launcher 部署脚本
    add_log("⚠️ Launcher 部署脚本暂未配置", "warning")
    return jsonify({"status": "started", "message": "Launcher 部署任务已启动"})


@app.route("/api/config/get", methods=["GET"])
def get_config():
    """获取 Launcher 配置"""
    add_log("收到获取配置请求", "info")
    # TODO: 实现配置获取逻辑
    add_log("⚠️ 配置获取功能暂未实现", "warning")
    return jsonify({"status": "success", "config": {}})


@app.route("/api/config/set", methods=["POST"])
def set_config():
    """设置 Launcher 配置"""
    add_log("收到设置配置请求", "info")
    config = request.json
    add_log(f"配置内容: {config}", "info")
    # TODO: 实现配置保存逻辑
    add_log("⚠️ 配置保存功能暂未实现", "warning")
    return jsonify({"status": "success", "message": "配置已保存"})


@app.route("/api/logs", methods=["GET"])
def get_logs():
    """获取日志"""
    return jsonify({"logs": logs})


@app.route("/api/logs/clear", methods=["POST"])
def clear_logs():
    """清空日志"""
    logs.clear()
    add_log("日志已清空", "info")
    return jsonify({"status": "success"})


# ==================== 启动服务器 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 自动化部署服务器启动中...")
    print("=" * 50)
    print(f"📁 工作目录: {SCRIPT_DIR}")
    print("=" * 50)
    print("按 Ctrl+C 停止服务器")
    print()

    kill_port (cur_port)
    
    add_log("服务器启动成功", "success")
    add_log("等待操作指令...", "info")
    
    app.run(host="0.0.0.0", port=cur_port, debug=False)
