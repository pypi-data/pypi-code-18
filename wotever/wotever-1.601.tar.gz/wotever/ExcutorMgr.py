#coding=utf8
import Queue
import threading
import contextlib
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ExcutorMgr(threading.Thread):
    def __init__(self,cnt=1,name=''):
        threading.Thread.__init__(self) 
        self.thread_stop = False
        self.name = name
        if cnt <= 0:
            cnt = 1
            self.thredList = []
            self.thredList.append(Excutor("#0"))
            self.curCnt = 1
        else:
            self.cnt = cnt
            self.curCnt = 0
            self.thredList = []

        self.start()
    def run(self):
        while not self.thread_stop: 
            time.sleep(0.1)

    def wait(self):
        while True:
            time.sleep(0.1)
            aliveCnt = 0
            for i in range(0,self.curCnt):
                if self.thredList[i].q.qsize()>0:                
                    aliveCnt += 1
            
            if aliveCnt == 0:
                for i in range(0,self.curCnt):                    
                    self.thredList[i].stop()                
                break                            
        self.thread_stop = True 

    def stop(self):     
        for i in range(0,self.curCnt):
            self.thredList[i].stop()
        self.thread_stop = True 
        

    def execute(self,job):
        executor = None
        for i in range(0,self.curCnt):
            if not self.thredList[i].q.qsize()>0 :
                executor = self.thredList[i]
                # print 'find one thread execute'
                break
        if executor == None:
            if self.curCnt < self.cnt:
                self.thredList.append(Excutor("#%d"%self.curCnt))
                self.curCnt+=1
                executor = self.thredList[self.curCnt-1]
                # print 'new thread execute'
            else:
                executor = self.thredList[0]
                # print 'first thread execute'
        executor.putJob(job)
    def toString(self):
        ret = 'ExcutorMgr(%s) now has %d Executors'%(self.name,self.curCnt)

        for i in range(0,self.curCnt):
            executor = self.thredList[i]
            ret += '\n\t%s'%(executor.toString())
        return ret

class Job(object):
    def __init__(self, func, params):    
        self.func = func
        self.params = params
    def call(self):
        return self.func(self.params)
class Excutor(threading.Thread):

    def __init__(self,name=''):
        threading.Thread.__init__(self) 
        self.thread_stop = False
        self.q = Queue.Queue()
        
        self.name = name
        self.start()
    def putJob(self,job):
        self.q.put(job)

    def run(self): #Overwrite run() method, put what you want the thread do here 
        while not self.thread_stop: 
            
            if self.q.qsize() > 0:
                job = self.q.get()                
                res = job.call()

            time.sleep(0.1) 

    def stop(self): 
        self.thread_stop = True 

    def toString(self):
        return "executor(%s) now running %d jobs"%(self.name,self.q.qsize())


def test2(t):
    print 'sleep start'
    time.sleep(t)
    print 'sleep over'

def test():
    t = ExcutorMgr(2,"mgr")
    t.toString()
    t.execute(Job(test2,2))
    t.execute(Job(test2,2))
    t.execute(Job(test2,2))
    t.execute(Job(test2,2))
    t.execute(Job(test2,2))
    t.execute(Job(test2,2))
    t.execute(Job(test2,2))
    time.sleep(0.1)
    t.stop() #t.wait()

    print 'task done'
