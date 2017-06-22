'''
Created on Mar 31, 2017
'''
import os
from stf.lib.logging.logger import Logger
from stf.modules.base_module import STFBaseModule
from stf.managers.plugin_manager import PluginManager
from stf.plugins.variable_plugin import STFVariablePlugin
from iniparse.ini import lower

logger = Logger.getLogger(__name__)

class STFDeployModuleError(BaseException):
    """If error, raise it."""
    pass

class STFDeployModule(STFBaseModule):
    """
    the build module of STF
    """
    def __init__(self, pluginManager):
        """
        constructor
        """
        super(STFDeployModule, self).__init__(pluginManager)
        self.pluginManager = pluginManager
        self.variablePlugin = pluginManager.getInstance("variable")
        #self.deployPlugin = pluginManager.getInstance("deployopenstackmcas")
        

    def checkMode(self, mode):
        """check mode, now only support the mode in ACCEPT_MODE"""
        pass

    def checkModeParameter(self, parameter):
        """check mode parameter"""
        pass

    def checkModuleParameter(self, module, jumphost_info, lab_info):
        """check module parameter"""
        pass

    def checkCaseIDs(self, cases):
        """check case id"""
        pass

    def checkTags(self, tags):
        """ check tags """
        pass

    def checkOthers(self, filePath):
        """ check build server is accessable """
        pass
        # buildFileSize = os.path.getsize("buildFile")
        # if buildFileSize == 0 :
        #    errorMsg = "build configuration not exist"
        #   logger.error(errorMsg)
        #   raise STFDeployModuleError(errorMsg)
    def run(self, caseInfo):
        """
        set user build configuration env
        """
        openstack=self.plugins.getInstance("deployopenstackmcas")
        operation = caseInfo.current_step.mode
        index = caseInfo.current_step.mode_argv
        if openstack.preCheck :
            return openstack.run(operation,index)
        #rc, output = self.runScriptOnRemote(self.server, scriptPath, "/u/"+ self.username ,account=self.username)
        #logger.info("run build script %s on %s return code is %s, output is %s", scriptPath, self.server, rc, output)

        
