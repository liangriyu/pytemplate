# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

import logging
import os
import time

from hdcloud.base.config import Configs


class _Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    timestamp = time.strftime("%Y-%m-%d", time.localtime())
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

    def __init__(self,level='info', prefix='', parent= ''):
        self.logger = logging.getLogger(__name__)
        self.level = level
        self.prefix = prefix
        self.parent = parent
        self.reset_parent_prefix(level,prefix,parent)

    def set_file_handler(self):
        if len(self.prefix)>0:
            logfilename = '%s_%s.log' % (self.prefix,self.timestamp)
        else:
            logfilename = '%s.log' % self.timestamp
        logfilepath = os.path.join(self.logs_dir, logfilename)
        fileHandler = logging.FileHandler(logfilepath, encoding='utf-8')
        # 设置输出格式
        fileHandler.setFormatter(self.formatter)
        fileHandler.setLevel(self.level_relations[self.level])
        self.logger.addHandler(fileHandler)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(self.level_relations[self.level])
        console.setFormatter(self.formatter)
        self.logger.addHandler(console)
        self.logger.setLevel(self.level_relations[self.level])

    def reset_parent_prefix(self,level=None, prefix='', parent= ''):
        if level:
            self.level = level
        self.prefix = prefix
        self.parent = parent
        # 创建文件目录
        self.logs_dir = os.path.abspath(os.path.dirname(__file__))[:-12] + "logs"
        if len(self.parent)>0:
            self.logs_dir = self.logs_dir + "/" + self.parent
        if os.path.exists(self.logs_dir) and os.path.isdir(self.logs_dir):
            pass
        else:
            os.mkdir(self.logs_dir)
        self.set_file_handler()

    def check_date(self):
        cur_date = time.strftime("%Y-%m-%d", time.localtime())
        if cur_date != self.timestamp:
            self.set_file_handler()


    def info(self, message):
        self.check_date()
        self.logger.info(message)

    def debug(self, message):
        self.check_date()
        self.logger.debug(message)

    def warning(self, message):
        self.check_date()
        self.logger.warning(message)

    def error(self, message):
        self.check_date()
        self.logger.error(message)

Configs.register()
Logger=_Logger(Configs.get("logger.level"),Configs.get("logger.prefix"),Configs.get("logger.parent"))
