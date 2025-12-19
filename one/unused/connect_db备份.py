
import pymysql

# 配置数据库信息（替换这里的host为你的服务器公网IP）
config = {
    "host": "43.153.71.169",  # 比如123.xxx.xxx.xxx
    "port": 3306,
    "user": "root",
    "password": "8ta6R",
    "database": "my_common_video_db"
}

# 连接并测试查询
try:
    # 1. 建立连接
    conn = pymysql.connect(**config)
    print("数据库连接成功！")

    # 2. 创建游标
    cursor = conn.cursor()

    # 3. 查看数据库中的表
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("\n数据库中的表：")
    for table in tables:
        print(table[0])

    # 4. 可选：查询某张表的内容（替换成你的表名）
    # cursor.execute("SELECT * FROM 你的表名 LIMIT 10;")
    # rows = cursor.fetchall()
    # print("\n表内容：", rows)

except Exception as e:
    print(f"连接失败：{e}")
finally:
    # 关闭连接
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()
        print("\n连接已关闭")
