# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu
import json
import logging
import os
import time
import uuid

from kafka import KafkaProducer

from hdcloud.base.config import Configs
from hdcloud.utils import baseutil
from hdcloud.vo.email import MailMessage


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
        self.fileHandler = None
        self.reset_parent_prefix(level,prefix,parent)
        if Configs.get("email.alarm") == "true":
            try:
                self.producer = KafkaProducer(bootstrap_servers=Configs.get("email.kafka_servers"))
            except Exception as e:
                self.warning(str(e))

    def set_file_handler(self):
        if len(self.prefix)>0:
            logfilename = '%s_%s.log' % (self.prefix,self.timestamp)
        else:
            logfilename = '%s.log' % self.timestamp
        logfilepath = os.path.join(self.logs_dir, logfilename)
        if self.fileHandler:
            self.logger.removeHandler(self.fileHandler)
        fileHandler = logging.FileHandler(logfilepath, encoding='utf-8')
        # 设置输出格式
        fileHandler.setFormatter(self.formatter)
        fileHandler.setLevel(self.level_relations[self.level])
        self.fileHandler = fileHandler
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
            self.timestamp = cur_date
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

    def error_and_mail(self, message):
        self.error(message)
        self._mailHandle(message)

    def _mailHandle(self, message):
        try:
            if Configs.get("email.alarm") == "true":
                vo = MailMessage()
                vo.mailUid = str(uuid.uuid1())
                vo.confCode = Configs.get("email.code")
                vo.mailContent = str(message)
                vo.mailSubject = Configs.get("email.subject")
                msg = json.dumps(vo.__dict__,cls=baseutil.DateEncoder,ensure_ascii=False)
                future = self.producer.send(Configs.get("email.kafka_topic"), value=msg.encode())
                result = future.get(timeout=60)
                Logger.info(result)
        except Exception as e:
            self.logger.warning(e)

Configs.register()
Logger=_Logger(Configs.get("logger.level"),Configs.get("logger.prefix"),Configs.get("logger.parent"))
