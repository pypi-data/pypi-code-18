from enum import Enum
import d3cryp7
import socket
import time

class Status(Enum):
	'''
	Operational status codes for the application
	'''

	RUNNING = 0
	WORKING = 1

__all__ = ['Status']
__conf__ = '.d3cryp7.ini'
__db__ = '.d3cryp7.db'
__host__ = 'localhost'
__port__ = 80
__start_time__ = int(time.time())
__status__ = Status.RUNNING
__running_tasks__ = 0
__total_tasks__ = 0
__version__ = '0.5.0'
config = None

def amRunning():
	'''
	Changes the status to RUNNING if no one else is WORKING
	'''

	d3cryp7.__running_tasks__ -= 1

	if d3cryp7.__running_tasks__ == 0:
		d3cryp7.__status__ = Status.RUNNING

def amWorking():
	'''
	Changes the status to WORKING
	'''

	d3cryp7.__status__ = Status.WORKING
	d3cryp7.__running_tasks__ += 1
	d3cryp7.__total_tasks__ += 1
