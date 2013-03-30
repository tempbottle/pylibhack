#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net copypasted & reestrucured from fpichel@isecauditors.com

__version__ = "$Revision: 0004000 $"

from net.netConfig import *
import pcap
import dpkt

class Sniff:
	def __init__(self):
		self.p = pcap.pcapObject()
		self.filter = ''
		self.callback = self.default_callback
		n = NetConfig()
		self.iface = n.bd['IFACE']
		del n

	def __del__(self):
		pass
	
	def setFilter(self,filter):
		self.filter = filter

	def setIface(self,iface):
		self.iface = iface

	def setCallback(self,callback):
		self.callback = callback

	def run(self):
		self.p.open_live(self.iface,1600,0,100)
		self.p.setnonblock(1)
		self.p.setfilter(self.filter,0,0)
		while 1:
		#	try:
			self.p.dispatch(1,self.callback)
		#	except (RuntimeError, TypeError, NameError):
		#		print RuntimeError
		#		print TypeError
		#		print NameError
		#		break

	def default_callback(self,pktlen,data,tstamp):
		print 'Change the callback!'
			
