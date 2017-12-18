# -*- coding:utf-8 -*-
# __author__ = 'gupan'

import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)
'''
需求:

    主机分组
    主机信息配置文件用configparser解析
    可批量执行命令、发送文件，结果实时返回，执行格式如下
        batch_run  -h h1,h2,h3   -g web_clusters,db_servers    -cmd  "df -h"　
        batch_scp   -h h1,h2,h3   -g web_clusters,db_servers  -action put  -local test.py  -remote /tmp/　
        简化：
        batch_run  -h h1,h2,h3   -cmd  "df -h"　
        batch_scp   -h h1,h2,h3  -action put  -local test.py  -remote /tmp/　
    主机用户名密码、端口可以不同
    执行远程命令使用paramiko模块
    批量命令需使用multiprocessing并发，改为用selectors实现
'''
from core import main

if __name__ == "__main__":
    main.run()