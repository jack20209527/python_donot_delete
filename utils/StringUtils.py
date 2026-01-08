

# 移除某个符号: 如":"
def remove_fuhao (fuhao: str, input_str: str) -> str:
    s = input_str.replace(fuhao, "")
    return s

# 转换为小写
def to_lowercase(input_str: str) -> str:
    s = input_str.lower()
    return s

# 转换为大写
def to_uppercase(input_str: str) -> str:
    return input_str.upper()

# 首字母大写（每个单词）
def to_titlecase(input_str: str) -> str:
    return input_str.title()

# 移除首尾空格/指定字符
def strip_str(input_str: str, chars=None) -> str:
    return input_str.strip(chars)

# 移除所有空格
def remove_all_space(input_str: str) -> str:
    return input_str.replace(" ", "")

# 替换指定子串
def replace_substr(input_str: str, old: str, new: str) -> str:
    return input_str.replace(old, new)

# 按分隔符分割字符串
def split_str(input_str: str, sep: str) -> list:
    return input_str.split(sep)

# 拼接列表为字符串
def join_str(str_list: list, sep: str) -> str:
    return sep.join(str_list)

# 截取子串（起始索引-结束索引）
def slice_str(input_str: str, start: int, end: int) -> str:
    return input_str[start:end]

# 判断是否包含子串
def contains_substr(input_str: str, substr: str) -> bool:
    return substr in input_str

# 判断是否以指定字符串开头
def startswith_str(input_str: str, prefix: str) -> bool:
    return input_str.startswith(prefix)

# 判断是否以指定字符串结尾
def endswith_str(input_str: str, suffix: str) -> bool:
    return input_str.endswith(suffix)

# 统计子串出现次数
def count_substr(input_str: str, substr: str) -> int:
    return input_str.count(substr)

# 查找子串首次出现的索引（不存在返回-1）
def find_substr(input_str: str, substr: str) -> int:
    return input_str.find(substr)

# 替换指定位置字符（字符串不可变，转列表操作）
def replace_char_at(input_str: str, index: int, char: str) -> str:
    str_list = list(input_str)
    str_list[index] = char
    return ''.join(str_list)

# 补全字符串长度（左侧补0）
def ljust_zero(input_str: str, length: int) -> str:
    return input_str.zfill(length)

# 移除指定字符（如冒号）
def remove_char(input_str: str, char: str) -> str:
    return input_str.replace(char, "")


if __name__ == "__main__":
    original_str = "12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF"

    # 去除冒号
    no_colon_str = remove_fuhao(":", original_str)
    # 转换为小写
    final_str = to_lowercase(no_colon_str)

    # 打印结果
    print("原始字符串：", original_str)
    print("去除冒号后：", no_colon_str)
    print("转小写后最终结果：", final_str)

