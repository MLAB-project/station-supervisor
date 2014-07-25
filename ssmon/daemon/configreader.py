#!/usr/bin/env python
import shlex
import doctest
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import sensors
import triggers
import actors
from worker import worker 
lexer=None #Slightly horrible to simplify error-handling.

def splitfile(s):
	"""Break a file or string down in to tokens
	
	This breaks a file or a string in to a list of list where each
	list represents a row in the in-file. Each such sub-list is then
	poppulated with the string-and numeric tokens found on that row.
	>>> list(splitfile("foo,bar"))
	[['foo', 'bar']]
	>>> list(splitfile("a= 1,2, 3"))
	[['a', '=', 1, 2, 3]]
	>>> list(splitfile('a="1,2, 3"'))
	[['a', '=', '1,2, 3']]
	>>> import StringIO
	>>> list(splitfile(StringIO.StringIO('[Section]\\ndata=foo')))
	[['[', 'Section', ']'], ['data', '=', 'foo']]
	"""
	global lexer
	lexer=shlex.shlex(s,getattr(s,"name",None))
	lexer.commenters="#"
	lexer.wordchars+=".-+()/&%!?"
	lexer.whitespace=", \t"
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
				yield row
				row=[]
			elif i:
				row.append(i)
		if len(row)>0:
			yield row
	except ValueError,ex:
		raise ValueError(lexer.error_leader()+ ex.message )

def _regtest_splitparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('str=foo\\nnum=1\\nnumlist=1,2,3')
	>>> list(splitfile(s))
	[['str', '=', 'foo'], ['num', '=', 1], ['numlist', '=', 1, 2, 3]]
	"""

def _regtest_splitparse_fail_quote():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('[Section]\\ndata="foo')
	>>> s.name="myFile"
	>>> list(splitfile(s))
	Traceback (most recent call last):
	ValueError: "myFile", line 2: No closing quotation
	"""


def parse(filename):
	"""
	blablablabla....

	filename -- might be a string representing a file to read or an 
						open file-descriptor, it will be closed when the
						parser terminates.
	"""
	try:
		if hasattr(filename,"read"):
			f=filename
		else:
			f= open(filename,"r")
		config=splitfile(f)
	finally:
		pass
		#f.close()
	
	structure={"server":{}, "workers":[], "triggers":{}, "actors":{}}
	section=None
	stack=[]
	errors=[]
	for i in config:
		if len(i)==3 and i[0]=="[" and i[-1]=="]":
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
	classes={"actor":parse_actor,"noop":lambda x,y,z: None ,"server":parse_server,
			"trigger":parse_trigger,"worker":parse_worker}
	try:
		classes[section](structure,section,stack)
	except Exception, e:
		errors.append(e)
		raise ##DEBUG


def parse_actor(structure,section,stack):
	opts={}
	#args=dict([i for i in post if i!="="] for post in stack)
	args=dictify(stack)
	actorname=args["name"][0]
	if structure["actors"].has_key(actorname):
		raise ValueError(lexer.error_leader()+" Dupplicate actor: "+actorname)
	actortype=args["type"][0]
	actorargs=args.get("arg",args.get("args",[]))
	actor=getattr(getattr(actors,actortype),actortype)(actorargs)
	structure["actors"][actorname]=actor

def parse_server(structure,section,stack): 
	if len(structure["server"])>0:
		raise ValueError(lexer.error_leader()+"Dupplicate server entry!")
	opts={}
	args=dict([i for i in post if i!="="] for post in stack)
	opts["port"]=args.pop("port",41133)
	opts["hostname"]=args.pop("hostname","localhost")
	structure["server"]=opts
	if len(args)!=0:
		raise RuntimeWarning(lexer.error_leader()+\
				"Above. Un-used arguments to server: "+\
				repr(args.keys()))

def parse_trigger(structure,section,stack):
	pass

def parse_worker(structure,section,stack):
	opts={}
	#args=dict([post[0],post[2:]] for post in stack)
	args=dictify(stack)
	sensorclass=getattr(sensors,args["sensor"][0])
	sensor=getattr(sensorclass,args["sensor"][0])

	trigg=[getattr(triggers,i) for i in args.get("triggers",[])]

	workerargs=args.get("args",[None])
	limits=args["limits"]
	w=worker(args["interval"][0],sensor,workerargs,limits,trigg)
	structure["workers"].append(w)

def dictify(struct):
	args={}
	n=0
	for post in struct:
		if len(post)==0:
			continue
		name=post[0].lower()
		if args.has_key(name):
			raise SyntaxError(lexer.error_leader() +"Near, dupplicate atribute:" +name )
		if len(post)<=2:
			args[name]=[]
		elif post[1]=="=":
			n+=1
			args[name]=post[2:]
		else:
			raise SyntaxError(lexer.error_leader() +"malformed command")
	return args

def _regtest_serverparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('[server]\\nport=1010\\nhostname="foo"')
	>>> p=parse(s)
	>>> p["server"]["port"]
	1010
	>>> p["server"]["hostname"]
	'foo'
	>>> s=StringIO.StringIO('[server]\\nport=1010\\n\
			hostname="foo"\\nmung="mung"\\n[noop]\\n#noop\\n#noop')
	>>> s.name="myFile"
	>>> p=parse(s)
	[RuntimeWarning('"myFile", line 6: Above. Un-used arguments to server: [\\'mung\\']',)]
	"""

def _regtest_workerparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('''[worker]\\n\
	interval=10\\n\
	sensor="dummy"\\n\
	args=arg\\n\
	limits=1, 9000\\n\
	#triggers=""\\n\
	''')
	>>> p=parse(s)
	>>> p["workers"]
	[worker(10, Dummy, allways returns one Pass, [])]
	"""

def _regtest_actorparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('''[actor]\\n\
	type=runshell\\n\
	name="shell_echo"\\n\
	arg=echo, test\\n\
	''')
	>>> p=parse(s)
	>>> p["actors"]
	{'shell_echo': runshell(['echo', 'test'])}
	>>> p["actors"]["shell_echo"].act()
	>>> #should print test, not captured by doctest
	"""

def _regtest_triggerparse():
	"""
	>>> import StringIO
	>>> s=StringIO.StringIO('''[actor]\\n\
	type=runshell\\n\
	name="reboot"\\n\
	arg=echo, "test won't reboot"\\n\
	\\n\
	[trigger]\\n\
	name="rebootonallfail"\\n\
	trigger=allfail\\n\
	effect=reboot\\n\
	''')
	>>> p=parse(s)
	>>> p["triggers"]
	{rebotonallfail(allfail(['echo', 'test won\'t reboot']))}
	"""

if __name__ == "__main__":
	doctest.testmod(optionflags=doctest.ELLIPSIS)

