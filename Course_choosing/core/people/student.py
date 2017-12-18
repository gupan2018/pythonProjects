# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from core.people.school_member import School_member

class Student(School_member):
    """
    classes：学生所报班级列表
    courses：学生所报课程列表
    schools：学生所报名的课程
    status：是否报名
    password:登录密码

    is_same_student(self, stu_obj)：判断stu_obj是否和自身是同一个学生对象

    memory(self, school_obj, course_obj, class_obj)：学生记忆报名信息（学校、课程、班级）
    view_schools(self)：展示报名学校信息
    view_classes(self)：查询班级信息

    view_one_class(self, class_obj)：查询一个班的基本信息
    view_one_class_classmates(self, class_obj)：查询一个班的同学
    """
    def __init__(self, name, age, addr, password):
        super(Student, self).__init__(name, age, addr)
        self.classes = []
        self.courses = []
        self.schools = []
        self.score = 0
        self.status = False
        self.password = password

    def is_same_student(self, stu_obj, ACCESS_LOG):
        """
        函数功能：判断stu_obj是否和自身是同一个学生对象
        :param stu_obj:
        :return:
        """
        if self.name == stu_obj.name and \
                        self.age == stu_obj.age and \
                        self.addr == stu_obj.addr:
            return True
        return False

    def memory(self, school_obj, course_obj, class_obj, ACCESS_LOG):
        """
        函数功能：学生记忆报名信息
        :param school_obj:  报名学校对象
        :param course_obj:  报名课程对象
        :param class_obj:  上课班级对象
        :return: 无
        """
        if school_obj not in self.schools:
            self.schools.append(school_obj)
        if course_obj not in self.courses:
            self.courses.append(course_obj)
        if class_obj not in self.classes:
            self.classes.append(class_obj)

    def view_schools(self, ACCESS_LOG):
        """
        函数功能：展示报名学校信息
        :return:
        """
        msg = None
        if not self.status:
            msg = "学生：{stu_name}没有报名任何学校".format(stu_name=self.name)
        else:
            msg = "——————————————该生报名的学校有————————————\n"
            for school in self.schools:
                msg += school.name
        return msg

    def view_classes(self, ACCESS_LOG):
        """
        查询班级信息
        :return:
            /**
            * 1： 查询失败：该生未报名课程
            * 2： 查询成功：该生报名课程信息如下：内容
            **/
        """
        classes_msg = None

        flag = None
        if not self.classes:
            flag = "1"
        else:
            for class_obj in self.classes:
                classes_msg += self.view_one_class(class_obj, ACCESS_LOG)
            flag = "2"

        menu = {
            "1": "查询失败：该生未报名课程",
            "2": "查询成功：该生报名课程信息如下\n{msg}：\n".format(
                msg = classes_msg
            )
        }
        return menu[flag]

    def view_one_class(self, class_obj, ACCESS_LOG):
        """
        函数功能：查询一个班的基本信息
        :param class_obj: 需要查询的班级对
        :return: 返回查询结果msg
        """
        class_msg = None
        name_info = "班级名称："
        tea_num = "授课老师人数："
        stu_num = "学生人数："
        classmates_info = "同学信息："

        classmates = None
        classmates = self.view_one_class_classmates(class_obj, ACCESS_LOG)

        if not classmates:
            classmates = "无\n"

        msg = "{h_class_name}{class_name}\n" \
              "     {h_tea_num}{tea_num}\n" \
              "     {h_stu_num}{stu_num}\n" \
              "     {h_classmates}{classmates_info}\n".format(
            h_class_name = name_info,
            class_name = class_obj.name,
            h_tea_num = tea_num,
            tea_num = class_obj.tea_num,
            h_stu_num = class_obj.stu_name,
            stu_num = class_obj.stu_name,
            h_classmates = classmates_info,
            classmates_info = classmates
        )
        return msg

    def view_one_class_classmates(self, class_obj, ACCESS_LOG):
        """
        函数功能：查询一个班的同学
        :param class_obj:
        :return: 返回查询结果
        """
        classmates = None
        for classmate in class_obj.students:
            if self is classmate:
                continue
            classmate_name = "同学姓名：{name}\n".format(name = classmate.name)
            classmates += classmate_name
        return classmates
