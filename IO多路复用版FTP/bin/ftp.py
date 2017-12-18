# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)

from core import main

'''
题目:IO多路复用版FTP

需求:

    实现文件上传及下载功能
    支持多连接并发传文件
    使用select or selectors

'''

if __name__ == "__main__":
    main.run()