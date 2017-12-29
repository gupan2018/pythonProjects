# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import re
from conf import settings
import threading

class Terminal(object):
    """
    终端类，用于控制控制台显示
    """
    def __init__(self):
        self.display = "[admin@localhost]#"
        self.usage = "run 'cmd' -h h1 [h2, ...]"

    def display(self):
        cmd = input(self.display)
        if cmd == 'b':
            print("bye".center(50, "-"))
            exit(0)
        if not cmd.startswith("run "):
            self.help()

        self.parse_cmd(cmd)

    def parse_cmd(self, cmd):
        try:
            cmd.index("-h")
        except ValueError:
            self.help()
            return
        commond = re.search("'.*'", cmd).group()
        commond = commond.strip("'")

        hosts = re.findall("h\d", cmd)
        for host in hosts:
            if host not in settings.hosts.keys():
                print("host %s not exists" % host)
                return

    def help(self):
        print("USAGE: %s" % self.usage)