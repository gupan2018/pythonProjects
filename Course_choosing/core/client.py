# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.common.db_handler import Db
from core.school import School
from core.options.manage import Manage
from core.options.auth import Auth
from core.options.userAuth import UserAuth
from core.options.teaOption import TeaOption
from core.options.stuOption import StuOption

class Client(object):
    """
    类功能：
    stu_entry(auth_data, ACCESS_LOG):学生操作接口，调用认证操作以及学生业务操作
    tea_entry(auth_data, ACCESS_LOG)：教师操作接口，调用认证操作以及教师相关业务操作
    mana_entry(ACCESS_LOG)：管理操作接口，调用学校管理接口
    """
    def __init__(self):
        super(Client, self).__init__()

    @staticmethod
    def stu_entry(auth_data, ACCESS_LOG):
        """
        函数功能：学生操作接口，调用认证操作以及学生相关业务操作
        :param auth_data: 记录用户登陆状态
        :param ACCESS_LOG: 记录用户操作logger
        :return: 无
        """
        msg = '''
        -----------------------------请选择您的操作-------------------------
        1：登陆或注册
        2：进行报名等操作
        b：返回上一层
        -----------------------------------end------------------------------
        '''
        print(msg)
        menu = {
            "1": Auth.stu_auth,
            "2": StuOption.stu_option
        }

        res_msg = {
            "1": "操作成功，您可以进行下一步操作",
            "2": "登陆或注册失败",
            "3": "操作成功",
            "4": "操作失败"
        }

        while True:
            choice = input("请输入您要进行的操作>>>").strip()
            if choice in menu.keys():
                res_code = menu[choice](auth_data, ACCESS_LOG)
                ACCESS_LOG.info(res_msg[res_code])
                break
            print("输入有误，请重新输入")

    @staticmethod
    def tea_entry(auth_data, ACCESS_LOG):
        """
        函数功能：教师操作接口，调用认证操作以及教师相关业务操作
        :param auth_data: 记录用户登陆状态
        :param ACCESS_LOG: 记录用户操作logger
        :return:
        """
        msg = '''
        -----------------------------请选择您的操作-------------------------
        1：登陆或注册
        2：进行教师也有操作
        b：返回上一层
        -----------------------------------end------------------------------
        '''
        print(msg)

        menu = {
            "1": Auth.tea_auth,
            "2": TeaOption.tea_option
        }

        res_msg = {
            "1": "操作成功，您可以进行下一步操作",
            "2": "登陆或注册失败",
            "3": "操作成功",
            "4": "操作失败"
        }

        while True:
            choice = input("请输入您要进行的操作>>>").strip()
            if choice in menu.keys():
                res_code = menu[choice](auth_data, ACCESS_LOG)
                ACCESS_LOG.info(res_msg[res_code])
                break
            print("输入有误，请重新输入")

    @staticmethod
    def mana_entry(auth_data, ACCESS_LOG):
        """
        函数功能：管理操作接口，调用学校管理接口
        :param ACCESS_LOG: 记录用户操作logger
        :return:
        """
        sql = "SELECT * FROM schools"
        schools = Db.db_handle()(sql)

        school_msg = ""

        if not schools:
            school_msg = "无"

        for school in schools:
            school_msg += "%s\n"%school

        msg = '''
        -----------------------------目前已开设的学校为----------------------
        {msg}
        \033[31;1m------------------------------------------------------------------\033[0m
        1：开办新学校
        2：对现有学校进行管理
        b：返回上一层
        -----------------------------------end------------------------------
        '''.format(msg = school_msg)

        print(msg)

        menu = {
            "1":Manage.create_school,
            "2":Manage.manage_school,
        }

        while True:
            choice = input("请输入您的选择\033[31;1m>>>\033[0m").strip()
            if not choice:
                print("输入不能为空")
                continue
            elif choice in menu.keys():
                menu[choice](ACCESS_LOG)
            elif choice == "b":
                break
            else:
                print("输入有误，请重新输入")