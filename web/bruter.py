#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"


from util.wordlist import *
from mechanize import *
import threading
import re


class WebBruter(Wordlist):
	def __init__(self):
		Wordlist.__init__(self)
		self.b = Browser()
		self.b.set_handle_robots(False)
		self.mutex = 1
		self.sem = threading.BoundedSemaphore(value=self.mutex)
		self.threads = []
		self.numthreads = 2
		self.badguy = ''
		self.attackStack = []
		self.running = 1
		self.r_vector = re.compile('#')
		self.numwordsattack = 0
		self.results = []
		#self.bd = 

	def auth(self,url,user,pwd):
		self.b.add_password(url,user,pwd)

	def status(self):
		self.sem.acquire()
		if self.running:
			sys.stdout.write("Running, ")
		else:
			sys.stdout.write("Stopped, ")
		l = len(self.attackStack)
		self.sem.release()
		t = self.numwordsattack

		print "%d%%  %d words remain." %  ((int(((t-l)/float(t))*100)), len(self.attackStack))

	def watch(self,sec=None):
		if not sec:
			sec = 15
		while self.running:
			self.status()
			time.sleep(sec)

	def stop(self):
		self.sem.acquire()
		self.running = 0
		self.attackStack = []
		self.numwordsattack = 0
		self.sem.release()

	def scan(self,url,post=None): 		# http://#.test.com/#/#.php?#=#  se reemplaza # por la wordlist 
		for w in self.words:
			try:
				target = self.r_vector.sub(w,url)
			except:
				continue
			self.attackStack.append(target)

		self.numwordsattack = len(self.attackStack)

		for i in range(0,self.numthreads):
			th = threading.Thread(target=self._attack, kwargs={})
			th.start()
			#th.join()
			self.threads.append(th)

	def _attack(self):
		self.running = 1
		while self.running:
			a = None
			self.sem.acquire()
			if self.attackStack:
				a = self.attackStack.pop()
			self.sem.release()
			if not a:
				print "Done."
				return
			try:
				#print "conectando a "+a
				r = self.b.open(a)
				data = r.get_data()
				if not re.findall(self.badguy,data):
					print 'sucess --> '+a	
		
				self.results.append(a)
			except HTTPError, e:
				if e.code != 404:
					print '->'+a
					self.results.append(a)
				elif e.code == 404:
					print '(404)'
			except:
				pass
				#self.sem.acquire()
				#self.attackStack.append(a)
				#self.sem.release()

		print "Stoped."

	def scan_slow(self):
		base = self.path
		progress = 0
		total = len(self.words)
		for w in self.words:
			sys.stdout.write("%.2d%%  \r" % (int((progress/float(total))*100)))
			sys.stdout.flush()	
			self.path = base+'/'+w+'/'
			try:
				htm = self.b.open(self.gen())
				self.path = base
				print "\n"+w
			except HTTPError, e:
				if e.code != 404:
					print "\n"+w
			self.path = base
			progress+=1
		print "Done."
	

