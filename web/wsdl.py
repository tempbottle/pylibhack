#!/usr/bin/python
import re
import sys
import urllib2
from navigator import *

'''
Raw quick and adaptable wsdl accessing  wsdl v2 support
jolmos@isecauditors.com
'''

#TODO: comillas simples

class LibWSDL:
	def __init__(self):
		self.nav = Navigator()
		self.nav.addHeader('Content-type','text/xml; charset=utf-8')
		#self.nav.setProxy('127.0.0.1','8080')  #Useful for debugging
		self.url = ''
		self.wsdl = ''
		self.target = ''
		self.showErrors = 0
		self.methods = []
		self.soap = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/1999/XMLSchema" ><SOAP-ENV:Body>'
		self.endSoap = '</SOAP-ENV:Body></SOAP-ENV:Envelope>'

	def __del__(self):
		try:
			del self.nav
		except:
			pass
	
	def load(self,url):
		self.url = url
		self.wsdl = self.nav.go(url)
		self.wsdl = re.sub('\r|\n','',self.wsdl)
		self.methods = re.findall('<element name="([^"]+)">',self.wsdl)
		#self.methods.sort()

	def list(self):
		for m in w.methods:
			print m
			for p in w.params(m):
				print '%s\t%s' % (p[0],p[1])
				print ''

	def params(self,method):
		ini = self.wsdl.find('<element name="'+method+'">')
		fin = ini + self.wsdl[ini:].find('</element>')
		ini += 10
		return re.findall('<element name="([^"]*)" [^>]*type="([^"]+)"',self.wsdl[ini:fin])

	#sample: launch('getBanco',[('codBanco','xsd:short','1')])

	def promptParams(self,method):
		parms = []
		pl = self.params(method)
		for p in pl:
			sys.stdout.write('(%s) %s: ' %(p[1],p[0]))
			input = sys.stdin.readline()[:-1]
			parms.append([p[0],p[1],input])
		return parms


	def launch(self,method,params):
		self.nav.addHeader('SOAPAction',method)

		envelop  = '<%s SOAP-ENC:root="1">' % method
		for p in params:
			envelop += '<%s xsi:type="%s">%s</%s>' % (p[0],p[1],p[2],p[0])
		envelop += '</%s>' % method
	
		post = self.soap + envelop + self.endSoap
                resp = self.nav.go(self.url,post)
		#r = re.findall('<soapenv:Body>(.*)</soapenv:Body>',resp)
		r = re.findall('<'+method+'[^>]+>(.*)</'+method,resp)
		if r:
			return r[0]

		if self.showErrors:
			return 'Err:\n'+resp
		else:
			return ''



class WSDLDebug(LibWSDL):
	def __init__(self):
		LibWSDL.__init__(self)

	def __del__(self):
		LibWSDL.__del__(self)

	def list(self):
		z = '--- Methods: ---\n'
		for m in self.methods:
			z += m
			z += '\n'
		z +='-'*16
		z += '\n'
		return z


	def listParams(self,method):
		parms = self.params(method)
		z = '\n- Name ---------------- Type -----\n'
		for p in parms:
			z += '%s\t\t%s\n' % (p[0],p[1])
		z += '-'*35 
		z += '\n'
		return z


