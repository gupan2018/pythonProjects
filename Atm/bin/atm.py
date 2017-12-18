# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from Atm.core import main

if __name__ == "__main__":
    Flag = True
    while Flag:
        Flag = main.main()