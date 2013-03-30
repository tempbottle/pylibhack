#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"



#TODO: pensar TAD ip
class IP:					#def
	def __init__(self,addr=None):
		self.addr = addr
	
	def alive(self):
		pass
		#ping, host, 



class IPv6:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

