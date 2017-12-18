# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import socketserver
from core.ftpServer import FtpServer

# base_msg_dic = {
#     "Action": None,
#     "Parameter":None,
#     "User": None,
#     "user_home":None,
#     "cur_path":None,
#     "ret_code":None,
#     "size": 0,
#     "OverWrite":True
# }

def run():
    HOST, PORT = "0.0.0.0", 8888
    server = socketserver.ThreadingTCPServer((HOST, PORT), FtpServer)
    server.serve_forever()
    server.server_close()