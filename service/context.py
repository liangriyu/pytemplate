from hdcloud.base.config import Configs
from hdcloud.base.logging import Logger
from service import datasource
# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

def start():
    #--脚本传参
    Configs.register()

def close():
    datasource.close()


def sender(msg):
    pass