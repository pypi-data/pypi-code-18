#coding=utf8
import Queue
import threading
import contextlib
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class fileHelper(object):

	def __init__(self):
		self.targetFile = ''



	def scan_files(directory,prefix=None,postfix=None,fullpath=False):
		files_list=[]
		
		for root, sub_dirs, files in os.walk(directory):
			
			for special_file in files:
				if postfix:
					if not special_file.endswith(postfix):
						continue
						# files_list.append(os.path.join(root,special_file))
						# files_list.append(special_file)
				if prefix:
					if not special_file.startswith(prefix):
						continue
						# files_list.append(os.path.join(root,special_file))
						# files_list.append(special_file)
				
					# files_list.append(os.path.join(root,special_file))
				if fullpath:
					files_list.append(os.path.join(root,special_file))
				else:
					files_list.append(special_file)
								 
		return files_list

	def getLines(filePath):
