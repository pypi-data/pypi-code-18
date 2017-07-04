#!/usr/bin/env python
#coding: utf-8 -*-

"""
time rotate, midnight, set multiprocess
has mail
"""

import commands
import os
import time
from multiprocessing import Process,Value,Lock
from xlogging import log

log.setConfig(module_name='case05',ro_rotateby=2, ro_when='midnight', ro_backupcount=4,logfile='test_case05.log',multiprocess=1,viamail=1,mailaddr='lilo@baidu.com')

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

	
