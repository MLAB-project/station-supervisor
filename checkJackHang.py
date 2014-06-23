#!/usr/bin/env python

import time
import multiprocessing
import jack
import sys
import Queue


class _testThread(multiprocessing.Process):
	"""Processthread object to test jack-connectivity in."""
	exitStatus=None
	def __init__(self,queue):
		"""queue -- any thrown exception will be placed on the queue must be a multiprocessing.Queue"""
		self.queue=queue
		super(_testThread, self).__init__()

	def run(self):
		try:
			jack.attach("jackTest"+str(int(time.time())))
			jack.detach()
		except:
			self.exitStatus=sys.exc_info()

class JackTimeOut(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)

def _safeQueueGet(queue):
	"""helper to get the top of the queue"""
	try:
		return queue.get(False)
	except Queue.Empty:
		return None

def testJack(timeOut=1):
	"""Attempts to attach to Jack and returns any error that was encountered.
	timeOut -- time out in seconds or fractional seconds to wait for attach/detach.

	Returns None in case no error was encountered otherwise the exception object.

	Might throw multiprocessing.ProcessError if it was unable to detach jack.
	"""
	q=multiprocessing.Queue()
	t=_testThread(q)
	t.start()
	t.join(timeOut)
	time.sleep(.1) #Because threads in python...
	if not t.is_alive():
		return _safeQueueGet(q)
	else:
		t.terminate()
		for i in range(20):
			time.sleep(.1)
			if not t.is_alive():
				break
		else:
			multiprocessing.ProcessError("Unable to terminate jack thread")
		return JackTimeOut("Jack attachment timed out after {} second{}".format(timeOut,("s" if timeOut!=1 else "")))


if __name__=="__main__":
	print ">>",testJack(2)
