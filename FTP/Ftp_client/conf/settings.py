# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import logging
import os


LOG_LEVEL = logging.INFO
BASE_DIR = BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_TYPES = {
    # 'transaction': 'transactions.logs',
    'access': 'access.logs',
}

res_msg = {
    200:"命令执行成功",
    400:"ls出错，该目录不存在",
    401:"用户注册失败",
    402:"用户登陆失败",
    403:"查询用户当前路径失败",
    404:"用户没有权限访问该路径",
    405:"该路径不存在",
    406:"文件传输损坏",
    407:"没有正在上传中的文件",
    408:"客户端输入异常",
    409:"客户端放弃继续下载",
    500:"服务器内部错误"
}