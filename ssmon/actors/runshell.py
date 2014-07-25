#!/usr/bin/env python

if __name__ == "__main__":
	import doctest
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import subprocess

class runshell(object):
	"""Actor to run an external command.

	The actor will not wait for the command to terminate or check if it
	is still running."""

	def __init__(self, args):
		"""
		args -- a list starting with the command to be run followed by
		any arguments"""
		if type(args) in [list,tuple]:
			self.args=args
		else:
			self.args=[args]

	def act(self):
		subprocess.Popen(self.args)
	
	def __repr__(self):
		return "runshell("+repr(self.args)+")"

	def __str__(self):
		return repr(self)

