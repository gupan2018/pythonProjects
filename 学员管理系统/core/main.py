# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core import Student

class Entry(object):
    __Usage = '''
    教师：teacher
    学生：student
    帮助文档：help
    '''
    def teacher(self):
        op_msg = {
            "1": "create_class",
            "2": "add_student",
            "3": "create_class_record",
            "4": "grade",
        }
        tea_usage = """
        1：创建班级
        2：为班级添加学员
        3：添加上课记录
        4：为学员打分
        """

    def student(self):
        op_msg = {
            "1": "submit_homework",
            "2": "achievements",
            "3": "check_rank"
        }
        stu_usage = """
                1：提交作业
                2：查看作业成绩
                3：查看排名
                """

    def help(self):
        print(self.__Usage)


def run():
    entry = Entry()
    while True:
        role = input("请输入您的角色：teacher/student\n>>>")
        if hasattr(entry, role):
            option = getattr(entry, role)
            option()
        if role == "b":
            break
        else:
            entry.help()