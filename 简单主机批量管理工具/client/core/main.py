# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.batchManager import BatchManager


def run():
    manager = BatchManager()
    while True:
        manager.send_cmd()


if __name__ == "__main__":
    run()