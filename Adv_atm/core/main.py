# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.common.logger import Logger
from conf import settings
from core import auth
from core.user_operate import Operate


#获取交易记录的logger对象
TRANS_LOGGER = Logger(settings.TRANS)
#获取总的logger对象
ACCESS_LOGGER = Logger(settings.ACCESS)

'''
用户状态字典，用来存储已登录用户状态

数据结构如下：
account_name：登陆用户名
is_authenticated：是否登陆
user_data：用户账户信息
'''
user_status = {
    "account_name":None,
    "is_authenticated":False,
    "user_data":None
}

def interactive(user_data):
    '''
    函数实现逻辑：
        由于函数需要根据用户输入来采取相应的操作，所以设置一个字典menu_dic，根据输入值来决定调用哪一个函数，字典结构如下：
        key：choice_num
        value：用户操作的函数名，即函数指针

        字典取值：
        1.  账户信息
        2.  还款(功能已实现)
        3.  取款(功能已实现)
        4.  转账
        5.  账单
        6.  退出

    函数参数：
        acc_data：用户账户信息
    返回值：
        NULL
    '''
    menu = '''
    -------------------菜单---------------------
        1.  账户信息
        2.  还款(功能已实现)
        3.  取款(功能已实现)
        4.  转账
        5.  账单
        6.  退出
    -------------------结束--------------------
    '''
    print(menu)
    choice = input("请输入您想要进行的操作>>>").strip()
    Operater = Operate()
    menu_dict = {
        "1":Operater.info,
        "2":Operater.repay,
        "3":Operater.withdraw,
        "4":Operater.transfer,
        "5":Operater.bill,
        "6":Operater.exit
    }

    if choice in menu_dict.keys():
        return menu_dict[choice](user_data)
    else:
        print("您选择的操作不存在，请重新输入")
        return True

def run():
    '''
    函数实现逻辑：
        定义一个menu菜单
        /**
        *1：登陆
        *2：注册
        **/
        首先判断用户是登陆还是注册，调用auth模块中的函数
        登陆：auth.login
        注册：auth.enroll
    '''

    menu = u'''
    ----------------MENU-----------------
    1：登陆
    2：注册
    ---------------------------------------
    '''
    print(menu)
    menu_dict = {
        "1":auth.login,
        "2":auth.enroll
    }

    choice = input("请输入您想要进行的操作>>>").strip()

    if choice in menu_dict.keys():
        user_data = menu_dict[choice](user_status)
        user_status["user_data"] = user_data
        if user_status["is_authenticated"]:
            ACCESS_LOGGER.info("%s成功"%user_data["name"])
            while interactive(user_data):
                choice = input("是否继续操作，按\033[31;1mb\033[0m结束")
                if choice == "b":
                    break
        else:
            ACCESS_LOGGER.error("%s失败"%menu_dict[choice].__name__)
    else:
        ACCESS_LOGGER.error("您选择的操作不存在，请重新输入")

