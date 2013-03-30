#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"



class FWTCP:				#def 			must be root!!
	def __init__(self):
		self.hping = Hping()
		#size:
		self.small = 1
		self.big = 999
		self.ok = '(V) '
		self.ko = '/!\\ '
		self.test = 0
		self.r_badchars = re.compile(' |-')
		self.r_syn = re.compile('S')

	def _launch(self,ip,port,flags):
		self.test += 1
		flgs = self.r_badchars.sub('',flags)		
		if len(flgs) == 0:
			flgs += '   '
		elif len(flgs) == 1:
			flgs += '  '
		elif len(flgs) == 2:
			flgs += ' '

		self.hping.tcpflag(ip, port, flags)

		if self.hping.resp['flags']:
			if self.r_syn.findall(self.hping.resp['flags'][0]):
				synked = 'Syncronized!!'
			else:
				synked = ''
			print 'Prueba %.2d (%s):\t%s\t%s\t%s' % (self.test, flgs, self.ko, self.hping.resp['flags'],synked)
		else:
			print 'Prueba %.2d (%s):\t%s' % (self.test, flgs, self.ok)

	def flagScan(self,ip,ini_port,end_port,flag):
		self.test = ini_port-1
		for p in range(ini_port,end_port+1):
			self._launch(ip,p,'-'+flag)
		

	def check(self,ip,port):
		self.test = 0
		print "========================";
		self._launch(ip,port,'    ')
		self._launch(ip,port,'  -S  ')
		self._launch(ip,port,'  -A  ')
		self._launch(ip,port,'  -R  ')
		self._launch(ip,port,'  -U  ')
		self._launch(ip,port,'  -P  ')
		self._launch(ip,port,'  -F  ')
		self._launch(ip,port,'  -S -A ')
		self._launch(ip,port,'  -S -R ')
		self._launch(ip,port,'  -S -U ')
		self._launch(ip,port,'  -S -P ')
		self._launch(ip,port,'  -S -F ')
		self._launch(ip,port,'  -A -R ')
		self._launch(ip,port,'  -A -U ')
		self._launch(ip,port,'  -A -P ')
		self._launch(ip,port,'  -A -F ')
		self._launch(ip,port,'  -R -U ')
		self._launch(ip,port,'  -R -P ')
		self._launch(ip,port,'  -R -F ')
		self._launch(ip,port,'  -U -P ')
		self._launch(ip,port,'  -U -F ')
		self._launch(ip,port,'  -P -F ')
		print "========================";
		self._launch(ip,port,'  -S -A -R ')
		self._launch(ip,port,'  -S -A -U ')
		self._launch(ip,port,'  -S -A -P ')
		self._launch(ip,port,'  -S -A -F ')
		self._launch(ip,port,'  -S -R -U ')
		self._launch(ip,port,'  -S -R -P ')
		self._launch(ip,port,'  -S -R -F ')
		self._launch(ip,port,'  -S -U -P ')
		self._launch(ip,port,'  -S -U -F ')
		self._launch(ip,port,'  -S -P -F ')
		self._launch(ip,port,'  -A -R -U ')
		self._launch(ip,port,'  -A -R -P ')
		self._launch(ip,port,'  -A -R -F ')
		self._launch(ip,port,'  -A -U -P ')
		self._launch(ip,port,'  -A -U -F ')
		self._launch(ip,port,'  -A -P -F ')
		self._launch(ip,port,'  -R -U -P ')
		self._launch(ip,port,'  -R -U -F ')
		self._launch(ip,port,'  -R -P -F ')
		self._launch(ip,port,'  -U -P -F ')

class FWICMP:
	def __init__(self):
		self.sing = Sing()
		self.hping = Hping()
		#size:
		self.small = 1
		self.big = 999
		self.ok = '(V) '
		self.ko = '/!\\ '

	def _launch(self,ip,type,code):
		print "===== TIPO %d CODIGO %d =====" % (type,code)
		self.hping.icmp(ip,type,code)
		if self.hping.resp['ip']:
			print self.ko
		else:
			print self.ok

		self.hping.icmp(ip,type,code,self.small,1)
		if self.hping.resp['ip']:
			print self.ko
		else:
			print self.ok

		self.hping.icmp(ip,type,code,self.big,1)
		if self.hping.resp['ip']:
			print self.ko
		else:
			print self.ok

	def check(self,ip):
		self._launch(ip,0,0)		#tipo0
		for i in range(0,255):		#tipo3 codigo 0-255
			self._launch(ip,3,i)
		for i in range(0,255):
			self._launch(ip,4,0)	#tipo4 codigo 0-255
		#tipo5 no permitido
		self._launch(ip,8,0)		#tipo8
		#tipo9 y tipo10 con sing
		for i in range(0,255):
			self._launch(ip,11,i)	#tipo11 code 0-255
		#tipo12 sing
		self._launch(ip,13,0) 		#tipo13
		#tipo15 sing
		self._launch(ip,17,0) 		#tipo13
