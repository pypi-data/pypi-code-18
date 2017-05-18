from enum import Enum
import libenable
import time

class Status(Enum):
	'''
	Operational status codes for the application
	'''

	RUNNING = 0
	WORKING = 1

__all__ = ['Status', 'internet']
__conf__ = '.libenable.ini'
__db__ = '.libenable.db'
__host__ = 'localhost'
__port__ = 80
__start_time__ = int(time.time())
__status__ = Status.RUNNING
__running_tasks__ = 0
__total_tasks__ = 0
__version__ = '0.2.1'
config = None

def amRunning():
	'''
	Changes the status to RUNNING if no one else is WORKING
	'''

	libenable.__running_tasks__ -= 1

	if libenable.__running_tasks__ == 0:
		libenable.__status__ = Status.RUNNING

def amWorking():
	'''
	Changes the status to WORKING
	'''

	libenable.__status__ = Status.WORKING
	libenable.__running_tasks__ += 1
	libenable.__total_tasks__ += 1
