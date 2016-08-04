#coding:utf-8
import threading
import time
import random
from pb_fun import syn
__author__ = 'zhoushengqiang'

class threadManager(object):
    def __init__(self, threadnum):
        self.threadNum = threadnum
        #线程池
        self.threadPool=[]

    def initThread(self):
        for i in range(self.threadNum):
            self.threadPool.append(workThread())

class workThread(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self, name='workThread')
        super(workThread, self).__init__(name='workThread')

    def run(self):
        s=syn()
        s.syn_contact()

if __name__ == '__main__':
    t = threadManager(800)
    t.initThread()

    for p in t.threadPool:
        p.start()
    for q in t.threadPool:
        q.join()




