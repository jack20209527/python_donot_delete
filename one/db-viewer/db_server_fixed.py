#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库查看工具 - Flask Web 服务
连接腾讯云 MySQL 数据库，提供 Web 界面查看表数据
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pymysql
from pymysql import Error
import json
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ==================== 数据库配置 ====================
DB_CONFIG = {
    'host': '43.153.71.169',
    'port': 3306,
    'user': 'root',
    'password': '8ta6R',
    'database': 'my_common_video_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# ==================== 全局缓存 ====================
cache = {
    'tables': [],
    'table_data': {},
    'connected': False,
    'error_message': ''
}

# ==================== 日志函数 ====================

def log_info(message: str):
    """打印信息日志"""
    print(f"ℹ️  {message}")


def log_success(message: str):
    """打印成功日志"""
    print(f"✓ {message}")


def log_error(message: str):
    """打印错误日志"""
    print(f"✗ {message}")


def log_warning(message: str):
    """打印警告日志"""
    print(f"⚠️  {message}")


# ==================== 数据库初始化 ====================

def init_database():
    """初始化数据库连接和缓存"""
    try:
        log_info("正在连接数据库...")
        log_info(f"服务器: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        log_info(f"用户: {DB_CONFIG['user']}")
        log_info(f"数据库: {DB_CONFIG['database']}")
        
        # 建立连接
        connection = pymysql.connect(**DB_CONFIG)
        log_success("数据库连接成功！")
        
        # 创建游标
        cursor = connection.cursor()
        
        # 获取所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # 提取表名
        if isinstance(tables[0], dict):
            # DictCursor 返回字典
            table_names = [list(table.values())[0] for table in tables]
        else:
            # 普通游标返回元组
            table_names = [table[0] for table in tables]
        
        cache['tables'] = table_names
        
        log_success(f"找到 {len(cache['tables'])} 个表: {', '.join(cache['tables'])}")
        
        # 预加载每个表的数据（前1000行）
        for table in cache['tables']:
            try:
                # 获取表结构
                cursor.execute(f"DESCRIBE {table}")
                columns_info = cursor.fetchall()
                
                if isinstance(columns_info[0], dict):
                    # DictCursor
                    columns = [col['Field'] for col in columns_info]
                else:
                    # 普通游标
                    columns = [col[0] for col in columns_info]
                
                # 查询表数据
                cursor.execute(f"SELECT * FROM {table} LIMIT 1000")
                rows = cursor.fetchall()
                
                # 转换为字典列表（处理日期时间对象）
                data = []
                for row in rows:
                    if isinstance(row, dict):
                        # DictCursor 已经是字典
                        row_dict = {}
                        for key, value in row.items():
                            if isinstance(value, datetime):
                                row_dict[key] = value.isoformat()
                            else:
                                row_dict[key] = value
                        data.append(row_dict)
                    else:
                        # 普通游标需要转换
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            if isinstance(value, datetime):
                                row_dict[col] = value.isoformat()
                            else:
                                row_dict[col] = value
                        data.append(row_dict)
                
                cache['table_data'][table] = {
                    'columns': columns,
                    'data': data,
                    'count': len(data)
                }
                log_success(f"表 '{table}' 已加载 ({len(data)} 行)")
                
            except Error as e:
                log_error(f"表 '{table}' 加载失败: {e}")
        
        cursor.close()
        connection.close()
        cache['connected'] = True
        log_success("所有数据已缓存到内存")
        
    except Error as e:
        error_msg = f"数据库连接失败: {e}"
        log_error(error_msg)
        cache['connected'] = False
        cache['error_message'] = str(e)
    except Exception as e:
        error_msg = f"初始化失败: {e}"
        log_error(error_msg)
        cache['connected'] = False
        cache['error_message'] = str(e)


# ==================== Flask 路由 ====================

@app.route('/')
def index():
    """提供 HTML 文件"""
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return f"<h1>错误</h1><p>无法加载 index.html: {e}</p>", 404


@app.route('/app.js')
def app_js():
    """提供 JS 文件"""
    try:
        return send_from_directory('.', 'app.js')
    except Exception as e:
        return f"console.error('无法加载 app.js: {e}');", 404


@app.route('/api/tables', methods=['GET'])
def get_tables():
    """获取所有表"""
    if not cache['connected']:
        return jsonify({
            'success': False,
            'error': '数据库未连接',
            'details': cache['error_message']
        }), 500
    
    return jsonify({
        'success': True,
        'tables': cache['tables'],
        'count': len(cache['tables'])
    })


@app.route('/api/query', methods=['POST'])
def query_data():
    """查询表数据"""
    if not cache['connected']:
        return jsonify({
            'success': False,
            'error': '数据库未连接',
            'details': cache['error_message']
        }), 500
    
    try:
        data = request.get_json()
        table = data.get('table')
        limit = data.get('limit', 1000)
        
        # 验证输入
        if not table or not isinstance(table, str):
            return jsonify({
                'success': False,
                'error': '无效的表名'
            }), 400
        
        if not isinstance(limit, int) or limit < 1 or limit > 10000:
            return jsonify({
                'success': False,
                'error': '行数必须在 1-10000 之间'
            }), 400
        
        # 防止 SQL 注入 - 只允许字母、数字、下划线
        if not all(c.isalnum() or c == '_' for c in table):
            return jsonify({
                'success': False,
                'error': '表名包含无效字符'
            }), 400
        
        # 从缓存获取数据
        if table not in cache['table_data']:
            return jsonify({
                'success': False,
                'error': f'表 {table} 不存在'
            }), 404
        
        table_info = cache['table_data'][table]
        columns = table_info['columns']
        all_data = table_info['data']
        
        # 返回指定数量的数据
        limited_data = all_data[:limit]
        
        return jsonify({
            'success': True,
            'columns': columns,
            'data': limited_data,
            'total': len(all_data),
            'returned': len(limited_data)
        })
        
    except Exception as e:
        log_error(f"查询失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok' if cache['connected'] else 'error',
        'connected': cache['connected'],
        'tables_count': len(cache['tables']),
        'error': cache['error_message'] if not cache['connected'] else None
    })


@app.route('/api/table-info/<table_name>', methods=['GET'])
def get_table_info(table_name):
    """获取表的详细信息"""
    if not cache['connected']:
        return jsonify({
            'success': False,
            'error': '数据库未连接'
        }), 500
    
    if table_name not in cache['table_data']:
        return jsonify({
            'success': False,
            'error': f'表 {table_name} 不存在'
        }), 404
    
    table_info = cache['table_data'][table_name]
    
    return jsonify({
        'success': True,
        'table': table_name,
        'columns': table_info['columns'],
        'row_count': table_info['count'],
        'column_count': len(table_info['columns'])
    })


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'success': False,
        'error': '请求的资源不存在'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500


# ==================== 主函数 ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 数据库查看工具启动中...")
    print("="*60)
    
    # 初始化数据库
    init_database()
    
    print("\n" + "="*60)
    if cache['connected']:
        print("✓ 服务器启动在 http://localhost:8888")
        print("✓ 打开浏览器访问: http://localhost:8888")
    else:
        print("✗ 数据库连接失败，请检查配置")
        print(f"✗ 错误信息: {cache['error_message']}")
    print("="*60 + "\n")
    
    # 启动 Flask 服务
    app.run(host='localhost', port=8888, debug=False)
