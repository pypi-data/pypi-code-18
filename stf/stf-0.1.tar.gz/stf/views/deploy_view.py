import os
import re
from stf.views.base_view import *
from stf.lib.stf_utils import *
from stf.lib.logging.logger import Logger
from stf.lib.SParser import SParser, GRE, SRE
from stf.managers.test_case_manager import TestSuite, TestCase, TestStep


logger = Logger.getLogger(__name__)

class STFDeployView(STFBaseView):
    def __init__(self, plugins):
        super(STFDeployView, self).__init__(plugins)
        self.op_list = ['setup', 'destroy', 'get']
        self.op = ''
        self.index = None
        self.module_name = 'deploy'

    def run(self):
        for case_suite in self.case_suite_list:
            case_suite.run()

        #logger.info('update tms ...')
        #self.report.reportToTms()
        #self.process.generateXmlReport()

    def preCheck(self):
        self._detectJenkins()
        # initialize tms here, _findTests has dependency on this
        #self.report = self.plugins.getInstance('report')
        #self.report.init()
        # initialize process plugin before call _findTests
        self.process = self.plugins.getInstance('process')
        self._findTests()

        for case_suite in self.case_suite_list:
            case_suite.preCheck()

    def initOp(self, op, index):
        if op not in self.op_list:
            raise Exception('Deploy operation not supported: %s' % op)
        self.op = op
        self.index = index

    def addCaseSource(self, case_dir):
        pass

    #
    def _findTests(self):
        self.prepareCaseSourceList()
        #pass view to TestSuite and TestCase
        TestSuite.setView(self)
        TestCase.setView(self)
        test_suite = TestSuite(self.module_name)

        # only setup and teardown cases have no and must have no tms ids
        self.global_test_id += 1

        test_ins = TestCase(path=None, name=None, tags=None)
        test_ins.module = self.module_name

        step_ins = TestStep(path=None, name=None, mode=self.op, mode_argv=self.index, module=self.module_name, step_tags=None, sid=None)
        test_ins.step_list.append(step_ins)

        test_suite.addCase(test_ins)

        self.case_suite_list.append(test_suite)

    #always return false, means delpoy view won't affected by any filter
    def _omitByTagFilter(self, tags):
        return False



