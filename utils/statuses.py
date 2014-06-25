#!/usr/bin/env python

class Status(object):
	"""Base class for returning more information about the status of a test """
	__name__="unknown"
	message=""
	def __init__(self,name):
		self.__name__=name

	def __nonzero__(self):
		raise NotImplementedError( "must be superclassed")

	def __repr__(self):
		return self.__name__

	def __str__(self):
		return self.__name__+self.message

	def getmsg(self):
		return self.message


class Pass(Status):
	"""Extended class for returning more information about the status of a passed test
>>> res=Pass("Everything is functioning")
>>> res
Pass
>>> res.getmsg()
'Everything is functioning'
>>> bool(res)
True
"""
	message=""
	def __init__(self,message=""):
		super(Pass,self).__init__("Pass")
		self.message=message

	def __nonzero__(self):
		return True


class Fail(Status):
	"""Extended class for returning more information about the status of a passed test
>>> res=Fail("Error: modem on fire")
>>> res
Fail
>>> res.getmsg()
'Error: modem on fire'
>>> bool(res)
True
"""
	message=""
	def __init__(self,message=""):
		super(Fail,self).__init__("Fail")
		self.message=message

	def __nonzero__(self):
		return False
