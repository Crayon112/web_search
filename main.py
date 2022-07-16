# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""入口文件

@File: main.py
@Time: 2022/07/16 16:08:41
@Author: Crayon112
@SoftWare: VSCode
@Description: 入口文件

"""


# 从文本格式的数据读入数据 -> 查找
from web_search import SixSoft, PhantomShark, SkyGrass, User
from web_search.ocr import LocalOCR as OCR


mapping = {
    "SixSoft": SixSoft,  # zyb666 a123456789
    "PhantomShark": PhantomShark,  # ATM666888 ATM666888
    "SkyGrass": SkyGrass,  # hm001 010010
}


def read_web_apis(user_path):
    apis = []
    with open(user_path, 'r') as user_file:
        for user_info in user_file.readlines():
            platform, username, password = user_info.split()
            apis.append(mapping[platform](
                user=User(username, password),
                ocr=OCR(),
            ))
    return apis


def read_search_keys(key_path):
    search_keys = []
    with open(key_path, 'r') as key_file:
        for row in key_file.readlines():
            search_keys.append(row.strip('\n'))
    return search_keys


if __name__ == '__main__':
    apis = read_web_apis("./data/users.txt")
    keywords = read_search_keys('./data/search.txt')
    log_file = './data/log.txt'

    with open(log_file, 'w') as f:
        for keyword in keywords:
            searched = False
            for api in apis:
                if api.search(keyword):
                    searched = True
                    break
            if not searched:
                print(f"{keyword}", file=f)
