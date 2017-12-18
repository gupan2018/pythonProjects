# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.people.student import Student
from conf import settings
from core.options.userAuth import UserAuth
from core.common.db_handler import Db

class StuOption(object):
    """
    stu_option(auth_data, ACCESS_LOG)：根据用户输入，调用报名、浏览所报名班级等接口
    stu_register(auth_data, ACCESS_LOG)：学生注册
    stu_login(auth_data, ACCESS_LOG)：学生登陆
    view_classes(auth_data, name, ACCESS_LOG):浏览班级同学
    apply(auth_data, name, ACCESS_LOG)：学生报名
    """
    def __init__(self):
        super(StuOption, self).__init__()

    @staticmethod
    def stu_option(auth_data, ACCESS_LOG):
        """
        函数功能：根据用户输入，调用报名、浏览所报名班级等接口
        :param auth_data:用以存储用户登陆状态数据
        :return:操作成功返回3
        """
        msg = '''
            -----------------------------请选择您的操作-------------------------
            1：浏览所报名班级
            2：报名
            b：返回上一层
            -----------------------------------end------------------------------
            '''
        print(msg)

        menu = {
            "1": StuOption.view_classes,
            "2": StuOption.apply
        }

        name = input("请输入您的账户名>>>").strip()

        while True:
            choice = input("请输入您要进行的操作>>>").strip()
            if choice in menu.keys():
                menu[choice](auth_data = auth_data, name = name, ACCESS_LOG = ACCESS_LOG)
                return "3"
            print("输入有误，请重新输入")

    @staticmethod
    def stu_register(auth_data, ACCESS_LOG):
        """
        函数功能：学生注册
        :return:
        """
        flag = "4"
        name = input("请输入用户名>>>")

        db_handle = Db.db_handle()
        sql = "SELECT name FROM students WHERE name = %s" % name
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
            addr = input("请输入居住地")
            stu_obj = Student(name, age, addr, password)
            db_handle = Db.db_handle()
            sql = "UPDATE customers SET data = update_obj WHERE name = %s"%stu_obj.name
            db_handle(sql, stu_obj)

            # 存储用户登陆状态
            auth_data[name] = []
            auth_data[name].insert(settings.User_obj, stu_obj)
            auth_data[name].insert(settings.Is_Authenticated, True)
            flag = "3"
        return flag

    @staticmethod
    def stu_login(auth_data, ACCESS_LOG):
        """
        函数功能：学生登陆
        :return:
            /**
            * 1 登陆成功
            * 2 登陆失败
            **/
        """
        flag = "2"
        name = input("请输入用户名>>>")
        password = input("请输入密码>>>")
        db_handle = Db.db_handle()
        sql = "SELECT * FROM customers WHERE student.name = %s"%name
        stu_obj = db_handle(sql)
        if password == stu_obj.password:
            flag = "1"
            # 存储用户登陆状态
            auth_data[name] = []
            auth_data[name].insert(settings.User_obj, stu_obj)
            auth_data[name].insert(settings.Is_Authenticated, True)
        else:
            flag = "2"
        return flag

    @staticmethod
    @UserAuth.is_login
    def view_classes(auth_data, name, ACCESS_LOG):
        """
        函数功能：浏览班级同学
        :return:
        """
        stu_obj = auth_data[name][settings.User_obj]
        msg = stu_obj.view_classes(ACCESS_LOG)

        ACCESS_LOG.info("%s查询所报班级信息成功\n查询到的信息是：\n"%name)
        ACCESS_LOG.info(msg)

    @staticmethod
    @UserAuth.is_login
    def apply(auth_data, name, ACCESS_LOG):
        """
        函数功能：学生报名学习
        :return:无
        """
        stu_obj = auth_data[name][settings.User_obj]

        sql = "SELECT * FROM schools"
        db_handle = Db.db_handle()
        schools = db_handle(sql)

        school_msg = ""

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
        '''.format(msg=school_msg)

        print(msg)

        addr = None
        while True:
            choice = input("请输入需要想要了解的学校>>>").strip()
            if choice in settings.courses.keys():
                addr = choice
                break
            print("输入有误，请重新输入")

        sql = "SELECT * FROM schools WHERE school.name = {addr}".format(addr=addr)
        db_handle = Db.db_handle()
        # 返回学校对象
        sch_obj = db_handle(sql)

        msg =sch_obj.get_opened_course(ACCESS_LOG)
        print(msg)

        course_name = None
        while True:
            course_name = input("请输入您想要报名的课程>>>").strip()
            if course_name in msg:
                break
            print("输入有误，请重新输入")

        sql = "SELECT * FROM courses WHERE course.name = {course_name}".format(course_name=course_name)
        # 返回学校对象
        course_obj = db_handle(sql)

        menu = {
            "1": "课程：{course_name}还未分班，不能招生".format(
                course_name=course_obj.name),
            "2": "学生{name}已经报名课程{course_name},无需重复报名".format(
                name=stu_obj.name,
                course_name=course_obj.name),
            "3": "课程{course_name}人数已满，不能报名，请增加该课程班级".format(
                course_name=course_obj.name),
            "4": "学生{name}报名课程{course_name}成功,但是该课程人数已满"
                 "，若想要继续招生，请增加班级数".format(
                name=stu_obj.name,
                course_name=course_obj.name),
            "5": "学生{name}报名课程{course_name}成功".format(
                name=stu_obj.name,
                course_name=course_obj.name),
            "6": "未知错误"
        }

        res_code = sch_obj.recruit(stu_obj, course_obj, ACCESS_LOG)

        ACCESS_LOG.info(menu[res_code])
        if res_code in ["4", "5"]:
            sch_obj = sch_obj
            stu_obj = stu_obj
            course_obj = course_obj
            tea_objs = course_obj.teachers
            class_objs = course_obj.classes

            sql = "UPDATE schools SET data = update_obj WHERE school.name = %s"%sch_obj.addr
            db_handle(sql, sch_obj)

            sql = "UPDATE customers SET data = stu_obj WHERE student.name = %s"%stu_obj.addr
            db_handle(sql, stu_obj)

            sql = "UPDATE courses SET data = course_obj WHERE student.name = %s"%course_obj.name
            db_handle(sql, course_obj)

            for tea_obj in tea_objs:
                sql = "UPDATE teachers SET data = tea_obj WHERE tea.name = %s"%tea_obj.name
                db_handle(sql, tea_obj)

            for class_obj in class_objs:
                sql = "UPDATE classes SET data = class_obj WHERE class.name = %s"%class_obj.name
                db_handle(sql, class_obj)