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
        self.username = self.variablePlugin.get("USER","Build:MCAS")
        self.password = self.variablePlugin.get("PASSWORD","Build:MCAS")
        self.server = self.variablePlugin.get("SERVER","Build:MCAS")
        try:
            self.sshManager.getClient(self.server, user=self.username, pw=self.password)
        except BaseException, msg:
            errorMsg = "cannot access to %s as user %s:%s, error msg is %s" % (self.server, self.username, self.password, str(msg))
            logger.error(errorMsg)
            raise STFBuildModuleError(errorMsg) 
        buildFile = self.variablePlugin.getBuildFile()
        # buildFileSize = os.path.getsize("buildFile")
        # if buildFileSize == 0 :
        #    errorMsg = "build configuration not exist"
        #   logger.error(errorMsg)
        #   raise STFBuildModuleError(errorMsg)
    def run(self, caseInfo):
        """
        set user build configuration env
        """
        localBuildlFile = self.variablePlugin.getBuildFile()
        logger.info("copy local build configuration profile %s to remote %s",localBuildlFile,self.server)
        rc, remoteBuildFile = self.copyFileToRemote(self.server, localBuildlFile, "/u/" + self.username, self.username)
        if not rc:
            return rc, "copy local build configuration profile %s to remote %S failed" % (localBuildlFile, self.server)
        scriptPath = caseInfo.path 
        scriptName = os.path.basename(scriptPath)
        #scriptPath = caseInfo
        logger.info("the file to run is %s", scriptPath)
        #scriptName = os.path.basename(scriptPath)
        logger.info("copy user's build srcipt to remote %s",scriptName,self.server)
        rc, remoteBuildScript = self.copyFileToRemote(self.server, scriptPath, "/u/" + self.username, self.username)
        if not rc:
            return rc, "copy user's build script %s to remote %S failed" % (scriptName, self.server)
        
        load = self.variablePlugin.get("LOAD","Build:MCAS")
        load_lower = lower(load)
        project = self.variablePlugin.get("PROJECT","Build:MCAS")
        if project == "R40":
            if load_lower == "latest":
                cmd = "Setenv -b "+ project +";"
            else:
                cmd = "Setenv -L "+ load + project + ";"
        elif project == "R50":
            if load_lower == "latest":
                cmd = "GSetenv -b "+ project +";"
            else:
                cmd = "GSetenv -L "+ load + project + ";"  
        else:
            errorMsg = "project %s cannot be identified" %(project)
            logger.error(errorMsg)
            raise STFBuildModuleError(errorMsg)
        cmd = "set -a; source /etc/profile;source /u/" + self.username +"/.profile;"\
                + "chmod +x "+ remoteBuildFile + ";" \
                + "chmod +x "+ remoteBuildScript + ";" \
                + "source " + remoteBuildFile  + ";"\
                + " set +a; rm " + remoteBuildFile + "; source "+ cmd
        os.remove(localBuildlFile)
        mynode= self.variablePlugin.get("MYNODE","Build:MCAS")
        cmd = cmd + "/u/suteam/AUTO/MCAScommon/helper/zapnodeCheck " + mynode + ";"\
               + "zapnode -f "+ mynode + ";" \
               +"mkdir -p /u/" + self.username + "/.MCAStf;"\
               + "export PATH=/u/suteam/AUTO/MCAScommon/helper:$PATH;"
        '''
        add user's build script to command
        '''
        cmd = cmd + "source " + remoteBuildScript
        rc, output = self.sshManager.run(self.server, cmd, user=self.username)
        logger.info("run command %s on %s as %s",cmd,self.server,self.username)
        return rc, output
        #rc, output = self.runScriptOnRemote(self.server, scriptPath, "/u/"+ self.username ,account=self.username)
        #logger.info("run build script %s on %s return code is %s, output is %s", scriptPath, self.server, rc, output)

        
