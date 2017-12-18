# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import threading
import paramiko
from core.hostOp import HostOp
from conf import settings


class MyThread(threading.Thread):
    def __init__(self, conn_info, cmd):
        super(MyThread, self).__init__()
        self.conn_info = conn_info
        self.cmd = cmd

    def run(self):
        ssh_conn = HostOp(self.conn_info)
        res = ssh_conn.execute(self.cmd)
        if res is False:
            print("parameters' type error")
        if res is True:
            print("file transport done")
        else:
            print(res)