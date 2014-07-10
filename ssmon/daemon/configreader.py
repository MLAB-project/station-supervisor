#!/usr/bin/env python
import shlex
import doctest

if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def split(s):
	"""Splits a string and returns a list of numbers and strings
	>>> split("foo,bar")
	['foo', 'bar']
	>>> split("a=1,2, 3")
	['a', '=', 1, 2, 3]
	>>> split('a="1,2, 3"')
	['a', '=', '1,2, 3']
	"""
	lexer=shlex.shlex(s)
	lexer.commenters="#"
	lexer.wordchars+=".-+()/&%!?"
	lexer.whitespace+=","
	r=[]
	for i in lexer:
		if i.isdigit():
			r.append(int(i))
		elif i.replace(".","").isdigit():
			r.append(float(i))
		elif i[0] in '\'"' and i[-1]==i[0]:
			r.append(i[1:-1])
		elif i:
			r.append(i)

	return r
def parse(filename):
	config = ConfigParser.ConfigParser()
	config.read("c:\\tomorrow.ini")


if __name__ == "__main__":
	doctest.testmod()

