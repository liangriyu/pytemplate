# -*- coding:utf-8 -*-
import json
import traceback
from hdcloud.base.logging import Logger
from hdcloud.vo.response import Resp, StatusCode
from web_model import rpc_data


@rpc_data.route('/task1', methods=['POST'])
def task1():
    res = Resp()
    try:
        res.message="数据处理成功。"
        Logger.info("test...")
    except:
        res.code = StatusCode.FAILED.value
        res.message = "数据处理失败。"
        Logger.error("数据处理 task1:"+traceback.format_exc())
    return json.dumps(res.__dict__,ensure_ascii=False)

