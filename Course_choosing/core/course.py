# -*- coding:utf-8 -*-
# __author__ = 'gupan'

class Course(object):
    def __init__(self, name, ref_skill):
        """
        name：课程名称
        ref_skill：教授课程需要技能
        classes：开设班级对象列表
        teachers：授课老师对象列表
        students：班级学生对象列表
        class_max_num：班级最多人数
        stu_num：课程人数
        class_num：开设班级数量
        addr：授课地点
        tea_num：教师数量

        is_same_course(self, course_obj):判断course_obj是否和自身是同一个对象

        required_skill(self):查询教授课程需要技能
        view_classes(self)：查询课程分班信息
        view_teachers(self)：查询课程的授课老师
        view_students(self)：查询报名该课程的学生

        add_teacher(self, tea_obj)：增加该课程任课教师
        teachers(self, tea_objs)：增加多名该课程任课教师
        del_teacher(self, tea_obj)： 将该教师移除出授课团队
        is_student_in_course： 判断学生是否报名该课程
        add_student(self, stu_obj) ： 添加学生进课程
        add_class(self, class_obj)：为课程新开设班级
        """
        super(Course, self).__init__()
        self.name = name
        self.ref_skill = ref_skill
        self.classes = []
        self.teachers = []
        self.students = []
        self.class_max_num = 30
        self.stu_num = 0
        self.class_num = 0
        self.addr = None
        self.tea_num = 0

    def is_same_course(self, course_obj, ACCESS_LOG):
        """
        函数功能：判断course_obj是否和自身是同一个对象
        :param course_obj:
        :return:
        """
        if self.name == course_obj.name and \
                        self.ref_skill == course_obj.ref_skill:
            return True
        return False

    def required_skill(self, ACCESS_LOG):
        """
        函数功能：查询教授课程需要技能
        :return:
        """
        return self.ref_skill

    def view_classes(self, ACCESS_LOG):
        """
        函数功能：查询课程分班信息
        :return:
        """
        msg = None
        if not self.classes:
            msg = "该课程还未分班"
        else:
            msg = "————————————课程：%s的班级为——————————\n"%self.name
            for class_obj in self.classes:
                msg += "%s\n"%class_obj.name
        return msg

    def view_teachers(self, ACCESS_LOG):
        """
        函数功能：查询课程的授课老师
        :return:
        """
        msg = None
        if not self.teachers:
            msg = "该课程没有授课老师"
        else:
            msg = "————————————课程：%s的授课老师为——————————\n" % self.name
            for teacher in self.classes:
                msg += "%s\n" % teacher.name
        return msg

    def view_students(self, ACCESS_LOG):
        """
        函数功能：查询报名该课程的学生
        :return:
        """
        msg = None
        if not self.students:
            msg = "该课程没有学生学习"
        else:
            msg = "————————————报名课程：%s的学生为——————————\n" % self.name
            for student in self.students:
                msg += "%s\n" % student.name
        return msg

    def add_teacher(self, tea_obj, ACCESS_LOG):
        """
        函数功能：添加教师至任课团队
        :param tea_obj: 欲添加教师对象
        :return: 无
        """
        self.teachers.append(tea_obj)
        self.tea_num += 1

    def add_teachers(self, tea_objs, ACCESS_LOG):
        """
        函数功能：添加多名教师至任课团队
        :param tea_objs: 欲添加教师对象列表
        :return: 无
        """
        self.teachers.extend(tea_objs)
        num = len(tea_objs)
        self.tea_num += num

    def del_teacher(self, tea_obj, ACCESS_LOG):
        """
        函数功能：解除教师任课资格
        :param tea_obj: 需要解除教师任聘资格教师对象
        :return: 无
        """
        for teacher in self.teachers:
            if tea_obj is teacher:
                self.teachers.remove(tea_obj)
                self.tea_num -= 1
                break

    def is_student_in_course(self, stu_obj, ACCESS_LOG):
        """
        函数功能：判断学生是否报名该课程
        :param stu_obj: 欲报名学生对象
        :return:
            /**
            * True ： 该生已报名该课程
            * False ： 该生未报名该课程
            **/
        """
        if stu_obj in self.students:
            return True
        return False

    def add_student(self, stu_obj, ACCESS_LOG):
        """
        函数功能 ： 添加学生进课程
        :param stu_obj:
        :return:
        """
        self.stu_num += 1
        self.students.append(stu_obj)

    def add_class(self, class_obj, ACCESS_LOG):
        """
        函数功能：为课程新开设班级
        :param class_obj:
        :return:
        """
        self.classes.append(class_obj)
        self.class_num += 1