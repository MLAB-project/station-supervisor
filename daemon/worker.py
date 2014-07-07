#!/usr/bin/env python


class worker():
	##DUMMY CODE NOT DONE
	def __init__(self,interval,test,triggers=[]):
		if interval <1:
			raise ValueError("interval must be 1 second or greater")
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

	def run(self):
		result=self.test()
		for trigger in self.triggers:
			trigger(result)
