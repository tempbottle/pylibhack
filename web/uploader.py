# -*- coding: utf8 -*- 

import pycurl
import base64
import socket
import StringIO


class Uploader:
	def __init__(self):
		self.setTimeout(5)
		self.ua = 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'
		self.headers = []
		self.multipart = False

	def init(self):
		c = pycurl.Curl()
		c.setopt(pycurl.SSL_VERIFYPEER, False)
		c.setopt(pycurl.SSL_VERIFYHOST, False)
		c.setopt(pycurl.USERAGENT, self.ua)
		return c
		
	def setMultipart(self):
		self.multipart = True
		self.headers.append('Content-Type: multipart/form-data')
		

	def setHeader(self,header):
		self.headers.append(header)

	def setAuth(self,user,passwd):
		token = base64.b64encode(user+':'+passwd)
		self.headers.append('Authorization: Basic %s' % token)

	def setTimeout(self,tmout):
		socket.setdefaulttimeout(tmout)

	def go(self,url,post=None):
		c = self.init()
		buff = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, buff.write)
		c.setopt(pycurl.HTTPHEADER, self.headers)
		c.setopt(pycurl.URL, url)

		if post:
			c.setopt(pycurl.POST, 1)
			c.setopt(pycurl.POSTFIELDS, post)
			#self.c.setopt(pycurl.HTTPPOST, [('',post)])
		else:
			c.setopt(pycurl.POST, 0)

		c.perform()
		#c.close()
		return buff.getvalue()


