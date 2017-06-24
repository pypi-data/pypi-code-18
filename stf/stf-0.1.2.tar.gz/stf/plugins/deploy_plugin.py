#!/usr/bin/env python
from abc import abstractmethod
from stf.plugins.base_plugin import STFBasePlugin
from stf.lib.logging.logger import Logger
logger = Logger.getLogger(__name__)
  
class STFDeployPlugin(STFBasePlugin):
    def __init__(self, plugins):
        super(STFDeployPlugin, self).__init__(plugins)
        self.variablePlugin = self.plugins.getInstance("variable")
        self.output="Success"
        self.error=""
  
    #derived class should not override this API
    #This API will called by STFDeployModule class
    def run(self,action,idx,labpar):
        self.preAction()
        if action == 'get':
            res=self.get(idx,labpar)
        elif action == 'setup':
            res=self.deploy(idx,labpar)
        elif action == 'destroy':
            res=self.destroy(idx, labpar)
        self.postAction()
        return res;
  
    #derived class should override this API
    @abstractmethod
    def preCheck(self):
        pass
  
    #derived class should override this API
    @abstractmethod
    def preAction(self):
        pass
      
    #derived class should override this API
    @abstractmethod
    def deploy(self,idx,labpar):
        pass
    
    #derived class should override this API
    @abstractmethod
    def destroy(self,idx,labpar):
        pass
    
    #derived class should override this API
    @abstractmethod
    def get(self,idx,labpar):
        pass
  
    #derived class should override this API
    @abstractmethod
    def postAction(self):
        pass
  
    def putLabIP(self,labname,labindex,hostname,hostindex,floatingip,vmip,internalip):
        logger.info("save floatingip")
        if floatingip :
            self.variablePlugin.updateDynamic('Deploy:IP:Dynamic',
                         labname+'__'+str(labindex+1)+'__'+hostname+'__host'+str(hostindex+1)+'__floating', 
                         floatingip)
        logger.info("save interfaceip")
        if vmip :
            self.variablePlugin.updateDynamic('Deploy:IP:Dynamic',
                         labname+'__'+str(labindex+1)+'__'+hostname+'__host'+str(hostindex+1)+'__interface', 
                         vmip)
        logger.info("save internalip")
        if internalip :
            self.variablePlugin.updateDynamic('Deploy:IP:Dynamic',
                         labname+'__'+str(labindex+1)+'__'+hostname+'__host'+str(hostindex+1)+'__internal', 
                         internalip)
        self.variablePlugin.flushDynamic()

    #other common helper APIs can be defined below
    #...