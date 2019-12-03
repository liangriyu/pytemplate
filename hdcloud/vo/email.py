import datetime

class MailMessage(object):

 def __init__(self):
    #邮件唯一标识（发送方生成）
    self.mailUid=""
    #计划发送时间
    self.planSendTime=datetime.datetime.now()
    #邮件主题
    self.mailSubject=""
    #邮件内容
    self.mailContent=""
    #发送次数
    self.sendNum = 0