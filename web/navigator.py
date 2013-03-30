#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net
import urllib
import urllib2
import base64
from mechanize import Browser


# NAVIGATOR   (clase browser experimental, mirar tambien spidermonkey)
# nav = Navigator()
# htm = nav.go('www.badchecksum.net')
# p = HtmlParse()    (utils/analysis.py)
# lnks = p.getLinks(htm)



class Navigator:						#def
	def __init__(self,cookie=None):
		self.opn = urllib2.build_opener()
		self.cookie = cookie
		self.auth = None
		self.authHash = None
		self.headers = {}
		self.addHeader('User-agent','Microsoft Internet Explorer 6.0')

	def urlencode(self,data):
                res = ''
                for b in data:
                        z = hex(ord(b))
                        res += re.sub('0x','%',z)
                return res

	def urldecode(self,data):
                bytes = data.split('%')
                res = ''
                for b in bytes:
			if b:	
				res += chr(int(b,16))
                return res

	def setCookie(self,cookie):
		self.cookie = cookie
		self.addHeader('Cookie',cookie)

	def setProxy(self,host,port,user=None,passwd=None):
		if not user or not passwd:
			l_proxy_support = urllib2.ProxyHandler({"http" : "http://%s:%s" % (host,port)})
		else:
			l_proxy_support = urllib2.ProxyHandler({"http" : "http://%s:%s@%s,%s" % (user,passwd,host,port)})

		self.opn = urllib2.build_opener(l_proxy_support, urllib2.HTTPHandler)

	def setAuth(self,mode,user,passwd):
		self.auth = mode
		self.authHash =  base64.encodestring('%s:%s' % (user, passwd))[:-1]

	def addHeader(self,header,value):
		self.headers.update({header:value})

	def go(self,url,postStr=None):
		if postStr:
			req = urllib2.Request(url,postStr)
		else:
			req = urllib2.Request(url)

		for k in self.headers.keys():
			req.add_header(k,self.headers[k])

		if self.auth:
			req.add_header("Authorization", self.auth+' '+self.authHash)

		try:
			hndl = self.opn.open(req)
			resp = hndl.read()
			if not hndl.fp.closed:
				hndl.fp.close()

		#except IOError, e:
		#	if e.code == 401:
		#		self.realm = e.headers['www-authenticate']
		#	resp = ""

		except:
			resp = ""

		return resp



class Bro(Browser):
	def __init__(self):
		Browser.__init__(self)
		self.set_handle_robots(False)
		self.myhistory=[]
		self.resp = None
		self.lnks = []
		self.frms = []

	def __del__(self):
		Browser.__del__(self)
		del self.lnks
		del self.frms
		del self.resp
		del self.myhistory

	def help(self):
		print "Navigation Methods:"
		print "\turl(url)"
		print "\tback()"
		print "\treload()"
		print "\tdoClick(idLink)"
		print "\tdoSubmit(idForm)\n"
		print "Response Methods:"
		print "\tshowLinks()"
		print "\tshowForms()"
		print "\thtml()"
		print "\theaders()"
		print "\ttitle()\n"
		print "Config Methods:"
		print "\thttpAuth(url,user,password)"
		print "\tformAuth(form,user,password)"
		print "\tproxy(host,port,user,password,proto)   default proto is http, user and password are optional"
		print "\tdiscoverProxy()\n\n"

	def __setitem__(self,key,value):
		Browser.__setitem__(self,key,value)

	#NAVIGATION
	def url(self,url):
		try:
			self.resp = self.open(url)
			self.myhistory.append(url)
		except HTTPError, e:
			pass
		except:
			print "Cannot go"

	def back(self):
		url = self.myhistory.pop()
		self.open(url)

	#def reload(self):

	def doClick(self,idLink):
		self.follow_link(self.lnks[idLink])

	def doSubmit(self,idForm):
		self.select_form(self.frms[idForm])
		self.submit()

	#RESPONSE
	def showLinks(self):
		id = 0
		self.lnks=[]
		for l in self.links():
			print '%d %s' % (id,l.url)
			self.lnks.append(l)
			id += 1

	def showForms(self):
		id = 0
		self.frms=[]
		for f in self.forms():
			print '\n** form %d **\n%s' % (id,f)
			self.frms.append(f.name)
			id +=1

	def html(self):
		print self.resp.get_data()

	def headers(self):
		print self.resp.info().headers

	#def title(self):

	#AUTH
	def httpAuth(self,url,user,pwd):
		self.add_password(url,user,pwd)

	def formAuth(self,user,pwd):
		#self.b.select_form()
		#self.b.submit()
		pass

	def discoverProxy(self):
		pass
		
	def proxy(self,host,port,user=None,pwd=None,proto=None):
		if not proto:
			proto = "http"

		if user and pwd:
			str = '%s:%s@%s:%d' % (user,pwd,host,port)
		else:
			str = '%s:%d' % (host,port)

		self.set_proxies({proto:str})


