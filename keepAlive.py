#!/usr/bin/env python

import checkJackHang
import sys
import time
from optparse import OptionParser
import subprocess as sub

def logWrite(file,msg,verbose=False):
	sep="\t"
	tim=time.asctime()
	log=tim+sep+msg+"\n"
	if file:
		file.write(log)
		file.flush()
	if verbose:
		sys.stdout.write(log)
		sys.stdout.flush()

def main():
	usage="usage: %prog [options] teardownscript [scriptargs]"
	epilog="""teardownscript: is the script to be run when the jack-tests fail.
	scriptargs: might be used to supply additional arguments to the script"""
	parser = OptionParser(usage,epilog=epilog)
	parser.add_option("-l", "--logfile", dest="logfile",
		help="File to log errors to.", metavar="LOGFILE")
	parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
		help="Write logdata to stdout")
	parser.add_option("-i", "--interval",dest="interval",
		help="Interval between checks in seconds or fractional seconds, default:%default", default="60", metavar="INTERVAL")
	(options, args)=parser.parse_args()
	if len(args)<1:
		parser.error("no script supplied")

	interval=float(options.interval)
	verbose=options.verbose

	logfile=None
	if options.logfile:
		logfile=open(options.logfile,"ac")

	while True:
		status=checkJackHang.testJack()
		if  status != None:
			logWrite(logfile,str(status),verbose)
			try:
				result=sub.check_output(args,stderr=sub.STDOUT)
			except sub.CalledProcessError:
				crashlog=str(sys.exc_info()[1])+" >> "+sys.exc_info()[1].output
				crashlog=crashlog.replace("\n","  ")
				logWrite(logfile,crashlog,True)


		time.sleep(interval)

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "Keyboard Interrupt received, terminating"
