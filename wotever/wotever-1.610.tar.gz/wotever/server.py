import functools
import time
import threading
import logging
import Queue
#import hunspell

import tornado.web
import tornado.websocket
import tornado.locale
import tornado.ioloop
import wotever as wt
from tornado.options import define, options

define('debug', type=bool, default=False, help='run in debug mode with autoreload (default: false)')

class Handler(tornado.web.RequestHandler):	
	def bg(self,p):
		time.sleep(5)
		print 'bg...'

	def get(self, word):
		self.write('....')		
		self.application.mainMgr.execute(wt.job(self.bg,None))
		print self.application.mainMgr.toString()

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/(.*)", Handler),
		]
		settings = {
			'cookie_secret': 'W/wT5ndaR/2sa3m8OOQ5q0xDvnZclE4BtimO1f+QM2Y=',
			'debug':options.debug,
		}
		tornado.web.Application.__init__(self, handlers, **settings)
		self.mainMgr=wt.exemgr(10,"mainmgr",True)
		# self.mainMgr.setDaemon(True)

if __name__ == "__main__":
	#tornado.options.parse_command_line()
	application = Application()
	application.listen(8888)
	application.mainMgr.setDaemon(True)
	tornado.ioloop.IOLoop.instance().start()