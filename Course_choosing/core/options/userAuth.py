# -*- coding:utf-8 -*-
# __author__ = 'gupan'
from conf import settings

class UserAuth(object):
    def __init__(self):
        super(UserAuth, self).__init__()

    @staticmethod
    def is_login(func):
        """
        装饰器：验证用户是否登陆
        :param func:被装饰的函数
        :return：失败返回2
        """
        def derector(*args, **kwargs):
            print("传入字典：", kwargs)
            user_data = kwargs["auth_data"]
            name = kwargs.get("name")
            ACCESS_LOG = kwargs["ACCESS_LOG"]
            if not user_data.get(name):
                return "2"
            if user_data[name][settings.Is_Authenticated]:
                func(*args, **kwargs)
            else:
                ACCESS_LOG.info("该用户还未进行登陆，等先登陆")
                return "2"

        return derector