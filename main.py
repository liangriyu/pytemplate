from gevent.pywsgi import WSGIServer

from service import context
from web_model import rpc_api
from flask import Flask
from geventwebsocket.handler import WebSocketHandler

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
        context.start()    # 必写项，上下文开始
        app.register_blueprint(rpc_api, url_prefix='/data/api')
        http_server = WSGIServer(('0.0.0.0', 9000), app, handler_class=WebSocketHandler)
        http_server.serve_forever()
    finally:
        context.close()
