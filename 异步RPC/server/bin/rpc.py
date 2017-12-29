# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys
import re
import socket

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)

from core import main

if __name__ == '__main__':
    main.run()
    # str = "csdbnhcs"
    # # print(str.index("p"))
    # print(str[1:])
    # run = "run 'df -h' -h h1, h2"
    # test = re.findall("h\d", run)
    # print(test[1])
    # print(re.search("'.*'", run).group().strip("'"))
    # myname = socket.getfqdn(socket.gethostname())
    # myaddr = socket.gethostbyname(myname)
    # print(type(myaddr))