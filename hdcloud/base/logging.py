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

    def __init__(self,level='info', prefix='', parent= ''):
        self.logger = logging.getLogger(__name__)
        # 创建文件目录
        logs_dir = os.path.abspath(os.path.dirname(__file__))[:-12]+"logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        if len(parent)>0:
            logfilename = '%s/%s_%s.log' % (parent, prefix, timestamp)
        else:
            if len(parent)>0:
                logfilename = '%s_%s.log' % (prefix,timestamp)
            else:
                logfilename = '%s.log' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        fileHandler = logging.FileHandler(logfilepath, encoding='utf-8')
        # 设置输出格式
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(self.level_relations[level])
        # 添加内容到日志句柄中
        self.logger.addHandler(fileHandler)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

Configs.register()
Logger=_Logger(Configs.get("logger.level"),Configs.get("logger.prefix"),Configs.get("logger.parent"))