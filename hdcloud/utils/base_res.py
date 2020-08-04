class Code:
    SUCCESS=200
    SERVER_ERR=500


class ApiResp(object):
    def __init__(self,code=Code.SUCCESS, msg=None, data=None):
        self.code=code
        self.msg=msg
        self.data=data