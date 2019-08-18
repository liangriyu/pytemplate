from hdcloud.base.config import Configs, Configs2
from hdcloud.base.logging import Logger
from hdcloud.datasource import MysqlPool
from hdcloud.dbutil.mysql import Pymysql

"""
**********************************************
*****************  主程序  *******************
**********************************************
"""

if __name__ == '__main__':
    Logger.info("测试")
    #################--脚本传参--###############
    Configs.register()
    #################--脚本传参--###############
    Configs2.set("datasource.mysql.port",4664)
    rs = Configs.get("datasource.mysql.port")
    print(rs)
    # mysql = Pymysql(MysqlPool)
    # rs = mysql.getOne("select * from city")
    # print(rs)


