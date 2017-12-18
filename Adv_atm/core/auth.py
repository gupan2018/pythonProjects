# -*- coding:utf-8 -*-
# __author__ = 'gupan'

"""
login()：用户登陆
enroll()：用户注册
is_authenrate()：装饰器，登陆状态验证

认证模块：
主要提供用户权限装饰器
1. 登陆用装饰器
2. 用户登陆认证用装饰器
3.
"""
from core.common.db_handler import Db
import json
import getpass
import time
'''
用户信息存储结构：
    /**
        *banlance：账户余额
        *credit：信用额度
        *enroll_day：注册日期
        *passwd:账户密码
        *name：用户名
        *status：账户状态 0表示正常，1表示异常，比如账户连续输错三次密码被冻结
    **/
'''
user_data = {
    "banlance":0,
    "credit":0,
    "status":False,

}

def acc_auth(name, passwd = None):
    handle = Db().db_handle()
    if passwd:
        sql = "SELECT * FROM accounts WHERE name = %s AND passed = %s"%(name, passwd)
    else:
        sql = "SELECT * FROM accounts WHERE name = %s"%(name,)
    data = handle(sql)
    return data

def login(user_status):
    '''
    登陆账户，若连续登陆失败三次，退出程序
    函数参数：
        user_status：字典格式，用来保存当前用户登陆状态
    返回值：
        data：用户数据

    函数执行成功后重置user_status中account_name和is_authenrated的值为用户名和True
    '''
    try_count = 0
    while try_count < 3:
        name = input("请输入用户名>>>")
        passwd = input("请输入密码>>>")
        data = acc_auth(name, passwd)
        if data:
            user_status["account_name"] = name
            user_status["is_authenticated"] = True
            return data
        print("用户名或密码错误，请重新输入")
        try_count += 1
    exit("登陆次数操作三次，禁止登陆")


def enroll(user_status):
    '''
    用户注册，执行登陆的sql语句，如果执行结果为None，那么该用户没有注册，可以进行注册
    函数参数：
        user_status：用户登陆状态函数，默认注册工程后处于登陆状态
    函数执行成功后返回用户数据data
    '''
    name = ""
    passwd = ""
    credit = 0
    time_format = "%Y-%m-%d"
    enroll_day = time.strftime(time_format)
    status = 0
    while True:
        name = input("请输入用户名>>>")
        if name == "b":
            exit("放弃注册")
        FLAG = acc_auth(name)
        #如果
        if not FLAG:
            print("该用户名已被注册，请重新输入")
            continue

        user_status["account_name"] = name
        user_status["is_authenticated"] = True
        break

    Input_auth = False
    while not Input_auth:
        passwd = input("请设置密码>>>")
        password_acc = input("请确认密码>>>")
        if not passwd or passwd != password_acc:
            print("\033[31[0m两次密码需一致\033[1m")
            continue
        credit = input("请输入该用户的信用额度>>>")
        if credit.isdigit() and int(credit) >= 15000:
            Input_auth = True

    handle = Db().db_handle()
    #{"balance": 752.5499999999884, "expire_date": "2021-01-01", "enroll_date": "2016-01-02", "credit": 15000, "id": 1234, "status": 0, "pay_day": 22, "password": "abc"}
    '''
    用户信息存储结构：
        /**
        *banlance：账户余额
        *credit：信用额度
        *enroll_day：注册日期
        *passwd:账户密码
        *name：用户名
        *status：账户状态 0表示正常，1表示异常，比如账户连续输错三次密码被冻结
        **/
    '''
    sql = "INSERT INTO (name, passwd, credit, balance, enroll_day, status) accounts VALUES" \
          " ({name}, {passwd}, {credit}, {balance}, {enroll_day}, {status})".format(
        name = name, passwd = passwd, credit = credit, balance = credit, enroll_day = enroll_day, status = status
    )

    data = handle(sql)
    return data

def is_authenrate(func):
    def derector(*args, **kwargs):
        TRANS_LOGGER = args[0]
        data = kwargs
        if not data["is_authenticated"]:
            TRANS_LOGGER.error("%s失败，用户未登陆"%func.__name__)
            return False
        if int(data["status"]) == 1:
            TRANS_LOGGER.error("\033[31;1m该用户已被冻结，请联系管理员\033[0m")
            return False
        else:
            return func(*args, **kwargs)
    return derector