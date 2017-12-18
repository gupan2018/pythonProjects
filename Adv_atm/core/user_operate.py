# -*- coding:utf-8 -*-
# __author__ = 'gupan'

class Operate:
    def __init__(self):
        pass

    def info(self, user_data):
        '''
        {"enroll_day": "2017-11-19", "name": "test001", "passwd": "123", "credit": "15000", "status": "0", "balance": "0"}
        '''

        judge_status = {
            "0":"正常",
            "1":"冻结"
        }

        name = user_data["name"]
        credit = user_data["credit"]
        balance = user_data["balance"]
        enroll_day = user_data["enroll_day"]
        status = user_data["status"]

        info = '''
        ------------------------------个人信息------------------------------
        姓名:{name}
        信用额度:{credit}
        余额:{balance}
        注册时间:{enroll_day}
        用户状态:{status}
        ---------------------------------end---------------------------------
        '''.format(name = name, credit = credit, balance = balance, enroll_day = enroll_day, status = judge_status[status])
        print(info)
        return True

    def repay(self, user_data):
        return True

    def withdraw(self, user_data):
        return True

    def transfer(self, user_data):
        return True

    def bill(self, user_data):
        return True

    def exit(self, user_data):
        return False