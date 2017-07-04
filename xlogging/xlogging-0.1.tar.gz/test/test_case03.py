#!/usr/bin/env python
#coding: utf-8 -*-

"""
file rotate, NOT set multiprocess
no mail
"""

import commands
import os
import time
from multiprocessing import Process,Value,Lock
from xlogging import log

log.setConfig(module_name='case03',ro_rotateby=1,ro_backupcount=4,ro_maxsize=1024,logfile='test_case03.log',multiprocess=0,viamail=0,mailaddr='lilo@baidu.com')

def log_a():
	while True:
        	log.debug('''a''')
		time.sleep(1)

def log_b():
	while True:
        	log.debug('''b''')
		time.sleep(1)

if __name__ == '__main__':
	pida = Process(target=log_a,args=())
	
	pidb = Process(target=log_b,args=())

        log.critical("test")

 	pida.start()
 	pidb.start()

	
