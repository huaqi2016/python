#coding=utf-8
import threading
import Queue
import time
import random
__author__ = 'zhoushengqiang'

class TaskManager(object):
    def __init__(self,maxTasks, maxThreads):
        #最大任务数，也就是Queue的容量
        self._maxTasks = maxTasks
        #线程池中线程数量
        self._maxThreads = maxThreads
        #任务池
        self._taskQueue = Queue.Queue(maxTasks)
        #线程池，使用列表实现
        self._threads = []

    #初始化任务池
    def initTaskQueue(self):
        while True:
            #业务代码
            if not self._taskQueue.full():
                rd=random.randint(1,100)
                print "random %d"%rd
                self._taskQueue.put(rd)
                print "aaa %d"%(self._taskQueue.qsize())
            time.sleep(1)
            print "xxx"

    #初始化线程池
    def initThreads(self):
        for i in range(self._maxThreads):
            #调用每个线程执行的具体任务
            self._threads.append(Work(self._taskQueue))
            print 'thread %d'%i

#具体执行的任务
class Work(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self, name='work')
        self._task = task

    def run(self):
        while True:
            try:
                #业务代码
                print threading.currentThread().ident
                print "bbb %s" %(self.getName())
                print "ccc %d %d" %(self._task.qsize(), self._task.get())
                time.sleep(2)
            except Exception,e:
                print e

if __name__ == '__main__':
    t=TaskManager(10, 2)
    t.initThreads()
    for p in t._threads:
        p.start()
    t.initTaskQueue()
    for q in t._threads:
        q.join()