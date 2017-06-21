from stf.plugins.base_plugin import STFBasePlugin
import sys
import pprint
import time
import datetime
import os
import signal
import copy
from stf.lib.logging.logger import Logger
from os import path
import collections

logger = Logger.getLogger(__name__)


CONST_STATUS = ['no', 'started', 'running', 'end']
class SuiteInfo(object):
    def __init__(self, path):
        self.path = path
        self.testInfo = []
        self.elapsed_time = "not evaluated"

class TestInfo(object):
    def __init__(self):
        self.tms_id_list = None
        self.starttime = None
        self.endtime = None
        #exitcode could be 0(success) or 1(failed)
        self.exitcode = 0
        self.status = 'no'
        self.fatal_error = None
        #key is step Id, value is StepInfo Instance
        self.stepInfo = collections.OrderedDict()

class StepInfo(object):
    def __init__(self):
        self.starttime = None
        self.endtime = None
        #exitcode could be 0(success) or 1(failed)
        self.exitcode = 0
        self.status = 'no'
        self.fatal_error = None
        #key is the processIndex, eg: 0 1 2 3 4 5 6 7 8, value is ProcessInfo Instance
        self.processInfo = collections.OrderedDict()

class ProcessInfo(object):
    def __init__(self):
        #the short description of the process
        self.processDesc = ""
        self.starttime = None
        self.endtime = None
        self.exitcode = 0
        self.status = 'no'
        self.fatal_error = None
        self.stdout = None
        self.stderr = None
        self.pid = None
        self.timeout = 0

def assertIsAttr(field, ins):
    """
    assert field is the attribute of the instance
    """
    if not hasattr(ins, field):
        logger.error("field %s not existed in %s", field, ins)
        raise Exception("field %s not existed in %s", field, ins)

def assertKeyExsit(key, dictIns):
    """
    assert key is existed in the dict instance
    """
    if key not in dictIns.keys():
        logger.error("Key %s not existed in %s", key, dictIns)
        raise Exception("Key %s not existed in %s", key, dictIns)

