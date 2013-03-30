#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
__author__ = 'Jesus Olmos (jolmos@isecauditors.com)'
__version__ = '0.4'

'''
	Limitaciones:
		1: 	Cuando encuentra un filename existente para, porque el server le empieza a enviar mil udps con
			el contenido, y los siguientes filenames se piensan que el ok se los da a ellos, y saldrian todos
			como positivos.

		2:	No se usan threads ni forks por la misma razon, las respuestas UDP son asincronas y no es posible
			saber a que proceso o thread estan respondiendo. Solo se me ocurre watermarkear.
'''


import time
import socket
import sys
import os
import re

class TftpClient:
	def __init__(self,timeout):
		#Opcodes
		self.PRQ = '\x00\x01'	#Read request
		self.WRQ = '\x00\x02'	#Write request
		self.DATA = '\x00\x03'	#Data
		self.ACK = '\x00\x04'	#ACK
		self.ERR = '\x00\x05'	#Error
		#Data
		self.header=''
		self.OK = '\x00\x03\x00\x01'
		self.ERR = '\x00\x05\x00\x02'
		#Error Codes
		self.UNDEFINED = '\x00\x00'
		self.NOT_FOUND = '\x00\x01'
		self.ACCESS_VIOLATION = '\x00\x02'
		self.DISK_FULL = '\x00\x03'
		self.ILLEGAL = '\x00\x04'
		self.UNKNOWN_ID = '\x00\x05'
		self.ALREADY_EXISTS = '\x00\x06'
		self.NO_SUCH_USER = '\x00\x07'
		self.NO_RESPONSE = '\x7a\x69'
		self.NOT_FOUND_MSG = re.compile('File not found',re.IGNORECASE)
		#Response
		self.ack = 0
		self.resp_error = 0
		self.resp_msg = ''
		#UDP Socket
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.settimeout(timeout)

                self.NETASCII = '\x00netascii\x00'
                self.OCTET = '\x00octet\x00blksize\x00512\x00'
                self.mode = self.NETASCII                       #NetAscii by defaul
		self.found = 0
		
	def get(self,filename,host):
		self.send(self.PRQ,filename,host)

	def put(self,filename,host):
		self.send(self.WRQ,filename,host)

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


class TftpAudit:	
	def __init__(self,timeout):
		self.tftp = TftpClient(timeout)
		self.NON_EXISTENT_FILENAME = 'adh4g21n'
		sys.stdout.flush()
		self.retorno = re.compile('\x0d|\x0a')
	
	def speech(self,msg):
		try:
			print msg
			os.popen('echo '+msg+' | festival --tts 2>/dev/null 1>&2','r')
		except:
			pass

	def check(self,host):
		print 'checking '+host
		sys.stdout.write('>> '+host)
		self.tftp.get(self.NON_EXISTENT_FILENAME, host)
		if self.tftp.resp_error != self.tftp.NO_RESPONSE:		
			self.speech('Service identified')
			sys.stdout.write('\tTFTP identified')
			if self.tftp.resp_error == self.tftp.ACCESS_VIOLATION:
				print '\tbut Denied!'
			elif self.tftp.ack:
				print '\tand is Readable!!'
			else:
				print '\tbut with errors!!'
		else:
			self.speech('No response')	
			print host+'\tNo response.'
		
	def scan(self,net,ini,end):
		end+=1
		for octet in range(ini,end):
			host = net+'.'+str(octet)
			self.tftp.get(self.NON_EXISTENT_FILENAME, host)
			sys.stdout.write(host)
			if self.tftp.resp_error != self.tftp.NO_RESPONSE:		
				self.speech('Service detected at '+host)
				sys.stdout.write('\tTFTP identified')
				if self.tftp.resp_error == self.tftp.ACCESS_VIOLATION:
					print '\tbut Denied!'
				elif self.tftp.ack:
					print '\tand is Readable!!'
				else:
					print '\tbut with errors!!'
			else:
				print '\tNo response.'
				
	def brute(self,host,wordlist):
		f = open(wordlist,'r')
		words = f.readlines()
		f.close()
		for w in words:
			if self.test(host,w):
				return

	def bof(self,host):
		evil=''
		for i in range(1,666):
			evil+='666'
		self.tftp.get(evil,host)

        def test(self,host,word):
                word = self.retorno.sub('',word)

		self.tftp.mode = self.tftp.NETASCII
                self.tftp.get(word,host)
                if self.tftp.header == self.tftp.OK:
			print word
			self.speech('netascii exist!!')
			return 1
		else:
			self.tftp.mode = self.tftp.OCTET
			self.tftp.get(word,host)
			if self.tftp.header == self.tftp.OK:
				print word
                        	self.speech('octet sream exist!!')	
				return 1
			else:
				return 0
	
		
	def end(self):
		self.tftp.end()


