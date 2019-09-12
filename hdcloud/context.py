from hdcloud import datasource
from hdcloud.base.config import Configs


def start():
    #--脚本传参
    Configs.register()


def close():
    datasource.close()