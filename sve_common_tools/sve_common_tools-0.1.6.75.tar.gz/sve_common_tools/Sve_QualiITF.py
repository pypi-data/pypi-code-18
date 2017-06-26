import os


class QualiITF:
    def __init__(self):
        pass

    @staticmethod
    def createPkLogPath(globalInputs):
        p =  QualiITF.getPrefixPath(globalInputs) + "PkLog_" + str(globalInputs["PkLog"]) + "\\"
        if (os.path.isdir(p)):
            pass
        else:
            os.makedirs(p)
        return p

    @staticmethod
    def getPrefixPath(globalInputs):
        return "T:\\_support\\" + globalInputs["Release"] + "\\" + globalInputs["ThemeName"] + "\\" + globalInputs[
            "SuiteName"] + "\\"

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
