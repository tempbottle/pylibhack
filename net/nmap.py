#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import threading
import mutex
import re
import os




class Nmap:
	def __init__(self):
		self.extra_flags = ''
		self.iface='eth0'
		self.mutex = 1
		self.sem = threading.BoundedSemaphore(value=self.mutex) 
		self.bd = {
			'tcp': {
				'open':[],
				'closed':[],
				'filtered':[],
			},
			'udp': {
				'open':[],
				'closed':[],
				'filtered':[],
			}
		}
		self.r_o = re.compile('([^ ]+) +open')
		self.r_c = re.compile('([^ ]+) +closed')
		self.r_f = re.compile('([^ ]+) +filtered')
                self.threads = []


	def clear(self):
		self.o=[]
		self.c=[]
		self.f=[]
		self.ips=[]

	def join(self):
		for t in self.threads:
			t.join()

	def parsePorts(self,resp):
		self.sem.acquire()
		o = self.r_o.findall(resp)
		c = self.r_c.findall(resp)
		f = self.r_f.findall(resp)
		if o:
			if o[0][-3:] == 'tcp':
				self.bd['tcp']['open'].append(o[0][:-4])
			if o[0][-3:] == 'udp':
				self.bd['udp']['open'].append(o[0][:-4])
		if c:
			if c[0][-3:] == 'tcp':
				self.bd['tcp']['closed'].append(c[0][:-4])
			if c[0][-3:] == 'udp':
				self.bd['udp']['closed'].append(c[0][:-4])
		if f:
			if f[0][-3:] == 'tcp':
				self.bd['tcp']['filtered'].append(f[0][:-4])
			if f[0][-3:] == 'udp':
				self.bd['udp']['filtered'].append(f[0][:-4])
		self.sem.release()

	def stats(self):
		print self.bd
	'''
		print "Open: "
		print self.o
		print "\nClosed: "
		print self.c
		print "\nFiltered: "
		print self.f
	'''

	def _scan(self,ip,p,flags):
		print "Scanning  ..."
		run  = '/usr/bin/nmap %s %s -p %s -n %s -e %s 2>/dev/null' % (flags,ip,p,self.extra_flags,self.iface)
		resp = ''
		o = os.popen(run,'r')
		while 1:
			try:
				self.parsePorts(o.next())
			except:
				break

		o.close()
		print "Scanned."

	def quick(self,ip):
		t = threading.Thread(target=self._scan, kwargs={}, args=(ip,'20-60,80,139,443,445,110,113,8080',' -sS -P0 -T4 '))
                self.threads.append(t)
		t.start()


	def full(self,ip):
		t = threading.Thread(target=self._scan, kwargs={}, args=(ip,'0-65535',' -sSV -P0 '))
                self.threads.append(t)
		t.start()

	def discover(self,range,port):
		t = threading.Thread(target=self._scan, kwargs={}, args=(range,port,' -sSV -P0'))
                self.threads.append(t)
		t.start()

        def finished(self):
                for t in self.threads:
                        if t.isAlive:
                                return True
                return False

