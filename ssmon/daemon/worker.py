#!/usr/bin/env python

if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class worker():
	"""Class to contain periodic test case.

	Workers are fed in to a scheduler and runs periodic tests.
	The results of these tests are fed to a list of triggers.
	These Triggers should then invoke an action via the trrigger class.
	"""
	def __init__(self,interval,sensor,args,limits,triggers=[]):
		"""
		interval -- the time between runs in seconds.
		sensor   -- sensorbase-class derivative to run.
		args     -- the argument to be sent as the first argument to the
							tests  check function.
		limits   -- the second argument to the tests check()-function.
		triggers -- a trigger function receives all the Pass/Fail results
							from the check and takes appropriate action.
		        """
		if interval <1:
			raise ValueError("interval must be 1 second or greater")
		self._interval=interval
		self._sensor=sensor(args,limits)
		self.triggers=triggers
		self._status="Initial"

	def run(self):
		"""Runs the actual test and appropriate triggers.

		This method is called by the scheduler at the requested interval.
		"""
		self._status="Running"
		result=self._sensor.check()
		self._status="Proccessing triggers"
		for trigger in self.triggers:
			trigger.validate(result)
		self._status="Idle"

	def get_interval(self):
		return self._interval

	def set_interval(self,interval):
		self._interval=interval

	@property
	def result(self):
		return self._sensor.lastcheck

	@property
	def status(self):
		return self._status

	def __repr__(self):
		return "worker("+\
				", ".join(repr(i) for i in (self._interval,self._sensor,
					self.triggers))+\
				")"

	def _test_basic_run():
		"""
		>>> from sensors.dummy import dummy
		>>> w=worker(10,dummy,"Yey","NO LIMITS ALLOWED!")
		>>> w.result
		[Pass]
		>>> [str(i) for i in w.result]
		['Pass:NO LIMITS ALLOWED!']
		"""

if __name__ == "__main__":
	import doctest
	doctest.testmod()
