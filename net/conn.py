#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "$Revision: 0004000 $"

import socket
import select
import time
import sys

class Conn:	
	def __init__(self):
		self.buffer = 100;
		self.srecv_timeout = 7
		self.select_timeout = 200

	def connectSend(self, ip, port, toSend):
		self.sock.connect(ip,port)
		self.sock.send(toSend)
		self.sock.shutdown(1)
		data = self.sock.recv(self.buffer)
		self.sock.close()
		return data

	def srecv(self):
		t0 = int(time.time())
		msg = ''
		while 1:
			(r,w,e) = select.select([self.sock],[self.sock],[self.sock],self.select_timeout)
			if r:
				y = r.pop()
				msg += y.recv(1)
				if msg[-1] == '\r' or msg[-1] == '\n':
					return msg				

			if not r and int(time.time()) > t0+self.srecv_timeout:
				return msg	


	def connect(self, ip, port):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.sock.connect((ip,port))
			print 'socket abierto '+self.sock
			return 1
		except:
			return 0

	def recv(self):
		return self.sock.recv(self.buffer)
		
		
	def send(self, msg):
		self.sock.send(msg)
		print
		return self.sock.recv(666)

	def close(self):
		self.sock.close()


