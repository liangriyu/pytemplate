from hdcloud.base.logging import Logger
from service import context

"""
**********************************************
*****************  主程序  *******************
**********************************************
"""


if __name__ == '__main__':
    #必写项，上下文开始
    context.start()

    ########## 业务代码 ##########

    Logger.info("test")

    # 必写项，上下文结束
    context.close()


