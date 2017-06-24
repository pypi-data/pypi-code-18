from abc import abstractmethod
from stf.plugins.buildbase_plugin import STFBuildbasePlugin
from stf.lib.ssh.ssh_manager import SshManager
from stf.lib.logging.logger import Logger
import os
import random,string

logger = Logger.getLogger(__name__)

class STFBuildmcasPlugin(STFBuildbasePlugin):
    def __init__(self,plugins):
        super(STFBuildmcasPlugin,self).__init__(plugins)
        self.variablePlugin = self.plugins.getInstance("variable")
        self.sshPlugin = self.plugins.getInstance("ssh")
        self.sshManager = self.sshPlugin.sshManager
        self.buildCommonPara = None
        self.buildProductPara = None
        self.buildUserPara = None
        self.buildServer = None
        self.relBranch = None
        self.username = None
 
    """
    derived class should not override this API
    #This API will called by STFBuildModule class
    """
    def generateRandomString(self,N):
        """
        # generate a random sring, length is N
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

    def run(self):
        self.preBuild()
        rc, output, err = self.build()
        self.postBuild()
        self.upload()
        return rc,output,err
    def preCheck(self):
        """
        check build common parameter file
        """
        self.buildCommonPara = self.variablePlugin.getBuildFile('Build')
        if self.buildCommonPara is None:
            errorMsg = "buid common parameters configuration not exist"
            logger.error(errorMsg)
          
        self.buildProductPara = self.variablePlugin.getBuildFile('Build:MCAS:Branch')
        if self.buildProductPara is None :
            errorMsg = "build Product-release level parameters configuration not exist"
            logger.error(errorMsg)
       
        self.buildUserPara = self.variablePlugin.getBuildFile('Build:USER')
        if self.buildProductPara is None :
            errorMsg = "build User level parameters configuration not exist"
            logger.error(errorMsg)
        
    def preBuild(self):
        logger.info('copy build common parameters configuration file to remote server')
        self.buildServer = self.variablePlugin.get('BUILD_SERVER','Build')
        self.username = self.variablePlugin.get("user","Build:USER")
        rc,remoteBuildFile = self.sshPlugin.copyFileToRemote(self.buildServer, \
                                self.buildCommonPara,"/u/" + self.username + "/CI/data/EnvLI", self.username)
        if not rc:
            return rc, "copy build common parameters configuration file %s to remote %s failure" %(self.buildCommonPara,self.buildServer)
        os.remove(self.buildCommonPara)
        
        logger.info('copy build Product-release parameters configuration file to remote server')
        rc,remoteBuildFile = self.sshPlugin.copyFileToRemote(self.buildServer, \
                                self.buildProductPara,"/u/" + self.username + "/CI/data/EnvLIRelBranch", self.username)
        if not rc:
            return rc, "copy build Product-release level parameters configuration file %s to  %s failure" %(self.buildProremoteductPara,self.buildServer)
        os.remove(self.buildProductPara)
        
        logger.info('copy build User level parameters configuration file to remote server')
        self.relBranch = self.variablePlugin.get("RelBranch","Build:MCAS:Branch")
        rc,remoteBuildFile = self.sshPlugin.copyFileToRemote(self.buildServer, \
                                self.buildUserPara,"/u/" + self.username +"/CI/data/buildID_"+self.relBranch, self.username)
        if not rc:
            return rc, "copy build User level parameters configuration file %s to remote %s failure" %(self.buildUserPara,self.buildServer)
        os.remove(self.buildUserPara)

    def build(self):
        buildType = self.variablePlugin.get("BUILDTYPE","Build")
        cmd = "chmod +x /u/" + self.username + "/CI/data/EnvLI; chmod +x /u/"+ self.username + \
                "/CI/data/EnvLIRelBranch; chmod +x /u/"+ self.username +"/CI/data/buildID_"+self.relBranch +";"
        if buildType == 'full':
            cmd = cmd +"source /u/" + self.username +"/.profile; /u/" + self.username + "/CI/litool/build.py"
        else:
            cmd = cmd + "source /u/" + self.username +"/.profile; /u/" + self.username + "/CI/litool/IncrementalBuild.py"

        rc, output, err = self.sshManager.run(self.buildServer, cmd, user=self.username, timeout=1200)

        if rc:
            logger.error("NOTE: command %s on build server %s failed.", cmd, self.buildServer)
            logger.error("NOTE: output is %s", output + os.linesep + err)
            raise BaseException("NOTE: command %s on build server %s failed.", cmd, self.buildServer)
        else:
            logger.info("output: %s", output)
            return rc, output, err
 
    #derived class should override this API
    def postBuild(self):
        logger.info("postbuild")
 
 
    #derived class should not override this API.
    #upload artifacts to Artifactory
    def upload(self):
        logger.info("upload")
 
    #other common helper APIs can be defined below.