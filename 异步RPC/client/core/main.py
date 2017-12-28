# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from core.rpcClient import RpcClient


def run():
    client = RpcClient()
    while True:
        client.call()