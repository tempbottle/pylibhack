#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
__author__ = 'Jesus Olmos (jolmos@isecauditors.com)'
__version__ = '0.1'

import time
import socket
import sys
import os
import re


class DHCP:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock.settimeout(timeout)

	def attack(self,host):
		
	


	def send(self,opcode,filename,host):
		packet = opcode+filename+self.mode
		self.sock.sendto(packet,(host,69))
		try:
			self.header = ''
			self.header = self.sock.recv(4)

			'''
			resp = self.sock.recv(666)
			if not self.NOT_FOUND_MSG.search(resp):
				self.found = 1
				print resp

			while self.sock.recv(666):
				pass

			#	print resp
			'''
					
		except:
			self.ack = 0
                        self.resp_error = self.NO_RESPONSE

	def parse(self,data):
		pass

	def end(self):
		self.sock.close()

