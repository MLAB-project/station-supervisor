#!/usr/bin/env python
import subprocess as sub
import os 
import sys
def run(ntpHost):
	"""Querys a given ntp host or ntp pool and returns the time difference """
#/usr/sbin/ntpdate -q europe.pool.ntp.org
	path=os.getenv("PATH").split(":")
	path+=[p.replace("bin","sbin") for p in path if "bin" in p ]
	ntppath=None
	for p in path:
		execpath= os.path.join(p,"ntpdate")
		try:
			os.stat(execpath)
			ntppath=execpath
		except:
			pass
	assert ntppath!=None, "Could not locate the ntpdate program"
	result=sub.check_output([ntppath, "-q",ntpHost]).strip().splitlines()
	return float(result[-1].split()[-2])

def repr(device):
	return "time drift:"

def check(ntpHosts):
	"""Takes a list of host-limit tuples and returns wether the system-time differs less than the limit value from the given ntp-host
	To check that the time is off with less than one second from the europe ntp-pool (should,probably be OK)
	and with less than 0.1 ms from ntp1.sp.se (should, probably fail)
>>> check([("europe.pool.ntp.org",1.0),("ntp1.sp.se",0.0001)])
[True, False]
	"""
	res=[]
	for host,limit in ntpHosts:
		if abs(run(host))<=limit:
			res.append(True)
		else:
			res.append(False)
	return res

if __name__ == "__main__":
	import doctest
	doctest.testmod()

