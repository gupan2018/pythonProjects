# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from conf import settings
from core.options.stuOption import StuOption
from core.options.teaOption import TeaOption

class Auth(object):
    """
    stu_auth(auth_data, ACCESS_LOG)：学生登陆或注册操作功能入口
    tea_auth(auth_data, ACCESS_LOG)：教师登陆或注册操作功能入口
    is_login(func)：验证用户是否登陆
    """
    def __init__(self):
        super(Auth, self).__init__()

    @staticmethod
    def stu_auth(auth_data, ACCESS_LOG):
        """
        函数功能：学生登陆或注册操作功能入口
        :param auth_data: 记录用户登陆或注册状态字典
        :param ACCESS_LOG: 日志操作logger
        :return: 返回状态码：
            /**
            * 1：成功
            * 2：失败
            **/
        """
        msg = '''
        -----------------------------请选择您的操作-------------------------
        1：登陆
        2：注册
        b：返回上一层
        -----------------------------------end------------------------------
        '''
        print(msg)
        menu = {
            "1": StuOption.stu_login,
            "2": StuOption.stu_register
        }

        res_msg = {
            "1": "登陆成功",
            "2": "登陆失败：账户名或密码错误",
            "3": "注册成功",
            "4": "注册失败：该用户已被注册"
        }

        while True:
            choice = input("请输入您要进行的操作>>>").strip()
            if choice in menu.keys():
                res_code = menu[choice](auth_data, ACCESS_LOG)
                ACCESS_LOG.info(res_msg[res_code])

                if res_code == "1" or res_code == "3":
                    return "1"
                else:
                    return "2"
            print("输入有误，请重新输入")

    @staticmethod
    def tea_auth(auth_data, ACCESS_LOG):
        """
        函数功能：教师登陆或注册操作功能入口
        :param auth_data:记录用户登陆或注册状态字典
        :param ACCESS_LOG:日志操作logger
        :return:返回状态码：
            /**
            * 1：成功
            * 2：失败
            **/
        """
        msg = '''
            -----------------------------请选择您的操作-------------------------
            1：登陆
            2：注册
            b：返回上一层
            -----------------------------------end------------------------------
            '''
        print(msg)
        menu = {
            "1": TeaOption.tea_login,
            "2": TeaOption.tea_register
        }

        res_msg = {
            "1": "登陆成功",
            "2": "登陆失败：账户名或密码错误",
            "3": "注册成功",
            "4": "注册失败：该用户已被注册"
        }

        while True:
            choice = input("请输入您要进行的操作>>>").strip()
            if choice in menu.keys():
                res_code = menu[choice](auth_data, ACCESS_LOG)
                ACCESS_LOG.info(res_msg[res_code])

                if res_code == "1" or res_code == "3":
                    return "1"
                else:
                    return "2"
            print("输入有误，请重新输入")