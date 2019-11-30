# -*- coding: utf-8 -*-
# @Time    : 2019/8/17 17:01
# @Author  : liangriyu

class ThreadPool(object):
    """
    构建线程池
    """
    def __init__(self,size):
        """
        :param size: 线程池大小
        """
        self.pool = []
        self.size = size

    def executor(self,thread_instance):
        """
        线程池启动器
        :return:
        """
        for i in range(self.size):
            self.pool.append(thread_instance)

    def join(self):
        """
        等待线程结束
        :return:
        """
        for thd in self.pool:
            if thd.isAlive():
                thd.join()