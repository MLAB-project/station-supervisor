#!/usr/bin/env python


class worker():
	"""Class to contain periodic test case.

	Workers are fed in to a scheduler and runs periodic tests.
	The results of these tests are fed to a list of triggers.
	These Triggers should then invoke an action via the trrigger class.
	"""
	def __init__(self,interval,test,args,limits,triggers=[]):
		"""
		interval -- the time between runs in seconds.
		test     -- name of the test-module to run.
		args     -- the argument to be sent as the first argument to the
							tests  check function.
		limits   -- the second argument to the tests check()-function.
		triggers -- a trigger function receives all the Pass/Fail results
							from the check and takes appropriate action.
		        """
		if interval <1:
			raise ValueError("interval must be 1 second or greater")
		self._interval=interval
		self._test=test
		self._args=args
		self._limits=limits
		self._triggers=triggers
		self._result=[]
		self.status="Initial"

	def run(self):
		"""Runs the actual test and appropriate triggers.

		This method is called by the scheduler at the requested interval.
		"""
		self.status="Running"
		self._result=self._test.check(self._arg,self._limits)
		self.status="Proccessing triggers"
		for trigger in self._triggers:
			trigger.validate(self._result)
		self.status="Idle"

	def get_interval(self):
		return self._interval

	def set_interval(self,interval):
		self._interval=interval

	def get_last_result(self):
		return self._result

	def get_status(self):
		return self.status

	def __repr__(self):
		return "worker("+\
				", ".join(repr(i) for i in (self._interval,self._test,
					self._args, self._limits, self._triggers))+\
				")"
