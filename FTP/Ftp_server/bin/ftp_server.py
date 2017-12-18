# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys

"""
需求：开发一个支持多用户在线的FTP程序

要求：

    用户加密认证
    允许同时多用户登录
    每个用户有自己的家目录 ，且只能访问自己的家目录
    对用户进行磁盘配额，每个用户的可用空间不同
    允许用户在ftp server上随意切换目录
    允许用户查看当前目录下文件
    允许上传和下载文件，保证文件一致性
    文件传输过程中显示进度条
    附加功能：支持文件的断点续传

"""

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_PATH)
sys.path.insert(0, BASE_PATH)

from core import main

if __name__ == "__main__":
    main.run()