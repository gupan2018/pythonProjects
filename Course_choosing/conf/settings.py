# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import logging

#项目主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'accounts',
    'path': "%s/db" % BASE_DIR
}
# 各个分校可以开设的课程
courses = {
    "北京":["linux", "python", "go"],
    "上海":["linux", "python"]
}

# 记录各用户登陆状态的标志位含义
User_obj = 0
Is_Authenticated = 1

# 打印日志等级
LOG_LEVEL = logging.INFO

# 打印日志位置
LOG_TYPES = {
    'access': 'access.log',
}