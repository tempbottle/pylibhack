#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

'''Dependences:
http://code.google.com/p/dict2xml/
http://code.google.com/p/xml2dict/


'''

'''Brain Storm:

* Crear red, ampliar red
* Estructura
	- lista de ips, que se le pueda asignar un nombre a cada ip
	- 


'''

__version__ = "$Revision: 0004000 $"

from dpkt.ip import IP   
from util.util import File
from net.sniff import Sniff
from net.packet import Packet
		
class NetEye(File,Sniff):
	def __init__(self):
		Sniff.__init__(self)
		self.bd = {}
		self.services = {
			'psi': {
				'remote':1,
				'ip':0,
				'port':0,
			}
		}
		self.setCallback(self._capture)

	def __del__(self):
		del self.bd

	def _capture(self,pktlen,data,tstamp):
		p = Packet(data)
		if not p.ip.has_key('ttl'):
			return 

		if p.ip['protocol_name'] == 'tcp':
			print '\n%s:%s -> %s:%s proto: %d (%s)' % (
				p.ip['source_address'],
				p.tcp['source_port'],
				p.ip['destination_address'],
				p.tcp['destination_port'],
				p.ip['protocol'],
				p.ip['protocol_name']
				)
		if p.ip['protocol_name'] == 'udp':
			print '\n%s:%s -> %s:%s proto: %d (%s)' % (
				p.ip['source_address'],
				p.udp['source_port'],
				p.ip['destination_address'],
				p.udp['destination_port'],
				p.ip['protocol'],
				p.ip['protocol_name']
				)

			print p.ip['data']

		del p

	def go(self):
		self.run()

