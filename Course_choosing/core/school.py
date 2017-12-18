# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from core.myClass import MyClass

class School(object):
    """
    学校类：
        用于创建一个学校对象

    addr：学校地址
    __tea_num：教师数量
    __stu_num：学生数量
    __staffs：聘用教师对象列表
    __customs：招收学生对象列表
    courses：开设课程列表
    classes：课程分班列表

    get_real_student(self, stu_obj)：返回存储在school中与stu_obj信息相同的学生对象，便于数据恢复
    get_real_teacher(self, tea_obj)：返回存储在school中与tea_obj信息相同的教师对象，便于数据恢复
    get_real_class(self, class_obj)：返回存储在school中与class_obj信息相同的班级对象，便于数据恢复
    get_real_course(self, course_obj)：返回存储在school中与course_obj信息相同的课程对象，便于数据恢复

    hire(self, tea_obj)：招聘教师
    dismiss(self, tea_obj)：未实现的接口方法
    recruit(self, stu_obj, course_obj):招收学生
    exclude(self, stu_obj)：开除学生
    develop_one_course(self, course_obj)：开设课程
    develop_one_class(self, course_name)：开设班级
    get_tea_num(self)：获取学校教师数量
    get_stu_num(self)：获取学校学生数量
    get_course_info(self, course_obj)：获取各个课程信息

    __del_teacher(tea_obj) 将教师移除出团队
    is_course_full(self, course_obj) ： 判断课程是否招满
    add_student2course(stu_obj, course_obj) ： 将学生加入课程
    add_student2class(self, class_obj, stu_obj) ： 将学生加入班级
    reg_stu2school(self, course_obj, class_obj, stu_obj) ： 学生报名后在学校注册
    get_opened_course(self)：返回用户已开设的课程名称
    """

    def __init__(self, addr):
        self.addr = addr
        self.__tea_num = 0
        self.__stu_num = 0
        self.__staffs = []
        self.__customs = []
        self.courses = []
        self.classes = []

    def get_real_student(self, stu_obj, ACCESS_LOG):
        """
        函数功能：返回存储在school中与stu_obj信息相同的学生对象，便于数据恢复
        :param stu_obj:
        :return:
        """
        for student in self.__customs:
            if stu_obj.is_same_student(student, ACCESS_LOG):
                return student
        return False

    def get_real_teacher(self, tea_obj, ACCESS_LOG):
        """
        函数功能：返回存储在school中与tea_obj信息相同的教师对象，便于数据恢复
        :param tea_obj:
        :return:
        """
        for teacher in self.__staffs:
            if tea_obj.is_same_teacher(teacher, ACCESS_LOG):
                return teacher
        return False

    def get_real_class(self, class_obj, ACCESS_LOG):
        """
        函数功能：返回存储在school中与class_obj信息相同的班级对象，便于数据恢复
        :param class_obj:
        :return:
        """
        for in_class_obj in self.classes:
            if in_class_obj.is_same_class(class_obj, ACCESS_LOG):
                return in_class_obj
        return False

    def get_real_course(self, course_obj, ACCESS_LOG):
        """
        函数功能：返回存储在school中与course_obj信息相同的课程对象，便于数据恢复
        :param course_obj:
        :return:
        """
        for course in self.courses:
            if course.is_same_course(course_obj, ACCESS_LOG):
                return course
        return False

    def hire(self, tea_obj, ACCESS_LOG):
        """
        函数功能：聘用教师

        :param tea_obj:教师对象
        :return:返回返回码
            /**
            *2：招聘失败：教师已被该校招聘，不能重复招聘
            *1：招聘成功：
            **/
        """
        menu = {
            "1": "招聘成功：{name}成为{sch_name}分校教师".format(
                name=tea_obj.name,
                sch_name=self.addr),
            "2": "招聘失败：教师：{name}已被{sch_name}分校招聘，不能重复招聘".format(
                sch_name=self.addr,
                name=tea_obj.name)
        }

        flag = None

        # 招聘失败：教师已被该学校招聘

        is_hired = False

        for teacher in self.__staffs:
            if teacher.name == tea_obj.name:
                is_hired = True

        # 招聘失败：教师已被该学校招聘
        if is_hired:
            flag = "2"
        # 招聘成功：添加教师至该学校，根据教师技能，将教师添加至对应授课团队
        else:
            # 判断教师是否掌握一开设的课程的授课资格，如果是，该教师加入授课团队
            for course in self.courses:
                if course.ref_skill in tea_obj.skills:
                    course.add_teacher(tea_obj, ACCESS_LOG)
                    tea_obj.add_course(course, ACCESS_LOG)
            # 聘用该教师
            self.__staffs.append(tea_obj)
            tea_obj.add_employer(self)
            self.__tea_num += 1
            flag = "1"

        msg = menu[flag]
        return flag

    def dismiss(self, tea_obj, ACCESS_LOG):
        """
        函数功能：解雇教师
        :param tea_obj:
        :return:返回返回码，根据返回码判断解雇信息
            /**
            *1：解雇成功
            *2：解雇失败：未被聘用
            **/
        """
        menu = {
            "1": "解雇成功：教师：{name}已被{sch_name}分校解雇".format(
                name=tea_obj.name,
                sch_name=self.addr),
            "2": "解雇失败：教师：{name}未被{sch_name}分校聘用，不能解雇".format(
                name=tea_obj.name,
                sch_name=self.addr)
        }

        flag = None
        # 解聘成功：如果该学校聘用了该教师
        if self.addr in tea_obj.employers:
            self.__del_teacher(tea_obj, ACCESS_LOG)
            flag = "1"
        # 解聘失败：学校没有聘用该教师
        else:
            flag = "2"
        msg = menu[flag]
        return flag

    def recruit(self, stu_obj, course_obj, ACCESS_LOG):
        """
        函数功能：招聘学生
        :param stu_obj:学生对象，打算报名的学生对象
        :param course_obj:学生想要报名的课程
        :return:返回返回码，根据返回码可以查看函数执行状态
            /**
            * 1：报名失败：该课程还未进行分班
            * 2：报名失败：该生已报名该课程，不能重复报名
            * 3：报名失败：该生所报名课程招生计划已满，需要学校再开班才能报名
            * 4：报名成功 ： 学生报名成功，但报名后课程人数已满，发出提示再进行分班
            * 5：报名成功
            * 6：未知错误
            **/
        """
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

        flag = None
        # 报名失败; 该课程还未分班，不能报名
        if not course_obj.classes:
            flag = "1"

        # 报名失败：该生已报名该课程，不能重复报名
        elif course_obj.is_student_in_course(stu_obj, ACCESS_LOG):
            flag = "2"

        # 报名失败：该生所报名课程招生计划已满，需要学校再开班才能报名
        elif self.is_course_full(course_obj, ACCESS_LOG):
            flag = "3"

        # 报名成功 ： 学生报名成功，但报名后课程人数已满，发出提示再进行分班
        elif course_obj.classes[-1].stu_num == course_obj.class_max_num - 1:
            one_class = self.add_student2course(course_obj, stu_obj, ACCESS_LOG)
            self.add_student2class(one_class, stu_obj, ACCESS_LOG)
            self.reg_stu2school(course_obj, one_class, stu_obj, ACCESS_LOG)

            flag = "4"

        # 报名成功
        elif course_obj.classes[-1].stu_num < course_obj.class_max_num - 1:
            one_class = self.add_student2course(course_obj, stu_obj, ACCESS_LOG)
            self.add_student2class(one_class, stu_obj, ACCESS_LOG)
            self.reg_stu2school(course_obj, one_class, stu_obj, ACCESS_LOG)
            flag = "5"

        # 未知错误
        else:
            flag = "6"

        return flag

    # 功能未实现
    def exclude_student(self, stu_obj, ACCESS_LOG):
        """
        函数功能：开除学生
        :param stu_obj:
        :return:
        """
        return "开除学生功能未实现"

    def develop_one_course(self, course_obj, ACCESS_LOG):
        """
        函数功能：新开设课程
        :param course_obj:需要开设的课程
        :return: 返回状态码，根据状态码判断可知函数执行状态
            /**
            * 1： 开设失败： 教师团队没有教师掌握技能{course_ref}，无法开设课程
            * 2： 开设成功
            * 3： 开设失败：课程已经开设，不必重复开设
            **/
        """
        menu = {
            "1": "{sch_name}分校教师团队没有教师掌握技能{course_ref}，无法开设课程：{course_name}".format(
                sch_name=self.addr,
                course_ref=course_obj.ref_skill,
                course_name=course_obj.name),
            "2": "{sch_name}分校开设课程{course_name}成功".format(
                sch_name=self.addr,
                course_name=course_obj.name),
            "3": "开设失败：课程{course_name}已经开设，不必重复开设".format(
                course_name=course_obj.name)
        }

        flag = None
        course_tea = self.get_course_ref_teacher(course_obj, ACCESS_LOG)

        # 开设失败：课程已经开设，不必重复开设
        if course_obj in self.courses:
            flag = "3"

        # 开设成功
        elif course_tea:
            course_obj.addr = self.addr
            for teacher in course_tea:
                teacher.add_course(course_obj, ACCESS_LOG)
            course_obj.add_teachers(course_tea, ACCESS_LOG)
            self.courses.append(course_obj)
            flag = "2"

        # 开设失败： 教师团队没有教师掌握技能{course_ref}，无法开设课程
        elif not course_tea:
            flag = "1"

        msg = menu[flag]

        return flag

    def develop_one_class(self, course_obj, ACCESS_LOG):
        """
        函数功能：开设新班级
        :param course_obj:
        :return:返回状态码，根据状态码可得到函数执行状态
        /**
        * 1： 开设新班级失败：分校没有开设该课程
        * 2： 开设新班级成功
        **/
        """
        flag = None
        class_id = None

        # 开设新班级失败：分校没有开设该课程
        if course_obj not in self.courses:
            flag = "1"

        # 开设新班级成功
        else:
            ref_skill = course_obj.ref_skill
            class_seq = len(course_obj.classes) + 1
            class_name = ref_skill + str(class_seq) + "班"
            class_addr = course_obj.addr
            teachers = course_obj.teachers
            new_class_obj = MyClass(class_name, ref_skill, class_addr, teachers)
            course_obj.add_class(new_class_obj, ACCESS_LOG)
            self.classes.append(new_class_obj)
            class_id = class_seq
            flag = "2"

        menu = {
            "1": "开设新班级失败：{addr}分校没有开设课程{course_name}".format(
                addr=self.addr,
                course_name=course_obj.name),
            "2": "开设新班级成功：现在班级数为{id}".format(id=class_id)
        }

        msg = menu[flag]
        return flag

    def get_tea_num(self):
        """
        函数功能：返回教师数量
        :return: 无
        """
        return self.__tea_num

    def get_stu_num(self):
        """
        函数功能：返回学生数量
        :return: 无
        """
        return self.__stu_num

    def get_course_info(self):
        """
        函数功能：获取课程信息
        :return:
        """
        info = ""
        for course in self.courses:
            str = ""
            course_name = course.name
            stu_num = course.stu_num
            couse_class_num = course.class_num
            teachers = ""
            for teacher in course.teachers:
                append_str = teacher.name + ", "
                teachers += append_str
            teachers.rstrip(", ")
            str = "课程名：" + course_name + "\n" + "报名课程人数：" + stu_num + "\n" + "开设班级数：" + couse_class_num + "\n" + "教师信息：" + teachers + "\n"
            info += str
        return info

    def __del_teacher(self, tea_obj, ACCESS_LOG):
        """
        函数功能：解雇教师子函数
        :param tea_obj: 待解雇教师对象
        :return: 无
        """
        self.__staffs.remove(tea_obj)
        self.__tea_num -= 1
        for course in self.courses:
            course.del_teacher(tea_obj, ACCESS_LOG)
        for one_class in self.classes:
            one_class.del_teacher(tea_obj, ACCESS_LOG)

    def is_course_full(self, course_obj, ACCESS_LOG):
        """
        函数功能：判断课程是否招满
        :param self:
        :param course_obj: 待判断课程
        :return:
            /**
            * True ： 已招满
            * False ： 未招满
            **/
        """
        return course_obj.classes[-1].stu_num >= course_obj.class_max_num

    def add_student2course(self, course_obj, stu_obj, ACCESS_LOG):
        """
        函数功能：学生加入课程
        :param stu_obj: 欲添加学生对象
        :param course_obj: 待添加课程对象
        :return:
        """
        one_class = None
        # 将学生添加进课程
        course_obj.add_student(stu_obj, ACCESS_LOG)

        # 将学生添加进班级
        for one_class in course_obj.classes:
            if not one_class.status:
                one_class.add_student(stu_obj, ACCESS_LOG)
                break

        # 学生报名课程
        return one_class

    def add_student2class(self, class_obj, stu_obj, ACCESS_LOG):
        """
        函数功能：将学生加入班级
        :param class_obj: 班级对象
        :param stu_obj: 学生对象
        :return: 无
        """
        class_obj.add_student(stu_obj, ACCESS_LOG)

    def reg_stu2school(self, course_obj, class_obj, stu_obj, ACCESS_LOG):
        """
        函数功能：学生报名后在学校注册
        :param course_obj: 学生所选课程对象
        :param class_obj: 学生所被分到班级对象
        :param stu_obj: 学生对象
        :return: 无
        """
        if not stu_obj.status:
            stu_obj.status = True
        if stu_obj not in self.__customs:
            self.__customs.append(stu_obj)
            self.__stu_num += 1

        # 学生记忆报名课程信息
        stu_obj.memory(self, course_obj, class_obj, ACCESS_LOG)

    def get_course_ref_teacher(self, course_obj, ACCESS_LOG):
        """
        函数功能：返回课程授课教师列表
        :param course_obj:
        :return:
        """
        course_tea = []
        for teacher in self.__staffs:
            if course_obj.ref_skill in teacher.skills:
                course_tea.append(teacher)
        return course_tea


    def get_opened_course(self, ACCESS_LOG):
        """
        函数功能：返回用户已开设的课程名称
        :return:
        """
        msg = ""
        for course in self.courses:
            msg += "课程名：%s\n"%course.name
            msg += "    班级数：%d\n"%course.class_num
        if not msg:
            msg = "无"
        return msg

    # def get_students(self):
    #     return self.__customs
    #
    # def get_staffs(self):
    #     return self.__staffs