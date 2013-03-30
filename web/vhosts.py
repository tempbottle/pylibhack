#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $" 


class VHostEnumerator:					#def
	def __init__(self,webserver):
		self.webserver = webserver
		self.port = 80
		self.buffer = 1024
		self.r_location = re.compile('Location: .*')
		self.r_modified = re.compile('Modified: .*')
		self.r_date = re.compile('Date: .*')
	
	def __del__(self):
		self.sock.close()

	def connect(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.sock.connect((self.webserver,self.port))
		except:
			print 'Cannot connect!'

	def send(self,msg):
		try:
			self.sock.send(msg)
		except:
			print 'Cannot send!'

	def direct(self,word = None):
		self.connect()
		if not word:
			word = 'dominioqueseguroquenoexisteaslsdf'
		
		sys.stdout.write(word+'                     \r')
		sys.stdout.flush()

		self.send('GET http://%s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\n\r\n' % (word,word))
		resp = self.sock.recv(self.buffer)
		self.sock.close()

		resp = self.r_location.sub('',resp)
		resp = self.r_modified.sub('',resp)
		resp = self.r_date.sub('',resp)
		return resp

	def directEnumerator(self, wordlist):	# Wordlist TAD
		novhost = self.direct()[:500]
		for w in wordlist.words:
			if self.direct(w)[:500] != novhost:
				 print '\n--->'+w
		print "\nend!"
