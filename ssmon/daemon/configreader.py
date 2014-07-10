#!/usr/bin/env python
import shlex
import doctest

if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def splitfile(s):
	"""Splits a string or file-like object and returns a list of numbers
	and strings for each row
	>>> splitfile("foo,bar")
	[['foo', 'bar']]
	>>> splitfile("a= 1,2, 3")
	[['a', '=', 1, 2, 3]]
	>>> splitfile('a="1,2, 3"')
	[['a', '=', '1,2, 3']]
	>>> import StringIO
	>>> splitfile(StringIO.StringIO('[Section]\\ndata=foo'))
	[['[', 'Section', ']'], ['data', '=', 'foo']]
	"""
	lexer=shlex.shlex(s)
	lexer.commenters="#"
	lexer.wordchars+=".-+()/&%!?"
	lexer.whitespace=", \t"
	f=[]
	row=[]
	for i in lexer:
		if i.isdigit():
			row.append(int(i))
		elif i.replace(".","").isdigit():
			row.append(float(i))
		elif i[0] in '\'"' and i[-1]==i[0]:
			row.append(i[1:-1])
		elif "\n" in i or "\r" in i:
			f.append(row)
			row=[]
		elif i:
			row.append(i)
	f.append(row)
	return f
def parse(filename):
	config = ConfigParser.ConfigParser()
	config.read("c:\\tomorrow.ini")


if __name__ == "__main__":
	doctest.testmod()

