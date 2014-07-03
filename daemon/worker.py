#!/usr/bin/env python

class worker():
	##DUMMY CODE NOT DONE
	triggers=[]
	interval=10
	test=None
	def __init__(self,interval,test,triggers):
		self.interval=interval
		self.test=test
		self.triggers=triggers
	def get_interval(self):
		return self.interval

	def set_interval(self,interval):
		self.interval=interval
	def __repr__(self):
		return "worker("+\
				",".join(str(i) for i in (self.interval,self.test, self.triggers))+\
				")"
	def run():
		raise NotImplemented("NOT DONE")
		for trigger in triggers:
			trigger(result)
