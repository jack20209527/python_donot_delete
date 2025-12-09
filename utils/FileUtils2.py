import os
import shutil

"""
    1.拷贝文件: 源文件的完整路径，目标文件夹的完整路径。[如果存在相同的，就先删除，再拷贝]
            输入的文件夹后面是否有斜杠，都不影响；
    2.拷贝文件夹: 
                original_dir_full_path (str): 目标父文件夹的完整路径（必须存在，新文件夹将拷贝到这里）。
                new_dir_full_path (str): 要拷贝的源子文件夹的完整路径（新文件夹）。
          original_dir_3 = "/Users/sun2022/Downloads/Kun/"
          new_dir_3 = "/Users/tempburstlibs"
          相当于这样: 相当于给new_dir_3拷贝到
    3.删除文件: delete_file：直接删除文件Kun(有误斜杠不影响)的文件下，如果Kun下有同名的文件夹，就删除(shutil.rmtree)同名的文件夹，再拷贝
    4.删除文件夹: delete_folder: /Users/sun2022/Downloads/Kun/Scenes/，会给Scenes文件夹删掉的
"""

def copy_file_to_folder(new_file_path: str, target_folder_path: str) -> bool:
    """
    拷贝文件到指定的文件夹内。

    执行流程:
    1. 确保源文件存在且为文件。
    2. 确保目标文件夹存在（不存在则创建）。
    3. 检查目标文件夹内是否有同名文件，如果有，则先删除。
    4. 拷贝源文件到目标文件夹。

    参数:
        new_file_path (str): 源文件的完整路径（要拷贝的文件）。
        target_folder_path (str): 目标文件夹的完整路径。

    返回:
        bool: 如果拷贝成功返回 True，否则返回 False。
    """
    # 1. 检查源文件是否存在且为文件
    if not os.path.exists(new_file_path):
        print(f"❌ 源文件不存在: {new_file_path}")
        return False
    if os.path.isdir(new_file_path):
        print(f"⚠️ 源路径指向的是文件夹，请使用 copy_folder 函数: {new_file_path}")
        return False

    try:
        # 2. 确保目标文件夹存在（不存在则创建）
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)
            print(f"💡 创建目标文件夹: {target_folder_path}")

        # 构造目标文件在目标文件夹内的完整路径
        target_file_in_folder = os.path.join(target_folder_path, os.path.basename(new_file_path))

        # 3. 检查并手动删除同名文件 (符合您的需求逻辑)
        # 如果构造的target_file_in_folder存在，下面的if如果判断不是文件，那么就报错，肯定是文件夹了
        if os.path.exists(target_file_in_folder):
            if os.path.isfile(target_file_in_folder):
                os.remove(target_file_in_folder)
                print(f"🔄 检测到同名文件，已删除目标文件: {target_file_in_folder}")
            # elif os.path.isdir(target_file_in_folder):
            #     shutil.rmtree(final_destination_path)
            else:
                # 目标路径存在但不是文件（可能是文件夹），此时我们不能直接删除，需要报错
                print(f"{target_file_in_folder} 是文件夹了，最好不要覆盖和删除: 是否是文件夹: ${os.path.isdir(target_file_in_folder)}")
                print(f"❌ 目标路径存在冲突，且不是文件: {target_file_in_folder}")
                return False

        # 4. 执行拷贝操作
        shutil.copy2(new_file_path, target_file_in_folder)

        print(f"✅ 文件拷贝成功: 从 {new_file_path} 到 {target_file_in_folder}")
        return True

    except PermissionError:
        print(f"❌ 权限错误：无法执行拷贝、删除或创建操作。")
        return False
    except OSError as e:
        print(f"❌ 拷贝文件时发生其他错误: {e}")


def copy_new_folder_into_existing_folder(original_dir_full_path: str, new_dir_full_path: str) -> bool:
    """
    将一个完整的源文件夹（即 new_dir_full_path）拷贝到指定的父文件夹（即 original_dir_full_path）中。
    如果父文件夹内存在同名子文件夹，则先删除旧的，再拷贝新的（实现覆盖）。

    参数:
        original_dir_full_path (str): 目标父文件夹的完整路径（必须存在，新文件夹将拷贝到这里）。
        new_dir_full_path (str): 要拷贝的源子文件夹的完整路径（新文件夹）。

    返回:
        bool: 如果拷贝成功返回 True，否则返回 False。
    """

    # 1. 检查目标父文件夹（original_dir_full_path）是否合法
    if not os.path.isdir(original_dir_full_path):
        print(f"❌ 目标父文件夹不存在或不是一个文件夹: {original_dir_full_path}")
        return False

    # 2. 检查源文件夹（new_dir_full_path）是否合法
    if not os.path.isdir(new_dir_full_path):
        print(f"❌ 源路径不是有效的文件夹: {new_dir_full_path}")
        return False


    # 获取要拷贝的子文件夹的名称（例如，从 '/a/b/my_folder' 得到 'my_folder'）
    folder_name = os.path.basename(new_dir_full_path)

    # 构造目标子文件夹的完整路径 (即在 original_dir_full_path 内部的路径)
    final_destination_path = os.path.join(original_dir_full_path, folder_name)

    try:
        # 3. 检查目标父文件夹内是否已存在同名子文件夹，如果存在，则先删除（覆盖逻辑）
        if os.path.exists(final_destination_path):
            shutil.rmtree(final_destination_path)
            print(f"🔄 检测到同名子文件夹，已删除目标路径: {final_destination_path}")

        # 4. 执行拷贝操作
        # 将 new_dir_full_path 拷贝到 final_destination_path
        shutil.copytree(new_dir_full_path, final_destination_path)

        print(f"✅ 文件夹拷贝成功: 将 {folder_name} 拷贝到 {original_dir_full_path} 中")
        return True

    except PermissionError:
        print(f"❌ 权限错误：无法执行拷贝或删除操作。")
        return False
    except OSError as e:
        print(f"❌ 拷贝文件夹时发生其他错误: {e}")
        return False

