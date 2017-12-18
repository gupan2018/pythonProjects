# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from Atm.common.tools import *
import logging

class CLog:
    # ----------------------------------------------------------------------------
    def __init__(self, path = "\\log\\test.log"):
        #日志文件的存放路径，根据自己的需要去修改
        LOG_FILE_PATH = Root_path().get_root_path() + path
        self.logger = logging.getLogger()
        fileHandler = logging.FileHandler(LOG_FILE_PATH)
        #日志的输出格式
        fmt = '\n' + '%(asctime)s - %(filename)s:%(lineno)s  - %(message)s'
        formatter = logging.Formatter(fmt)  # 实例化formatter
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.NOTSET)

    def DebugMessage(self, msg):
        self.logger.debug(msg)
        pass