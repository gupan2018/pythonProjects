# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from conf import settings
import copy
import json
import socket
import hashlib
import os
import sys

class FtpClient(object):
    def __init__(self, *args, **kwargs):
        super(FtpClient, self).__init__()
        self.client = socket.socket()
        self.islogin = False
        self.username = None
        # print(kwargs)
        self.msg_dic = kwargs
        self.TRANS_LOG = args[0]

    def help(self):
        msg = """
        ls
        cd
        pwd
        get filename
        put filename
        login
        regist
        ...
        """
        print(msg)

    def connect(self, IP, PORT):
        self.client.connect((IP, PORT))

    def interactive(self):
        while True:
            cmd_str = input(">>>").strip()
            if cmd_str == "exit":
                break

            cmd = cmd_str.split()[0].strip()
            flag = hasattr(self, "cmd_%s"%cmd)
            if flag:
                func = getattr(self, "cmd_%s"%cmd)
                func(cmd_str)
            else:
                self.help()

    def cmd_close(self, *args, **kwargs):
        self.client.close()

    def cmd_regist(self, *args, **kwargs):
        username = input("请输入用户名>>>").strip()
        pwd = input("请输入密码>>>").strip()
        if not username or not pwd:
            print("用户注册失败")
            return

        sha_handle = hashlib.sha256()
        sha_handle.update(pwd.encode("utf-8"))

        update_pwd = sha_handle.hexdigest()

        self.msg_dic["Action"] = "regist"
        self.msg_dic["User"] = username
        self.msg_dic["Password"] = update_pwd
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))
        res_msg = self.client.recv(1024)
        res_dic = json.loads(res_msg.decode())
        res_code = res_dic["ret_code"]
        if res_code == 401:
            print(settings.res_msg[401])
        elif res_code == 200:
            print("注册成功")
            self.TRANS_LOG.info("用户%s注册成功" % username)
        else:
            print("未知错误")
        self.cleanup()

    def check_put(self, *args, **kwargs):
        if not self.islogin:
            print("尚未登录，请先登录")
            return

        self.msg_dic["Action"] = "check_put"
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))

        recv_data = self.client.recv(1024)
        recv_dic = json.loads(recv_data.decode())
        ret_code = recv_dic["ret_code"]
        if ret_code == 407:
            print("您目前没有正在上传的文件")
            return

        uploading_data = recv_dic["Parameter"]
        uploading_len = len(uploading_data.keys())

        print("您有%s条正在上传的记录".center(50, "-") % uploading_len)
        for i in range(uploading_len + 1):
            msg = "文件名：%s,  完成度%s" % (
                uploading_data[i][0],
                "%s%" % (uploading_data[i][3] / uploading_data[i][5] * 100,)
            )
        choice = input("请选择要继续下载的文件>>>").strip()

        if choice == "b":
            self.msg_dic["ret_code"] = 409
            print("放弃继续下载")
            self.client.send(json.dumps(self.msg_dic).encode("utf-8"))
            return

        if not choice.isdigit() or int(choice) > uploading_len:
            self.msg_dic["ret_code"] = 408
            print("输入错误")
            self.client.send(json.dumps(self.msg_dic).encode("utf-8"))
            return

        self.msg_dic["ret_code"] = 200
        self.msg_dic["Parameter"] = int(choice)
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))

        # 避免粘包
        self.client.recv(1024)

        put_path = uploading_data[choice][1]
        begin_addr = uploading_data[choice][3]

        with open(put_path, "rb") as put_file:
            addr = put_file.seek(begin_addr, 0)
            for line in put_file:
                self.client.send(line)

    def cmd_login(self, *args, **kwargs):
        username = input("请输入用户名>>>").strip()
        pwd = input("请输入密码>>>").strip()
        if not username or not pwd:
            print("用户注册失败")
            return

        sha_handle = hashlib.sha256()
        sha_handle.update(pwd.encode("utf-8"))

        update_pwd = sha_handle.hexdigest()
        self.msg_dic["Action"] = "login"
        self.msg_dic["User"] = username
        self.msg_dic["Password"] = update_pwd
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))
        res_msg = self.client.recv(1024)
        res_dic = json.loads(res_msg.decode())
        res_code = res_dic["ret_code"]
        if res_code == 402:
            print(settings.res_msg[402])
        elif res_code == 200:
            print("登录成功")
            self.islogin = True
            self.TRANS_LOG.info("用户%s登录成功" % username)
            self.msg_dic["user_home"] = "/%s" % username
            self.msg_dic["cur_path"] = "/%s" % username
        else:
            print("未知错误")
        self.cleanup()

    def cmd_put(self, *args, **kwargs):
        if not self.islogin:
            print("尚未登录，请先登录")
            return
        cmd_str = args[0]
        action, parameter = cmd_str.split()

        if not os.path.isfile(parameter):
            print("上传文件不存在：%s" % parameter)
            return

        size = os.stat(parameter).st_size

        self.msg_dic["Action"] = action
        self.msg_dic["Parameter"] = parameter
        self.msg_dic["size"] = size
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))

        res_msg = self.client.recv(1024)
        res_dic = json.loads(res_msg.decode())
        res_code = res_dic["ret_code"]

        if res_code != 200:
            return

        sha_handle = hashlib.sha256()
        put_length = 0

        with open(parameter, "rb") as put_file:
            try:
                for line in put_file:
                    self.client.send(line)
                    sha_handle.update(line)
                    put_length += len(line)
                    width = 30
                    process = 30 * put_length / size

                    processbar = "\r[%s%s]%d%" % ("*" * int(process), "-" * (width - int(process)), int(put_length / size * 100))
                    sys.stdout.write(processbar)
                    sys.stdout.flush()
                self.client.send(sha_handle.hexhexdigest().encode("utf-8"))

                res_msg = self.client.recv(1024)
                res_dic = json.loads(res_msg.decode())
                ret_code = res_dic["ret_code"]
                if ret_code == 200:
                    print("文件传输成功 :%s" % parameter)
                elif res_code == 406:
                    print(settings.res_msg[res_code])
                else:
                    print("未知错误")
            except KeyboardInterrupt as e:
                print("上传文件中断，已上传 %s%" % (int(put_length / size * 100)),)

        self.cleanup()

    def cmd_get(self, *args, **kwargs):
        if not self.islogin:
            print("尚未登录，请先登录")
            return

    def cmd_ls(self, *args, **kwargs):
        if not self.islogin:
            print("尚未登录，请先登录")
            return
        cmd_str = args[0]

        action = "ls"
        parameter = None

        cmd_str = args[0]
        is_parameter = True if len(cmd_str.split()) > 1 else False
        if is_parameter:
            parameter = cmd_str.split()[1].strip()

        self.msg_dic["Action"] = action
        self.msg_dic["Parameter"] = parameter

        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))

        recv_str = self.client.recv(1024)
        recv_dic = json.loads(recv_str.decode())

        if recv_dic["ret_code"] == 500:
            print(settings.res_msg[500])
            self.TRANS_LOG.info("执行命令^%s %s失败" % (action, parameter))
            return

        if recv_dic["ret_code"] == 200 and \
                        recv_dic["size"] == 0:
            print()
            return

        # 若发送的命令有执行结果，那么就发送乐易ack消息，告诉server端可以发包了
        self.client.send("ack".encode("utf-8"))

        cmd_res_size = recv_dic["size"]

        print("cmd_res_size:", cmd_res_size)
        recv_len = 0

        cmd_res = ""
        while recv_len < cmd_res_size:
            recv_size_once = 1024
            if cmd_res_size - recv_len <= 1024:
                recv_size_once = cmd_res_size - recv_len
            recv_data = self.client.recv(recv_size_once)
            cmd_res += recv_data.decode()
            recv_len += len(recv_data)

        self.cleanup()
        print(cmd_res)

    def cmd_pwd(self, *args):
        if not self.islogin:
            print("尚未登录，请先登录")
            return

        cmd_str = args[0]
        if len(cmd_str.split()) > 1:
            print("参数错误")
            return

        action = "pwd"
        self.msg_dic["Action"] = action
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))

        res_msg = self.client.recv(1024)
        res_dic = json.loads(res_msg.decode())
        res_code = res_dic["ret_code"]
        if res_code == 403:
            print(settings.res_msg[403])

        self.client.send("ack".encode("utf-8"))
        size = res_dic["size"]
        recv_str = ""
        recv_len = 0
        while recv_len < size:
            recv_size_once = 1024
            if size - recv_len < 1024:
                recv_size_once = size - recv_len
            recv_data = self.client.recv(recv_size_once)
            recv_len += len(recv_data)
            recv_str += recv_data.decode()
        print(recv_str)
        self.cleanup()

    def cmd_cd(self, *args):
        if not self.islogin:
            print("尚未登录，请先登录")
            return

        cmd_str = args[0]
        if len(cmd_str.split()) != 2:
            return
        action, parameter = cmd_str.split()
        self.msg_dic["Action"] = action
        self.msg_dic["Parameter"] = parameter
        self.client.send(json.dumps(self.msg_dic).encode("utf-8"))
        res_msg = self.client.recv(1024)
        res_dic = json.loads(res_msg.decode())
        res_code = res_dic["ret_code"]

        username = res_dic["User"]

        if res_code != 200:
            print(settings.res_msg[res_code])
            self.TRANS_LOG.info("用户%s切换目录失败" % username)
            self.cleanup()
            return

        self.msg_dic["cur_path"] = res_dic["cur_path"]
        self.cleanup()

    def cleanup(self, *args, **kwargs):
        self.msg_dic["Parameter"] = None
        self.msg_dic["Action"] = None
        self.msg_dic["ret_code"] = None
        self.msg_dic["size"] = 0
        self.msg_dic["Password"] = None