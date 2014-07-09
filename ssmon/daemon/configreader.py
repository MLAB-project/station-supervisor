#!/usr/bin/env python
import ConfigParser
if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse(filename):
	config = ConfigParser.ConfigParser()
	config.read("c:\\tomorrow.ini")


if __name__ == "__main__":
	doctest.testmod()

