#!/usr/bin/env python
import shlex
import doctest
import sensors
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
	lexer=shlex.shlex(s,getattr(s,"name",None))
	lexer.commenters="#"
	lexer.wordchars+=".-+()/&%!?"
	lexer.whitespace=", \t"
	f=[] #could be more efficient by yeilding row instead of building this
	row=[]
	try:
		for i in lexer:
			if i.isdigit():
				row.append(int(i))
			elif i.replace(".","",1).isdigit():
				row.append(float(i))
			elif i[0] in '\'"' and i[-1]==i[0]:
				row.append(i[1:-1])
			elif "\n" in i or "\r" in i:
				f.append(row)
				row=[]
			elif i:
				row.append(i)
		if len(row)>0:
			f.append(row)
		return f
	except ValueError,ex:
		raise ValueError(lexer.error_leader()+ ex.message)

def _regtest_splitparse_fail_quote():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('[Section]\\ndata="foo')
	>>> s.name="myFile"
	>>> splitfile(s)
	Traceback (most recent call last):
	ValueError: "myFile", line 2: No closing quotation
	"""


def parse(filename):
	try:
		if hasattr(filename,"read"):
			f=filename
		else:
			f= open(filename,"r")
		config=splitfile(f)
	finally:
		f.close()
	
	structure={"server":{}, "workers":[], "triggers":[], "actors":[]}
	section=None
	stack=[]
	errors=[]
	for i in config:
		if i[0]=="[" and i[-1]=="]":
			if len(i) >= 3:
				oldsection=section
				section=i[1].lower()
				if oldsection:
					parse_section(structure,oldsection,stack,errors)
					stack=[]
		else:
			stack.append(i)
	parse_section(structure,section,stack,errors)
	if errors:
		print errors
	return structure

def parse_section(structure,section,stack,errors):
	classes={"actor":parse_actor,"server":parse_server,
			"tigger":parse_trigger,"worker":parse_worker}
	try:
		classes[section](structure,section,stack)
	except Exception, e:
		errors.append(e)


def parse_actor(structure,section,stack):
	pass

def parse_server(structure,section,stack): 
	if len(structure["server"])>0:
		raise ValueError("Dupplicate server entry!")
	opts={}
	args=dict([i for i in post if i!="="] for post in stack)
	opts["port"]=args.pop("port",41133)
	opts["hostname"]=args.pop("hostname","localhost")
	structure["server"]=opts
	if len(args)!=0:
		raise RuntimeWarning("Un-used arguments to server: "+repr(args.keys()))

def parse_trigger(structure,section,stack):
	pass
def parse_worker(structure,section,stack):
	opts={}
	args=dict([i for i in post if i!="="] for post in stack)
	pass

def _regtest_serverparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('[server]\\nport=1010\\nhostname="foo"')
	>>> p=parse(s)
	>>> p["server"]["port"]
	1010
	>>> p["server"]["hostname"]
	'foo'
	>>> s=StringIO.StringIO('[server]\\nport=1010\\nhostname="foo"\\nmung="mung"\\n')
	>>> s.name="myFile"
	>>> p=parse(s)
	[RuntimeWarning("Un-used arguments to server: ['mung']",)]
	"""

def _regtest_workerparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('''[worker]\\n\
	interval=10\\n\
	sensor="dummy"''')
	>>> s.name="myFile"
	>>> p=parse(s)
	"""

if __name__ == "__main__":
	doctest.testmod(optionflags=doctest.ELLIPSIS)

