# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.course import Course
from core.school import School
from conf import settings
from core.common.db_handler import Db

class Manage(object):
    """
    类功能：管理类，提供申请学校、添加课程、开设班级、任聘教师等操作接口
    create_school(ACCESS_LOG)：创建学校
    manage_school(ACCESS_LOG)：管理学校，根据输入调用招聘教师、开设课程、开设新班级等接口
    hire(sch_obj, ACCESS_LOG)：招聘教师
    develop_course(sch_obj, ACCESS_LOG)：开设课程
    develop_class(sch_obj, ACCESS_LOG)：新开设班级
    """
    def __init__(self):
        super(Manage, self).__init__()

    @staticmethod
    def create_school(ACCESS_LOG):
        """
        函数功能：创建学校
        :param ACCESS_LOG: 操作日志logger
        :return: 无
        """
        db_handle = Db.db_handle()
        addr = input("请输入办学地点>>>").strip()
        while not addr and addr not in settings.courses.keys():
            addr = input("请输入办学地点>>>").strip()
        school = School(addr)
        # sql写法有问题
        sql = "UPDATE schools SET data = update_obj WHERE school.name = %s"%addr
        msg = db_handle(sql, school)
        if not msg:
            ACCESS_LOG.info("创建学校%s失败" % addr)
        else:
            ACCESS_LOG.info("创建学校%s成功" % addr)

    @staticmethod
    def manage_school(ACCESS_LOG):
        """
        函数功能：管理学校，根据输入调用招聘教师、开设课程、开设新班级等接口
        :param ACCESS_LOG: 操作日志logger
        :return: 无
        """

        sql = "SELECT * FROM schools"
        db_handle = Db.db_handle()
        schools = db_handle(sql)
        # print(schools)
        opened_school = ""
        for school in schools:
            opened_school += "%s\n"%school

        if not opened_school:
            print("当前还未开设任何学校，该窗口拒绝操作")
            return

        print('''
        ---------------------------当前已开设的学校有---------------------------
        %s
        --------------------------------end------------------------------------
        '''%opened_school)

        addr = None

        while True:
            choice = input("请输入需要进行操作的学校>>>").strip()
            if choice in schools:
                addr = choice
                break
            print("输入有误，请重新输入")

        db_handle = Db.db_handle()
        sql = "SELECT * FROM schools WHERE school.name = {addr}".format(addr=addr)
        # 返回学校对象
        sch_obj = db_handle(sql)

        menu = {
            "1": "招聘教师",
            "2": "开设课程",
            "3": "开设新班级",
            "b": "退出"
        }

        op_manage = {
            "1": Manage.hire,
            "2": Manage.develop_course,
            "3": Manage.develop_class
        }

        print('''
            ---------------------------您可以进行的操作为---------------------------
            "1": "招聘教师",
            "2": "开设课程",
            "3": "开设新班级",
            "b": "退出"
            --------------------------------end------------------------------------
        ''')

        while True:
            choice = input("请输入您的选择\033[31;1m>>>\033[0m").strip()
            if not choice:
                print("输入不能为空")
                continue
            if choice in op_manage.keys():
                op_manage[choice](sch_obj, ACCESS_LOG)

            if choice == "b":
                print("bye".center(50, "-"))
                break
            print("输入有误，请重新输入")

    @staticmethod
    def hire(sch_obj, ACCESS_LOG):
        """
        函数功能：招聘教师
        :param sch_obj:
        :param ACCESS_LOG:
        :return:
        """
        sql = "SELECT * FROM teachers"

        db_handle = Db.db_handle()

        tea_names = db_handle(sql)
        tea_objs = []
        msg = ""
        for tea_name in tea_names:
            db_handle = Db.db_handle()
            sql = "SELECT * FROM teachers WHERE teacher.name = %s"%tea_name
            tea_obj = db_handle(sql)

            is_hired = False

            # 判断该学生是否被目标学校所雇佣
            for school in tea_obj.employers:
                if school.addr == sch_obj.addr:
                    is_hired = True

            # 若没有被雇佣，则列出该教师信息
            if not is_hired:
                # 列出可以被雇佣的职工的姓名
                tea_objs.append(tea_obj)
                msg += "姓名：%s\n" % tea_obj.name

        if not tea_objs:
            msg = "无"
            print("无可雇佣职工")
            return
        # 列出可以被雇佣的职工的姓名
        print(msg)

        while True:
            flag = False
            # 选择要雇佣的职工
            choice = input("请输入意向职工>>>").strip()
            for teacher in tea_objs:
                print("choice", choice)
                print("teacher.anme", teacher.name)
                if choice == teacher.name:
                    db_handle = Db.db_handle()
                    res_code = sch_obj.hire(teacher, ACCESS_LOG)

                    menu = {
                        "1": "招聘成功：{name}成为{sch_name}分校教师".format(
                            name=tea_obj.name,
                            sch_name=sch_obj.addr),
                        "2": "招聘失败：教师：{name}已被{sch_name}分校招聘，不能重复招聘".format(
                            sch_name=sch_obj.addr,
                            name=tea_obj.name)
                    }

                    sql = "UPDATE teachers SET data = tea_obj WHERE tea.name = %s" % teacher.name
                    db_handle(sql, teacher)

                    course_objs = teacher.courses
                    stu_objs = teacher.students
                    class_objs = []
                    teachers = []

                    if course_objs:
                        class_objs = course_objs[0].classes
                        teachers = course_objs[0].teachers

                    sql = "UPDATE schools SET data = update_obj WHERE school.name = %s" % sch_obj.addr
                    db_handle(sql, sch_obj)

                    for course_obj in course_objs:
                        sql = "UPDATE courses SET data = course_obj WHERE student.name = %s" % course_obj.name
                        db_handle(sql, course_obj)

                    for stu_obj in stu_objs:
                        sql = "UPDATE customers SET data = stu_obj WHERE student.name = %s" % stu_obj.addr
                        db_handle(sql, stu_obj)

                    for class_obj in class_objs:
                        sql = "UPDATE classes SET data = class_obj WHERE class.name = %s"%class_obj.name
                        db_handle(sql, class_obj)

                    for teacher in teachers:
                        sql = "UPDATE teachers SET data = tea_obj WHERE tea.name = %s"%teacher.name
                        db_handle(sql, teacher)

                    ACCESS_LOG.info(menu[res_code])

                    flag = True
                    break
            if flag:
                break

    @staticmethod
    def develop_course(sch_obj, ACCESS_LOG):
        """
        函数功能：开设课程
        :param sch_obj:
        :param ACCESS_LOG:
        :return:
        """
        may_course = settings.courses[sch_obj.addr]
        courses = ""
        for course in may_course:
            courses += "%s, " % course
        courses = courses.rstrip(", ")
        msg = '''
        -------------------------您可以开设的课程为----------------------------
        %s
        ''' % courses
        # 打印可以开设的课程
        print(msg)

        msg = '''
        -------------------------您已经开设的课程为----------------------------
        %s
        ''' % sch_obj.get_opened_course(ACCESS_LOG)
        print(msg)

        while True:
            choice = input("请输入您想要开设的课程>>>")
            if choice in may_course:
                new_course = Course(choice, choice)
                msg = sch_obj.develop_one_course(new_course, ACCESS_LOG)

                menu = {
                    "1": "{sch_name}分校教师团队没有教师掌握技能{course_ref}，无法开设课程：{course_name}".format(
                        sch_name=sch_obj.addr,
                        course_ref=new_course.ref_skill,
                        course_name=new_course.name),
                    "2": "{sch_name}分校开设课程{course_name}成功".format(
                        sch_name=sch_obj.addr,
                        course_name=new_course.name),
                    "3": "开设失败：课程{course_name}已经开设，不必重复开设".format(
                        course_name=new_course.name)
                }
                ACCESS_LOG.info(menu[msg])
                if msg != "2":
                    break

                db_handle = Db.db_handle()
                sql = "UPDATE schools SET data = update_obj WHERE school.name = %s" % sch_obj.addr
                db_handle(sql, sch_obj)

                sql = "UPDATE courses SET data = course_obj WHERE student.name = %s" % new_course.name
                db_handle(sql, new_course)

                break

    @staticmethod
    def develop_class(sch_obj, ACCESS_LOG):
        """
        函数功能：新开设班级
        :param sch_obj:
        :param ACCESS_LOG:
        :return:
        """
        courses = '''
        -------------------------您已经开设的课程为----------------------------
        %s
        ''' % sch_obj.get_opened_course(ACCESS_LOG)

        print(courses)

        while True:
            choice = input("请输入您想要新增班级的课程>>>").strip()
            for course in sch_obj.courses:
                if choice == course.name:
                    msg = sch_obj.develop_one_class(course, ACCESS_LOG)

                    menu = {
                        "1": "开设新班级失败：{addr}分校没有开设课程{course_name}".format(
                            addr=sch_obj.addr,
                            course_name=course.name),
                        "2": "开设新班级成功：现在班级数为{id}".format(id=len(sch_obj.courses))
                    }
                    ACCESS_LOG.info(menu[msg])

                    if msg == "1":
                        print("开设新班级失败")
                        break

                    db_handle = Db.db_handle()

                    course_obj = course
                    sch_obj = sch_obj
                    stu_objs = course.students
                    teachers = course.teachers
                    classes = course.classes

                    sql = "UPDATE courses SET data = course_obj WHERE student.name = %s" % course_obj.name
                    db_handle(sql, course_obj)

                    sql = "UPDATE schools SET data = update_obj WHERE school.name = %s" % sch_obj.addr
                    db_handle(sql, sch_obj)

                    for stu_obj in stu_objs:
                        sql = "UPDATE customers SET data = stu_obj WHERE student.name = %s" % stu_obj.addr
                        db_handle(sql, stu_obj)

                    for tea_obj in teachers:
                        sql = "UPDATE teachers SET data = tea_obj WHERE tea.name = %s" % tea_obj.name
                        db_handle(sql, tea_obj)

                    for class_obj in classes:
                        sql = "UPDATE classes SET data = class_obj WHERE class.name = %s" % class_obj.name
                        db_handle(sql, class_obj)

                print("输入有误，未开设此课程")