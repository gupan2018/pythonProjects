# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import logging
import os


LOG_LEVEL = logging.INFO
BASE_DIR = BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_TYPES = {
    # 'transaction': 'transactions.log',
    'access': 'access.log',
}

# print(BASE_DIR)

DB_ROOT = BASE_DIR + "/db/Users"

res_msg = {
    200:"命令执行成功",
    500:"服务器内部错误"
}