#!/usr/bin/env python
import threading
from worker import worker
from time import time

class scheduler:
	def __init__(self):
		self.modlock=threading.Lock()
		self.timer=threading.Event()
		self.workers=set()
		self.runqueue=_prioqueue()
		self._exit=False
		self.threadpool={}

	def add(self,worker):
		"""Adds a new worker to the scheduler.
		"""
		interval=worker.get_interval()
		with self.modlock:
			self.workers.add(worker)
			self._requeue([worker])

	def change_interval(self,worker,interval):
		with self.modlock:
			if self.runqueue.remove_item(worker):
				if self.runqueue.peek():
					oldNextRun=self.runqueue.peek()[0]
				else:
					oldNextRun=2**30
				worker.set_interval(interval)
				self._requeue([worker])
				if oldNextRun!=self.runqueue.peek()[0]:
					self.timer.set()
					self.timer.clear()
			else:
				raise ValueError("the worker\""+repr(worker)+"was not found.")

	def run(self):
		self._exit=False
		self.timer.clear()
		while not self._exit:
			with self.modlock:
				w=self._dequeue()
				self.work(w)
				self._requeue(w)
			self.timer.wait(self.runqueue.peek()[0]-time())

	def stop(self):
		self._exit=True
		with self.modlock:
			self.timer.set()

	def work(self,workers):
		for worker in workers:
			if not self.threadpool.has_key(worker) or not self.threadpool[worker].is_alive():
				t=threading.Thread(target=worker.run)
				self.threadpool[worker]=t
				t.start()
			

	def _dequeue(self):
		"""pops worker from the queue untill the next runtime is in the future"""
		t=time()
		w=set()
		q=self.runqueue
		while q.peek([[-1]])[0]<=t:
			w.update(q.pop()[1])
		return w

	def _requeue(self,workers):
		"""Re-adds the provided workers to the run-queue"""
		t=time()
		q=self.runqueue
		for worker in workers:
			i=worker.get_interval()
			newtime=t+i-t%i
			q.add(newtime,worker)
		pass

	def _regtest_testadds():
		""">>> import worker
			>>> s=scheduler()
			>>> s.add(worker.worker(10,"foo",[None]))
			>>> s.workers
			set([worker(10,foo,[None])])
			>>> s.runqueue
			[(..., set([worker(10,foo,[None])]))]
			>>> a=abs(int(time()-time()%10+10)-s.runqueue.pop()[0] )
			>>> a <=1, a
			(True, ...)
			>>> s.add(worker.worker(317,"foo",[None]))
			>>> when=s.runqueue.peek()[0]
			>>> ival=list(s.runqueue.pop()[1])[0].get_interval()
			>>> when %ival, when >= time()
			(0, True)
			>>>
		"""
	def _regtest_testupdate():
		""">>> import worker
			>>> s=scheduler()
			>>> w=worker.worker(10,"foo",[None])
			>>> newival=17
			>>> s.add(w)
			>>> s.workers
			set([worker(10,foo,[None])])
			>>> s.change_interval(w,newival)
			>>> w2=s.runqueue.pop()
			>>> w2[0]%newival,list(w2[1])[0].get_interval()
			(0, ...)
		"""
	def _regtest_run():
		""">>> import threading
		>>> import worker
		>>> s=scheduler()
		>>> def pr(s):
		...	print "Running once"
		...	yield
		...	print "Running twice"
		...	s.stop()
		...	yield
		...	print "derp"
		>>> s.add(worker.worker(2,pr(s).next))
		>>> s.run()
		Running once
		Running twice
		"""
		# >>> threading.Thread(target=s.run).start()


	def __repr__(self):
		return repr(self.runqueue)

class _prioqueue(object):
	def __init__(self):
		self.queue=[]

	def pop(self):
		return self.queue.pop(0)

	def peek(self,defl=[]):
		""">>> q=_prioqueue()
		>>> q.add(10,"10")
		>>> time, tasks=q.peek()
		>>> time, tasks
		(10, set(['10']))
		"""
		if self.queue:
			return self.queue[0]
		else:
			return defl
	def has_item(self,data):
		""">>> q=_prioqueue()
		>>> q.add(10,"10")
		>>> q.has_item("10")
		True
		>>> q.has_item("11")
		False
		"""
		for post in self.queue:
			for task in post[1]:
				if data==task:
					return True
		return False


	def remove_item(self,data):
		"""Removes a particular item from the queue.
		Returns true if something was removed, otherwise false"""
		killist=[]
		for n,(time,post) in enumerate(self.queue):
			if data in post:
				killist.append(n)
				post.remove(data)
		for i in reversed(killist):
			post=self.queue[i]
			if len(post[1])==0:
				self.queue.pop(i)
		if len(killist)>0:
			return True
		else:
			return False


		

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

	def _regtest_testremoves():
		""">>> qt=_prioqueue()
		>>> qt.add(10,"10")
		>>> qt.add(20,"20")
		>>> qt.has_item('11')
		False
		>>> qt.add(10,"11")
		>>> qt.has_item('11')
		True
		>>> qt.remove_item('11')
		True
		>>> qt.remove_item('20')
		True
		>>> qt.remove_item('20')
		False
		>>> qt
		[(10, set(['10']))]
		"""


if __name__ == "__main__":
	import doctest
	doctest.testmod(optionflags=doctest.ELLIPSIS)

