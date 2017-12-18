# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import configparser

class IniParse(object):
    def __init__(self, ini_path):
        super(IniParse, self).__init__()
        pass

    def handle(self, ini_path):
        handle = configparser.ConfigParser()
        handle.read(ini_path)
        return handle



