# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import optparse
from core.batchManager import BatchManager

ret_msg = {
    200:"batch search success",
    201:"batch transport success",
    500:"input error, try again",
    501:"not host have been defined, check settings",
    502:"the put file not exists",
    503:"in the get action, local dir is not exists"
}

class ArgvHandler(object):
    def __init__(self):
        super(ArgvHandler,self).__init__()
        parse = optparse.OptionParser()
        (option, args) = parse.parse_args()
        self.verify_args(args)

    def verify_args(self, *args):
        if len(args) > 1:
            exit("too many parameter")
        if hasattr(self, args[0]):
            func = getattr(self, args[0])
            func()
        else:
            exit("error command")

    def start(self):
        manager = BatchManager()
        while True:
            res = manager.send_cmd()
            if res == 500:
                print(ret_msg[res])
                manager.help()

    def end(self):
        exit("nothing have been done")