# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

import logging
import os
import time

class _Logger(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # 创建文件目录
        logs_dir = os.path.abspath(os.path.dirname(__file__))[:-4]+"logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.log' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        fileHandler = logging.FileHandler(logfilepath)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(logging.ERROR)
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

Logger=_Logger()