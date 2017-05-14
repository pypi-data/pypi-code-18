#!/usr/bin/python
import sys
import os
string = sys.argv

null = ''
for name in string:
	null = null+(' ')+name


if string:
	os.system("python arjuno/bin.py {string}".format(string=null))
else:
	os.system("python arjuno/bin.py")