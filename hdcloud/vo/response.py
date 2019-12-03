# -*- coding: utf-8 -*-
# @Time    : 2019/11/9 17:01
# @Author  : liangriyu
from enum import Enum, unique


class Resp:
    def __init__(self):
        self.code = StatusCode.SUCCESE.value
        self.message = ""



@unique
class StatusCode(Enum):
    SUCCESE = 0
    FAILED = 1