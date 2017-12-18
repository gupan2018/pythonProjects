# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from core.people.school_member import School_member

class Teacher(School_member):
    """
    classes：教师授课班级
    courses：教师授课课程
    employer：任聘公司名称
    students：教师所带学生
    skills：教师精通技能

    add_employer(self, sch_obj)：入职学校
    is_same_teacher(self, tea_obj)：判断tea_obj是否自身是同一个老师

    add_course(self, course_obj)：为教师添加任课课程
    add_classes(self, class_objs)：为教师添加任课班级
    view_students_info(self)：浏览该教师所带学生信息
    view_classes_info(self)：查看该教师所授课班级信息
    show_employers_info(self)：查看该教师雇主信息
    """
    def __init__(self, name, age, addr, password, skills):
        super(Teacher, self).__init__(name, age, addr)
        self.skills = skills
        self.password = password
        self.classes = []
        self.courses = []
        self.employers = []
        self.students = []

    def add_employer(self, sch_obj):
        """
        函数功能：入职学校
        :param sch_obj: 待入职学校
        :return: 无
        """
        self.employers.append(sch_obj)

    def is_same_teacher(self, tea_obj, ACCESS_LOG):
        """
        函数功能：判断tea_obj是否自身是同一个老师
        :param tea_obj:
        :return:
        """
        if self.name == tea_obj.name and \
                        self.age == tea_obj.age and \
                        self.addr == tea_obj.addr and \
                        self.skills == tea_obj.skills:
            return True
        return False

    def add_course(self, course_obj, ACCESS_LOG):
        """
        函数功能：为教师添加任课课程
        :param course_obj:
        :return: 无
        """
        self.courses.append(course_obj)
        self.add_classes(course_obj.classes, ACCESS_LOG)
        self.add_students(course_obj.students, ACCESS_LOG)

    def add_classes(self, class_objs, ACCESS_LOG):
        """
        函数功能：为教师添加任课班级
        :param class_objs:
        :return:
        """
        if not class_objs:
            self.classes.extend(class_objs)

    def add_students(self, students, ACCESS_LOG):
        """
        函数功能：为教师添加学生人数
        :param students:
        :return:
        """
        if not self.students:
            self.students.extend(students)

    def view_students_info(self, ACCESS_LOG):
        """
        函数功能：浏览该教师所带学生信息
        :return: 查询信息
        """
        msg = "------------------%s所教授的学生如下：-------------------\n"%self.name
        for student in self.students:
            msg += "%s\n"%student.name
        return msg

    def view_classes_info(self, ACCESS_LOG):
        """
        函数功能：查看该教师所授课班级信息
        :return: 查询信息
        """
        msg = "------------------%s所教授的班级如下：-------------------\n"%self.name
        for class_obj in self.classes:
            msg += "%s\n"%class_obj.name
        return msg

    def show_employers_info(self, ACCESS_LOG):
        """
        函数功能：查看该教师雇主信息
        :return: 查询信息
        """
        msg = None
        if not self.employers:
            msg = "%s还未被聘用"%self.name
        else:
            for employer in self.employers:
                msg += "雇主：{employer_name}分校".format(
                    employer_name = employer.addr)
        return msg

    def show_self_skills(self, ACCESS_LOG):
        """
        函数功能：查看该教师所掌握技能
        :return: 查询信息
        """
        msg = None
        if not self.skills:
            msg = "这可能是个假教师"
        else:
            for skill in self.skills:
                msg = "%s\n"%skill
        return msg