class STFProcessPlugin(STFBasePlugin):
    def __init__(self, plugins):
        super(STFProcessPlugin, self).__init__(plugins)
        #key is (test_id), value is TestInfo
        self.testInfo = collections.OrderedDict()
        self.suite_info = collections.OrderedDict()

    
    def _getIns(self, key):
        """
        get the instance according the give key
        :param List key: for TestInfo, key is [test_id], 
                          for StepInfo, key is [test_id, step_id]
                          for ProcessInfo, key is [test_id, step_id, process_id]
        :return instance: TestInfo or StepInfo or ProcessInfo instance
        """
        if isinstance(key, basestring):
            key = [key]

        if len(key) == 1:
            assertKeyExsit(key[0], self.testInfo)
            return self.testInfo[key[0]]

        if len(key) == 2:
            test_id = key[0]
            step_id = key[1]
            assertKeyExsit(test_id, self.testInfo)
            testInfoIns = self.testInfo[test_id]
            assertKeyExsit(step_id, testInfoIns.stepInfo)
            return testInfoIns.stepInfo[step_id]

        if len(key) == 3:
            test_id = key[0]
            step_id = key[1]
            process_id = key[2]
            assertKeyExsit(test_id, self.testInfo)
            testInfoIns = self.testInfo[test_id]
            assertKeyExsit(step_id, testInfoIns.stepInfo)
            stepInfo = testInfoIns.stepInfo[step_id]
            assertKeyExsit(process_id, stepInfo.processInfo)
            return stepInfo.processInfo[process_id]
    
    def _setKv(self, key, field, value):
        """
        set value to self.testInfo
        :param List key: for testInfo, key is [test_id,], for stepInfo, key is [test_id, step_id]
                          for processInfo, key is [test_id, step_id, process_id]
        :param str filed: the name of the filed
        :param N/A value: the value for this filed, type can be any
        """
        ins = self._getIns(key)
        assertIsAttr(field, ins)
        setattr(ins, field, value)

    def addSuiteItem(self, suite_id, test_id=None):
        if suite_id is None:
            return

        if suite_id not in self.suite_info.keys():
            self.suite_info[suite_id] = SuiteInfo(suite_id)

        if test_id is None:
            return

        self.suite_info[suite_id].testInfo.append(test_id)

    #t seconds
    def setSuiteElapsedTime(self, suite_id, t):
        if suite_id is None:
            return

        if suite_id not in self.suite_info.keys():
            raise Exception("Test suite id not found: %s" %suite_id)

        self.suite_info[suite_id].elapsed_time = '%ss' %t

    def addItem(self, test_id, step_id=None, process_id=None):
        """
        
        """
        if test_id not in self.testInfo.keys():
            self.testInfo[test_id] = TestInfo()

        if step_id is not None:
            testInfoIns = self.testInfo[test_id]
            if step_id not in testInfoIns.stepInfo.keys():
                testInfoIns.stepInfo[step_id] = StepInfo()

        if process_id is not None:
            stepInfoIns = testInfoIns.stepInfo[step_id]
            if process_id not in stepInfoIns.processInfo.keys():
                stepInfoIns.processInfo[process_id] = ProcessInfo()

    def getValue(self, key, field):
        """
        get the value of the filed
        :param List key: for testInfo, key is [test_id], for stepInfo, key is [test_id, step_id]
                          for processInfo, key is [test_id, step_id, process_id]
        
        >>> self.getValue([test_id], "tms_id_list")
        >>> self.getValue([test_id, step_id], "starttime")
        >>> self.getValue([test_id, step_id, process_id], "pid")
        """
        ins = self._getIns(key)
        return getattr(ins, field)

    def setStdout(self, test_id, step_id, process_id, out):
        """
        """
        logger.debug("set test %s, step %s, process %s stdout to be %s", test_id, step_id, process_id, out)
        self._setKv([test_id, step_id, process_id], "stdout", out)

    def setStderr(self, test_id, step_id, process_id, err):
        """
        """
        logger.debug("set test %s, step %s, process %s stderr to be %s", test_id, step_id, process_id, err)
        self._setKv((test_id, step_id, process_id), "stderr", err)

    def setPid(self, test_id, step_id, process_id, pid):
        """
        """
        logger.debug("set test %s, step %s, process %s pid to be %s", test_id, step_id, process_id, pid)
        self._setKv((test_id, step_id, process_id), "pid", pid)

    def setTimeout(self, test_id, step_id, process_id, timeout):
        """
        """
        logger.debug("set test %s, step %s, process %s timeout to be %s", test_id, step_id, process_id, timeout)
        self._setKv((test_id, step_id, process_id), "timeout", timeout)

    def setprocessDesc(self, test_id, step_id, process_id, processDesc):
        """
        """
        logger.debug("set test %s, step %s, process %s processDesc to be %s", test_id, step_id, process_id, processDesc)
        self._setKv((test_id, step_id, process_id), "processDesc", processDesc)

    def setTmsId(self, test_id, tms_id_list):
        """
        """
        logger.debug("set test %s, tms_id_list to be %s", test_id, tms_id_list)
        self._setKv((test_id), "tms_id_list", tms_id_list)

    def addTmsId(self, test_id, tms_id_list):
        """
        """
        logger.debug("test %s add tms_id_list to be %s", test_id, tms_id_list)
        self.testInfo[test_id].tms_id_list.extend(tms_id_list)

    def _setKvStack(self, field_name, field_value, test_id, step_id = None, process_id = None):
        if test_id is None:
            raise Exception("test_id is None")

        if process_id is not None and step_id is None:
            raise Exception("process_id is not None while step_id is None")

        self._setKv([test_id], field_name, field_value)

        if step_id is not None:
            self._setKv([test_id, step_id], field_name, field_value)

        if process_id is not None:
            self._setKv([test_id, step_id, process_id], field_name, field_value)

    def setExitcode(self, exitcode, test_id, step_id = None, process_id = None):
        """
        """
        if exitcode < 0 or exitcode > 255:
            raise Exception("exitcode illegal: %d" %(exitcode))

        if exitcode == 0:
            return

        if test_id is None:
            raise Exception("test_id is None")

        if process_id is not None and step_id is None:
            raise Exception("process_id is not None while step_id is None")

        if exitcode != 0:
            self._setKv((test_id), "exitcode", 1)

        if step_id is not None:
            if exitcode != 0:
                self._setKv((test_id, step_id), "exitcode", 1)

        if process_id is not None:
            self._setKv((test_id, step_id, process_id), "exitcode", exitcode)

    def setStatus(self, status, test_id, step_id = None, process_id = None):
        if status not in CONST_STATUS:
            raise Exception('parameter illegal: %s, must be %s' % (status, CONST_STATUS))

        if test_id is None:
            raise Exception("test_id is None")

        if process_id is not None and step_id is None:
            raise Exception("process_id is not None while step_id is None")

        key = [keyIndex for keyIndex in (test_id, step_id, process_id) if keyIndex is not None]
        self._setKv(key, 'status', status) 

    def setFatalError(self, fatal_error, test_id, step_id = None, process_id = None):
        self._setKvStack('fatal_error', fatal_error, test_id, step_id, process_id)

    
    def setProcessStartTime(self, test_id, step_id, process_id):
        self._setKv([test_id, step_id, process_id], 'starttime', int(time.time()))

    def setProcessEndTime(self, test_id, step_id, process_id):
        self._setKv([test_id, step_id, process_id], 'endtime', int(time.time()))
    
    def setStepStartTime(self, test_id, step_id):
        self._setKv((test_id, step_id), 'starttime', int(time.time()))

    def setStepEndTime(self, test_id, step_id):
        self._setKv((test_id, step_id), 'endtime', int(time.time()))

    def setTestStartTime(self, test_id):
        self._setKv(test_id, 'starttime', time.time())

    def setTestEndTime(self, test_id):
        self._setKv(test_id, 'endtime', time.time())

    def _seconds2date(self, sec):
        return datetime.datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')

    def _duration(self, start, end):
        seconds = end - start
        #m, s = divmod(seconds, 60)
        #h, m = divmod(m, 60)
        # 3h 2m 1s
        #return "%d h %02d m %02d s" % (h, m, s)
        return "%.6fs" %seconds

    def getStepStartTime(self, test_id, step_id):
        return self._seconds2date(self.getValue((test_id, step_id), 'starttime'))

    def getStepEndTime(self, test_id, step_id):
        return self._seconds2date(self.getValue((test_id, step_id), 'endtime'))

    def getStepDuration(self, test_id, step_id):
        return self._duration(self.getValue((test_id, step_id), 'starttime'), self.getValue((test_id, step_id), 'endtime'))


    def getTestStartTime(self, test_id):
        return self._seconds2date(self.getValue(test_id, 'starttime'))

    def getTestEndTime(self, test_id):
        return self._seconds2date(self.getValue(test_id,  'endtime'))

    def getTestDuration(self, test_id):
        return self._duration(self.getValue((test_id), 'starttime'),self.getValue((test_id), 'endtime'))

    def setStepStart(self, test_id, step_id):
        self.addItem(test_id, step_id)
        self.setStepStartTime(test_id, step_id)
        self.setStatus('started', test_id, step_id)

    def setTestStart(self, test_id):
        self.addItem(test_id)
        self.setTestStartTime(test_id)
        self.setStatus('started', test_id)
        
    def setStepEnd(self, test_id, step_id):
        self.setStepEndTime(test_id, step_id)
        self.setStatus('end', test_id, step_id)
        
    def setTestEnd(self, test_id):
        self.setTestEndTime(test_id)
        self.setStatus('end', test_id)
        
    def getFailedTestList(self):
        error_list = []
        for k in self.testInfo.keys():
            if self.testInfo[k].exitcode != 0:
                error_list.append(k)

        return error_list

    def isTestFailed(self, test_id):
        if self.testInfo[test_id].exitcode != 0:
            return False
        else:
            return True

    @staticmethod
    def getPidStatus(pid):
        try:
            for line in open("/proc/%d/status" % pid).readlines():
                if line.startswith("State:"):
                    return line.split(":",1)[1].strip().split(' ')[0]
        finally:
            return 'N'

    @staticmethod
    def isPidAlive(pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def getAllProcessInfoIns(self, test_id = None):
        """
        """
        testList = []
        ProcessInfoInsList = []
        if not test_id:
            testList.append(self.testInfo[test_id])
        else:
            testList = self.testInfo.values()

        for testInfoIns in testList:
            stepList = testInfoIns.stepInfo.values()
            if not stepList:
                for stepInfoIns in stepList:
                    ProcessInfoInsList.extend(stepInfoIns.processInfo.values())
        return ProcessInfoInsList
    
    def checkProcessTimeout(self, processInfoIns):
        """
        """
        if processInfoIns.timeout:
            startTime = processInfoIns.starttime
            duration = int(time.time()) - startTime
            if processInfoIns.timeout < duration:
                return True
            else:
                return False
        else:
            return False
            
    def terminate(self, test_id = None, checkTimeout=True):
        processInfoList = self.getAllProcessInfoIns(test_id)
        alive = False
        for processInfoIns in processInfoList:
            if checkTimeout and (not self.checkProcessTimeout(processInfoIns)):
                    continue    
            status = self.getPidStatus(processInfoIns.pid)
            if status != 'N':
                alive = True
                print('%s %d status is %s - %s' %(processInfoIns.processDesc, processInfoIns.pid, status, processInfoIns.status))
                os.kill(self.PprocessInfoIns.pid, signal.SIGTERM)

        if not alive:
            return

        alive = False
        time.sleep(10)
        for processInfoIns in processInfoList:
            if checkTimeout and (not self.checkProcessTimeout(processInfoIns)):
                continue  
            status = self.getPidStatus(processInfoIns.pid)
            if status != 'N':
                alive = True
                print('%s %d status is %s - %s' %(processInfoIns.processDesc, processInfoIns.pid, status, processInfoIns.status))
                os.kill(processInfoIns.pid, signal.SIGKILL)

        if not alive:
            return

        time.sleep(10)
        for processInfoIns in processInfoList:
            if checkTimeout and (not self.checkProcessTimeout(processInfoIns)):
                continue
            status = self.getPidStatus(processInfoIns.pid)
            if status != 'N':
                raise Exception('Cleanup Error: %s %d status is %s - %s' %(processInfoIns.processDesc, processInfoIns.pid, status, processInfoIns.status))

    def getTestStatus(self, test_id, step_id=None, process_id=None):
        """
        display the test status
        """
        testInfoIns = copy.deepcopy(self.testInfo[test_id])
        testInfodict = {}
        if not step_id:
            testInfodict = testInfoIns.__dict__
            testStepInsDict = testInfoIns.stepInfo
            testStepDict = {}
            for key in testStepInsDict:
                value = testStepInsDict[key]
                testStepDict[key] = value.__dict__
                processInsDict = value.processInfo
                processDict = {}
                for pKey in processInsDict:
                    pValue = processInsDict[pKey]
                    processDict[pKey] = pValue.__dict__
                testStepDict[key]["processInfo"] = processDict
                    
            testInfodict["stepInfo"] = testStepDict
            logger.debug("%s: status is \n%s", test_id, pprint.pformat(testInfodict, width=1))
            return testInfodict, pprint.pformat(testInfodict, width=1)  
        if step_id and not process_id:
            testStepIns = testInfoIns.stepInfo[step_id]
            testStepDict = testStepIns.__dict__
            processInsDict = testStepIns.processInfo
            processDict = {}
            for pKey in processInsDict:
                pValue = processInsDict[pKey]
                processDict[pKey] = pValue.__dict__
            testStepDict["processInfo"] = processDict
            logger.debug("%s step %s : status is \n%s", test_id, step_id, pprint.pformat(testStepDict, width=1))
            return testStepDict, pprint.pformat(testStepDict, width=1)
        
        if step_id and process_id:
            processDict = testInfoIns.stepInfo[step_id].processInfo[process_id].__dict__
            logger.debug("%s step %s process %s : status is \n%s",
                        test_id, step_id, process_id, pprint.pformat(processDict, width=1))
            return processDict, pprint.pformat(processDict, width=1)

    def getErrMsg(self, test_id):
        """
        display the test status
        """
        testInfoIns = copy.deepcopy(self.testInfo[test_id])
        testInfodict = {}
        
        testInfodict = testInfoIns.__dict__
        testStepInsDict = testInfoIns.stepInfo
        testStepDict = {}
        for key in testStepInsDict:
            value = testStepInsDict[key]
            testStepDict[key] = value.__dict__
            processInsDict = value.processInfo
            processDict = {}
            for pKey in processInsDict:
                pValue = processInsDict[pKey]
                processDict[pKey] = pValue.__dict__
            testStepDict[key]["processInfo"] = processDict
                    
        testInfodict["stepInfo"] = testStepDict
        logger.debug("%s: status is \n%s", test_id, pprint.pformat(testInfodict, width=1))
        return pprint.pformat(testInfodict, width=1)
        
