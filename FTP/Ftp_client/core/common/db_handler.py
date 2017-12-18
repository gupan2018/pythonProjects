# -*- coding:utf-8 -*-
# __author__ = 'gupan'

"""
数据库操作接口：
在conf.settings模块中设置了DATABASE
"""

from conf import settings
import os
import sys
import json

class Db:
    """
    改进建议（未实现功能）：
        该类封装了一个数据库的初始化以及sql执行函数
        建议后期封装一个Db_Handle类，该类集成了sql语句的执行方法，而Db类的功能只是初始化Db_Handle对象
    """

    """
    根据conf.settings模块中的DATABASE字典中的engine字典判断操作数据库的类型
        file_storage：文件类型
        mysql：mysql数据库
        oracle：oracle数据库
    __init__()：
        待实现，考虑将db_handle()函数的功能在此函数中实现，返回一个self.handler对数据库进行操作
        /**
        *考虑实现代码如下
        *db = Db()
        *db(sql)#执行sql语句
        **/

    db_handle()：
        用户判断数据库类型，返回不同类型的数据库操作对象
    file_db_handle()：
        载入文件类型数据库链接信息，返回操作文件类型数据库的对象
    mysql_db_handle()：
        载入mysql类型数据库链接信息，返回操作mysql类型数据库的对象
    oracle_db_handle()：
        载入oracle类型数据库链接信息，返回操作oracle类型数据库的对象

    mysql_execute()：
        执行sql语句操作mysql数据库
    file_execute()：
        执行sql语句操作文本文件
    oracle_execute()：
        执行sql语句操作oracle
    """
    def __init__(self):
        pass

    def db_handle(self):
        db_dic = settings.DATABASE
        db_type = db_dic["engine"]
        if db_type == "file_storage":
            return self.file_db_handle()
        elif db_type == "mysql":
            return self.mysql_db_handle()
        elif db_type == "oracle":
            return self.oracle_db_handle()
        else:
            exit("\033[31;1m this function is under develping, please wait\033[0m")



    def file_execute(self, sql):
        '''
        file_execute(sql)函数详解
        需要处理的sql语句的类型
        "SELECT * FROM accounts WHERE name = %s AND passwd = %s"%(name, passwd)
        "SELECT * FROM accounts WHERE name = %s"%(name,)
        "INSERT INTO accounts (****) VALUES (%s)"%json.dumps(data)
        "UPDATE accounts SET balance = {balance}, status = {status}, credit = {credit} WHERE name = {name}".format(balance = balance, status = status, credit = credit, name = name)
        '''

        '''
        优化建议：
            sql语句中将表名写死了，后续需做好动态参数化
            用os.path.isdir()判断该表是否存在
        '''

        if "SELECT" in sql:
            '''
            用split分割sql语句，用name判断accounts表中是否有{name}.json表存在，如果存在验证密码
            '''
            head, body = sql.split("WHERE")
            head = head.strip()
            body = body.strip()
            name, passwd = None, None
            if "AND" in body:
                name, passwd = body.split("AND")
                name = name.strip().split("=")[1].strip()
                passwd = passwd.strip().split("=")[1].strip()
            else:
                name = body.split("=")[1].strip()
            account_path = settings.BASE_DIR + "\\db\\accounts\\{name}.json".format(name = name)
            #验证登陆
            if passwd:
                if not os.path.exists(account_path):
                    exit("\033[31;1m您还未注册，请先注册\033[0m")
                with open(account_path, "r") as f_account:
                    b_data = f_account.read()
                    data = json.loads(b_data)
                    if data["passwd"] != passwd:
                        return False
                return data
            #验证注册
            else:
                if not os.path.exists(account_path):
                    return True
                else:
                    return False

        if "INSERT" in sql:
            '''
            用split分割sql语句，用name判断accounts表中是否有{name}.json表存在，不能注册，如果不存在，注册并写入数据
            '''
            head, body = sql.split("VALUES")
            head = head.strip()
            body = (body.strip().lstrip("(").rstrip(")")).split(",")

            for index in range(len(body)):
                body[index] = body[index].strip()

            head = head.split("(")[1].strip().split(")")[0].strip().split(",")
            for index in range(len(head)):
                head[index] = head[index].strip()

            index = head.index("name")
            name = body[index]
            account_path = settings.BASE_DIR + "\\db\\accounts\\{name}.json".format(name = name)
            if os.path.exists(account_path):
                return False
            data = {}
            with open(account_path, "w") as f_new:
                for item in head:
                    index = head.index(item)
                    data[item] = body[index]
                f_new.write(json.dumps(data))
            return data

        if "UPDATE" in sql:
            '''
            用split分割sql语句，用name判断accounts表中是否有{name}.json表存在，修改数据
            '''
            head, body = sql.split("SET")
            head = head.strip()
            body = body.strip()
            updates, where = body.split("WHERE")
            updates = updates.strip()
            where = where.strip()
            name = where.split("=")[1].strip()
            account_path = settings.BASE_DIR + "\\db\\accounts\\{name}.json".format(name = name)
            if os.path.exists(account_path):
                return False
            with open(account_path, "r") as f_account:
                b_data = f_account.read()
                data = json.loads(b_data)

            items = updates.split(",")
            for item in items:
                key, value = item.split("=")
                key = key.strip()
                value = value.strip()
                data[key] = value

            with open(account_path, "w") as f_update:
                f_update.write(json.dumps(data))
            return data
        exit("\033[31;0m Error SQL\033[0m")

    def mysql_execute(self, sql):
        pass

    def oracle_execute(self, sql):
        pass

    def file_db_handle(self):
        return self.file_execute

    def mysql_db_handle(self):
        print("\033[31;1m mysql \033[0m this function is under develping, please wait")
        return self.mysql_execute

    def oracle_db_handle(self):
        print("\033[31;1m oracle \033[0m this function is under develping, please wait")
        return self.oracle_execute