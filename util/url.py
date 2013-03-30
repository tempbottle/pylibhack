#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

# URL
# u = Url()
# u.set('http://aa.bb.bb/cc/dd.dd?e1=v1&e2=v2')
# u.path = 'ccc'
# u.params.append('e3=v3')
# u.gen()

#TODO: puerto


import re

class Url:						#def
	def __init__(self):
		self.url = ''
		self.host = ''
		self.proto = ''
		self.port = ''
		self.domain = ''
		self.path = ''
		self.cgi = ''
		self.params = {}
		self.params2 = []
	
	def gen(self):
		#TODO:Comprobar más casos				
		self.url = self.proto+'://'+self.host
		if self.path:
			self.url += self.path
		if self.cgi:
			self.url += '/'+self.cgi+'?'
			#for p in self.params2:
				#self.url += p+'&'
			for k in self.params.keys():
				self.url += '%s=%s&' % (k,self.params[k])

		return self.url


	def set(self,url):
		Url.__init__(self)
		url = re.compile('&amp;').sub('&',url)
		self.url = url
		self.proto = re.compile('https?').findall(url)[0]
		self.host = re.compile('https?://([^/]+)').findall(url)[0]
		self.domain = re.compile('[^\.]+.[^\.]+$').findall(self.host)[0]

		fullPath = re.compile('https?://[^/]+(/[^?]+)').findall(url)
		if len(fullPath)>0:
			p = re.compile('^/.+/').findall(fullPath[0])
			if len(p) > 0:
				self.path = p[0]
			x = re.compile('/([^/]+)$').findall(fullPath[0])
			if x:
				p = x[0]
				if len(p) > 0:
					self.cgi = p
		try:
			allParams = re.compile('\?(.*)').findall(url)[0]
			if allParams:
				self.params2 = re.compile('[^&]*=[^&]*').findall(allParams)
				for nom in re.compile('([^&]*)=[^&]*').findall(allParams):
					self.params[nom] = re.compile(nom+'=([^&]*)').findall(allParams)[0]
		except:
			pass

class Target(Url):						#def
	def __init__(self):
		Url.__init__(self)
		self.cookie=''
		self.post=''

	def setUrl(self,url):
		self.set(url)
	def setPost(self,post):
		self.post=post
	def setCook(self,cook):
		self.cookie=cook

class Urls:							#def
	def __init__(self):
		self.urls = []
		#Url.__init__(self)

	def load(self,file):
		fd = open(file,'r')
		self.urls = fd.readlines()
		fd.close()

	def save(self,file):
		fd = open(file,'w')
		for u in self.urls:
			fd.write(u+"\n")
		fd.close()

	def removeUrlValues(self):
		urls = []
		for u in self.urls:
			u = re.compile('\r|\n').sub('',u)
			urls.append(re.compile('=[^&]+').sub('=',u))

		self.urls = urls

	def parse(self): #sort and delete similar urls 
		urlsok=[]
		self.removeUrlValues()
		self.urls.sort()
		last=''
		for u in self.urls:
			if last != u:
				urlsok.append(u)
			last = u
		self.urls = urlsok

