# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)

import configparser
ini_path = BASE_PATH + "\\conf\\settings.ini"

handle = configparser.ConfigParser()
if not os.path.isfile(ini_path):
    print("not such file")
handle.read(ini_path)

# 获取配置的主机号
HOSTS = handle.items('hosts')
hosts = {}
for section in HOSTS:
    hosts[section[0]] = section[1]