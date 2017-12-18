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
import pickle

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

    @staticmethod
    def db_handle():
        db_dic = settings.DATABASE
        db_type = db_dic["engine"]
        if db_type == "file_storage":
            return Db.file_db_handle()
        elif db_type == "mysql":
            return Db.mysql_db_handle()
        elif db_type == "oracle":
            return Db.oracle_db_handle()
        else:
            exit("\033[31;1m this function is under develping, please wait\033[0m")


    @staticmethod
    def file_execute(sql, obj = None):
        '''
        file_execute(sql)函数详解
        需要处理的sql语句的类型
        "SELECT school.name FROM schools%(name, passwd)
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
            if "WHERE" in sql:
                # 处理类似SELECT * FROM schools WHERE school.name = "北京"的sql
                head, condition = sql.split("WHERE")

                head, table = head.split("FROM")
                table = table.strip()
                condition = condition.split("=")[1].strip()
                search_path = settings.BASE_DIR + "/db/%s/%s.pickle" % (table, condition)

                if not os.path.exists(search_path):
                    # print("SELECT %s ：您所要查询的项目不存在"%table)
                    return False

                with open(search_path, "rb") as search_file:
                    data = search_file.read()
                    data = pickle.loads(data)
                    return data
            else:
                # 处理类似SELECT * FROM schools的sql
                head, table = sql.split("FROM")
                # 获取表名
                table = table.strip()
                head = head.strip("SELECT").strip()

                search_path = settings.BASE_DIR + "/db/%s" % table
                res_lists = []
                if not os.path.exists(search_path):
                    print("SELECT %s ：您所要查询的表不存在"%table)
                    return False
                file_list = os.listdir(search_path)
                # print(file_list)
                for file in file_list:
                    file = file.split(".")[0].strip()
                    # print(file)
                    res_lists.append(file)
                # 将返回查询到的名称列表
                return res_lists

        elif "INSERT" in sql:
            '''
            用split分割sql语句，用name判断accounts表中是否有{name}.json表存在，不能注册，如果不存在，注册并写入数据
            '''
            print("INSERT 语句未实现，请用UPDATE语句来代替")
            return False
            # head, body = sql.split("VALUES")
            # head = head.strip()
            # body = (body.strip().lstrip("(").rstrip(")")).split(",")
            #
            # for index in range(len(body)):
            #     body[index] = body[index].strip()
            #
            # head = head.split("(")[1].strip().split(")")[0].strip().split(",")
            # for index in range(len(head)):
            #     head[index] = head[index].strip()
            #
            # index = head.index("name")
            # name = body[index]
            # account_path = settings.BASE_DIR + "\\db\\accounts\\{name}.json".format(name = name)
            # if os.path.exists(account_path):
            #     return False
            # data = {}
            # with open(account_path, "w") as f_new:
            #     for item in head:
            #         index = head.index(item)
            #         data[item] = body[index]
            #     f_new.write(json.dumps(data))
            # return data

        if "UPDATE" in sql:
            if not obj:
                print("sql语句错误")
                return False
            # 用来处理类似sql语句
            # UPDATE schools SET data = update_obj WHERE school.name = "北京"
            head, condition = sql.split("WHERE")
            table = head.split("SET")[0].strip("UPDATE").strip()
            condition = condition.split("=")[1].strip()
            update_path = settings.BASE_DIR + "/db/%s/%s.pickle" % (table, condition)
            if not os.path.exists(update_path):
                print("%s//%s.pickle ：您所要修改/创建的项目不存在， 正在创建该项目"%(table, condition))
            with open(update_path, "wb") as update_file:
                data = pickle.dumps(obj)
                update_file.write(data)
                return True

    @staticmethod
    def mysql_execute(sql):
        pass

    @staticmethod
    def oracle_execute(sql):
        pass

    @staticmethod
    def file_db_handle():
        return Db.file_execute

    @staticmethod
    def mysql_db_handle():
        print("\033[31;1m mysql \033[0m this function is under develping, please wait")
        return Db.mysql_execute

    @staticmethod
    def oracle_db_handle():
        print("\033[31;1m oracle \033[0m this function is under develping, please wait")
        return Db.oracle_execute