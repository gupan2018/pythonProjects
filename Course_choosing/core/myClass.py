# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import time
class MyClass(object):
    """
        name：课程名称
        ref_skill：课程需要掌握的技能

        setup_time：开班时间
        start_time：开课时间
        period：上课周期（天）
        stu_num：学生人数
        teachers：教师对象列表
        tea_num：教师数量
        addr：授课地点

        is_same_class(self, class_obj)：判断class_obj是否和自身是同一门课程

        required_skill(self)：查询所需要技能
        view_teachers(self)：查询任课教师
        view_students(self)：查询报班学生
        get_tea_num(self)：查询授课教师人数

        get_stu_num(self)：查询报班学生人数
        get_tea_num(self)：查询班级授课教师人数

        del_teacher(self, tea_obj)：解除教师任课资格
        add_student(self, stu_obj)： 为班级添加学生
        """
    def __init__(self, name, ref_skill, addr, teachers):
        super(MyClass, self).__init__()
        self.name = name
        self.ref_skill = ref_skill
        self.addr = addr
        self.teachers = teachers
        self.tea_num = len(teachers)
        str_format = "%Y-%m-%d %X"
        self.setup_time = time.strftime(str_format)
        self.period = 90
        self.start_time = self.setup_time

        self.students = []
        self.stu_num = 0
        self.status = False

    def is_same_class(self, class_obj, ACCESS_LOG):
        """
        函数功能：判断class_obj是否和自身是同一门课程
        :param class_obj:
        :return:
        """
        if self.name == class_obj.name and \
                        self.ref_skill == class_obj.ref_skill:
            return True
        return False

    def required_skill(self, ACCESS_LOG):
        """
        函数功能：查询所需要技能
        :return:
        """
        return self.ref_skill

    def view_teachers(self, ACCESS_LOG):
        """
        函数功能：查询任课教师
        :return:
        """
        msg = "——————————授课教师有——————————————\n"
        for teacher in self.teachers:
            msg += "%s\n"%teacher.name
        return msg

    def view_students(self, ACCESS_LOG):
        """
        函数功能：查询报班学生
        :return:
        """
        msg = None
        if not self.students:
            msg = "该班级还未招收学生"
        else:
            for student in self.students:
                msg += "%s\n"%student.name
        return msg

    def get_stu_num(self, ACCESS_LOG):
        """
        函数功能：查询报班学生人数
        :return:
        """
        return self.stu_num

    def get_tea_num(self, ACCESS_LOG):
        """
        函数功能：查询授课教师人数
        :return:
        """
        return self.tea_num

    def del_teacher(self, tea_obj, ACCESS_LOG):
        """
        函数功能 ： 解除教师任课资格
        :param tea_obj:  教师对象
        :return: 无
        """
        for teacher in self.teachers:
            if tea_obj is teacher:
                self.teachers.remove(tea_obj)
                self.tea_num -= 1
                break

    def add_student(self, stu_obj, ACCESS_LOG):
        """
        函数功能 ： 为班级添加学生
        :param stu_obj:  要添加的学生对象
        :return: 无
        """
        self.stu_num += 1
        self.students.append(stu_obj)
