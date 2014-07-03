#!/usr/bin/env python
import asynchat

if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.statuses import Pass,Fail

DEFPORT=41133		#Linux ephemeral base 32768 + 8365
from asynchat_echo_handler import EchoHandler

class Dispatcher(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(1)
        return

    def handle_accept(self):
        client_info = self.accept()
        EchoHandler(sock=client_info[0])
        self.handle_close() ##DEBUGGING ONLY
        return
    
    def handle_close(self):
        self.close()

class http_request_handler(asynchat.async_chat):

    def __init__(self, sessions, log):

def _regtest_basicConnectivity():
	""">>> s=socket.socket()
>>> s.connect( ('127.0.0.1', 41133))
>>> s.send('["noop"]\\n')
9
>>> s.recv(100)
'[];'
"""
	pass
if __name__ == "__main__":
	import socket
	import doctest
	doctest.testmod()

