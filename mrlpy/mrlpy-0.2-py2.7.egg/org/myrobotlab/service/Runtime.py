from mrlpy import mcommand
from Test import Test


def createAndStart(name, type):
	return mcommand.callService("runtime", "createAndStart", [name, type])
	
	
def shutdown():
	mcommand.sendCommand("runtime", "shutdown", [])

def getRuntime():
	return mcommand.callService("runtime", "start", ["runtime", "Runtime"])

def start(name, type):
        return mcommand.callService("runtime", "start", [name, type])

