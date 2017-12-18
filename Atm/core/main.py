# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from Atm.core.shopping import *
from Atm.core.card import *

def main():
    print("\033[31;1m请输入您想要的操作\033[0m")
    print("\033[32:1m"
          "添加商品进购物车：1\n"
          "删除购物车中的商品：2\n"
          "结算购物车中的商品：3\n"
          "管理账户：4\n"
          "提现：5\n"
          "还款：6\n"
          "转账：7\n\033[0m")
    choice = input("\033[33;1m输入q退出\033[0m>>>")

    if choice == "q":
        return False

    if not choice.isdigit():
        return True
    choice = int(choice)

    if choice == 4:
        pwd = input("\033[32;1m请输入root户密码>>>\033[0m")
        Shopping().manage(name = "root", pwd = pwd)
        return True

    name = input("\033[33;1m请输入登陆用户姓名>>>\033[0m")
    pwd = input("\033[31;1m请输入登陆用户密码>>>\033[0m")
    if choice == 1:
        Shopping().add_good(name = name, pwd = pwd)
    if choice == 2:
        Shopping().reduce_good(name = name, pwd = pwd)
    if choice == 3:
        Shopping().pay(name = name, pwd = pwd)

    if choice == 5:
        Shopping().withdraw(name = name, pwd = pwd)
    if choice == 6:
        Shopping().repayment(name = name, pwd = pwd)
    if choice == 7:
        Shopping().transfer(name = name, pwd = pwd)
    return True