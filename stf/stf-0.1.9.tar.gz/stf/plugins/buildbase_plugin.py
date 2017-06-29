from abc import abstractmethod
from stf.plugins.base_plugin import STFBasePlugin
from stf.lib.ssh.ssh_manager import SshManager
from stf.lib.logging.logger import Logger
import os
import random,string

logger = Logger.getLogger(__name__)

class STFBuildbasePlugin(STFBasePlugin):
    def __init__(self,plugins):
        super(STFBuildbasePlugin,self).__init__(plugins)


    #derived class should not override this API
    #This API will called by STFBuildModule class
    def run(self):
        self.preBuild()
        self.build()
        self.postBuild()
        self.upload()
 
    #derived class should override this API
    @abstractmethod
    def preCheck(self):
        pass
 
    #derived class should override this API
    @abstractmethod
    def preBuild(self):
        pass
     
    #derived class should override this API
    @abstractmethod
    def build(self):
        pass
 
    #derived class should override this API
    @abstractmethod
    def postBuild(self):
        pass
 
 
    #derived class should not override this API.
    #upload artifacts to Artifactory
    def upload(self):
        pass
 
    #other common helper APIs can be defined below
    