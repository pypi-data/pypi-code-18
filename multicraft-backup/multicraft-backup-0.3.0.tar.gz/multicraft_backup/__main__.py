#!/usr/bin/env python3
# encoding: utf-8

import multicraft_backup
from configparser import ConfigParser


def main(argv):
	try:
		cp = ConfigParser()
		cp.read('multicraft_backup.ini')
		
		server = multicraft_backup.ServerBase(cp)
		ftp = multicraft_backup.BackerUpper(cp, argv[1])
		
		server.stop()
		ftp.do_it_all_everything()
		server.start()
		
		# close the browser window
		server.close()
	else:
		return 0


if __name__ == '__main__': # can't see any reason why it wouldn't, but so it goes
	import sys
	
	sys.exit(main(sys.argv))
