import uuid

from hdcloud.base.logging import Logger
from service import context

"""
**********************************************
*****************  主程序  *******************
**********************************************
"""


if __name__ == '__main__':
    try:
        #必写项，上下文开始
        context.start()

        ########## 业务代码 ##########

        Logger.info("test")
        print(str(uuid.uuid1()))
        raise
    except Exception as e:
        Logger.error_and_mail("测试告警邮件")
    finally:
        # 必写项，上下文结束
        context.close()


