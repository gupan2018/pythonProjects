# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import re
from conf import settings
from core.rpcServer import RpcServer
import threading
import queue

class Terminal(object):
    """
    终端类，用于控制控制台显示
    """
    def __init__(self):
        self.display = "[admin@localhost]#"
        self.usage = """
        run 'cmd' -h h1 [h2, ...]
        get
        """
        self.q = queue.Queue()

    def run_thread(self, cmd, hosts, lock):
        server = RpcServer(hosts, lock, self.q)
        for host in hosts:
            server.call(cmd, host)

    def run(self, cmd):
        res = self.parse_cmd(cmd)
        if not res["flag"]:
            return
        data = res["data"]
        cmd = data[0]
        hosts = data[1]
        lock = threading.Lock()

        t1 = threading.Thread(target=self.run_thread, args=(cmd, hosts, lock))
        t1.setDaemon(True)
        t1.start()

    def get(self, cmd):
        msg = self.q.get()
        print(msg)

    def terminal(self):
        cmd = input(self.display)
        if cmd == 'b':
            print("bye".center(50, "-"))
            exit(0)

        option = cmd.split()[0]
        if not hasattr(self, option):
            self.help()
        op_func = getattr(self, option)
        op_func(cmd)

    def parse_cmd(self, cmd):
        res = {
            "flag" : False,
            "data" : None
        }
        try:
            cmd.index("-h")
        except ValueError:
            self.help()
            return res
        commond = re.search("'.*'", cmd).group()
        commond = commond.strip("'")

        host_names = re.findall("h\d", cmd)
        hosts = []
        for host in host_names:
            if host not in settings.hosts.keys():
                print("host %s not exists" % host)
                return res
            hosts.append(settings.hosts[host])
        res["flag"] = True
        res["data"] = [commond, hosts]
        return res

    def help(self):
        print("USAGE: %s" % self.usage)