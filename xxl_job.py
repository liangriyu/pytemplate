import traceback

from gevent.pywsgi import WSGIServer
from flask import Flask

from hdcloud.base.logging import Logger
from web_model import rpc_data
from service import context

# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

"""
**********************************************
*****************  主程序  *******************
**********************************************
"""

app = Flask(__name__)


if __name__ == '__main__':
    try:
        # 必写项，上下文开始
        context.start()
        app.register_blueprint(rpc_data, url_prefix='/weather-clean')
        http_server = WSGIServer(('0.0.0.0', 8001), app)
        http_server.serve_forever()
    except:
        Logger.error("数据处理接口服务："+traceback.format_exc())
    finally:
        context.close()