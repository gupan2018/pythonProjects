# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.people.teacher import Teacher
from conf import settings
from core.options.userAuth import UserAuth
from core.common.db_handler import Db

class TeaOption(object):
    """
    tea_option(auth_data, ACCESS_LOG)：调用教师查询授课班级信息、查询授课学生信息、给学生打分接口
    tea_register(auth_data, ACCESS_LOG)：教师注册
    tea_login(auth_data, ACCESS_LOG)：教师登陆
    view_self_classes(auth_data, name, ACCESS_LOG)：查看教师自己所教授班级
    view_self_students(auth_data, name, ACCESS_LOG)：查看教师自己所教授学生
    grade_student(auth_data, name, ACCESS_LOG)：给学生打分
    """
    def __init__(self):
        super(TeaOption, self).__init__()

    @staticmethod
    def tea_option(auth_data, ACCESS_LOG):
        """
        函数功能：调用教师查询授课班级信息、查询授课学生信息、给学生打分接口
        :param auth_data:记录用户登陆状态
        :return:
        """
        msg = '''
            -----------------------------请选择您的操作-------------------------
            1：浏览所教授班级信息
            2：浏览所教授学生信息
            3：为学生打分
            b:退出
            -----------------------------------end------------------------------
            '''
        print(msg)

        menu = {
            "1": TeaOption.view_self_classes,
            "2": TeaOption.view_self_students,
            "3": TeaOption.grade_student
        }

        name = input("请输入您的账户名>>>").strip()

        while True:
            choice = input("请输入您要进行的操作>>>").strip()
            if choice in menu.keys():
                menu[choice](auth_data=auth_data, name=name, ACCESS_LOG = ACCESS_LOG)
                return "3"
            if choice == "b":
                print("bye".center(50, "-"))
                break
            print("输入有误，请重新输入")

    @staticmethod
    def tea_register(auth_data, ACCESS_LOG):
        """
        函数功能：教师注册
        :param auth_data:记录用户登陆状态
        :return:
        """
        flag = "4"
        name = input("请输入用户名>>>").strip()
        db_handle = Db.db_handle()
        sql = "SELECT * FROM teachers WHERE name = %s" % name
        res = db_handle(sql)
        if not res:
            password = input("请输入密码>>>")
            age = 0
            while True:
                age = input("请输入年龄>>>")
                if age.isdigit():
                    break
                else:
                    print("请输入数字")
            addr = input("请输入居住地>>>")
            skills = []
            while True:
                skill = input("请输入您所掌握的技能，输入b退出>>>").strip()
                if skill == "b":
                    break
                skills.append(skill)
            tea_obj = Teacher(name, age, addr, password, skills)
            sql = "UPDATE teachers SET data = update_obj WHERE teacher.name = %s" % name

            db_handle = Db.db_handle()
            db_handle(sql, tea_obj)

            # 存储用户登陆状态
            auth_data[name] = []
            auth_data[name].insert(settings.User_obj, tea_obj)
            auth_data[name].insert(settings.Is_Authenticated, True)
            flag = "3"
        return flag

    @staticmethod
    def tea_login(auth_data, ACCESS_LOG):
        """
        函数功能：教师登陆
        :param auth_data:记录用户登陆状态
        :return:无
        """
        flag = "2"
        name = input("请输入用户名>>>")
        password = input("请输入密码>>>")
        db_handle = Db.db_handle()
        sql = "SELECT * FROM teachers WHERE name = %s" % name
        tea_obj = db_handle(sql)
        if password == tea_obj.password:
            flag = "1"
            # 存储用户登陆状态
            auth_data[name] = []
            auth_data[name].insert(settings.User_obj, tea_obj)
            auth_data[name].insert(settings.Is_Authenticated, True)
        else:
            flag = "2"
        return flag

    @staticmethod
    @UserAuth.is_login
    def view_self_classes(auth_data, name, ACCESS_LOG):
        """
        函数功能：查看教师所教授班级
        :param auth_data:记录用户登陆状态
        :return:无
        """
        tea_obj = auth_data[name][settings.User_obj]
        msg = tea_obj.view_classes_info(ACCESS_LOG)

        ACCESS_LOG.info("%s查询所所授课班级成功\n查询到的信息是：\n" % name)
        ACCESS_LOG.info(msg)

    @staticmethod
    @UserAuth.is_login
    def view_self_students(auth_data, name, ACCESS_LOG):
        """
        函数功能：查看教师所教授学生
        :param auth_data:记录用户登陆状态
        :return:无
        """
        tea_obj = auth_data[name][settings.User_obj]
        msg = tea_obj.view_students_info(ACCESS_LOG)

        ACCESS_LOG.info("%s查询所所授课学生成功\n查询到的信息是：\n" % name)
        ACCESS_LOG.info(msg)

    @staticmethod
    @UserAuth.is_login
    def grade_student(auth_data, name, ACCESS_LOG):
        """
        函数功能：为学生打分，未实现
        :param auth_data:记录用户登陆状态
        :return:无
        """
        ACCESS_LOG.info("为学生打分功能开发中，敬请期待")