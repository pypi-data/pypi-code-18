#coding=utf8
import Queue
import threading
import contextlib
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# _colors = dict(black=30, red=31, green=32, yellow=33,blue=34, magenta=35, cyan=36, white=37)
def print_with_color(c, s):
    print "\x1b[%dm%s\x1b[0m" % (c, s)

class ExcutorMgr(threading.Thread):
    
    def __init__(self,cnt=1,name='',logable=False,timeout=-1):
        threading.Thread.__init__(self) 
        self.thread_stop = False
        self.name = name
        self.timeout = timeout
        self.lastJobTime = -1
        self.q=Queue.Queue()
        self.logable=logable
        if cnt <= 0:
            cnt = 1
            self.thredList = []
            self.thredList.append(Excutor("#0"))
            self.curCnt = 1
        else:
            self.cnt = cnt
            self.curCnt = 0
            self.thredList = []
        self.index=0
        self.setDaemon(True)
        self.start()
    def _print(self,content):
        if self.logable:
            print content
    def run(self):
        while not self.thread_stop:             
            if self.q.qsize()>0:
                self.lastJobTime = -1
                executor = self.getAvalExecutor()
                if executor != None:
                    job = self.q.get()                    
                    executor.execute(job)
                    self._print('%s executing job(%s)'%(executor.name,job.toString()))


            #decide whether to clear son threads
            if self.q.qsize() == 0 and self.curCnt > 0:
                
                isExecuting = False
                for i in range(0,self.curCnt):
                    if self.thredList[i].isExecuting:
                        isExecuting = True
                if not isExecuting:
                    if self.lastJobTime == -1:
                        self.lastJobTime = time.time()                    
                    elif time.time() - self.lastJobTime > 60:
                            for i in range(0,self.curCnt):
                                self.thredList[i].stop()
                            self._print('%s clear exemgr(%s) %d threads'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),self.name,self.curCnt))
                            self.curCnt = 0
                            del self.thredList[:]
            if self.timeout != -1:
                for i in range(0,self.curCnt):
                    if self.thredList[i].startTime != -1 and time.time() - self.thredList[i].startTime > self.timeout:
                        self.thredList[i].stop()
                        self.thredList[i]=Excutor("#%d"%i)
                        self._print('%s restart Executor %d,because of timeout'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),i))

            time.sleep(0.1)

    def getLeftJobsCnt(self):
        return self.q.qsize()

    def wait(self):
        while not self.thread_stop:
            time.sleep(0.1)
            jobclear = False
            executorRunning = False
            if self.q.qsize() == 0:
                jobclear = True
            for i in range(0,self.curCnt):
                if self.thredList[i].isExecuting:
                    executorRunning = True
            if jobclear and not executorRunning:
                break
        self.stop()

    def stop(self):     
        for i in range(0,self.curCnt):
            self.thredList[i].stop()
        self.thread_stop = True 
        self._Thread__stop()

    def getAvalExecutor(self):
        executor = None
        for i in range(0,self.curCnt):
            if not self.thredList[i].isExecuting:
                executor = self.thredList[i]
                # print dir(executor)
                # print 'find one thread execute'
                break
        if executor == None:
            if self.curCnt < self.cnt:
                self.thredList.append(Excutor("#%d"%self.curCnt))
                self.curCnt+=1
                executor = self.thredList[self.curCnt-1]
                # print 'new thread execute'            
        return executor


    def execute(self,job):
        self.q.put(job)
        
    def toString(self):
        ret = 'ExcutorMgr(%s) now has %d Executors & %d jobs'%(self.name,self.curCnt,self.q.qsize())

        for i in range(0,self.curCnt):
            executor = self.thredList[i]
            ret += '\n\t%s'%(executor.toString())
        return ret

class Job(object):
    def __init__(self, func, params,name=''):    
        self.func = func
        self.params = params
        self.name = name
    def call(self):
        try:
            return self.func(self.params)
        except Exception,e:
            # print self.toString(),'exception:',e
            import traceback
            print_with_color(33,"%s exception details:\n %s"%(self.toString(),traceback.format_exc()))
            # print e.message
        return None

    def toString(self):
        return "#job %s"%(self.name)
class Excutor(threading.Thread):
    
    def __init__(self,name=''):
        threading.Thread.__init__(self) 
        self.thread_stop = False
        self.job = None        
        self.name = name
        self.isExecuting = False#for executormgr
        self.isRunning = False#for executor
        self.startTime = -1
        self.setDaemon(True)
        self.start()

    def execute(self,job):
        self.isExecuting = True
        self.job = job

    def run(self): #Overwrite run() method, put what you want the thread do here 
        
        while not self.thread_stop: 
            if not self.isRunning and self.job != None:
                self.isRunning = True
                self.startTime = time.time() 
                res = self.job.call()
                self.startTime = -1
                self.isRunning = False
                self.job = None
                self.isExecuting = False
                

            time.sleep(0.1) 

    def stop(self): 
        self.thread_stop = True 
        self._Thread__stop()

    def toString(self):
        if  self.isRunning :
            return "executor(%s) now running %s "%(self.name,self.job.toString())
        else:
            return "executor(%s) now has no jobs"%(self.name)

class Test():
    lock = threading.Lock()  
    def test2(self,obj):
        t=obj["time"]
        res=obj["res"]
        
        # print 'sleep start'
        time.sleep(t)
        # print 'sleep over'
        self.lock.acquire()
        res['total']+=t
        self.lock.release()
    def test3(self,obj):
        a=3/0


    def test(self,):
        startTime = time.time()
        # t = ExcutorMgr(3,"mgr",logable= True,timeout=10)
        t = ExcutorMgr(3,"mgr",logable= True)        
        res = {}
        res['total']=0
        t.execute(Job(self.test2,{'time':2,'res':res},"job1xx"))
        t.execute(Job(self.test2,{'time':5,'res':res},"job2xx"))
        
        t.execute(Job(self.test2,{'time':5,'res':res},"job3xx"))
        t.execute(Job(self.test2,{'time':5,'res':res},"job4xx"))
        t.execute(Job(self.test2,{'time':5,'res':res},"job5xx"))
        t.execute(Job(self.test2,{'time':2,'res':res},"job6xx"))
        t.execute(Job(self.test2,{'time':2,'res':res},"job7xx"))
        time.sleep(1)
        print t.toString()
        time.sleep(3)

        t.execute(Job(self.test3,{'time':5,'res':res},"job_test_xx"))

        t.execute(Job(self.test2,{'time':5,'res':res},"job9xx"))
        t.execute(Job(self.test2,{'time':5,'res':res},"job10xx"))
        t.execute(Job(self.test2,{'time':2,'res':res},"job11xx"))
        t.execute(Job(self.test2,{'time':2,'res':res},"job12xx"))
        t.execute(Job(self.test2,{'time':2,'res':res},"job13xx"))
        t.execute(Job(self.test2,{'time':2,'res':res},"job14xx"))
        # t.stop() 
        t.wait()
        print 'task done',time.time() - startTime,res["total"]



# Test().test()

# time.sleep(50)