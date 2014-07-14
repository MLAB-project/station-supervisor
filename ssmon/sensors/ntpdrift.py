#!/usr/bin/env python
import subprocess as sub
import os 
import sys
if __name__ == "__main__":
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.statuses import Pass,Fail
from sensorbase import sensorbase


path=os.getenv("PATH").split(":")
path+=[p.replace("bin","sbin") for p in path if "bin" in p ]
ntppath=None
for p in path:
	execpath= os.path.join(p,"ntpdate")
	try:
		os.stat(execpath)
		ntppath=execpath
		break
	except:
		pass
assert ntppath!=None, "Could not locate the ntpdate program"
	

class ntpdrift(sensorbase):
	"""Sensor to check if systems clock is in sync with an NTP source
	
	Depends on the ntpdate program.
	"""

	def __init__(self,ntpServer,limits):
		self.server=ntpServer
		self.limits=limits
		self._value=None
		self._checks=None
		
	def _run(self,ntpHost):
		"""Querys a given ntp host or ntp pool and returns the time difference"""
		result=sub.check_output([ntppath, "-q",ntpHost]).strip().splitlines()
		summaryline=result[-1].split()
		diff=summaryline[summaryline.index("sec")-1]
		self._value=float(diff)
		return self._value

	def check(self):
		"""checks the ntp-host against the limit values.

		Returns a list of Pass/Fail for each limit.

		For example to check if the time is within 2 seconds and if it
		is within 0.1ms from these servers.
	>>> ntpdrift("europe.pool.ntp.org",[2,0.00001]).check()
	[Pass, Fail]
	>>> ntpdrift("ntp1.sp.se",[2,0.00001]).check()
	[Pass, Fail]
		"""
		res=[]
		diff=self._run(self.server)
		
		for limit in self.limits:
			if abs(diff)<=limit:
				res.append(Pass())
			else:
				res.append(Fail("{} was {:.2f} seconds off".format(self.server,diff)))
		return res

	def repr_result(self):
		return "Difference between system time and {} was\
	{:.2f}".format(self.server,self._value)

	def __str__(self):
		return "Time-diff from "+self.server

if __name__ == "__main__":
	import doctest
	doctest.testmod()

