import redis

# 配置Redis连接信息
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "decode_responses": True,  # 自动把bytes转字符串，不用手动decode
    "socket_timeout": 5,       # 连接超时时间
}

def test_redis_connection():
    """测试Redis连接和基础操作"""
    try:
        # 创建Redis连接
        r = redis.Redis(**REDIS_CONFIG)

        # 测试连接
        # r.ping()
        print("✅ 成功连接到Redis服务器！")

        # 测试基础操作
        key = "test_key"
        value = "hello_redis"
        r.set(key, value)  # 设置键值对
        result = r.get(key)  # 获取值
        print(f"✅ 键{key}的值为：{result}")

        r.set(key, "dollar")
        result = r.get(key)  # 获取值
        print(f"✅ 键{key}的值为：{result}")

        # 删除测试键
        r.delete(key)
        print("✅ 测试完成，已清理测试数据")

    except redis.ConnectionError as e:
        print(f"❌ 连接Redis失败：{e}")
        print("   请检查：1.Redis服务是否启动 2.主机/端口是否正确 3.防火墙是否拦截")
    except Exception as e:
        print(f"❌ 未知错误：{e}")

if __name__ == "__main__":
    test_redis_connection()