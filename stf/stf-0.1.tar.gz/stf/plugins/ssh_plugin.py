'''
Created on May 12, 2017

@author: root
'''
import os
import datetime
import time
from stf.lib.ssh.ssh_manager import SshManager
from stf.plugins.base_plugin import STFBasePlugin
from stf.lib.logging.logger import Logger
logger = Logger.getLogger(__name__)

class STFSshPlugin(STFBasePlugin):

    def __init__(self, plugins):
        super(STFSshPlugin, self).__init__(plugins)
        
    def getSshManager(self, host, user=None, pw=None, useKey=True, sshGateway=None, sshUser=None, sshPassword=None):
        """
        """
        if not sshGateway:
            sshGateway = os.getenv("SSH_GATEWAY")
        if not sshUser:
            sshUser = os.getenv("SSH_GATEWAY_USER")
        if not sshPassword:
            sshPassword = os.getenv("SSH_GATEWAY_PASSWORD")
        sshManager = SshManager(sshGateway, sshUser, sshPassword)
        sshManager.getClient(host, user=user, pw=pw)
        return sshManager


    def prepareCaseSourceList(self, serverInfo):
        """
        r51.ih.lucent.com:/u/xguan005/test/@@xguan005:mypasswd
        """
        remoteInfo = serverInfo.split("@@")[0]
        server = remoteInfo.split(":")[0]
        caseRemotePath = remoteInfo.split(":")[1]
        accountInfo = serverInfo.split("@@")[1]
        account = accountInfo.split(":")[0]
        if ":" in accountInfo:
            password = accountInfo.split(":")[1]
            useKey = False
        else:
            password = None
            useKey = True

        sshManager = self.getSshManager(server, account, password, useKey)

        logger.debug("try to clone %s from server %s", caseRemotePath, server)
        date = datetime.datetime.now().strftime("%Y%m%d-"+ time.tzname[1] + "-%H%M%S.%f")
        caseDir = "TestCase-" + date
        
        sshManager.scpGetDir(server, caseRemotePath, account, caseDir)
        caseDirFullPath = os.path.join(os.getcwd(), caseDir)
        logger.info("case dir is %s", caseDirFullPath)
        return caseDirFullPath

        
        
