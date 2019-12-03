# -*- coding: utf-8 -*-
# @Time    : 2019/8/18 20:57
# @Author  : liangriyu

from hdcloud.base.config import Configs
from hdcloud.dbutil.mysql import PymysqlPool

MysqlPool=PymysqlPool(host=Configs.get("datasource.mysql.host"),
                      port=Configs.get("datasource.mysql.port"),
                      user=Configs.get("datasource.mysql.user"),
                      passwd=Configs.get("datasource.mysql.passwd"),
                      db=Configs.get("datasource.mysql.db"),
                      charset=Configs.get("datasource.mysql.charset"))


def close():
    """关闭所有数据源"""
    MysqlPool.close()
