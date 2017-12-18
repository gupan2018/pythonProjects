# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import os,sys,time
class Root_path:
    def get_root_path(self):
        return os.path.dirname(os.path.dirname(__file__))

class File:
    def file_copy(self, path_origin, path_target):
        with open(path_origin, "r") as f_target,\
        open(path_target, "w") as f_origin:
            f_target = open(path_target, "w")

            for line in f_origin:
                f_target.write(line)

    def file_modify(self, path_origin, content_origin, content_target):
        print("old:{old},new:{new}".format(old = content_origin, new = content_target))
        Mod_Flag = False
        path_tmp = os.path.splitext(path_origin)[0] + "_tmp"
        with open(path_origin, "r") as f_origin,\
            open(path_tmp, "w") as f_tmp:
            for line in f_origin:
                if content_origin in line:
                    Mod_Flag = True
                f_tmp.write(line)
        sys.stdout.flush()

        with open(path_tmp, "r") as f_tmp,\
            open(path_origin, "w") as f_origin:
            for line in f_tmp:
                #print(line)
                if content_origin in line:
                    line = line.replace(content_origin, content_target)
                    #print(line)
                f_origin.write(line)
        os.remove(path_tmp)
        sys.stdout.flush()
        return Mod_Flag

    def file_add(self, path_origin, **kw_args):
        with open(path_origin, "a") as f_origin:
            f_origin.write("\nbakend {0}\n".format(kw_args["host"]))
            f_origin.write("\tserver {server} weight {weight} maxconn {maxconn}\n".format(
                server = kw_args["server"],
                weight = kw_args["weight"],
                maxconn = kw_args["maxconn"]))

        sys.stdout.flush()


    def file_delete(self, path_origin, key_begin, key_end):
        path_tmp = os.path.splitext(path_origin)[0] + "tmp"
        with open(path_origin, "r") as f_origin,\
            open(path_tmp, "w") as f_tmp:
            for line in f_origin:
                f_tmp.write(line)

        #time.sleep(10)
        D_Flag = False
        R_Flag = False
        sys.stdout.flush()

        with open(path_tmp, "r") as f_tmp,\
            open(path_origin, "w") as f_origin:
            for line in f_tmp:
                if key_begin in line:
                    R_Flag = True
                    D_Flag = True
                    continue

                if not D_Flag:
                    f_origin.write(line)

                if key_end in line and D_Flag:
                    D_Flag = False
                    f_origin.write(line)
        os.remove(path_tmp)
        return R_Flag

    def file_search(self, path_origin, host):
        host_origin = host
        host = "backend " + host + "\n"
        #print(host)
        S_Flag = False
        with open(path_origin, "r") as f_origin:
            for line in f_origin:
                if S_Flag:
                    print("this mas of {host} is '{msg}'".format(host = host_origin, msg = line.lstrip()))
                if "backend" in line and S_Flag:
                    break
                if host in line:
                    S_Flag = True
        return S_Flag

class Time:
    def __init__(self):
        self.format = "%Y-%m-%d %X"

    def format_time(self):
        time_str = time.strftime(self.format)
        return time_str

# print(Time().format_time())