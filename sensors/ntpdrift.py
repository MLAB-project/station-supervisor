#!/usr/bin/env python
import subprocess as sub
import os 
import sys
if __name__ == "__main__":
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail

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
	

def run(ntpHost):
	"""Querys a given ntp host or ntp pool and returns the time difference """
	result=sub.check_output([ntppath, "-q",ntpHost]).strip().splitlines()
	summaryline=result[-1].split()
	diff=summaryline[summaryline.index("sec")-1]
	return float(diff)

def repr(host):
	return "time drift relative to {}: {:.2f}".format(host,run(host))

def check(ntpHosts):
	"""Takes a list of host-limit tuples and returns wether the system-time differs less than the limit value from the given ntp-host
	To check that the time is off with less than one second from the europe ntp-pool (should,probably be OK)
	and with less than 0.1 ms from ntp1.sp.se (should, probably fail)
>>> check([("europe.pool.ntp.org",1.0),("ntp1.sp.se",0.0001)])
[Pass, Fail]
	"""
	res=[]
	for host,limit in ntpHosts:
		diff=run(host)
		if abs(diff)<=limit:
			res.append(Pass())
		else:
			res.append(Fail("{} was {:.2f} seconds off".format(host,diff)))
	return res

if __name__ == "__main__":
	import doctest
	doctest.testmod()

