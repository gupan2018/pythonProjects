# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from Atm.core.CONSTANT import *
from Atm.common.tools import *
import json
import time
from Atm.core.decorator import *
import copy
from Atm.core.card import Card
from Atm.common.logs import CLog

class Shopping:
    def __init__(self):
        self.db_dir = Root_path().get_root_path() + "\\db\\"
        path_goods = self.db_dir + "goods"
        with open(path_goods, "r") as f_goods:
            self.goods = f_goods.read()
            if not self.goods:
                self.goods = {}
            else:
                self.goods = json.loads(self.goods)

    def per_shopping(self, name):
        path_account = self.db_dir + "accounts"
        with open(path_account, "r") as f_accounts:
            accounts = json.loads(f_accounts.read())
            #获取用户购物车内的商品及其数量
            goods = accounts[name][GOODS]
        return goods

    def list_per_shopping(self, name):
        per_shopping = self.per_shopping(name)
        print("\033[33;1m您购物车中的商品为>>>\033[0m")
        for item in iter(per_shopping.items()):
            print("商品名：{name}，数量：{count}".format(
                name = item[0],
                count = item[1]))
        return True

    def get_accounts(self):
        path_account = self.db_dir + "accounts"
        with open(path_account, "r") as f_accounts:
            data = f_accounts.read()
            if not data:
                return False
            accounts = json.loads(data)
        return accounts

    def write_accounts(self, accounts):
        path_account = self.db_dir + "accounts"
        with open(path_account, "w") as f_accounts:
            f_accounts.write(json.dumps(accounts))
        return True

    def per_total(self, name):
        total = 0
        per_shopping = self.per_shopping(name)

        print("\033[33;1m您购物车中的商品为>>>\033[0m")
        for item in iter(per_shopping.items()):
            print("商品名：{name}，数量：{count}".format(
                name = item[0],
                count = item[1]))

            univalence = self.goods[item[0]]
            count = item[1]
            total += univalence * count
        return total

    def write_per_recods(self, name, str):
        path_name = Root_path().get_root_path() + "\\db\\accounts_records\\" + name

        with open(path_name, "a") as f_name:
            f_name.write(str)

    # #登陆
    # @test_login
    # def login(self, *args, **kwargs):
    #     return True

    @test_login
    def manage(self, *args, **kwargs):
        R_Flag = True
        name = kwargs["name"]
        if name != "root":
            R_Flag = False
            print("\033[31;1m非root用户权限受限\033[1m")
            return R_Flag

        choice = input("\033[31;1m请输入操作类型：\n添加用户：1\n冻结用户：2\n查询额度：3\n输入q退出>>>\033[1m")
        while True:
            if choice.isdigit() and choice in ["1", "2", "3"]:
                choice = int(choice)
                break
            if choice == "q":
                print("\033[31;1m放弃操作\033[0m")
                return R_Flag
            choice = input("\033[31;1m请输入操作类型：\n添加用户：1\n冻结用户：2\n查询额度：3\n输入q退出\033[1m")
        CLog().DebugMessage("开始进行权限管理")
        if choice == 1:
            return self.register()
        if choice == 2:
            return self.freeze_account()
        if choice == 3:
            return self.see_balance()

    def see_balance(self):
        accounts = self.get_accounts()
        print("\033[31;1m您可查询的用户为\033[0m")
        for name in iter(accounts.keys()):
            if name != "root":
                print(name)
        choice = input("\033[31;1m请输入您要查询的用户名称>>>\033[0m")
        while choice not in iter(accounts.keys()):
            if choice == "q":
                print("\033[31;1m放弃查询\033[0m")
                return True
            choice = input("\033[31;1m请输入您要查询的用户名称>>>\033[0m")
        print("查询成功，{name}的账户余额为\033[31;1m{balance}\033[0m".format(
            name = choice,
            balance = accounts[choice][BALANCE]))
        CLog().DebugMessage("查询{name}账户余额成功".format(name = choice))
        return True

    def freeze_account(self):
        accounts = self.get_accounts()
        print("\033[31;1m您可冻结的用户为\033[0m")
        for name in iter(accounts.keys()):
            if name != "root":
                print(name)
        choice = input("\033[31;1m请输入您要冻结的用户名称>>>\033[0m")
        while choice not in iter(accounts.keys()):
            if choice == "q":
                print("\033[31;1m放弃\033[0m")
                return True
            choice = input("\033[31;1m请输入您要冻结的用户名称>>>\033[0m")
        accounts[choice][STATUS] = FREEZE

        CLog().DebugMessage("冻结{name}账户".format(name = choice))
        self.write_accounts(accounts)
        return True

    #注册
    def register(self):
        accounts = self.get_accounts()
        if accounts == False:
            accounts = {}
        R_Flag = True
        balance = 15000
        name = input("\033[34;1m请输入注册用户名>>>\033[0m")
        pwd = input("\033[34;1m请输入密码>>>\033[0m")
        if accounts.get(name):
            R_Flag = False

        balance = input("\033[33;1m请输入您的额度，默认15000>>>\033[0m")
        while R_Flag:
            if balance == "":
                balance = 15000
                break
            if balance.isdigit():
                balance = int(balance)
                break
            else:
                print("\033[31;1m只能输入数字，请重新输入\033[0m")

        if R_Flag:
            msg = "{time} {name}注册成功，账户额度{balance}\n".format(
                    name = name,
                    time = Time().format_time(),
                    balance = balance)
            self.write_per_recods(name, msg)
            CLog().DebugMessage(msg)
            accounts[name] = [pwd, balance, {}, LOMAL, balance]
            self.write_accounts(accounts)
        return R_Flag

    #添加购物车商品
    @test_login
    def add_good(self, *args, **kwargs):
        R_Flag = False
        name = kwargs["name"]
        accounts = self.get_accounts()
        per_shopping = self.per_shopping(name)
        balance = accounts[name][BALANCE]

        print("\033[31;1m您可以挑选的商品为>>>\033[0m")
        for item in iter(self.goods.items()):
            print("\033[31;1m商品：{name},价格：{price}\033[0m".format(
                name = item[0],
                price = item[1]))

        print("您的余额为：\033[31;1m{balance}\033[0m".format(balance=balance))
        if balance < min(self.goods.values()):
            print("您的余额不足以购买商品，请充值")
            return R_Flag

        good_name = input("\033[34;1m请输入您想要添加进购物车的商品>>>\033[0m")

        if self.goods.get(good_name.strip()):
            if per_shopping.get(good_name):
                per_shopping[good_name] += 1
            else:
                per_shopping[good_name] = 1
            R_Flag = True

        if R_Flag:
            accounts[name][GOODS] = per_shopping
            self.write_accounts(accounts)
        return R_Flag

    #删除购物车商品
    @test_login
    def reduce_good(self, *args, **kwargs):
        R_Flag = False
        name = kwargs["name"]
        accounts = self.get_accounts()
        reduce_count = 0
        per_shopping = self.per_shopping(name)
        total = self.per_total(name)

        while True:
            if per_shopping == {}:
                print("购物车已空")
                break
            if reduce_count != 0:
                for item in iter(per_shopping.items()):
                    print("商品名：{name}，数量：{num}".format(name = item[0], num = item[1]))

            del_good = input("请输入想要减少的商品名，每次只能减1，输入q退出>>>")
            if del_good == "q":
                break

            if not per_shopping.get(del_good):
                print("\033[32;1m{good}不在{name}的购物车共，请重新输入\033[0m".format(good=del_good,name=name))
                continue

            per_shopping[del_good] -= 1
            if per_shopping[del_good] == 0:
                per_shopping.pop(del_good)
            total -= self.goods[del_good]
            if total <= accounts[name][BALANCE]:
                R_Flag = True

            if total > accounts[name][BALANCE]:
                print("余额不足，请继续清理购物车")

            reduce_count += 1

            if input("\033[31;1m是否继续删除，确认：y，其余n>>>\033[0m") == "y":
                continue

        if reduce_count == 0:
            R_Flag = True
            print("您的购物车没有发生变化")
        if reduce_count > 0:
            print("您删除了{count}件商品".format(count = reduce_count))

        accounts[name][GOODS] = per_shopping
        self.write_accounts(accounts)
        return R_Flag

    #支付，信用卡接口
    def pay(self,  *args, **kwargs):
        # card_pay = kwargs["func"]
        R_Flag = False
        name = kwargs["name"]
        accounts = self.get_accounts()
        total = self.per_total(name)
        balance = accounts[name][BALANCE]
        goods = copy.deepcopy(accounts[name][GOODS])

        if total >= balance:
            choice = input("您的余额不足，是否删减购物车？是：y>>>")
            if choice != "y":
                return R_Flag
            if not self.reduce_good(*args, **kwargs):
                print("余额不足")
                return R_Flag
            total = self.per_total(name)

        choice = input(("您的购物车的商品总价为\033[31;1m{total}\033[0m是否支付？\n是请输入y，其余为否>>>".format(total = total)))
        if choice.strip() == "y":
            pwd = input("\033[31;1m请输入密码>>>\033[0m")
            Card().pay(pwd = pwd, name = name, accounts = accounts, total = total)
            R_Flag = True

        return R_Flag

    #提现
    @test_login
    def withdraw(self, *args, **kwargs):
        name = kwargs["name"]
        accounts = self.get_accounts()
        balance = accounts[name][BALANCE]

        R_Flag = True
        Input_legal = False
        amount = 0

        print("您的余额为{balance}".format(balance=balance))

        if balance < 100:
            R_Flag = False

        while not Input_legal:
            amount = input("\033[31;1m请输入提现金额>>>\033[0m")
            if not amount.isdigit():
                print("提现金额只能是数字")
                continue
            amount = int(amount)

            if amount * 1.005 > balance:
                print("\033[31;1m提现金额大于账户余额\033[0m")
                continue

            if amount < 100:
                print("提现金额需大于100")
                continue

            Input_legal = True

        choice = input("提现金额{amount}， 需手续费{comission}，是否继续，确认输入y，其余放弃>>>".format(amount=amount, comission = amount*0.05))
        if choice != "y":
            R_Flag = False
            return R_Flag

        pwd = input("\033[31;1m请输入密码>>>\033[0m")
        Card().withdraw(pwd = pwd, balance = balance, amount = amount, accounts = accounts, name = name)

        return R_Flag

    @test_login
    def transfer(self, *args, **kwargs):
        name = kwargs["name"]
        accounts = self.get_accounts()
        origin_balance = accounts[name][BALANCE]

        print("\033[31;1m可转账的储户为:\033[0m")
        for account in iter(accounts.keys()):
            if account != name:
                print(account)

        dest_name = input("\033[32;1m请输入收款人账户， 输入q退出>>>\033[0m")

        while True:
            if dest_name == "q":
                print("放弃转账")
                return True

            if dest_name == name:
                print("\033[32;1m不能给自己转账\033[0m")
                dest_name = input("\033[32;1m请输入收款人账户， 输入q退出>>>\033[0m")
                continue

            if dest_name in accounts.keys():
                break
            print("\033[32;1m该账户不存在，请重新输入\033[0m")
            dest_name = input("\033[32;1m请输入收款人账户， 输入q退出>>>\033[0m")

        amount = input("\033[32;1m请输入转账金额， 输入q退出>>>\033[0m")

        while True:
            if amount == "q":
                print("放弃转账")
                return True
            if not amount.isdigit():
                print("请输入数字，必须是\033[31;1m100的整数倍\033[0m")
            else:
                amount = int(amount)
                if amount % 100 != 0 or amount < 100:
                    print("请输入数字，必须是\033[31;1m100的整数倍\033[0m")
                    amount = input("\033[32;1m请输入转账金额， 输入q退出>>>\033[0m")
                    continue
                if amount * 1.005 > origin_balance:
                    print("\033[31;1m账户余额不足,请重新输入\033[0m")
                    amount = input("\033[32;1m请输入转账金额， 输入q退出>>>\033[0m")
                    continue
                break

        pwd = input("\033[31;1m请输入密码>>>\033[0m")

        Card().transfer(name = name, pwd = pwd, amount = amount, accounts = accounts, dest_name = dest_name)
        return True

    @test_login
    def repayment(self, *args, **kwargs):
        name = kwargs["name"]
        accounts = self.get_accounts()
        init_account = accounts[name][INIT]
        balance = accounts[name][BALANCE]

        require_repay = init_account - balance
        if require_repay <= 0:
            print("您的账户信用良好，不需要还款")
            return True

        while True:
            choice = input("\033[31;1m您需要偿还的金额为{money},是否还款？\n是：y\n放弃：q\n请输入>>>\033[0m".format(money=require_repay))
            if choice == "q":
                print("放弃还款")
                return True
            if choice == "y":
                break

        pwd = input("\033[32;1m请输入密码>>>\033[0m")
        Card().repayment(name = name, requiry = require_repay, accounts = accounts, pwd = pwd)
        return True