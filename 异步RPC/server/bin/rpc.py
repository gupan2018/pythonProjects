# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys
import re

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)

from core import main

if __name__ == '__main__':
    # main.run()
    str = "csdbnhcs"
    # print(str.index("p"))
    print(str[1:])
    run = "run 'df -h' -h h1, h2"
    print(re.findall("h\d", run))
    print(re.search("'.*'", run).group().strip("'"))