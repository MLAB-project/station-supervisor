#!/usr/bin/env python
import SocketServer
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail
from scheduler import scheduler
import threading

DEFPORT=41133		#Linux ephemeral base 32768 + 8365

class Storage():
	def __init__(self,workers=[]):
		self.scheduler=sheduler()
		self.workers=workers
		self.thread=threading.Thread(target=scheduler.run)

	def run(self):
		if self.thread.is_alive():
			raise Warning("Allredy running")
		if self.thread()
		try:
			self.thread.start()
		except RuntimeError:
			self.thread=threading.Thread(target=scheduler.run)
			self.thread.start()


if __name__ == "__main__":
	import socket
	import doctest
	doctest.testmod()

