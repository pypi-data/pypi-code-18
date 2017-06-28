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

class STFBuildModuleError(BaseException):
    """If error, raise it."""
    pass

class STFBuildModule(STFBaseModule):
    """
    the build module of STF
    """
    def __init__(self, pluginManager):
        """
        constructor
        """
        super(STFBuildModule, self).__init__(pluginManager)
        self.username=""
        self.password=""
        self.server=""
        self.pluginManager = pluginManager
        self.variablePlugin = pluginManager.getInstance("variable")

    def checkMode(self, mode):
        """check mode, now only support the mode in ACCEPT_MODE"""
        if mode:
            logger.error("build module do not support %s mode", mode)
            raise STFBuildModuleError("build module do not support %s mode", mode)

    def checkModeParameter(self, parameter):
        """check mode parameter"""
        if parameter:
            logger.error("parameter should be empty", parameter)
            raise STFBuildModuleError("parameter should be empty", parameter)

    def checkModuleParameter(self, module, jumphost_info, lab_info):
        """check module parameter"""
        if module.lower() != "build":
            logger.error("this is build module, not %s", module)
            raise STFBuildModuleError("this is build module, not %s", module)

    def checkCaseIDs(self, cases):
        """check case id"""
        pass

    def checkTags(self, tags):
        """ check tags """
        pass

    def checkOthers(self, filePath):
        """ check build server is accessable """
        logger.info("check build server is accessable")
        self.username = self.variablePlugin.get("user","Build:USER")
        self.password = self.variablePlugin.get("password","Build:USER")
        self.server = self.variablePlugin.get("BUILD_SERVER","Build")
        try:
            self.sshManager.getClient(self.server, user=self.username, pw=self.password)
        except BaseException, msg:
            errorMsg = "cannot access to %s as user %s:%s, error msg is %s" % (self.server, self.username, self.password, str(msg))
            logger.error(errorMsg)
            raise STFBuildModuleError(errorMsg)    
    def run(self, caseInfo):
        caseFileLocation = caseInfo.current_step.path
        caseFileName = os.path.basename(caseFileLocation)
        mode = caseInfo.current_step.mode
        parameter = caseInfo.current_step.mode_argv 
        module = caseInfo.current_step.module
        module_argv = caseInfo.current_step.module_argv
        
        buildPluginName = 'base'
        if module_argv:
            buildPluginName = module_argv.split('~')[0]
        buildPluginName = 'build%s' %buildPluginName
        logger.info("buildPluginName is %s",buildPluginName)
        jumphost_info = caseInfo.current_step.jumphost_info
        lab_info = caseInfo.current_step.lab_info
        tags = caseInfo.current_step.step_tags
        
#         casefile = self.appendExtToCaseFile(caseFileLocation)
        logger.info( "casefile is %s", caseFileLocation)
        self.buildPlugin = self.pluginManager.getInstance(buildPluginName)
        self.processStart(caseInfo, 0)
        self.buildPlugin.preCheck()
        rc, stdoutput, erroroutput = self.buildPlugin.run()
        if rc:
            logger.error("build module failure")
        else:
            logger.info("build module success")
        self.processEnd(caseInfo, 0, caseFileName, rc, stdoutput, erroroutput, 0)
        
        
