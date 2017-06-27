import os
import time
from datetime import datetime
import paramiko
import Sve_SSHManager as sveM


class QualiITF:
    def __init__(self):
        pass

    @staticmethod
    def createPkLogPath(globalInputs):
        p = QualiITF.getPrefixPath(globalInputs) + "Output\\PkLog_" + str(QualiITF.getPkLog(globalInputs)) + "\\"
        if (os.path.isdir(p)):
            pass
        else:
            os.makedirs(p)
        return p

    @staticmethod
    def getPrefixPath(globalInputs):
        return "T:\\_support\\" + \
               QualiITF.getRelease(globalInputs) + "\\" + \
               QualiITF.getThemeName(globalInputs) + "\\" + \
               QualiITF.getSuiteName(globalInputs) + "\\"

    @staticmethod
    def getThemeName(globalInputs):
        return globalInputs["ThemeName"]

    @staticmethod
    def getSuiteName(globalInputs):
        return globalInputs["SuiteName"]

    @staticmethod
    def getTestName(globalInputs):
        return globalInputs["TestName"]

    @staticmethod
    def getWhatifName(globalInputs):
        return globalInputs["WhatifName"]

    @staticmethod
    def getRelease(globalInputs):
        return globalInputs["Release"]

    @staticmethod
    def getSecret(globalInputs):
        return globalInputs["Secret"]

    @staticmethod
    def getPkLog(globalInputs):
        return globalInputs["PkLog"]

    @staticmethod
    def getQualiITFService(globalInputs):
        return globalInputs["QualiITFService"]

    @staticmethod
    def getUserEmail(globalInputs):
        return globalInputs["UserEmail"]

    @staticmethod
    def QualiITFService_Name():
        return "QualiITF Service Instance"

    @staticmethod
    def QualiITFService_getAllParams():
        return "getAllParams"

    @staticmethod
    def QualiITFService_getAllParamsExtended():
        return "getAllParamsExtended"

    @staticmethod
    def getTltrepoReportsPath(globalInputs, subDir):
        startTime = time.time()
        userEmail = QualiITF.getUserEmail(globalInputs) if "@" in QualiITF.getUserEmail(globalInputs) \
            else "unknown@unknown.com"
        return QualiITF.getRelease(globalInputs) + "/" + \
               QualiITF.getThemeName(globalInputs) + "/" + \
               QualiITF.getSuiteName(globalInputs) + "/" + \
               datetime.fromtimestamp(startTime).strftime('%Y/%m') + '/' + \
               'ID_' + str(QualiITF.getPkLog(globalInputs)) + "_" + userEmail.split("@")[0] + "/" + \
               (subDir.strip("\\").strip("/") + "/" if (subDir is not None) else "")

    @staticmethod
    def sendToTltrepoReportsPath(tltrepoIP, tltrepoPort, tltrepoUser, tltrepoPass, tltrepoRemoteUnixPath,
                                 globalInputs, localPath, fileName, subDir):

        rp = QualiITF.getTltrepoReportsPath(globalInputs, subDir)
        unixrp = tltrepoRemoteUnixPath + "/_reports/" + rp

        # CREATE REMOTE DIR
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(tltrepoIP, int(tltrepoPort), tltrepoUser, tltrepoPass)
        tokens = rp.replace("\\", "/").replace("//", "/").strip("/").split("/")
        d = ""
        for token in tokens:
            if (token != ""):
                d = d + "/" + token
                stdin, stdout, stderr = ssh.exec_command("mkdir " + tltrepoRemoteUnixPath + "/_reports" + d)
        ssh.close()

        # SEND FILE
        returnFlag = sveM.SSHManager.upload_file_via_SFTP(remote_hostname=tltrepoIP,
                                                          remote_port=int(tltrepoPort),
                                                          remote_user=tltrepoUser,
                                                          remote_password=tltrepoPass,
                                                          remote_dir=unixrp,
                                                          local_dir=localPath.strip("\\").strip("/"),
                                                          local_filename=fileName)
        return {
            "status": returnFlag,
            "html": {"path": "http://" + tltrepoIP + "/_reports/" + rp,
                     "name": fileName
                     }
        }
