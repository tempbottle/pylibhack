#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import os
import re

class Hping:	
	def __init__(self):
		#Resultant data
		self.resp = {
			'ttl':'',
			'ip':'',
			'sport':'',
			'flags':'',
			'ipid':'',
		}
		self.filter = '2>/dev/null | grep -v HPING | grep -v statistics'
		#For the parser
		self.getTTL = re.compile(' ttl=([0-9]+)',re.IGNORECASE)
		self.getIP = re.compile(' ip=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',re.IGNORECASE)
		self.getSport = re.compile(' sport=([0-9]+)',re.IGNORECASE)
		self.getFlags = re.compile(' flags=([A-Z]+)',re.IGNORECASE)
		self.getIPID = re.compile(' id=([0-9]+)',re.IGNORECASE)
		#Tool
		self.base='/usr/sbin/hping3 '
		self.debug=0

	def clear(self):
		self.resp['ttl'] = ''
		self.resp['ip'] = ''
		self.resp['sport'] = ''
		self.resp['flags'] = ''
		self.resp['ipid'] = ''
		
	def parse(self,resp):
		#TODO: recoger más datos (rtt y icmp_seq)
		self.resp['ttl'] = self.getTTL.findall(resp)
		self.resp['ip'] = self.getIP.findall(resp)
		self.resp['sport'] = self.getSport.findall(resp)
		self.resp['flags'] = self.getFlags.findall(resp)
		self.resp['ipid'] = self.getIPID.findall(resp)
		#TODO: recoger timestamp
		#local @originate = ($rec =~ /Originate=\d{1,10} /g);
		#local @receive   = ($rec =~ /Receive=\d{1,10} /g);
		#local @transmit  = ($rec =~ /Transmit=\d{1,10} /g);


	def run(self,params):
		self.clear()
		if self.debug:
			print params
		o = os.popen(params,'r')
                resp = o.readline()
		o.close()
		if self.debug:
			print resp
		self.parse(resp)

	#Methods:
	def icmp(self,ip,type,code,data=None,frag=None):
		hping = '%s -1 -c 1 --icmptype %d --icmpcode %d %s ' % (self.base,type,code,ip)
		if data:
			hping += ' -d %d ' % data
		if frag:
			hping += ' -f '
		hping += self.filter
		self.run(hping)

	def tcpflag(self,ip,port,flags):
		hping = '%s -c 1 %s -p %d %s %s' % (self.base, ip, port, flags, self.filter)
		self.run(hping)

	def syn(self,ip,port,ttl=None):
		hping = self.base+ip+' -S -c 1-p '+str(port)
		if ttl:	
			hping += '-t '+str(ttl)
		hping += ' 2>/dev/null'
		self.run(hping)

	def raw(self,params):
		hping = self.base+params+' 2>/dev/null'
		self.run(hping)
