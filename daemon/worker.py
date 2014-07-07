#!/usr/bin/env python


class worker():
	##DUMMY CODE NOT DONE
	def __init__(self._interval,test,triggers=[]):
		if interval <1:
			raise ValueError("interval must be 1 second or greater")
		self._interval=interval
		self._test=test
		self._triggers=triggers
		self._result=[]
		self.status="Initial"

	def get_interval(self):
		return self._interval

	def set_interval(self._interval):
		self._interval=interval

	def run(self):
		self.status="Running"
		self._result=self._test()
		for trigger in self._triggers:
			trigger(self._result)
		self.status="Idle"

	def get_last_result(self):
		return self._result

	def get_status(self):
		return self.status

	def __repr__(self):
		return "worker("+\
				",".join(str(i) for i in (self._interval,self._test, self._triggers))+\
				")"
