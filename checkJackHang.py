#!/usr/bin/env python

import time
import multiprocessing
import jack
import sys
import Queue

class _testThread(multiprocessing.Process):
	exitStatus=None
	def __init__(self,queue):
		self.queue=queue
		super(_testThread, self).__init__()

	def run(self):
		try:
			jack.attach("jackTest")
			jack.detach()
		except:
			self.exitStatus=sys.exc_info()

class JackTimeOut(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)

def _safeQueueGet(queue):
	try:
		return queue.get(False)
	except Queue.Empty:
		return None

def testJack(timeOut):
	q=multiprocessing.Queue()
	t=_testThread(q)
	t.start()
	#print "thread started"
	t.join(timeOut)
	time.sleep(.1) #Because threads in python...
	if not t.is_alive():
		return _safeQueueGet(q)
	else:
		t.terminate()
		return JackTimeOut("Jack attachment timed out after %f second%s"%(timeOut,("s" if timeOut!=1 else "")))


if __name__=="__main__":
	print testJack(2)
