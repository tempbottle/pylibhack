#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import urllib
import urllib2
import re

class IXQuick:				#def
	def __init__(self):
		self.URL_BASE = 'http://s8.eu2.ixquick.com/do/metasearch.pl?cmd=process_search&query='
		self.opn = urllib2.build_opener()
		self.INIT_PAGE = 0 #Can change this from main program
		self.MAX_PAGES = 10
		self.USER_AGENT = 'Microsoft Internet Explorer 6.0'
		self.html=''
		self.emails = []
		self.r_results = re.compile('href="([^"]+)',re.IGNORECASE)
		self.r_ixquick = re.compile('ixquick.com',re.IGNORECASE)
		self.r_email = re.compile('[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+')

	def search(self,keyword):
		self.html = ''
		self.emails = []
		for page in range(self.INIT_PAGE,self.MAX_PAGES*10,10):
			target = self.URL_BASE + keyword + '&startat=' + str(page)
			req = urllib2.Request(target)
			req.add_header('User-Agent', self.USER_AGENT)
			self.html += self.opn.open(req).read()
			self.emails += self.r_email.findall(self.html)

	def getRefs(self):
		links = []
		allLinks = self.r_results.findall(self.html)
		for l in allLinks:
			if not self.r_ixquick.findall(l) and l != '#':
				links.append(l)
		return links

	def show(self):
		for r in self.getRefs():
			print r

class Google:				#def
	def __init__(self):
		self.HOST = 'google.es'
		self.URL_BASE = 'http://www.'+self.HOST+'/search?num=100&hl=es&meta=&q='
		self.URL_TRANSLATOR = 'http://www.'+self.HOST+'/translate_t?langpair='
		self.opn = urllib2.build_opener()
		self.INIT_PAGE = 0 #Can change this from main program
		self.MAX_PAGES = 3
		self.USER_AGENT = 'Microsoft Internet Explorer 7.0'
		self.results = []
		self.r_resul = re.compile('<div class=\'?"?s\'?"?>([^"]*)<cite>')
		self.r_titulo = re.compile('<h3 class=\'?"?r\'?"?>[^>]+>([^"]*)</a>')
		self.r_em = re.compile('<em>|</em>|<b>|\.\.\.|</b>|&#[0-9]{1,7};')
		self.r_br = re.compile('<br>')
		self.r_cite = re.compile('<cite>([^<]*)<')
		self.r_link = re.compile('<h3 class="?\'?r"?\'?><a href="([^"]*)"')
		self.r_email = re.compile('[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+')
		self.html = ''
		self.links = []
		self.titulos = []
		self.descrip = []
		self.emails = []


	def search(self,keyword):
		html = ''
		for page in range(self.INIT_PAGE,((self.MAX_PAGES+1)*100),100):
			target = self.URL_BASE + keyword + '&start=' + str(page)
			req = urllib2.Request(target)
			req.add_header('User-Agent', self.USER_AGENT)
			req.add_header('HOST', self.HOST)
			html += self.opn.open(req).read()

		self.html = html
		self.titulos = self.r_titulo.findall(html)
		self.descrip = self.r_resul.findall(html)
		self.links = self.r_link.findall(html)
		self.links += self.r_cite.findall(html)
		self.emails = self.r_email.findall(html)


		for i in range(0,len(self.titulos)):
			self.titulos[i] =  self.r_em.sub('',self.titulos[i])

		for i in range(0,len(self.descrip)):
			self.descrip[i] =  self.r_em.sub('',self.descrip[i])
			self.descrip[i] =  self.r_br.sub('\n',self.descrip[i])


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
class Bing:
    def __init__(self):
        self.max_pages = 10
        self.r_dot = re.compile('\.')
        self.r_resultados = re.compile('de ([0-9\.]+) resultados')
        self.r_bloque = re.compile('<h3>.*?</p>')
        self.r_url = re.compile('href="(.*?)"')
        self.r_titulo = re.compile('">(.*?)</a>')
        self.r_texto  = re.compile('<p>(.*?)</p>')
        self.r_email1 = re.compile('@.*?\.[a-zA-Z]{1,4}') # (?[?at]?)?
        self.r_basura = re.compile('(</?strong>)|(</?b>)')
	self.r_email = re.compile('[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+')
        self.show = True
        self.clear()

    def clear(self):
        self.urls = []
        self.titulos = []
        self.textos = []
        self.mails = []
        self.allHtml = []
        self.allBlks = []
        self.regexp = None

    def results(self, html):
        res = self.r_resultados.findall(html)[0]
        res = self.r_dot.sub('',res)
        return int(res)

    def search(self,keyword):
        resp = urllib2.urlopen('http://www.bing.com/search?q=%s&filt=all&first=1' % keyword)
        html = resp.read()
        resp.close()
        limit = self.results(html)
        if limit > (self.max_pages*10):
            limit = self.max_pages*10

        for p in range(1,limit,10):
            #print "pag %d of %d" % (p,limit)
            resp = urllib2.urlopen('http://www.bing.com/search?q=%s&filt=all&first=%d' % (keyword, p))
            html = resp.read()
            resp.close()
            self.allHtml.append(html)
            self.parse(html,True)

    def parse(self,html,append=False):
            blks = self.r_bloque.findall(html)
            for blk in blks:
                blk = self.r_basura.sub('',blk)

                if self.regexp:
                        if not re.findall(self.regexp,blk):
                            continue

                url = self.r_url.findall(blk)[0]
                tit = self.r_titulo.findall(blk)[0]
                txt = self.r_texto.findall(blk)[0]

                if append:
                    self.urls.append(url)
                    self.titulos.append(tit)
                    self.textos.append(txt)

                if self.show:
                    print '-'*30
                    print tit
                    print
                    print url
                    print
                    print txt
                    print '-'*30
                    print '\n'


            #sys.stdin.readline()

#b = Bing()
#b.regexp = '[a-zA-Z0-9\._-]@serviabertis.(com|es)'
#b.search('@serviabertis.com')


'''
# Cargamos el objeto
b = Bing()

# Busqueda básica
b.search('navidad')
...

# Borramos resultados, y buscaremos solo un patron personalizado
b.clear()
b.regexp = '[a-zA-Z0-9\._-]@serviabertis.(com|es)'
b.search('@serviabertis.com')
b.search('@serviabertis.es')


# Buscaremos textos links y mails de varios keywords
b.clear()
b.show = False
b.search('hack')
b.search('hacker')
b.search('hackers')
b.search('hacking')
b.search('hacked')
b.textos
...
b.links
...
b.emails          #tiene una regexp propia para  localizar emails, aunque hagan trucos del tipo pepe[at]lepe[.]com u otras combinaciones
...
'''


