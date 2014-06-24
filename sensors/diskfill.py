#!/usr/bin/env python
import subprocess as sub

def run(device):
	"""Takes a device name and returns the used space and the total size of the device in kibibytes"""
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
"""
	avail,size=run(device)
	return "{}/{} {:.2%} used".format(humanize(avail),humanize(size),float(avail)/size)

def check(device,limits):
	"""Takes a device and a list of limit-values, returns a list of booleans.

	If the values are floats <=1 it is interpreted as a percentage of the drive-space, if its an int or >1 it is interpeted as an absolute number of kibibytes that must be free. The program then returns a list of booleans where True mean that there was more free % or Kis than the limit.
	
>>> check("/dev/null",[10**100,0.5,40])
[False, True, True]
"""
	used,size=run(device)
	avail=size-used
	perc=float(avail)/size
	res=[]
	for i in limits:
		if type(i)==float and i <=1:
			if perc >= i:
				res.append(True)
			else:
				res.append(False)
		else:
			if avail >= i:
				res.append(True)
			else:
				res.append(False)
	return res


if __name__ == "__main__":
	import doctest
	doctest.testmod()

