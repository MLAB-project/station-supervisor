#!/usr/bin/env python
import subprocess as sub
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail
from sensorbase import sensorbase

class diskfill(sensorbase):
	"""
	Sensor to see if the usage of a disk is nearing the disks capacity.

	Relies on the -k and --output parameters to du.
	"""
	def __init__(self,device,limits):
		"""
		device -- should be a device or mount point  like /dev/sda1 or /home

		limits -- a list of values the diskfill should be compared to.
			If the values are floats between 0 an 1 it is interpreted as
			the maximum used percentage of the drive-space.

			If its an int or >1 it is interpreted as an absolute number of
			kibibytes that must be free.
		"""
		self.device=device
		self.limits=limits
		self._value=None
		self._checks=None

	def _run(self):
		"""Uses df to check the amount of free space on the associated
		device
	"""
		if self.device == "/dev/sdtest": #Hardcoded for regression-testing.
			result="""    Used 1K-blocks
			73826416  98697828 """.splitlines()
		else:
			result=sub.check_output(["df", "-k","--output=used,size",self.device],8000).splitlines()
		if len(result) <2:
			raise ValueError('Device:"'+device +'" was not found')
		elif len(result)>2:
			raise ValueError('Ambigous devicedescriptor:"'+device)
		self._value=[int(i) for i in result[1].split()]
		return self._value

	def _test_dryrun():
		"""
		for a drive like:
		Filesystem      Size  Used Avail Use% Mounted on
		/dev/sdtest      95G   71G   19G  79% /
		the output would be
		>>> d=diskfill("/dev/sdtest",[])
		>>> d._run()
		[73826416, 98697828]
		>>> d._value
		[73826416, 98697828]
		"""


	def check(self):
		"""Retreives data from the designated devic and compares to the
		saved limits. Returns a list of Succes states, Pass and Fail.


	On the same /dsv/sdtest drive  as for .run() the folowing thest will check that:
	We have at least 10GB (should be OK)
	25GB free on /dev/sdtest (should fail)
	at most 90% fill (should be OK)
	at most 70% fill (should fail)
	>>> d=diskfill("/dev/sdtest",[10**7,2.5*10**7,0.9,0.7])
	>>> d.check()
	[Pass, Fail, Pass, Fail]

	/dev/null is a bit artificial but it should be availible everywhere
	>>> d=diskfill("/dev/null",[10**100,0.5,40])
	>>> d.check()
	[Fail, Pass, Pass]
	"""
		used,size=self._run()
		avail=size-used
		perc=float(used)/size
		res=[]
		for i in self.limits:
			if type(i)==float and i <=1:
				if perc <= i:
					res.append(Pass("{:.2%} used < {:.2%}".format(perc,i)))
				else:
					res.append(Fail("{:.2%} is more than the allowed {:.2%} used space".format(perc,i)))
			else:
				if avail >= i:
					res.append(Pass("{} free > {}".format(humanize(avail),humanize(i))))
				else:
					res.append(Fail("{} is less than the allowed {} free space".format(humanize(avail),humanize(i))))
		self._checks=res
		return res

	def repr_result(self):
		""" returns a human-readable representation of the last data collected
		>>> d=diskfill("/dev/sdtest",[10**7,2.5*10**7,0.9,0.7])
		>>> d.repr_result()
		'70.41 GiB/94.13 GiB (74.80% used)'
		"""
		if self._value==None:
			self._run()
		return "{}/{} ({:.2%} used)".format(
				humanize(self._value[0]),
				humanize(self._value[1]),
				float(self._value[0])/self._value[1])

	def _test_repr_check():
		"""
		>>> d=diskfill("/dev/sdtest",[10**7,2.5*10**7,0.9,0.7])
		>>> d.check()
		[Pass, Fail, Pass, Fail]
		>>> d.repr_check()
		'Fail:23.72 GiB is less than the allowed 23.84 GiB free space, \\nFail:74.80% is more than the allowed 70.00% used space'
		>>> d=diskfill("/dev/sdtest",[10**7])
		>>> d.repr_check()
		'All Pass:70.41 GiB/94.13 GiB (74.80% used)'
		>>> d.check()
		[Pass]
		>>> d.repr_check()
		'All Pass:70.41 GiB/94.13 GiB (74.80% used)'
		"""


	def __str__(self):
		return self.device
	

def humanize(kbytes):
	"""Transforms kilobytes into larger binary units
>>> humanize(1)
'1.0 KiB'

>>> humanize(1000)
'0.98 MiB'

>>> humanize(1024)
'1.0 MiB'
"""

	factors=(
			("KiB",1),("MiB",1024.),("GiB",1024.**2),
			("TiB",1024.**3),("PiB",1024.**4),("EiB",1024.**5))
	nam,fact=factors[0]
	for i in range(len(factors)):
		if (1000**i>kbytes):
			break
		nam,fact=factors[i]
	return "{} {}".format(round(kbytes/fact,2),nam)

if __name__ == "__main__":
	import doctest
	doctest.testmod()

