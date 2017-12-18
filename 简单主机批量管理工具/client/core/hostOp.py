# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import paramiko
from conf import settings
import time


class HostOp(object):
    def __init__(self, conn_info):
        # print(conn_info)
        self.host = conn_info[settings.HOST]
        self.port = int(conn_info[settings.PORT])
        self.username = conn_info[settings.USERNAME]
        self.password = conn_info[settings.PASSWORD]



    def execute(self, cmd):
        address_cmd = cmd.split()
        if type(cmd) is not str:
            return False
        strip_str = ""
        for i in range(4):
            strip_str = strip_str + address_cmd[i] + " "
            # print(i, strip_str)
        strip_str = strip_str.strip()
        cmd = cmd.lstrip(strip_str).strip()
        if not cmd.startswith(address_cmd[4]):
            cmd = address_cmd[4][0] + cmd

        if address_cmd[3] == "-action":
            res = self.scp(cmd)

        else:
            res = self.ssh(cmd)

        # print("running")
        return res

    def scp(self, cmd):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username,
                       password=self.password)
        handle = paramiko.SFTPClient.from_transport(transport)

        cmd_list = cmd.split()

        action = cmd_list[0]

        func = getattr(self, action)
        func(handle, cmd_list)


    def get(self, *args):
        handle = args[0]
        cmd_list = args[1]

        local, remote = self.get_path(cmd_list)
        handle.get(remote, local)
        handle.close()
        return True


    def put(self, *args):
        handle = args[0]
        cmd_list = args[1]

        local, remote = self.get_path(cmd_list)
        handle.put(local, remote)
        handle.close()
        return True

    def get_path(self, *args):
        cmd_list = args[0]
        local_index = cmd_list.index("-local")
        local_path_index = local_index + 1

        remote_index = cmd_list.index("-remote")
        remote_path_index = remote_index + 1
        return local_path_index, remote_path_index


    def ssh(self, cmd):
        handle = paramiko.SSHClient()
        handle.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        handle.connect(hostname=self.host,
                       port=self.port,
                       username=self.username,
                       password=self.password)
        stdin, stdout, stderr = handle.exec_command(cmd)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        return result