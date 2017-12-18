# -*- coding:utf-8 -*-
# __author__ = 'gupan'

# from core.course import Course
# from core.myClass import MyClass
# from core.school import School
# from core.people.teacher import Teacher
# from core.people.student import Student

from core.client import Client
from core.common.logger import Logger
import os
# import pickle
# import time
PATH = os.path.dirname(os.path.abspath(__file__)) + "/teat_data"

# 记录用户操作logger
ACCESS_LOG = Logger("access")

# 记录用户登陆状态
'''
字典键值
key：用户姓名
value：列表格式数据
    0：用户对象
    1：用户登陆状态：
        False：未登录
        True：已登录
'''
auth_data = {
}

def run():
    """
    函数功能：程序执行入口，提供以下3个视图
        1. 学生视图
        2. 教师视图
        3. 管理视图
    :return:
    """
    choice_menu = {
        "1":Client.stu_entry,
        "2":Client.tea_entry,
        "3":Client.mana_entry
    }

    menu = '''
    -----------------------------输入选项---------------------------
    学生入口：1
    教师入口：2
    管理入口：3
    退出：4
    -------------------------------end-----------------------------
    '''
    while(True):
        print(menu)
        choice = input("请选择身份\033[31;1m>>>\033[0m").strip()
        if choice in choice_menu.keys():
            choice_menu[choice](auth_data, ACCESS_LOG)
        elif choice == "4":
            break
        else:
            print("输入有误，请重新输入")
    print("bye".center(100, "-"))






    # t1 = Teacher("gupan", 12, "北京", "python")
    # course = Course("python班", "python")
    # student = Student("s1", 12, "北京")
    # school = School("北京")
    # school.hire(t1)
    # school.develop_one_course(course)
    # school.develop_one_class(course)
    # school.recruit(student, course)
    #
    # t1 = pickle.dumps(t1)
    # course = pickle.dumps(course)
    # student = pickle.dumps(student)
    # school = pickle.dumps(school)

    # t1_path = PATH + "/t1.pickle"
    # course_path = PATH + "/course.pickle"
    # student_path = PATH + "/student.pickle"
    # school_path = PATH + "/school.pickle"
    #
    #
    # with open(t1_path, "rb") as t1_file, \
    #         open(course_path, "rb") as course_file, \
    #         open(student_path, "rb") as student_file, \
    #         open(school_path, "rb") as school_file:
    #     t1 = t1_file.read()
    #     course = course_file.read()
    #     student = student_file.read()
    #     school = school_file.read()
    #
    # t1 = pickle.loads(t1)
    # course = pickle.loads(course)
    # student = pickle.loads(student)
    # school = pickle.loads(school)
    #
    # course = school.get_real_course(course)
    # t1 = school.get_real_teacher(t1)
    # student = school.get_real_student(student)
    #
    # if student is course.students[-1]:
    #     print("是同一个对象")
    # else:
    #     print("不是同一个对象")
    #
    # student.addr = "上海"
    # print(student.addr)
    # time.sleep(10)