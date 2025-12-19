from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 数据库配置
DB_CONFIG = {
    'host': '43.153.71.169',
    'port': 3306,
    'user': 'root',
    'password': '8ta6R',
    'database': 'my_web_common'
}

# 全局缓存
cache = {
    'tables': [],
    'table_data': {},
    'connected': False
}

def init_database():
    """初始化数据库连接和缓存"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cache['tables'] = [table[0] for table in tables]
        
        print(f"✓ 数据库连接成功！")
        print(f"✓ 找到 {len(cache['tables'])} 个表: {', '.join(cache['tables'])}")
        
        # 预加载每个表的数据（前1000行）
        for table in cache['tables']:
            try:
                cursor.execute(f"DESCRIBE {table}")
                columns_info = cursor.fetchall()
                columns = [col[0] for col in columns_info]
                
                cursor.execute(f"SELECT * FROM {table} LIMIT 1000")
                rows = cursor.fetchall()
                
                # 转换为字典列表
                data = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col] = row[i]
                    data.append(row_dict)
                
                cache['table_data'][table] = {
                    'columns': columns,
                    'data': data,
                    'count': len(data)
                }
                print(f"  ✓ 表 '{table}' 已加载 ({len(data)} 行)")
            except Error as e:
                print(f"  ✗ 表 '{table}' 加载失败: {e}")
        
        cursor.close()
        connection.close()
        cache['connected'] = True
        print("✓ 所有数据已缓存到内存")
        
    except Error as e:
        print(f"✗ 数据库连接失败: {e}")
        cache['connected'] = False

@app.route('/')
def index():
    """提供HTML文件"""
    return send_from_directory('.', 'index.html')

@app.route('/app.js')
def app_js():
    """提供JS文件"""
    return send_from_directory('.', 'app.js')

@app.route('/api/tables', methods=['GET'])
def get_tables():
    """获取所有表"""
    if not cache['connected']:
        return jsonify({'success': False, 'error': '数据库未连接'}), 500
    
    return jsonify({
        'success': True,
        'tables': cache['tables']
    })

@app.route('/api/query', methods=['POST'])
def query_data():
    """查询表数据"""
    if not cache['connected']:
        return jsonify({'success': False, 'error': '数据库未连接'}), 500
    
    try:
        data = request.get_json()
        table = data.get('table')
        limit = data.get('limit', 1000)
        
        # 验证输入
        if not table or not isinstance(table, str):
            return jsonify({'success': False, 'error': '无效的表名'}), 400
        
        if not isinstance(limit, int) or limit < 1 or limit > 10000:
            return jsonify({'success': False, 'error': '行数必须在 1-10000 之间'}), 400
        
        # 防止SQL注入 - 只允许字母、数字、下划线
        if not all(c.isalnum() or c == '_' for c in table):
            return jsonify({'success': False, 'error': '表名包含无效字符'}), 400
        
        # 从缓存获取数据
        if table not in cache['table_data']:
            return jsonify({'success': False, 'error': f'表 {table} 不存在'}), 404
        
        table_info = cache['table_data'][table]
        columns = table_info['columns']
        all_data = table_info['data']
        
        # 返回指定数量的数据
        limited_data = all_data[:limit]
        
        return jsonify({
            'success': True,
            'columns': columns,
            'data': limited_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'connected': cache['connected'],
        'tables_count': len(cache['tables'])
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 数据库查看工具启动中...")
    print("="*50)
    
    # 初始化数据库
    init_database()
    
    print("\n" + "="*50)
    print("✓ 服务器启动在 http://localhost:8888")
    print("✓ 打开浏览器访问: http://localhost:8888")
    print("="*50 + "\n")
    
    app.run(host='localhost', port=8888, debug=False)
