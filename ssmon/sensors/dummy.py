#!/usr/bin/env python
import subprocess as sub
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail

def run(arg="noarg"):
	return [arg]
	

def repr(arg):
	return "dummy testclass called with: " +arg

def check(arg,limits):
	return [new Pass(arg),Pass(limits)]


if __name__ == "__main__":
	import doctest
	doctest.testmod()

