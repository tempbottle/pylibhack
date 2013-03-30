#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import os
import sys

#TODO: arreglar GW get mac

class NetConfig:			
	def __init__(self):
		self.bd={}
		if os.getuid() != 0:
			print 'Root needed'
			sys.exit(1)

		self.getIface()
		self.getIP()
		self.getMAC()
		self.getGW()
		self.getGW_MAC()
	
	def getIface(self):
		fd = os.popen("mii-tool 2>&1")
		resp = fd.read()
		fd.close()
		self.bd["IFACE"] = resp.split(':')[0]
	def getIP(self):
		fd = os.popen("ifconfig %s | grep inet\ addr\: | awk '{ print $2 }' | cut -d: -f2" % self.bd["IFACE"])
		self.bd["IP"] = fd.read()[:-1]
		fd.close()
	def getMAC(self):
		fd = os.popen("ifconfig | grep %s | awk '{ print $5 }'"%self.bd["IFACE"])
		self.bd["MAC"] = fd.readlines()[0][:-1]
		fd.close()
	def getGW(self):
		fd = os.popen("route -n |  grep eth1 | awk '{ print $2 }' | grep -v 0.0.0.0","r")
		self.bd["GW"] = fd.read()[:-1]
		fd.close()
	def getGW_MAC(self):
		if self.bd["GW"]:
			os.popen("ping %s -c 1" % self.bd["GW"])
			fd = os.popen("arp -a | grep %s | awk '{ print $4 }'" % self.bd["GW"],"r")
			self.bd["GW_MAC"] = fd.read()[:-1]
			fd.close()
