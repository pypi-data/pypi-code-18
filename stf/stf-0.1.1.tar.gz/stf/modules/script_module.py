'''
Created on Mar 31, 2017

@author: Zhao Xia
'''
import os
import subprocess32 as subprocess
from subprocess32 import TimeoutExpired
from stf.lib.logging.logger import Logger
from stf.modules.base_module import STFBaseModule
from posix import X_OK
import signal

logger = Logger.getLogger(__name__)

ACCEPT_MODE = ["parallel", "loop", "async"]

class STFScriptModuleError(BaseException):
    """If error, raise it."""
    pass

class STFScriptModule(STFBaseModule):
    """
    """
    def __init__(self, pluginManager):
        """
        constructor
        """
        super(STFScriptModule, self).__init__(pluginManager)

    def checkMode(self, mode):
        """check mode, now only support the mode in ACCEPT_MODE"""
        if mode not in ACCEPT_MODE:
            logger.error("script module do not support %s mode, now only support %s", mode, ACCEPT_MODE)
            raise STFScriptModuleError("script module do not support %s mode, now only support %s", mode, ACCEPT_MODE)

    def checkModeParameter(self, parameter):
        """check mode parameter"""
        pass

    def checkModuleParameter(self, module, jumphost_info, lab_info):
        """check module parameter"""
        logger.debug("module name is %s, justhost is %s,  access node is %s", module, jumphost_info, lab_info)
        if module.lower() != "script":
            logger.error("this is script module, not %s", module)
            raise STFScriptModuleError("this is script module, not %s", module)

        if lab_info:
            nodeName = lab_info.split("@")[1]
            userName = lab_info.split("@")[0]
            if not jumphost_info:
                labs = self.variablePlugin.getLabInfo(nodeName, userName)
                if not labs:
                    logger.error("there is no lab for %s  as %s" % (nodeName, userName))
                    raise STFScriptModuleError("there is no lab for %s  as %s" % (nodeName, userName))
                for lab in labs:
                    account = lab.user
                    passwd = lab.password
                    ip = lab.IP
                    becomeUser = lab.become_user
                    becomePW = lab.become_password
                    try:
                        if not becomeUser:
                            self.sshManager.getClient(ip, user=account, pw=passwd)
                        else:
                            self.sshManager.getClient(ip, account, passwd, becomeUser, becomePW)
                    except BaseException, msg:
                        errorMsg = "cannot access to %s as user %s:%s, error msg is %s" % (ip, account, passwd, str(msg))
                        logger.error(errorMsg)
                        raise STFScriptModuleError(errorMsg)
            else:
                raise STFScriptModuleError("not support jump host now")

    def checkCaseIDs(self, cases):
        """check case id"""
        pass

    def checkTags(self, tags):
        """ check tags """
        pass

    def checkOthers(self, filePath):
        """ check others """
        if not os.access(filePath, X_OK):
            logger.debug("add +x for %s", filePath)
            command = "chmod +x " + filePath
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outs, errs = proc.communicate()
            rc = proc.returncode
            if rc:
                raise STFScriptModuleError("command %s failed: rc is %s, output is %s, errs is %s ", command, rc, outs, errs)

    def run(self, caseInfo):
        """
        :param string scriptPath: the full path of the script file
        :return tuple(returnCode, output)
        """
        scriptPath = caseInfo.current_step.path
        scriptName = os.path.basename(scriptPath)
        mode = caseInfo.current_step.mode
        parameter = caseInfo.current_step.mode_argv 
        module = caseInfo.current_step.module
        jumphost_info = caseInfo.current_step.jumphost_info
        lab_info = caseInfo.current_step.lab_info
        tags = caseInfo.current_step.step_tags

        results = dict()
        if not lab_info:
            if not mode:
                self.processStart(caseInfo, 0)
                self._setEnvLocal()
                pid, rc, output, errs = self.runScriptLocal(scriptPath)
                logger.debug("run script %s pid is %s, return code is %s, output is %s", scriptName, pid, rc, output)
                self.processEnd(caseInfo, 0, scriptName, rc, output, errs, pid)
            if mode == "async":
                self.processStart(caseInfo, 0, parameter)
                pid, rc,output, errs = self.runScriptLocal(scriptPath, 0.1, async=True)
                logger.debug("run script %s pid is %s, return code is %s, output is %s", scriptName, pid, rc, output)
                self.processRunning(caseInfo, 0, pid)
            if mode == "parallel":
                pass
            results[scriptName] = (pid, rc, output, errs)
        else:
            if not mode:
                nodeName = lab_info.split("@")[1]
                userName = lab_info.split("@")[0]
                labs = self.variablePlugin.getLabInfo(nodeName, userName)
                results = dict()
                index = 0
                for lab in labs:
                    self.processStart(caseInfo, index)
                    account = lab.user
                    ip = lab.IP
                    becomeUser = lab.become_user
                    becomePW = lab.become_password
                    passwd = lab.password
                    if not becomeUser:
                        self.sshManager.getClient(ip, user=account, pw=passwd)
                        finalAccount = account
                    else:
                        self.sshManager.getClient(ip, account, passwd, becomeUser, becomePW)
                        finalAccount = becomeUser
                            
                    pid, rc, stdout, stderr = self.runScriptOnRemote(ip, scriptPath, account=finalAccount)
                    results[ip + ":" + scriptName] = (pid, rc, stdout, stderr)
                    logger.debug("run script %s on %s pid is %s, return code is %s, output is %s",
                                scriptName, pid, ip, rc, stdout+os.linesep+stderr)
                    self.processEnd(caseInfo, index, ip + ":" + scriptName, rc, stdout, stderr, pid)
        return results
    
    def runScriptLocal(self, localScriptPath, timeout=None, async=False):
        """
        run a script on current machine
        
        :param str localScriptPath: the path of the script
        :param int timeout: unit is second
        :param boolean kill: if False, will not kill the process
        :return tuple (returnCode, output)
        """
        command = localScriptPath
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            pid = proc.pid
            if not pid:
                logger.debug("get process %s pid failed ",command)
                raise STFScriptModuleError("get process %s pid failed ",command)
            outs, errs = proc.communicate(timeout=timeout)
            logger.debug("process %s: output is %s ",command, outs)
            rc = proc.returncode
        except TimeoutExpired:
            if async:
                outs = ""
                errs = "%s timeout reached" % command
                rc = 0
            else:
                logger.debug("%s timeout reached, kill the process %s",command, pid)
                proc.kill()
                os.kill(pid, signal.SIGKILL)
                outs, errs = proc.communicate()
                rc = 255
        logger.debug("process %s: output is %s, errs is %s ", command, str(outs), str(errs))
        return pid, rc, outs, errs
    
    def runScriptOnRemote(self, remoteNode, localFilepath, remoteFileDir=None, account='root'):
        """
        run remote script with a env profile, (source remoteProfile, then run the script on remote)
        
        :param string remoteNode: the hostname or the ipadress of the remote node
        :param sring localFilepath: the full path of local file
        :param string remoteFileDir: the full path of the remoteFileDir
        :param string account: default is 'root'
        :return tuple (returnCode, output)
        """
        pid = None
        rc, remoteScriptPath = self.copyFileToRemote(remoteNode, localFilepath, remoteFileDir, account)

        if not rc:
            return rc, "copy local script %s to remote %S failed" % (localFilepath, remoteNode)
        localEnvProfile = self._generateEnvProfile()
        rc, remoteEnvProfile = self.copyFileToRemote(remoteNode, localEnvProfile, remoteFileDir, account)
        if not rc:
            return rc, "copy local env profile %s to remote %S failed" % (localEnvProfile, remoteNode)
        
        command = "set -a; source " + remoteEnvProfile + "; "\
                  + "chmod +x "+ remoteScriptPath + "; " + remoteScriptPath
        logger.debug("run command %s on %s as %s", command, remoteNode, account)
        rc, stdout, stderr = self.sshManager.run(remoteNode, command, user=account)
        logger.debug("run command %s on %s as %s, rc is %s, output is %s ",
                    command, remoteNode, account, rc, stdout+os.linesep+stderr)
        rmCommand = "rm " + remoteEnvProfile + " " + remoteScriptPath
        logger.debug("run command %s on %s as %s", rmCommand, remoteNode, account)
        self.sshManager.run(remoteNode, rmCommand, user=account)
        logger.debug("return %s, %s, %s", rc, stdout, stderr)
        return pid, rc, stdout, stderr

