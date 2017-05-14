#!/usr/bin/python
import sys
import os
string = sys.argv

null = ''
for name in string:
	null = null+(' ')+name


if string:
	os.system("python bin.py {string}".format(string=null))
else:
	os.system("python bin.py")