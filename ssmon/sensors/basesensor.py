#!/usr/bin/env python
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail

class basesensor(object):
	def __init__(self,target,limits):
		"""Base class for a sensor,

		target -- A refference to what this sensor should be monitoring
		for example a device like "/dev/sda1" or similar. Even if the
		sensor does not need this it should accept an argument, might be
		None.
		
		limits -- a list of bounds which the sensors should check against
		it is upp to the sensor-implementation to decide format and if it
		should be considdered upper or lower bounds.
		"""
		self._value=None
		self._checks=None
		raise NotImplementedError("run not implemented")

	def check(self):
		"""Runs the tests and compares to the threshold values.

		returns a list of Pass and Fail objects. These should allso be
		stored inside the self._checks atribute."""
		raise NotImplementedError("check not implemented")

	@property
	def lastvalue(self):
		return self._value

	@property
	def lastcheck(self):
		return self._checks

	@property
	def repr_result(self):
		"""Should return a human readable representation of the last last
		run.
		
		for example: "19/200GiB (22.5%) used"
		"""
		raise NotImplementedError("result_repr not implemented")

	@property
	def repr_check(self):
		"""Should return a human readable representation of the last
		check. Prefferably with any fails first.
		
		for example: "<20% used (FAIL), >90GiB Free (Pass)"
		"""
		raise NotImplementedError("repr_check not implemented")

	def __str__(self):
		"""A human readable representation of the sensor.
		
		For example "Disk usage: /dev/sda1" """
		raise NotImplementedError("str not implemented")

	if __name__ == "__main__":
		import doctest
		doctest.testmod()

