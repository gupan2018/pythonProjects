# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from Atm.core.CONSTANT import *
from Atm.common.tools import *
import json
import time
from Atm.core.decorator import *
import copy
from Atm.common.logs import CLog

class Card:
    def __init__(self):
        self.db_dir = Root_path().get_root_path() + "\\db\\"

    def write_accounts(self, accounts):
        path_account = self.db_dir + "accounts"
        with open(path_account, "w") as f_accounts:
            f_accounts.write(json.dumps(accounts))
        return True

    def write_per_recods(self, name, str):
        path_name = Root_path().get_root_path() + "\\db\\accounts_records\\" + name

        with open(path_name, "a") as f_name:
            f_name.write(str)

    @test_login
    def pay(self, *args, **kwargs):
        name = kwargs["name"]
        accounts = kwargs["accounts"]
        balance = accounts[name][BALANCE]
        total = kwargs["total"]
        goods = copy.deepcopy(accounts[name][GOODS])

        balance -= total
        accounts[name][BALANCE] = balance
        accounts[name][GOODS].clear()

        msg = "{time} {name}于消费{total}，账户额度{balance}, 购买的商品以及数量为{items}\n".format(
                    time = Time().format_time(),
                    name = name,
                    total = total,
                    balance = balance,
                    items = str(goods))
        CLog().DebugMessage(msg)
        self.write_per_recods(name, msg)
        self.write_accounts(accounts)
        return True

    @test_login
    def withdraw(self, *args, **kwargs):
        balance = kwargs["balance"]
        amount = kwargs["amount"]
        accounts = kwargs["accounts"]
        name = kwargs["name"]
        balance -= amount * 1.005
        accounts[name][BALANCE] = balance

        self.write_accounts(accounts)

        msg = "{time} {name}于{time}提现{amount}，手续费{commission}，账户余额{balance}\n".format(
            time = Time().format_time(),
            name = name,
            amount = amount,
            commission = amount *0.005,
            balance = balance)
        CLog().DebugMessage(msg)
        self.write_per_recods(name, msg)
        return True

    def charge(self, *args, **kwargs):
        amount = kwargs["amount"]
        accounts = kwargs["accounts"]
        origin_name = kwargs["origin_name"]
        dest_name = kwargs["dest_name"]

        balance = accounts[dest_name][BALANCE]


        balance -= amount
        accounts[dest_name][BALANCE] = balance

        self.write_accounts(accounts)

        msg = "{time} {dest_name}收到{origin_name}转账{amount}，账户余额{balance}\n".format(
            time = Time().format_time(),
            dest_name = dest_name,
            origin_name = origin_name,
            amount = amount,
            balance = balance)
        CLog().DebugMessage(msg)
        self.write_per_recods(dest_name, msg)
        return True

    @test_login
    def transfer(self, *args, **kwargs):
        amount = kwargs["amount"]
        accounts = kwargs["accounts"]
        origin_name = kwargs["name"]
        dest_name = kwargs["dest_name"]
        balance = accounts[origin_name][BALANCE]


        balance -= amount * 1.005
        accounts[origin_name][BALANCE] = balance

        self.write_accounts(accounts)

        msg = "{time} {origin_name}转账给{dest_name}人民币{amount}，手续费{commission}，账户余额{balance}\n".format(
            time = Time().format_time(),
            origin_name = origin_name,
            dest_name = dest_name,
            amount = amount,
            commission = amount *0.005,
            balance = balance)

        CLog().DebugMessage(msg)
        self.write_per_recods(origin_name, msg)

        self.charge(amount=amount, dest_name=dest_name, origin_name=origin_name, accounts = accounts)
        return True

    def repayment(self, *args, **kwargs):
        name = kwargs["name"]
        accounts = kwargs["accounts"]
        money = kwargs["requiry"]

        accounts[name][BALANCE] = accounts[name][INIT]
        balance = accounts[name][BALANCE]
        self.write_accounts(accounts)

        msg = "{time} {name}还款人民币{money}，账户余额{balance}\n".format(
            time = Time().format_time(),
            name = name,
            money = money,
            balance = balance)
        CLog().DebugMessage(msg)
        self.write_per_recods(name, msg)
        return True