import sys
import os
from stf.modules.base_module import STFBaseModule
from blivet.zfcp import loggedWriteLineToFile
from babel.localtime import DSTDIFF
from Crypto.Random.random import shuffle
from lsm.lsmcli.data_display import out

class STFCopyModuleError(BaseException):
    """If error, raise it."""
    pass
class STFCopyModule(STFBaseModule):
    def __init__(self, plugins):
        super(STFCopyModule, self).__init__(pluginManager)

    def checkMode(self, mode):
        """
        TBD
        """
        pass
    
    def checkModeParameter(self, parameter):
        """
        TBD
        """
        pass
    
    def getlabs(self, lab_info):
        if lab_info:
            nodeName = lab_info.split("@")[1]
            userName = lab_info.split("@")[0]
            
            labs = self.variablePlugin.getLabInfo(nodeName, userName)
            if not labs:
                logger.error("there is no lab for %s  as %s" % (nodeName, userName))
                raise STFCopyModuleError("there is no lab for %s  as %s" % (nodeName, userName))
            return labs  
    
    def getlabdetailInfo(self,lab):
        account = lab.user
        passwd = lab.password
        ip = lab.IP
        becomeUser = lab.become_user
        becomePW = lab.become_password
        return account, passwd, ip, becomeUser, becomePW
        
    def checkLabs(self, labs):
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
                 raise STFCopyModuleError(errorMsg)
            else:
                 raise STFCopyModuleError("not support jump host now")  
                 
    def checkModuleParameter(self, module, jumphost_info, lab_info):
        """
        :param module parameter
        """
        logger.info("module name is %s, justhost is %s,  access node is %s", module, jumphost_info, lab_info)
        if module.lower() != "copy":
            logger.error("this is copy module, not %s", module)
            raise STFCopyModuleError("this is copy module, not %s", module)
        if jumphost_info:
            logger.error("not support jump host now")
            raise STFCopyModuleError("not support jump host now")  
        labs = self.getlabs(lab_info) 
        for lab in labs:
            account, passwd,ip,becomeUser,becomePW = self.getlabdetailInfo(lab)
            try:
                if not becomeUser:
                    self.sshManager.getClient(ip, user=account, pw=passwd)
                else:
                    self.sshManager.getClient(ip, account, passwd, becomeUser, becomePW)
            except BaseException, msg:
                 errorMsg = "cannot access to %s as user %s:%s, error msg is %s" % (ip, account, passwd, str(msg))
                 logger.error(errorMsg)
                 raise STFCopyModuleError(errorMsg)
    
    def checkTags(self, tags):
        pass
    
    def checkCaseIDs(self, cases):
        pass
    
    def checkOthers(self, f):
        pass
    
    def copyLocal(self, src, dst):
        try:
            if not os.path.exists(src):
                raise STFCopyModuleError("Source  %s does not exits" , src);
            if not os.path.isdir(dst):
                raise STFCopyModuleError("Target dir %s does not exits" , dst);
            if os.path.isdir(src):
                shutil.copytree (src, dst)
            if os.path.isfile(src):
                if not dst.endswith("/"):
                    dst = dst + "/"
                shutil.copy(src, dst)
        except Exception as err:
                logger.error("copy local from %s to %s fail, error msg is %s" , (src, dst, err))
                rc = 255
                output = "copy fail"
        else:
            rc = 0
            output = "copy success"
                
        return rc, output, errs
        
    def run(self, caseInfo):
        
        caseFileLocation = caseInfo.current_step.path
        caseFileName = os.path.basename(caseFileLocation)
        mode = caseInfo.current_step.mode
        parameter = caseInfo.current_step.mode_argv 
        module = caseInfo.current_step.module
        jumphost_info = caseInfo.current_step.jumphost_info
        lab_info = caseInfo.current_step.lab_info
        tags = caseInfo.current_step.step_tags
        
#         casefile = self.appendExtToCaseFile(caseFileLocation)
        logger.debug( "copycasefile is %s", caseFileLocation)
        #file content format: 
        #download :remotefile -> localdir
        #upload:   localdir -> :remotefilepath
        file = open("tmptest")
        for line in file:
            print line.strip("\n")
            linearray = line.strip("\n").split("->")
            src = linearray[0]
            dst = linearray[1]
            if ":" in src and not ":" in dst:
                cpmode = "Download"
            elif ":" in dst and ":" not in src :
                cpmode = "Upload"
            elif not ":" in src and not ":" in dst:
                cpmode = "Local"
            else:
                cpmode = "Error"
            
            logger.debug("copy mode is %s", cpmode)
        
        if not lab_info and cpmode == "Local":
                logger.debug("copy in local, src is %s, dst is %s", (src, dst))
                self.processStart(caseInfo, 0)
                rc, output, errs = self.copyLocal(src, dst)
                logger.debug("run copy %s pid is %s, return code is %s, output is %s", scriptName, pid, rc, output)
                self.processEnd(caseInfo, 0, caseFileName, rc, output, errs, 0) 
        if lab_info:
            for lab in self.getlabs(lab_info):
                account, passwd,ip,becomeUser,becomePW = self.getlabdetailInfo(lab)
                if cpmode == "Upload":
                    pass
                if cpmode == "Download":
                    pass
                
            
            
if __name__ == '__main__':
    file = open("tmptest")
    path = "/home/dongxiao_test"
    if  path.endswith("/"):
        print "ok" 
        
    
           
        