#!/usr/bin/env python
import threading
from worker import worker
from time import time

class scheduler:
	modlock=threading.Lock()
	timer=threading.Event()
	workers=set()
	runqueue=[]
	def add(self,worker):
		"""Adds a new worker to the scheduler.
		"""
		interval=worker.get_interval()
		with self.modlock:
			self.workers.add(worker)
			simultanious=self.intervals.get(interval,set())
			self.intervals[interval]=simultanious.union([worker])

	def run(self):
		exit=False
		while not exit:
			cycle()
			timer.wait(calc_next_run())
			pass

	def cycle(self):
		t=time()
		curent = [val for key,val in self.intervals.iteritems() if key % int(t) ==0]
		print current


	def calc_next_run(self,t=None):
		if t==None:
			t=time()
		"""Returns the time to sleep untill the next event"""
		if len(self.intervals)==0:
			return 2**30
		times=[(tim-t%tim,func) for tim,func in self.intervals.iteritems()]
		print times
		nextTime=min(times[:][0])
		return nextTime, [func for tim,func,in times if tim==nextTime]

	def _regtest_testAdds():
		"""
		"""
	def __repr__(self):
		return repr(self.runqueue)

class _prioqueue(object):
	queue=[]
	def __init__(self):
		pass

	def pop():
		return queue.pop(0)
	def add(self,time,data):
		""">>> q=_prioqueue()
		>>> q.add(10,"10")
		>>> q.add(20,"20")
		>>> q.add(10,"10a")
		>>> q
		[(10, set(['10', '10a'])), (20, set(['20']))]
		"""
		q=self.queue
		time=int(time)
		found,index=self._gettimeindex(time)
		if found :
			q[index][1].add(data)
		else:
			self.queue.insert(index,(time,set([data])))

	def _gettimeindex(self,time):
		q=self.queue
		for i in range(len(q)):
			if q[i][0]==time:
				return (True,i)
			elif q[i][0]>time:
				return (False,i)
		return (False,len(q))

	def __repr__(self):
		return repr(self.queue)


if __name__ == "__main__":
	import doctest
	doctest.testmod()

