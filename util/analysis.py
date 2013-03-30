#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

class Compare:
	def __init__(self):
		self.data1 = ''
		self.data2 = ''

	def load(self,file1,file2):
		fd = open(file1)
		self.data1 = fd.read()
		fd.close()
		fd = open(file2)
		self.data2 = fd.read()
		fd.close()

	def wordPercent(self):
		if self.data1 == self.data2:
			return 100

		words1 = re.findall(' [^ ]+ ',self.data1) 
		words2 = re.findall(' [^ ]+ ',self.data2) 
		total1 = len(words1)
		total2 = len(words2)
		if total1 < total2:
			maxTotal = total2
			lessTotal = total1
		else:
			maxTotal = total1
			lessTotal = total2

		count = 0
		for i in range(0,total2):
			if words1[i] == words2[i]:
				count+=1

		return (count*100)/float(maxTotal)


class HtmlParse:			#def
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
		if not html:
			return ''
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



