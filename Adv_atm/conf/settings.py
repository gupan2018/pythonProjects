# -*- coding:utf-8 -*-
# __author__ = 'gupan'

"""
提供配置信息
"""

import os
import sys
import logging

#项目主目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
数据库配置信息
engine:数据库引擎
    file_storage：操作数据库为文件
    mysql：操作数据库为mysql
    oracle：操作数据库为oracle
    others：其余数据库引擎待扩展
name：
path：
"""
DATABASE = {
    'engine': 'file_storage', #support mysql,postgresql in the future
    'name':'accounts',
    'path': "%s/db" % BASE_DIR
}

#打印日志等级
LOG_LEVEL = logging.INFO

#打印日志位置
TRANS = "transaction"
ACCESS = "access"
"""
以字典格式设置日志打印位置
在日志打印类中设置初始化参数log_type，通过LOG_TYPES字典的键值形式，限制其类型
"""
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}


"""
业务操作接口字典，用于存储业务操作接口操作类型以及对应操作

业务类型：
    replay：还款
    withdraw：提现
    transfer：转账
    consume：消费

action:
    业务对应账户金额增减
    plus：账户余额增加
    minus：账户余额减少

interest：
    利息
    = 0：该操作不需要支付额外利息
    >0：该操作所对应得利率
"""
#操作类型及其对应操作
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},
}