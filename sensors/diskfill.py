#!/usr/bin/env python
import subprocess as sub
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail

def run(device):
	"""Takes a device name and returns the used space and the total size of the device in kibibytes.
for a drive like:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdtest      95G   71G   19G  79% /
the output would be
>>> run("/dev/sdtest")
[73826416, 98697828]
"""
	if device == "/dev/sdtest": #Hardcoded for regression-testing.
		result="""    Used 1K-blocks
		73826416  98697828 """.splitlines()
	else:
		result=sub.check_output(["df", "-k","--output=used,size",device],8000).splitlines()
	if len(result) <2:
		raise ValueError('Device:"'+device +'" was not found')
	elif len(result)>2:
		raise ValueError('Ambigous devicedescriptor:"'+device)
	return [int(i) for i in result[1].split()]

def humanize(kbytes):
	"""Transforms kilobytes into larger binary units
>>> humanize(1)
'1.0 KiB'

>>> humanize(1000)
'0.98 MiB'

>>> humanize(1024)
'1.0 MiB'
"""

	factors=(("KiB",1),("MiB",1024.),("GiB",1024.**2),("TiB",1024.**3),("PiB",1024.**4),("EiB",1024.**5))
	nam,fact=factors[0]
	for i in range(len(factors)):
		if (1000**i>kbytes):
			break
		nam,fact=factors[i]
	return "{} {}".format(round(kbytes/fact,2),nam)


def repr(device):
	"""Returns the diskusage of a named device in a "human readable form"

>>> repr("/dev/null")
'0.0 KiB/1.92 GiB 0.00% used'

>>> repr("/dev/sdtest")
'70.41 GiB/94.13 GiB 74.80% used'

"""
	avail,size=run(device)
	return "{}/{} {:.2%} used".format(humanize(avail),humanize(size),float(avail)/size)

def check(device,limits):
	"""Takes a device and a list of limit-values, returns a list of booleans.

	If the values are floats between 0 an 1 it is interpreted as the maximum used percentage of the drive-space, if its an int or >1 it is interpeted as an absolute number of kibibytes that must be free. The program then returns a list of booleans where Pass mean that there was more free % or Kis than the limit.

On the same /dsv/sdtest drive  as for .run() the folowing thest will check that:
We have at least 10GB (should be OK)
25GB free on /dev/sdtest (should fail)
at most 90% fill (should be OK)
at most 70% fill (should fail)
>>> check("/dev/sdtest",[10**7,2.5*10**7,0.9,0.7])
[Pass, Fail, Pass, Fail]

/dev/null is a bit artificial but it should be availible everywhere
>>> check("/dev/null",[10**100,0.5,40])
[Fail, Pass, Pass]
"""
	used,size=run(device)
	avail=size-used
	perc=float(used)/size
	res=[]
	for i in limits:
		if type(i)==float and i <=1:
			if perc <= i:
				res.append(Pass())
			else:
				res.append(Fail("{:.2%} is more than the allowed {:.2%} used space".format(perc,i)))
		else:
			if avail >= i:
				res.append(Pass())
			else:
				res.append(Fail("{} is less than the allowed{} free space".format(humanize(avail),humanize(i))))
	return res


if __name__ == "__main__":
	import doctest
	doctest.testmod()

