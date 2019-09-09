# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

import re
import requests
from urllib.parse import quote
import string


def get(url, headers=None, params=None, proxies=None, timeout=None, except_fun=None):
    '''
    GET请求
    :param url:
    :param headers: 请求头
    :param data: 请求参数
    :param proxies: 代理IP
    :param timeout: 超时时间
    :param except_fun: 响应非200时执行回调函数
    :return:
    '''
    url = quote(url, safe=string.printable)
    res = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=timeout)
    return get_response(res, except_fun)

def post(url, headers=None, data=None, proxies=None, timeout=None, except_fun=None):
    '''
    POST请求
    :param url:
    :param headers: 请求头
    :param data: 请求参数
    :param proxies: 代理IP
    :param timeout: 超时时间
    :param except_fun: 响应非200时执行回调函数
    :return:
    '''
    url = quote(url, safe=string.printable)
    res = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=timeout)
    return get_response(res, except_fun)

def get_response(res, except_fun=None):
    """
    获取响应内容
    :param res: 响应response对象
    :return:
    """
    if res.status_code != 200:  # 如果返回不是200
        if except_fun:
            return except_fun
        else:
            raise Exception(res.status_code)
    else:
        content_type = res.headers['Content-Type']
        if 'text/html' in content_type:
            encoding = get_html_encode(content_type, res.text)
            if encoding:
                res.encoding = encoding
            return res.text
        elif 'application/json' in content_type:
            return res.text
        elif 'application/x-www-form-urlencoded' in content_type:
            return res.text
        elif 'application/pdf' in content_type:
            return res.content  # 返回字节
        elif 'image' in content_type:  # 图片
            return res.content  # 返回字节
        else:
            return res.content

def get_html_encode( content_type, page_raw):
    '''
    :param content_type: str, response headers里面的参数 里面一般有编码方式
    :param page_raw: str, html源码信息, 里面的meta里面一般有编码方式
    :return: 返回编码方式
    '''

    encode_list = re.findall(r'charset=([0-9a-zA-Z_-]+)', content_type, re.I)
    if encode_list:
        return encode_list[0]

    encode_list = re.findall(r'<meta.+charset=[\'"]*([0-9a-zA-Z_-]+)', page_raw, re.I)
    if encode_list:
        return encode_list[0]
