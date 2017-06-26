class QualiITF:
    def __init__(self):
        pass

    @staticmethod
    def getLogPath(relaseName, themeName, suiteName):
        return "T:\\_support\\" + relaseName + "\\" + themeName + "\\" + suiteName

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

