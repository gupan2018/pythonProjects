# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from conf import settings
import paramiko
import optparse
import configparser
import threading
import os
from core.myThread import MyThread

class BatchManager(object):
    def __init__(self):
        super(BatchManager, self).__init__()
        self.prefix = "manager$"

    def send_cmd(self):
        cmd = input(self.prefix)
        self.verify_cmd(cmd)

    def verify_cmd(self, cmd):
        address_cmd = cmd.split()
        if hasattr(self, address_cmd[0]):
            func = getattr(self, address_cmd[0])
            return func(cmd)
        else:
            return 500

    def batch_run(self, cmd):
        address_cmd = cmd.split()
        if len(address_cmd) <= 4:
            return 500

        if "-h" != address_cmd[1] and "-cmd" != address_cmd[3]:
            return 500

        hosts_dic = self.verify_host(address_cmd[2])
        if not hosts_dic:
            return 501

        self.execute_cmd(cmd, **hosts_dic)

    def batch_scp(self, cmd):
        # print("running")
        address_cmd = cmd.split()
        if len(address_cmd) != 9:
            return 500

        if "-h" != address_cmd[1] \
                and address_cmd[4] not in ["put", "get"] \
                and address_cmd[5] != "-local" \
                and address_cmd[7] != "-remote":
            return 500

        hosts_dic = self.verify_host(address_cmd[2])
        if not hosts_dic:
            return 501
        local_index = address_cmd.index("-local")
        action_index = address_cmd.index("-action")

        action_type_index = action_index + 1
        local_file_index = local_index + 1

        if address_cmd[action_type_index] == "put" \
            and not os.path.isfile(address_cmd[local_file_index]):
            print(os.popen("dir").read())
            return 502

        if address_cmd[action_type_index] == "get" \
            and not os.path.exists(os.path.dirname(address_cmd[local_file_index])):
            return 503

        self.execute_cmd(cmd, **hosts_dic)


    def execute_cmd(self, *args, **kwargs):
        cmd = args[0]
        hosts_dic = kwargs

        hosts = hosts_dic.keys()
        ssh_handles = []
        for host in hosts:
            host_msg = hosts_dic[host]
            ssh_handle = MyThread(host_msg, cmd)
            ssh_handles.append(ssh_handle)
            ssh_handle.start()

        for handle in ssh_handles:
            handle.join()



    def verify_host(self, hosts):
        host_tags = hosts.split(",")
        handle = configparser.ConfigParser()
        handle.read(settings.ini_path)
        exist_hosts = handle.sections()
        hosts_dic = {}
        for host_tag in host_tags:
            if host_tag not in exist_hosts:
                return False
            host_info = []
            HOST = handle.get(host_tag, "HOST")
            PORT = handle.get(host_tag, "PORT")
            USERNAME = handle.get(host_tag, "USERNAME")
            PASSWORD = handle.get(host_tag, "PASSWORD")
            host_info.append(HOST)
            host_info.append(PORT)
            host_info.append(USERNAME)
            host_info.append(PASSWORD)
            hosts_dic[host_tag] = host_info
        return hosts_dic

    def help(self):
        msg = '''
        this standard input is :
        batch_run -h h1,h2 -cmd df -h　
        batch_scp -h h1,h2 -action put -local ..\\core\\hostOp.py -remote \\tmp\\test.py
        '''
        print(msg)