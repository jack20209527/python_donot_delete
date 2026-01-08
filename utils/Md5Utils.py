import hashlib


# 计算文件的MD5（大文件分块读取）
def md5_file(file_path: str) -> str:
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()

# 计算字符串的MD5（返回32位小写十六进制）
def md5_str(input_str: str) -> str:
    return hashlib.md5(input_str.encode()).hexdigest()

# 计算字符串的MD5（32位大写十六进制）
def md5_str_upper(input_str: str) -> str:
    return hashlib.md5(input_str.encode()).hexdigest().upper()


# 验证字符串与MD5是否匹配
def verify_md5_str(input_str: str, md5_val: str) -> bool:
    return md5_str(input_str) == md5_val.lower()

# 验证文件与MD5是否匹配
def verify_md5_file(file_path: str, md5_val: str) -> bool:
    return md5_file(file_path) == md5_val.lower()

# 计算字符串的MD5（返回bytes类型摘要）
def md5_bytes(input_str: str) -> bytes:
    return hashlib.md5(input_str.encode()).digest()

if __name__ == "__main__":

    md5 = md5_file("/Users/sun2022/Downloads/公司/全量版本418/app_honor_release_v4.8.apk")
    print(md5)


