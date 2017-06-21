import sys
from stf.modules.base_module import STFBaseModule


class STFCopyModule(STFBaseModule):
    def __init__(self, plugins):
        pass

    def run(self, case):
        print("I AM running copy")
        print(vars(case))

    def preCheck(self, case):
        print('I AM doing precheck: %s' % vars(case))
