Jack Deamon Monitor
===================

This program validates that it is possible to connect to the Jack-deamon. If connection fails it executes an arbitrary script which supposedly will attempt to restart jackd and associated processes.

it depends on py-jack which is availible via
	pip install py-jack

Usage example:
--------------
To check if jackd is still running and responding every two minutes, if not run recover.sh

	keepJackAlive.py -i 120 recover.sh

It can be made more verbose by using the -v flag or logging to a file with the -l flag. More usage help is availible via the -h flag.

Furhter notes:
--------------
It can be disowned or nohuped but currently does not do so on its own accord.
