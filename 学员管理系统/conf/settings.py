# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import configparser
ini_path = BASE_DIR + "\\conf\\settings.ini"
ini_handle = configparser.ConfigParser()
ini_handle.read(ini_path)

# 获取数据库连接信息
User = ini_handle.get("mysql", "user")
Password = ini_handle.get("mysql", "password")
Host = ini_handle.get("mysql", "host")
Database = ini_handle.get("mysql", "database")
Charset = ini_handle.get("mysql", "charset")