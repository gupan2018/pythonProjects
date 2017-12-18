# -*- coding:utf-8 -*-
# __author__ = 'gupan'

from core.common.logger import Logger
from core.ftpClient import FtpClient

TANS_LOGGER = Logger("access")

base_msg_dic = {
    "Action": None,
    "Password":None,
    "Parameter":None,
    "user": None,
    "user_home":None,
    "cur_path":None,
    "ret_code":None,
    "size": 0,
    "OverWrite":True
}

def input_host():
    while True:
        addr = input("Input IP addr>>>").strip()
        if addr == "localhost":
            return addr

        if "." not in addr:
            continue
        check_codes = addr.split(".")

        if len(check_codes) != 4:
            continue

        for check_code in check_codes:
            if not check_code.isdigit() or \
                            int(check_code) > 225 or \
                            int(check_code) < 0:
                continue
        return addr

def input_pwd():
    while True:
        port = input("Input Port>>>").strip()
        if port.isdigit():
            port = int(port)
            return port
        continue

def run():
    HOST = input_host()
    PORT = input_pwd()

    client = FtpClient(TANS_LOGGER, **base_msg_dic)
    client.connect(HOST, PORT)
    while True:
        client.interactive()