def rename_folder(folder_path: str, new_name: str) -> str:
    """
    重命名文件夹。

    参数:
        folder_path (str): 要重命名的文件夹的完整路径。
        new_name (str): 新的文件夹名称（仅名称，不是完整路径）。

    返回:
        str: 如果重命名成功返回新的完整路径，否则返回空字符串。
    """
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在: {folder_path}")
        return ""

    if not os.path.isdir(folder_path):
        print(f"⚠️ 路径指向的是文件，不是文件夹: {folder_path}")
        return ""

    # 获取父目录
    parent_dir = os.path.dirname(folder_path.rstrip('/'))
    # 构造新的完整路径
    new_folder_path = os.path.join(parent_dir, new_name)

    # 检查新路径是否已存在
    if os.path.exists(new_folder_path):
        print(f"⚠️ 目标路径已存在，先删除: {new_folder_path}")
        shutil.rmtree(new_folder_path)

    try:
        os.rename(folder_path, new_folder_path)
        print(f"✅ 文件夹重命名成功: {folder_path} -> {new_folder_path}")
        return new_folder_path
    except PermissionError:
        print(f"❌ 权限错误：无法重命名文件夹: {folder_path}")
        return ""
    except OSError as e:
        print(f"❌ 重命名文件夹时发生错误: {e}")
        return ""


def delete_file(file_path: str) -> bool:

    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False

    if os.path.isdir(file_path):
        print(f"⚠️ 路径指向的是文件夹，请使用 delete_folder 函数: {file_path}")
        return False

    try:
        os.remove(file_path)
        print(f"✅ 文件删除成功: {file_path}")
        return True
    except PermissionError:
        print(f"❌ 权限错误：无法删除文件 (可能文件正在被使用): {file_path}")
        return False
    except OSError as e:
        print(f"❌ 删除文件时发生其他错误: {file_path}. 错误信息: {e}")
        return False


def delete_folder(folder_path: str) -> bool:
    """
    递归删除指定的文件夹及其所有内容（即使文件夹非空）。
    bool: 如果删除成功返回 True，否则返回 False。
    """
    if not os.path.exists(folder_path):
        print(f"❌ 文件夹不存在: {folder_path}")
        return False

    if not os.path.isdir(folder_path):
        print(f"⚠️ 路径指向的是文件，请使用 delete_file 函数: {folder_path}")
        return False

    try:
        # shutil.rmtree 递归删除文件夹及其内容
        shutil.rmtree(folder_path)
        print(f"✅ 文件夹删除成功: {folder_path}")
        return True
    except PermissionError:
        print(f"❌ 权限错误：无法删除文件夹 (可能文件夹中的文件正在被使用): {folder_path}")
        return False
    except OSError as e:
        print(f"❌ 删除文件夹时发生其他错误: {folder_path}. 错误信息: {e}")
        return False


# --- 示例用法 ---
if __name__ == '__main__':

    file1 = "/Users/sun2022/Downloads/Kun/Scenes/BluetoothTest.unity"
    dir1 = "/Users/sun2022/Downloads/Kun/Scenes"

    # delete_file (file1)
    # delete_folder(dir1)

    file2 = "/Users/sun2022/Downloads/Kun/Scripts/Gyro.meta"
    target_folder2 = "/Users/sun2022/Downloads/Kun/"
    # copy_file_to_folder (file2, target_folder2)

    original_dir_3 = "/Users/sun2022/Downloads/Kun/"
    new_dir_3 = "/Users/tempburstlibs"
    # new_dir_3 = "/Users/sun2022/Downloads/YZOS/yzos_BurstDebugInformation_DoNotShip/tem333pburstlibs"
    copy_new_folder_into_existing_folder (original_dir_3, new_dir_3)



    # 1. 设置测试路径
    # test_dir = "test_cleanup_dir"
    # test_file = os.path.join(test_dir, "temp_file.txt")
    #
    # # 2. 准备环境 (创建文件和文件夹)
    # if not os.path.exists(test_dir):
    #     os.makedirs(test_dir)
    # with open(test_file, 'w') as f:
    #     f.write("This is a temporary file.")
    #
    # print("\n--- 开始测试 ---")
    #
    # # 3. 测试删除文件
    # print("\n--- 测试 delete_file ---")
    # delete_file(test_file)
    # delete_file(test_file) # 再次尝试删除不存在的文件
    #
    # # 4. 测试删除文件夹 (注意：在删除文件后，文件夹可能变为空)
    # print("\n--- 测试 delete_folder ---")
    # delete_folder(test_dir)
    # delete_folder(test_dir) # 再次尝试删除不存在的文件夹
    #
    # # 5. 测试路径误用
    # print("\n--- 测试路径误用 ---")
    # os.makedirs(test_dir) # 重新创建文件夹
    # with open(test_file, 'w') as f: # 重新创建文件
    #     f.write("File for misuse test.")
    #
    # delete_file(test_dir) # 尝试用 delete_file 删除文件夹
    # delete_folder(test_file) # 尝试用 delete_folder 删除文件
    #
    # # 清理残留环境
    # if os.path.exists(test_dir):
    #     shutil.rmtree(test_dir)
    #
    # print("\n--- 测试结束 ---")