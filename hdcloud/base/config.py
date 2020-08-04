# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

import yaml
import sys
import os
import threading
from hdcloud.base import excepts


class _Config(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        if not hasattr(self, '_init_falg'):#实现单例
            with self._instance_lock:
                if not hasattr(self, '_init_falg'):
                    self._init_falg = True
                    file_path = os.path.abspath(os.path.dirname(__file__))[:-12] + "config.yaml"
                    self._configs = yaml.load(open(file_path, 'r', encoding='utf-8'), Loader=yaml.Loader)
                    self._get_env(self._configs)
                    self._merge_active_profile()

    def __new__(self, *args, **kwargs):
        if not hasattr(_Config, "_instance"):
            with _Config._instance_lock:
                if not hasattr(_Config, "_instance"):
                    _Config._instance = object.__new__(self)
        return _Config._instance

    def _merge_active_profile(self):
        """
        合并启用额外配置文件字典
        :return:
        """
        active_key="profile.active"
        if self.check_key(active_key) and len(self.get(active_key))>0:
            active = self.get(active_key)
            file_path = os.path.abspath(os.path.dirname(__file__))[:-12] + "config-"+active+".yaml"
            if os.path.exists(file_path):
                configs = yaml.load(open(file_path, 'r', encoding='utf-8'), Loader=yaml.Loader)
                self._get_env(configs)
                tar_dict = self._merge(self._configs, configs)
                self._configs = {**self._configs, **tar_dict}
            else:
                raise Exception("配置文件不存在:"+file_path)

    def _merge(self, src_dict, tar_dict):
        """
        合并字典
        :param src_dict:
        :param tar_dict:
        :return:
        """
        r = {}
        for k, v in tar_dict.items():
            if k in src_dict:
                if isinstance(v, dict):
                    r[k] = self._merge(src_dict[k], v)
                    if isinstance(src_dict[k], dict):
                        r[k]={**src_dict[k],**r[k]}
                else:
                    r[k] = tar_dict[k]
            else:
                r[k] = v
        return r



    def _get_env(self,conf_dict):
        """
        获取环境变量替换默认配置
        :param conf_dict: 配置文件字典
        :return:
        """
        for k, v in conf_dict.items():
            if isinstance(v, dict):
                self._get_env(v)
            else:
                if str(v).startswith("${") and str(v).endswith("}"):
                    tmp_v = str(v)[2:-1]
                    index = tmp_v.find(":")
                    if index != -1:
                        env_key = tmp_v[:index]
                        def_value = tmp_v[index+1:]
                        conf_dict[k] = os.getenv(env_key,def_value)
                    else:
                        conf_dict[k] = os.getenv(tmp_v)


    def get(self, key):
        """
        获取配置字典值
        :param key: 字典key xxx.xxx.xx
        :return:
        """
        keys = str(key).split(".")
        l = len(keys)
        if l == 1:
            return self._configs[key]
        else:
            p = 0
            dic = self._configs[keys[0]]
            for k in keys:
                if p == l - 1:
                    return dic[k]
                if p == 0:
                    dic = self._configs[k]
                else:
                    dic = dic[k]
                p = p + 1
        return dic[key]

    def check_key(self,key):
        """
        判断字典key是否存在
        :param key: xxx.xxx.xx
        :return:
        """
        keys = str(key).split(".")
        if len(keys) == 1:
            return key in self._configs
        else:
            dic = {}
            for i in range(len(keys)):
                if i==0 :
                    dic = self._configs[keys[0]]
                else:
                    ck = keys[i] in dic
                    if ck :
                        dic = dic[keys[i]]
                    else:
                        return False
            return True

    def set(self,key,value):
        """

        :param key:
        :param value:
        :return:
        """
        if not self.check_key(key):
            raise excepts.NotAcceptException("key error: %s" % key)
        keys = str(key).split(".")
        if len(keys) == 1:
            if not isinstance(self._configs[keys[0]], dict):
                self._configs[keys[0]] = value
                print(self._configs)
            else:
                raise excepts.NotAcceptException("not accept to set a dict!")
        else:
            dic = {}
            for i in range(len(keys)):
                if i==0 :
                    dic = self._configs[keys[0]]
                else:
                    if i==len(keys)-1:
                        if not isinstance(dic[keys[i]], dict):
                            dic[keys[i]]=value
                            print(self._configs)
                        else:
                            raise excepts.NotAcceptException("not accept to set a dict!")
                    else:
                        dic = dic[keys[i]]

    def register(self):
        """
        接收脚本传参
        :return:
        """
        args = sys.argv[1:]
        if args:
            for arg in args:
                if str(arg).startswith('-') and args != '-'  and str(arg).find('=')>0:
                    i = arg.index('=')
                    opt, optarg = arg[1:i], arg[i + 1:]
                    if not optarg:
                        raise excepts.NotAcceptException(('option -%s requires argument') % opt)
                    self.set(opt,optarg)

    def print(self):
        print(self._configs)

Configs = _Config()





