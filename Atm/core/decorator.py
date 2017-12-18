# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from Atm.common.tools import *
from Atm.core.CONSTANT import *

import json
path_account = Root_path().get_root_path() + "\\db\\accounts"
path_name_dir = Root_path().get_root_path() + "\\db\\accounts_records\\"
#print(path_account)

def test_login(func):
    def decorator(*args, **kwargs):
        R_Flag = False
        name = kwargs["name"]
        pwd = kwargs["pwd"]

        with open(path_account, "r") as f_account:
            data = f_account.read()
            if not data:
                print("系统尚无用户注册")
                return False
            accounts = json.loads(data)
        if accounts.get(name) and accounts[name][PWD] == pwd:
            R_Flag = True
        if not R_Flag:
            print("登陆失败")
            return R_Flag

        if not accounts[name][STATUS]:
            print("\033[31;1m账户被冻结，请联系管理员解除冻结状态\033[0m")
            return False

        R_Flag = func(*args, **kwargs)
        if not R_Flag:
            print("{name}失败".format(name = func.__name__))
        return R_Flag
    return decorator

        # if Flag:
        #     self.balance = int(self.accounts[name][BALANCE])
        #     self.name = name