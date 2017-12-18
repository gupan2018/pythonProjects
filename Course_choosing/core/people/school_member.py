# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from core.people.people import People

class School_member(People):
    def __init__(self, name, age, addr):
        super(School_member, self).__init__(name, age)
        self.addr = addr