from hdcloud import context
from hdcloud.datasource import MysqlPool

"""
**********************************************
*****************  主程序  *******************
**********************************************
"""


if __name__ == '__main__':
    #必写项，上下文开始
    context.start()

    ########## 业务代码 ##########

    mysql = MysqlPool.getConn()
    rs = mysql.getOne("select * from test")
    print(rs)
    mysql2 = MysqlPool.getConn()
    rs = mysql2.getOne("select * from test")
    print(rs)

    # 必写项，上下文结束
    context.close()


