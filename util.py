import os
import random
import shutil


# 实现数据划分，并完成文件移动
def split_data(file_path, train_data_ratio):
    # filepath：里面包含类别
    train_path = os.path.join(file_path, "train")
    dev_path = os.path.join(file_path, "dev")
    clear_and_mkdir_file_path(train_path)
    clear_and_mkdir_file_path(dev_path)

    category_list = os.listdir(file_path)
    category_list.remove("train")
    category_list.remove("dev")
    for category in category_list:
        file_list = os.listdir(os.path.join(file_path, category))
        random.shuffle(file_list)  # 打乱顺序
        train_num = int(len(file_list) * train_data_ratio)
        category_train_path = mkdir_file_path(os.path.join(train_path, category))
        category_dev_path = mkdir_file_path(os.path.join(dev_path, category))
        for i, file in enumerate(file_list):
            src = file_path + "//" + category + "//" + file
            if i < train_num:
                dst = category_train_path + "//" + file
            else:
                dst = category_dev_path + "//" + file
            shutil.copy(src, dst)
    return train_path, dev_path



def mkdir_file_path(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    return file_path


# 清空文件夹并且创建
def clear_and_mkdir_file_path(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.mkdir(file_path)
    pass



if __name__ == '__main__':
    file_path = "../4.深度学习软件/data/test"
    train_data_ratio = 0.7
    split_data(file_path=file_path, train_data_ratio=train_data_ratio)
