import hashlib
import json

import datetime


def get_md5(content):
  # 因为python3运行内存中编码方式为unicode，所以将urlmd5压缩之前首先需要编码为utf8。
	if isinstance(content, str):
	   	content = content.encode("utf-8")
	m = hashlib.md5()
	m.update(content)
	return m.hexdigest()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

