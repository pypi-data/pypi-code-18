'''
Created on Mar 31, 2017

@author: Zhao Xia
'''
import os
import random, string
from abc import abstractmethod
from stf.lib.SParser import SParser
from stf.lib.logging.logger import Logger
from stf.lib.ssh.ssh_manager import SshManager

logger = Logger.getLogger(__name__)

def generateRandomString(N):
    """
    generate a random sring, length is N
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

class STFBaseModuleError(BaseException):
    """If error, raise it."""
    pass

class STFBaseModule(object):
    """
    the base module of the 
    """
    def __init__(self, pluginManager):
        """
        constructor
        """
        sshGateway = os.getenv("SSH_GATEWAY")
        sshUser = os.getenv("SSH_GATEWAY_USER")
        sshPassword = os.getenv("SSH_GATEWAY_PASSWORD")
        self.sshManager = SshManager(sshGateway, sshUser, sshPassword)
        self.pluginManager = pluginManager
        self.variablePlugin = pluginManager.getInstance("variable")
        self.processPlugin = pluginManager.getInstance("process")
        
    @abstractmethod
    def checkMode(self, mode):
        """check mode"""

    @abstractmethod
    def checkModeParameter(self, parameter):
        """check mode parameter"""

    @abstractmethod
    def checkModuleParameter(self, module, jumphost_info, lab_info):
        """check module parameter"""

    @abstractmethod
    def checkCaseIDs(self, cases):
        """check case id"""

    @abstractmethod
    def checkTags(self, tags):
        """ check tags """

    @abstractmethod
    def checkOthers(self, filePath):
        """ check others """


    def checkFileExistAndNotEmpty(self, filePath):
        """
        """
        if os.path.exists(filePath):
            if not os.path.getsize(filePath):
                errorMsg = "file %s is empty" %(filePath)
                logger.error(errorMsg)
                raise STFBaseModuleError(errorMsg) 
        else:
            errorMsg = "file %s is not exist" %(filePath)
            logger.error(errorMsg)
            raise STFBaseModuleError(errorMsg)

    def preCheck(self, caseInfo):
        """
        :param string filePath: the full path of the file
        """
        mode = caseInfo.current_step.mode
        parameter = caseInfo.current_step.mode_argv 
        module = caseInfo.current_step.module
        jumphost_info = caseInfo.current_step.jumphost_info
        lab_info = caseInfo.current_step.lab_info
        tags = caseInfo.current_step.step_tags
        cases = caseInfo.tms_ids
        filePath = caseInfo.current_step.path
        
        logger.debug("filename is %s, mode is %s, parameter is %s, module is %s, tags is %s, cases is %s", filePath, mode, parameter, module, tags, cases)
        self.checkFileExistAndNotEmpty(filePath)
        if mode:
            self.checkMode(mode)
        if parameter:
            self.checkModeParameter(parameter)
        if module:
            self.checkModuleParameter(module, jumphost_info, lab_info)
        if tags:
            self.checkTags(tags)
        if cases:
            self.checkCaseIDs(cases)
        self.checkOthers(filePath)

    def run(self, caseInfo):
        """
        :param string scriptPath: the full path of the script file
        """
        raise NotImplementedError("You can't use parent class STFBaseModule. Use only subclass")

    def processStart(self, caseInfo, process_id, timeout=0):
        """
        before run, update process_plugin
        1) add item for processInfo and stepInfo
        2) set starttime
        2) set status to be 'no'
        """
        self.processPlugin.addItem(caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setStatus('no', caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setProcessStartTime(caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setFatalError(True, caseInfo.id, caseInfo.current_step.id, process_id)
        if timeout:
            self.processPlugin.setTimeout(caseInfo.id, caseInfo.current_step.id, process_id, timeout)
    
    def processRunning(self, caseInfo, process_id, pid):
        """
        this is use for async mode, after the process is running, update the process info
        1) set status to be 'running'
        2) set pid 
        """
        self.processPlugin.setStatus('running', caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setFatalError(False, caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setPid(caseInfo.id, caseInfo.current_step.id, process_id, pid)
   
    def processEnd(self, caseInfo, process_id, processDesc, exitcode, stdout, stderr, pid):
        """
        After run, when process end, update the process info
        
        """
        self.processPlugin.setStdout(caseInfo.id, caseInfo.current_step.id, process_id, stdout)
        self.processPlugin.setStderr(caseInfo.id, caseInfo.current_step.id, process_id, stderr)
        self.processPlugin.setPid(caseInfo.id, caseInfo.current_step.id, process_id, pid)
        self.processPlugin.setprocessDesc(caseInfo.id, caseInfo.current_step.id, process_id, processDesc)
        self.processPlugin.setExitcode(exitcode, caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setStatus('end', caseInfo.id, caseInfo.current_step.id, process_id)
        self.processPlugin.setProcessEndTime(caseInfo.id, caseInfo.current_step.id, process_id)

    def copyFileToRemote(self, remoteNode, localFilePath, remoteFileDir=None, account='root'):
        """
        copy local file to remote, return False if copy file action failed.
        
        :param string remoteNode: the hostname or the ipadress of the remote node
        :param string localFilePath: the local file path
        :param sring remoteFileDir: remote file dir path, if None, will use /tmp
        :param string account: default is 'root'
        :return tuple(returnCode, remoteFilePath), returnCode is true means copy action success
        """
        filename = os.path.basename(localFilePath)
        if not remoteFileDir:
            remoteFilePath = "/tmp/" + filename +"_" + generateRandomString(6)
        else:
            remoteFilePath = remoteFileDir + "/" + filename
        logger.debug("copy file %s to %s %s", localFilePath, remoteNode, remoteFilePath)
        rc = self.sshManager.scpPut(localFilePath, remoteNode, remoteFilePath, account)
        return rc, remoteFilePath
 
    def _setEnvLocal(self):
        """
        set env local
        use os.environ['ABC'] to set env; os.getenv('ABC') to get env parameter

        :return boolean, true mean set success
        """
        envList = self._getEnvList()
        if envList:
            logger.debug("try to set up env %s on local", envList)
            for key, value in envList:
                os.environ[key] = value
                if os.getenv(key) != value:
                    logger.error("set env %s to be %s failed", key, value)
                    raise STFBaseModuleError("set env %s to be %s failed", key, value)

    def _getEnvList(self):
        """
        get env list
    
        :return List:  a tuple list of the env which will be set on local, eg [(key1, value1), (key2, value2)]
        """
        return self.variablePlugin.getEnvs()
    
    def _generateEnvProfile(self):
        """
        use to generate a profile for env seting

        :return the local path of the profile
        """
        return self.variablePlugin.getEnvFile()

    
    
    
    
