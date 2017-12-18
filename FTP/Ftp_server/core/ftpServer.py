# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import socketserver
from conf import settings
import os
import json
import hashlib
import re

from core.common.logger import Logger

TRANS_LOGGER = Logger("access")

class FtpServer(socketserver.BaseRequestHandler):
    """
    支持功能：
    1. ls等操作系统命令
    2. 客户端get获取服务器文件
    3. 客户端put上传文件至服务器
    4. 客户端切换目录cd
    5. 用户登陆功能
    """
    def setup(self):
        pass

    def handle(self):
        print("connecting with %s", self.client_address)
        while True:
            try:
                msg_str = self.request.recv(1024).decode()
                msg_dic = json.loads(msg_str)
                action = msg_dic["Action"]
                parameter = msg_dic["Parameter"]
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(**msg_dic)
                else:
                    # 返回程序执行失败错误码
                    msg_dic["ret_code"] = 500
                    self.request.send(json.dumps(msg_dic).encode("utf-8"))
                    TRANS_LOGGER.info("Server端执行命令%s %s失败" % (action, parameter))

            except ConnectionResetError as e:
                print("\033[31;1mclient :%s disconnect\033[0m", self.client_address)

    def finish(self):
        pass

    def put(self, *args, **kwargs):
        msg_dic = kwargs
        user_home = msg_dic["user_home"]
        cur_path = msg_dic["cur_path"]
        size = msg_dic["size"]
        put_path = msg_dic["Parameter"]
        filename = os.path.split(put_path)[1]
        recv_dir = settings.DB_ROOT + cur_path
        recv_path = recv_dir + "/" + filename

        msg_dic["ret_code"] = 200

        self.request.send(json.dumps(msg_dic).encode("utf-8"))
        recv_len = 0
        sha_handle = hashlib.sha256()
        flag = False
        with open(recv_path, "wb") as put_file:
            while True:
                recv_once = 1024
                if size - recv_len < 1024:
                    recv_once = size - recv_len
                recv_data = self.request.recv(recv_once)
                recv_len += len(recv_len)
                sha_handle.update(recv_data)

                if not recv_data:
                    print("文件put中断， 已接收%s" % (int(recv_len / size * 100)),)
                    flag = True
                    break
                    
                sha_handle.update(recv_data)
                put_file.write(recv_data)

            # 如果上传中断，直接退出
            if flag:
                recoord_path = settings.DB_ROOT + user_home + "puting"
                with open(recv_path, "a") as record_file:
                    record_data = record_file.read()

                    upload_record = {}
                    record_len = 0
                    if not record_data:
                        pass
                    else:
                        upload_record = json.loads(record_file.read())
                        record_len = len(upload_record.keys())

                    # 记录文件传输位置和状态
                    upload_record[record_len + 1] = [
                        filename, put_path, recv_path, recv_len, size - recv_len, size
                    ]
                    record_str = json.dumps(upload_record)
                    record_file.write(record_str)
                    return

            recv_code = self.request.recv(1024)
            if recv_code.decode() != sha_handle.hexdigest():
                msg_dic["ret_code"] = 406
                os.popen("rm -rf %s" % recv_path)
            else:
                msg_dic["ret_code"] = 200
            self.request.send(json.dumps(msg_dic).encode("utf-8"))

    def check_put(self, *args, **kwargs):
        msg_dic = kwargs

        user_home = msg_dic["user_home"]
        check_path = settings.DB_ROOT + user_home + "puting"
        if not os.path.isfile(check_path):
            with open(check_path, "a") as upload_file:
                record_data = {}
                record_str = json.dumps(record_data)
                upload_file.write(record_str)

        with open(check_path, "r") as record_file:
            record_data = json.loads(record_file.read())

        if record_data == {}:
            msg_dic["ret_code"] = 407
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
            return

        msg_dic["ret_code"] = 200
        msg_dic["Parameter"] = record_data
        self.request.send(json.dumps(msg_dic).encode("utf-8"))

        recv_msg = self.request.recv(1024)
        msg_dic = json.loads(recv_msg.decode())

        if msg_dic["ret_code"] == 408:
            print("客户端输入异常，放弃连接")
            return

        if msg_dic["ret_code"] == 409:
            print("客户端放弃")
            return

        user_choice = msg_dic["Parameter"]
        put_path = record_data[user_choice][1]
        recv_path = record_data[user_choice][2]
        recv_len = record_data[user_choice][3]
        leave_size = record_data[user_choice][4]
        recv_size = 0

        self.request.send(b"ack")

        while recv_size < leave_size:
            recv_size_once = 1024
            if recv_size - leave_size < 1024:
                recv_size_once = recv_size - leave_size
            self.request.recv(recv_size_once)

    def get(self, *args, **kwargs):
        pass


    def login(self, *args, **kwargs):
        msg_dic = kwargs
        login_name = msg_dic["User"]
        login_pwd = msg_dic["Password"]
        root_path = settings.DB_ROOT
        check_path = root_path + "/" + login_name

        if not os.path.isdir(check_path):
            msg_dic["ret_code"] = 402
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
            return

        pwd_path = check_path + "/" + "PWD"
        with open(pwd_path, "r") as pwd_file:
            pwd = pwd_file.read()

        if pwd == login_pwd:
            msg_dic["ret_code"] = 200
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
        else:
            msg_dic["ret_code"] = 402
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
            return

    def regist(self, *args, **kwargs):
        msg_dic = kwargs
        reg_name = msg_dic["User"]
        reg_pwd = msg_dic["Password"]
        root_path = settings.DB_ROOT
        check_path = root_path + "/" + reg_name

        if os.path.isdir(check_path):
            msg_dic["ret_code"] = 401
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
            return

        os.popen("mkdir %s" % check_path)

        pwd_path = check_path + "/" + "PWD"
        with open(pwd_path, "w") as pwd_file:
            pwd_file.write(reg_pwd)

        msg_dic["ret_code"] = 200
        self.request.send(json.dumps(msg_dic).encode("utf-8"))

    def ls(self, *args, **kwargs):
        msg_dic = kwargs
        parameter = msg_dic["Parameter"]
        check_path = settings.DB_ROOT + msg_dic["cur_path"]
        if not parameter:
            pass
        elif parameter.startswith("/"):
            check_path = settings.DB_ROOT + parameter
        else:
            check_path = check_path + "/" + parameter

        if not os.path.isdir(check_path):
            msg_dic["ret_code"] = 400
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
            return

        cmd = "ls %s" % check_path
        print("服务器执行%s命令" % cmd)
        TRANS_LOGGER.info("服务器执行%s命令" % cmd)
        cmd_res = os.popen(cmd).read()

        # 此时cmd_res是一个str类型，而encode("utf-8")之后，数据大小会变化，所以对于str类型数据，需要encode一下之后才能进行判断数据大小
        cmd_res_size = len(cmd_res.encode("utf-8"))
        msg_dic["size"] = cmd_res_size
        msg_dic["ret_code"] = 200
        self.request.send(json.dumps(msg_dic).encode("utf-8"))

        # 如果执行结果为空
        if not cmd_res:
            return
        # 采用recv后，阻塞，必须等到客户端响应之后才能执行下面的命令
        client_ack = self.request.recv(1024)

        self.request.send(cmd_res.encode("utf-8"))

    def pwd(self, *args, **kwargs):
        msg_dic = kwargs
        cur_path = msg_dic["cur_path"]
        ret_size = len(cur_path.encode("utf-8"))
        msg_dic["size"] = ret_size
        msg_dic["ret_code"] = 200
        self.request.send(json.dumps(msg_dic).encode("utf-8"))
        self.request.recv(1024)
        self.request.send(cur_path.encode("utf-8"))

    def cd(self, *args, **kwargs):
        msg_dic = kwargs
        parameter = msg_dic["Parameter"].strip()
        userhome = msg_dic["user_home"]
        cur_path = msg_dic["cur_path"]

        if parameter.startswith("/"):
            if not parameter.startswith("/%s" % userhome):
                msg_dic["ret_code"] = 404
                self.request.send(json.dumps(msg_dic).encode("utf-8"))
                return
            else:
                if not os.path.isdir(parameter):
                    msg_dic["ret_code"] = 405
                    self.request.send(json.dumps(msg_dic).encode("utf-8"))
                    return
            msg_dic["ret_code"] = 200
            msg_dic["cur_path"] = parameter
            print("用户切换到%s路径下" % parameter)
            self.request.send(json.dumps(msg_dic).encode("utf-8"))
        else:
            switch_counts = parameter.split("/")
            if switch_counts[-1] == "":
                switch_counts.remove("")

            for swith_choice in switch_counts:
                if swith_choice == ".":
                    pass
                elif swith_choice == "..":
                    if cur_path != userhome:
                        cur_path = cur_path.rstrip("/" + cur_path.split("/")[-1])
                        print("cur_path", cur_path)
                    else:
                        msg_dic["ret_code"] = 404
                        self.request.send(json.dumps(msg_dic).encode("utf-8"))
                        return
                else:
                    cur_path += "/" + swith_choice
                    check_path = settings.DB_ROOT + cur_path
                    if not os.path.isdir(check_path):
                        msg_dic["ret_code"] = 405
                        self.request.send(json.dumps(msg_dic).encode("utf-8"))
                        return
            msg_dic["ret_code"] = 200
            msg_dic["cur_path"] = cur_path

            print("用户切换到%s路径下" % cur_path)
            self.request.send(json.dumps(msg_dic).encode("utf-8"))