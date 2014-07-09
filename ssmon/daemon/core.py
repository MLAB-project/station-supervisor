#!/usr/bin/env python
import SocketServer
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail
from scheduler import scheduler
import configreader
import threading

DEFPORT=41133		#Linux ephemeral base 32768 + 8365

class Storage():
	"""Class working as an intermediate storage between the scheduler 
	ant the data-serving TCP-threads.
	
	It is meant as the primary "owner" of the worker-objects and the
	scheduler. It will thusly setup a new scheduler at start and add any.
	worker-objects to the scheduler.
	"""
	def __init__(self,workers=[],actors=[]):
		self.scheduler=sheduler()
		self.workers=set(workers)
		self.actors=set(actors)
		self.sthread=threading.Thread(target=scheduler.run)

	def add_worker(self,worker):
		self.workers.add(worker)

	def remove_worker(self,worker):
		self.workers.remove(worker)

	def get_all_workers(self):
		return self.workers

	def set_interval(self,worker,interval):
		self.scheduler.change_interval(worker,interval)

	def run(self):
		if selfs.sthread.is_alive():
			raise Warning("Allredy running")
		if self.sthread()
		try:
			self.sthread.start()
		except RuntimeError:
			self.sthread=threading.Thread(target=scheduler.run)
			self.sthread.start()


	class core():#should perhaps use python-daemon from PIP (PEP3143)
		def __init__(self,configfile):
			self.conf=conf=configreader.configreader(configfile)
			self.storage=storage=storage(self.conf.generateworkers())
if __name__ == "__main__":
	import socket
	import doctest
	doctest.testmod()

