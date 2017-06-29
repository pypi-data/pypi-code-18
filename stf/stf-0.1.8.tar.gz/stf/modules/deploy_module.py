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
        self.plugins = pluginManager
        self.variablePlugin = self.plugins.getInstance("variable")
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
        index = int(caseInfo.current_step.mode_argv)
        self.processStart(caseInfo, 0)
        rc=1
        if self.variablePlugin.hasSection('Deploy'):
            nodelist=[]
            for x in self.variablePlugin.childHeaders('Deploy:Lab'):
                if x == 'dynamic':
                    continue
                node={}
                node['Name']=x
                node['count']=1
                if self.variablePlugin.hasOption('count','Deploy:Lab:'+x):
                    node['count']=self.variablePlugin.getInt('count','Deploy:Lab:'+x)
                for j in self.variablePlugin.options('Deploy:Lab:'+x):
                    node[j]=self.variablePlugin.get(j,'Deploy:Lab:'+x)
                vmlist=[]
                for y in self.variablePlugin.childHeaders('Deploy:Lab:'+x):
                    if y == 'dynamic':
                        continue
                    vm={}
                    vm['Name']=y
                    vm['count']=1
                    if self.variablePlugin.hasOption('count','Deploy:Lab:'+x+':'+y):
                        vm['count']=self.variablePlugin.getInt('count','Deploy:Lab:'+x+':'+y)
                    for j in self.variablePlugin.options('Deploy:Lab:'+x+':'+y):
                        vm[j]=self.variablePlugin.get(j,'Deploy:Lab:'+x+':'+y)
                    for z in self.variablePlugin.childHeaders('Deploy:Lab:'+x+':'+y):
                        extra={}
                        for k in self.variablePlugin.options('Deploy:Lab:'+x+':'+y+':'+z):
                            extra[k]=self.variablePlugin.get( k,'Deploy:Lab:'+x+':'+y+':'+z)
                        vm[z]=extra
                    vmlist.append(vm)
                node['VM']=vmlist
                nodelist.append(node)
            if openstack.preCheck() :
                if operation == 'get' :
                    for x in nodelist:
                        for i in range(0,int(x['count'])):
                            if not openstack.run(operation,i,x):
                                self.processEnd(caseInfo, 0, "", rc,openstack.output, openstack.error, 0);
                                return rc
                            else:
                                rc=0
                else:
                    iid=int(index)
                    for x in nodelist:
                        if iid>=int(x['count']):
                            iid=iid-int(x['count'])
                        else:
                            if openstack.run(operation,index,x):
                                rc=0
        self.processEnd(caseInfo, 0, "", rc,openstack.output, openstack.error, 0);
        return rc
        #rc, output = self.runScriptOnRemote(self.server, scriptPath, "/u/"+ self.username ,account=self.username)
        #logger.info("run build script %s on %s return code is %s, output is %s", scriptPath, self.server, rc, output)

        
