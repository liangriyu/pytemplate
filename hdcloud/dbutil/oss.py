
import oss2



class PyOSS2(object):
    """
    aliyun OSS对象存储操作
    """

    def __init__(self,key_id,key_secret,end_point,bucket_name):
        self._auth = oss2.Auth(key_id, key_secret)
        self.bucket = oss2.Bucket(self._auth, end_point, bucket_name)

    def upload(self,file_name, data, headers=None, callback=None):
        """
        简单上传文件
        :param file_name:上传到OSS的文件名
        :param data: 待上传的内容。 bytes，str或file-like object
        :param headers: 用户指定的HTTP头部。可以指定Content-Type、Content-MD5、x-oss-meta-开头的头部等
        :param callback: 用户指定的进度回调函数。可以用来实现进度条等功能。参考 :ref:`progress_callback` 。
        :return:
        """
        return self.bucket.put_object(key=file_name, data=data, headers=headers,progress_callback=callback)

    def download(self, key, byte_range=None,headers=None,progress_callback=None,process=None,params=None):
        """下载一个文件。

        用法 ::

            >>> result = bucket.get_object('readme.txt')
            >>> print(result.read())
            'hello world'

        :param key: 文件名
        :param byte_range: 指定下载范围。参见 :ref:`byte_range`

        :param headers: HTTP头部
        :type headers: 可以是dict，建议是oss2.CaseInsensitiveDict

        :param progress_callback: 用户指定的进度回调函数。参考 :ref:`progress_callback`

        :param process: oss文件处理，如图像服务等。指定后process，返回的内容为处理后的文件。

        :param params: http 请求的查询字符串参数
        :type params: dict

        :return: file-like object

        :raises: 如果文件不存在，则抛出 :class:`NoSuchKey <oss2.exceptions.NoSuchKey>` ；还可能抛出其他异常
        """
        return self.bucket.get_object(key,
                   byte_range=byte_range,
                   headers=headers,
                   progress_callback=progress_callback,
                   process=process,
                   params=params)

    def object_exists(self, key):
        return self.bucket.object_exists(key)


