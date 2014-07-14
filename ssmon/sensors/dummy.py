#!/usr/bin/env python
import subprocess as sub
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail

from sensorbase import sensorbase

class dummy(sensorbase):
	"""Dummy, allways returns one Pass"""
	def __init__(self,servers,limits):
		self.limits=limits
		self._value=None
		self._checks=[Pass(arg),Pass(limits)]
		
	def check(self):
		return self._checks

	def repr_result(self):
		return "Dummycheck: a-alright!"
	def __str__(self):
		return "Dummy, allways returns one Pass"

if __name__ == "__main__":
	import doctest
	doctest.testmod()

