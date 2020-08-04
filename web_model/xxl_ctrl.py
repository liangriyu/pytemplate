# -*- coding:utf-8 -*-
import json
import traceback

from flask import jsonify
from flask import request

from hdcloud.base.logging import Logger
from hdcloud.utils.base_res import ApiResp, Code
from hdcloud.utils.validator import validator
from service import common
from web_model import rpc_api
from web_model.rules import weather_avg_rules


@rpc_api.route('/tmp_prov_day_avg', methods=['POST'])
@validator(rules=weather_avg_rules, strip=True, json=True)
def tmp_prov_day_avg_api():
    """
    :return:
    """
    try:
        args = request.json
        prov_id = args.get("prov_id")
        start_date = args.get("start_date")
        end_date = args.get("end_date")

        return json.dumps(ApiResp(data={"prov_id":prov_id,"start_date":start_date,"end_date":end_date}).__dict__, cls=common.DateEncoder)
    except:
        Logger.error("获取温度数据异常 %s" % (traceback.format_exc()))
        return jsonify(ApiResp(Code.SERVER_ERR, msg="获取温度数据异常").__dict__)

