import mysql.connector
from mysql.connector import Error

# 数据库连接配置
DB_CONFIG = {
    'host': '43.153.71.169',
    'port': 3306,
    'user': 'root',
    'password': '8ta6R',
    'database': 'my_web_common'
}

# DB_CONFIG = {
#     'host': 'usw-cynosdbmysql-grp-1gt4j3b5.sql.tencentcdb.com',
#     'port': 23829,
#     'user': 'root',
#     'password': 'cC52048078307',
#     'database': 'my_common_video_db'
# }

class DatabaseConnector:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接到数据库"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("✓ 数据库连接成功！")
            return True
        except Error as e:
            print(f"✗ 连接失败: {e}")
            return False
    
    def get_tables(self):
        """获取数据库中的所有表"""
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            return [table[0] for table in tables]
        except Error as e:
            print(f"✗ 获取表列表失败: {e}")
            return []
    
    def get_table_structure(self, table_name):
        """获取表的结构"""
        try:
            self.cursor.execute(f"DESCRIBE {table_name}")
            columns = self.cursor.fetchall()
            return columns
        except Error as e:
            print(f"✗ 获取表结构失败: {e}")
            return []
    
    def get_table_data(self, table_name, limit=10):
        """获取表的数据"""
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            return columns, rows
        except Error as e:
            print(f"✗ 获取表数据失败: {e}")
            return [], []
    
    def get_table_count(self, table_name):
        """获取表的行数"""
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"✗ 获取表行数失败: {e}")
            return 0
    
    def query(self, sql):
        """执行自定义SQL查询"""
        try:
            self.cursor.execute(sql)
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            return columns, rows
        except Error as e:
            print(f"✗ 查询失败: {e}")
            return [], []
    
    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ 数据库连接已关闭")

def print_table_data(columns, rows):
    """格式化打印表数据"""
    if not columns:
        print("没有数据")
        return
    
    # 计算列宽
    col_widths = [max(len(str(col)), max([len(str(row[i])) for row in rows] if rows else [0])) for i, col in enumerate(columns)]
    
    # 打印表头
    header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
    print(header)
    print("-" * len(header))
    
    # 打印数据行
    for row in rows:
        print(" | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row)))

def main():
    # 创建连接器
    db = DatabaseConnector(DB_CONFIG)
    
    # 连接数据库
    if not db.connect():
        return
    
    try:
        # 1. 获取所有表
        print("\n" + "="*50)
        print("📋 数据库中的所有表:")
        print("="*50)
        tables = db.get_tables()
        if tables:
            for i, table in enumerate(tables, 1):
                count = db.get_table_count(table)
                print(f"{i}. {table} (行数: {count})")
        else:
            print("没有找到任何表")
        
        # 2. 交互式查询
        print("\n" + "="*50)
        print("🔍 交互式查询")
        print("="*50)
        
        while True:
            print("\n选择操作:")
            print("1. 查看某个表的结构")
            print("2. 查看某个表的数据")
            print("3. 执行自定义SQL")
            print("4. 退出")
            
            choice = input("\n请输入选择 (1-4): ").strip()
            
            if choice == '1':
                table_name = input("请输入表名: ").strip()
                if table_name in tables:
                    print(f"\n表 '{table_name}' 的结构:")
                    structure = db.get_table_structure(table_name)
                    print(f"{'字段名':<20} {'类型':<20} {'Null':<10} {'Key':<10} {'默认值':<15}")
                    print("-" * 75)
                    for col in structure:
                        print(f"{col[0]:<20} {col[1]:<20} {col[2]:<10} {col[3]:<10} {str(col[4]):<15}")
                else:
                    print(f"✗ 表 '{table_name}' 不存在")
            
            elif choice == '2':
                table_name = input("请输入表名: ").strip()
                if table_name in tables:
                    limit = input("请输入要查看的行数 (默认10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    
                    print(f"\n表 '{table_name}' 的数据 (前{limit}行):")
                    columns, rows = db.get_table_data(table_name, limit)
                    print_table_data(columns, rows)
                else:
                    print(f"✗ 表 '{table_name}' 不存在")
            
            elif choice == '3':
                sql = input("请输入SQL语句: ").strip()
                if sql:
                    columns, rows = db.query(sql)
                    print_table_data(columns, rows)
            
            elif choice == '4':
                print("退出程序")
                break
            
            else:
                print("✗ 无效的选择")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
