from hdcloud.base.config import Configs
from service import datasource


def start():
    #--脚本传参
    Configs.register()


def close():
    datasource.close()