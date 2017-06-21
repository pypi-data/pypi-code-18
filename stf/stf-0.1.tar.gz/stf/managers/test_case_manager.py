import os
import time
from stf.lib.SParser import SParser, SParserError
from stf.lib.logging.logger import Logger

logger = Logger.getLogger(__name__)

class TestSuite(object):
    view = None
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)
        self.current_case = None
        self.case_list = []
        self.has_failed = False
        self.has_run = False
        self.setup = None
        self.teardown = None

    @staticmethod
    def setView(view):
        TestSuite.view = view

    def addCase(self, case):
        self.case_list.append(case)

    def caseNumbers(self):
        return len(self.case_list)

    def preCheck(self):
        logger.debug('test info is: %s', self.__dict__)

        if self.caseNumbers() < 1:
            logger.warning('No test cases found in current test suite: %s', self.path)
            return

        logger.debug('PRECHECK Test Suite %s ...' % self.path)
        for case in self.case_list:
            self.current_case = case
            self.current_case.preCheck()

    def run(self):
        if self.has_run:
            return

        self.has_run = True

        if len(self.case_list) < 1:
            logger.warning('No test cases found in current test suite: %s', self.path )
            return

        try:
            start_time = time.time()
            TestSuite.view.process.addSuiteItem(self.path)
            if self.setup:
                self.current_case = self.setup
                self.current_case.run()
                TestSuite.view.process.addSuiteItem(self.path, self.current_case.id)

            for case in self.case_list:
                self.current_case = case
                self.current_case.run()
                TestSuite.view.process.addSuiteItem(self.path, self.current_case.id)

            if self.teardown:
                self.current_case = self.teardown
                self.teardown.run()
                TestSuite.view.process.addSuiteItem(self.path, self.current_case.id)

            end_time = time.time()
            TestSuite.view.process.setSuiteElapsedTime(self.path, "{0:.6f}".format(end_time - start_time))

        except BaseException, e:
            self.has_failed = True
            raise Exception(str(e))

class TestCase(object):
    view = None
    def __init__(self, path, name, tags, tms_ids=None, tid=None):
        self.path = path
        self.name = name
        self.id = tid
        self.test_tags = tags
        self.tms_ids = tms_ids
        self.step_list = []
        self.current_step = None

        self.has_run = False
        self.has_precheck = False
        self.has_failed = False

    @staticmethod
    def setView(view):
        TestCase.view = view

    def addStep(self, step):
        self.step_list.append(step)

    def preCheck(self):
        logger.debug('test info is: %s', self.__dict__)
        if self.has_precheck:
            return

        self.has_precheck = True

        if len(self.step_list) < 1:
            logger.warning('No step found in current case: %s', self.path )
            return

        for step in self.step_list:
            self.current_step = step
            m = TestCase.view.modules.getInstance(self.current_step.module)
            if m is None:
                raise SParserError('Module %s not found.', self.current_step.module)

            logger.debug('PRECHECK %s ...' % self.current_step.path)
            try:
                m.preCheck(self)
            except Exception,e:
                self.has_failed = True
                raise SParserError(str(e))
            

    def run(self):
        if self.has_run:
            return

        self.has_run = True

        if len(self.step_list) < 1:
            logger.warning('No step found in current case: %s', self.path )
            return

        TestCase.view.variables.refreshCaseEnv()
        TestCase.view.process.setTestStart(self.id)
        for step in self.step_list:
            self.current_step = step
            m = TestCase.view.modules.getInstance(self.current_step.module)
            if m is None:
                raise SParserError('Module %s not found.' % self.current_step.module)

            logger.debug('RUN %s ...' % self.current_step.path)
            TestCase.view.process.setStepStart(self.id, self.current_step.id)
            try:
                d = m.run(self)
            except BaseException,e:
                logger.error(str(e))
                self.has_failed = True
                break

            TestCase.view.process.terminate(self.id)
            TestCase.view.process.setStepEnd(self.id, self.current_step.id)
            # Begin to update report and variable plugin
            step_ins = TestCase.view.process._getIns([self.id, self.current_step.id])
            for i in step_ins.processInfo:
                process_ins = step_ins.processInfo[i]
                TestCase.view.variables.parseStdout(process_ins.stdout, TestCase.view.report)
            # End the update

        TestCase.view.process.setTestEnd(self.id)
        # Begin to update report plugin
        case_ins = TestCase.view.process._getIns(self.id)
        if case_ins.exitcode == 0:
            TestCase.view.report.setCaseListPass(self.tms_ids)
        else:
            TestCase.view.report.setCaseListFail(self.tms_ids)
        # End the update

        
class TestStep(object):
    def __init__(self, path, name, mode, mode_argv, module, step_tags, sid):
        self.path = path
        self.name = name
        self.id = sid
        self.mode = mode
        self.mode_argv = mode_argv
        self.module, self.jumphost_info, self.lab_info = SParser.parseModule(module)
        self.step_tags = step_tags
