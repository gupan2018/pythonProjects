# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)
print(BASE_PATH)

from core import main

if __name__ == "__main__":
    main.run()