#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

# CRAWL AND TXTSAVE
# c = Crawl('www.badchecksum.net')
# c.go()
# c.saveAll()

# BETTER CRAWL AND XMLSAVE
# c = Crawl2('www.test.com')
# c.login(form,user,uservalue,password,passwordvalue)
# c.go()
# xml = c.exportForms()


__version__ = "$Revision: 0004000 $"

from util.url import *
from util.util import *
from mechanize import Browser
import re


class Crawl:				#def
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




#TODO: rellenar los forms con valores aceptables y submitir para seguir crawleando
#TODO: eliminar del xml caracteres & y $  comillas en el nombre
class Crawl2:					#def
	def __init__(self,url):
		if url[-1] == '/':
			url = url[0:-1]
		u = Url()
		u.set(url)
		self.domain = u.domain
		self.url = u.url
		self.b = Browser()
		self.b.set_handle_robots(False)
		self.b.open(url)
		self.callback = None
		self.showForms = 1
		self.showLinks = 1
		self.showHtml  = 1
		self.showExtern = 1
		self.recursProgress = ""
		self.visited = []
		self.blacklist = []
		self.whitelist = []
		self.allForms=[]
		self.allLinks=[]
		self.allExterns=[]
		self.r_jsession = re.compile(';jsessionid=[^?]*')

	def clear(self):
		self.__init__(self.url)

	def login(self,form,user,uservalue,password,passwordvalue):
		self.b.select_form(form)
		self.b[user] = uservalue
		self.b[password] = passwordvalue
		self.b.submit()

	def setCallback(self,call):
		self.callback = call


	def exportForms(self,filename):
                xml='<?xml version="1.0" ?><xml>'
		r_amp = re.compile('&')
		self.allForms.sort()
		norepe=[]
		xml+='<GETS>\n'
                for f in self.allForms:
			if f.method == 'GET':
				try:
					norepe.index(f.action)
				except:
					xml+='<%s ' % f.method
					if f.name:
						xml+='name="%s" ' % f.name
					if f.action:
						f.action = r_amp.sub('&amp;',f.action)
						print "-->"+f.action
						xml+='url="%s" ' % f.action
					xml+='controls="%d">\n' % len(f.controls)
			
					for c in f.controls:
						n = c.name.replace(' ','_').replace('$','').replace('&','').replace('"','')
						try:
							if type(v.value) == type([]):
								v = ''
								for z in v.value:
									v+= z.replace('$','').replace('&','').replace('"','')
									v+=' '
							else:
								v = c.value.replace('$','').replace('&','').replace('"','')
						except:
							v = ''

						xml+='<%s type="%s" value="%s" />\n' % (n, c.type, v)
					xml+='</%s>\n' % f.method
					norepe.append(f.action)
				else:
					pass #form repe ..
			else:
				if f.method != 'POST':
					print 'method raro: '+self.method

		xml+='</GETS><POSTS>\n'
		norepe=[]
                for f in self.allForms:
			if f.method == 'POST':
				try:
					norepe.index(f.action)
				except:
					xml+='<%s ' % f.method
					if f.name:
						xml+='name="%s" ' % f.name
					if f.action:
						f.action = r_amp.sub('&amp;',f.action)
						print "-->"+f.action
						xml+='url="%s" ' % f.action
					xml+='controls="%d">\n' % len(f.controls)
			
					for c in f.controls:
						n = c.name.replace(' ','_').replace('$','').replace('&','').replace('"','')
						try:
							if type(v.value) == type([]):
								v = ''
								for z in v.value:
									v += z.replace('$','').replace('&','').replace('"','')
									v += ' '
							else:
								v = c.value.replace('$','').replace('&','').replace('"','')
						except:
							v=''
						xml+='<%s type="%s" value="%s"  />\n' % (n, c.type, v)

					xml+='</%s>\n' % f.method
					norepe.append(f.action)
				else:
					pass #form repe

		xml+='<EXTERNS>\n'	
		for l in self.allExterns:
			if l[0] != '#':
				l = r_amp.sub('&amp;',l)
				#print "-->"+f.action
				xml+='<link url="%s"/>\n' % l
		xml+='</EXTERNS>\n'	
                xml+='</POSTS></xml>\n'
		f = File()
		f.save(xml,filename)
		del f
		#return xml

	def go(self):
		#print self.recursProgress
		if self.callback:
			self.callback()


		for f in self.b.forms():
			self.allForms.append(f)
			if self.showForms:
        	        	print f

		for l in self.b.links():
			#BlackList
			linkAllowed = (l.url[0] != '#' and l.url[0:7] != 'mailto:')
			for i in self.blacklist:
				if re.compile(i).findall(l.url):
					linkAllowed=0
					break
			

			if linkAllowed:
				#if l.url[0] == '/' or l.url[0:2] == './' or l.url[0:3] == '../':
				#	l.url = self.url+l.url
				if l.url[0:4] != 'http':
					l.url = self.url+'/'+l.url

				l.url = self.r_jsession.sub('',l.url) #Quitar el ;jsesion=123asdf!-1243

               	       		try:
                               		self.visited.index(l.url)
				except:
					#White List
					white=0
					for w in self.whitelist:
						if re.compile(w).findall(l.url):
							white=1
							break

                       	       		if re.compile(self.domain).findall(l.url) or white:
						if not re.compile(self.domain).findall(l.url):
							self.url = re.compile('https?://([^/]+)/?').sub('',l.url)
							
						self.allLinks.append(l.url)
						if self.showLinks:
                       	        	       		print "\nfollowing "+l.url
                         	       		self.visited.append(l.url)
                              	       		try:
                               	              		r = self.b.follow_link(l)
                                      			#       print r.read()
							self.recursProgress += "X"
							self.go()
                                       		except:
                                               		pass
                              		else:
						self.allExterns.append(l.url)
						if self.showExtern:
                                       			print"\nNot Folloging: "+l.url
		try:
			self.recursProgress = self.recursProgress[:-1]
        		self.b.back()
		except:
			pass
