#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net (copypasted && reestructured)

__version__ = "$Revision: 0004001 $"

import struct
import pcap
import socket


class Packet:
	'''
		Packet Parsing Class
	'''

	def __init__(self,data):
		#BD
		self.datalink = {}
		self.ip = {}
		self.tcp = {}
		self.udp = {}
		self.icmp = {}
		self.proto = {}
		self.tcpflags = {}

		#Init
		self._init_protocols()
		self._init_flags()

		#Parsing
		self._parser(data)

	def _make_addr( self, addr ):
        	return "%d.%d.%d.%d" % ( ord(addr[0]), ord(addr[1]), ord(addr[2]), ord(addr[3]) )

	def _parser(self,data):
		#2. DATALINK
		self._datalink_parse(data)

		#3. IP
		if self.datalink['type'] == 'Ethernet II':
			if self.datalink['ethernet_type'] == '\x18\x00':
				self._ip_parse(data[16:])
			elif self.datalink['ethernet_type'] == '\x08\x00':
				self._ip_parse(data[14:])
			else:
				#print 'Unknowk ethernet:'+data
				return

			#4. TCP UDP ICMP
			if self.ip.has_key('ttl'):
				if self.ip['protocol_name'] == 'tcp':
					self._tcp_parse(self.ip['data'])	
					if not self.tcp.has_key('source_port'):
						self.ip['protocol_name'] == 'unknown'	
						print 'tcp mal decodificado'
						
				elif self.ip['protocol_name'] == 'udp':
					self._udp_parse(self.ip['data'])
					if not self.udp.has_key('source_port'):
						self.ip['protocol_name'] == 'unknown'
						print 'udp mal decodificado'

				elif self.ip['protocol_name'] == 'icmp':
					print 'ICMP!!'
				#else:
				#	print 'ip pero sin tcp udp ni icmp, sctp?'
				#	print self.ip['source_address']
				#	print self.ip['destination_address']
		#else:
		#	print 'No Ethernet:'+data

	def _datalink_parse(self,data):
		type = socket.ntohs(struct.unpack('H', data[12:14])[0])
		self.datalink['type_num'] = type
		self.datalink['type'] = 'Unknown'

		#Ethernet II
    		if type > 1500:
			self.datalink['source'] = socket.ntohs(struct.unpack('BBBBBB', data[0:6])[0])
        		self.datalink['destination'] = socket.ntohs(struct.unpack('BBBBBB', data[6:12])[0])
		        self.datalink['type'] = 'Ethernet II'
		        self.datalink['ethernet_type'] = data[12:14]
		        self.datalink['data'] = data[14:60]
		        self.datalink['fcs'] = data[60:64]

	        # parse vlan information if this is a 802.1Q frame
	        if type == 8100:
			self.datalink['type'] = 'vlan'
			self.datalink['vlan_priority'] = data[64:67]
			self.datalink['vlan_cfi'] = data[67:68]
			self.datalink['vlan_vid'] = data[68:80]


	def _ip_parse(self,data):
	        self.ip['version']    = ( ord(data[0]) & 0xf0 ) >> 4
	        self.ip['header_len'] = ord(data[0]) & 0x0f
	        self.ip['tos']        = ord(data[1])
	        self.ip['total_len']  = socket.ntohs(struct.unpack('H',data[2:4])[0])
	        self.ip['id']         = socket.ntohs(struct.unpack('H',data[4:6])[0])
	        self.ip['flags']      = (ord(data[6]) & 0xe0) >> 5
	        self.ip['fragment_offset'] = socket.ntohs(struct.unpack('H',data[6:8])[0] & 0x1f)
	        self.ip['ttl']             = ord(data[8])
	        self.ip['protocol']        = ord(data[9])
		self.ip['protocol_name']   = self._protoByCode(self.ip['protocol'])
	        self.ip['checksum']        = socket.ntohs(struct.unpack('H',data[10:12])[0])
	        self.ip['source_address']  = self._make_addr(data[12:16])
	        self.ip['destination_address'] = self._make_addr(data[16:20])
	
		if self.ip['header_len']>5:
			self.ip['options'] = data[20:4*(self.ip['header_len']-5)]
		else:
			self.ip['options'] = None
			self.ip['data'] = data[4*self.ip['header_len']:]

	def _tcp_parse(self,data):
        	self.tcp['source_port']      = socket.ntohs(struct.unpack('H',data[0:2])[0])
	        self.tcp['destination_port'] = socket.ntohs(struct.unpack('H',data[2:4])[0])
	        self.tcp['seq_number']       = struct.unpack('i',data[8-1:4-1:-1])[0]  # "ntoa"
	        self.tcp['ack_number']       = struct.unpack('i',data[12-1:8-1:-1])[0] # "ntoa"
		self.tcp['data_offset']	     = ord(data[12]) & 0xf0 >> 4
		self.tcp['reserved']	     = socket.ntohs(struct.unpack('H',data[12:14])[0]) & 0x0fc0 >> 6
	        self.tcp['window_size']      = socket.ntohs(struct.unpack('H',data[14:16])[0])
	        self.tcp['checksum']         = socket.ntohs(struct.unpack('H',data[16:18])[0])
		self.tcp['urgent_ptr']	     = socket.ntohs(struct.unpack('H',data[18:20])[0])
	        self.tcp['header_len']       = ord( data[12] ) >> 4
	        self.tcp['flags']            = ord( data[13] )
	        #self.tcp['data']             = data[4* self.tcp['header_len']:]
	        if len(data) > 20:
			self.ip['options'] = struct.unpack('I', data[20:24])[0] & 0x0fff
		if len(data) > 24:
			self.ip['padding'] = ord(data[24])
			self.ip['data'] = data[25:]

	def _udp_parse(self,data):
		self.udp['source_port'] = struct.unpack('H', data[1:3])[0]
		self.udp['destination_port'] = struct.unpack('H', data[3:5])[0]
		self.udp['length'] = struct.unpack('H', data[5:7])[0]
		self.udp['checksum'] = struct.unpack('H', data[7:9])[0]
		self.udp['data'] = data[9:]

	def _protoByName(self,name):
		return self.proto[name]

	def _protoByCode(self,code):
		for k in self.proto.keys():
			if self.proto[k] == code:
				return k
		return ''

	def _init_flags(self):
		self.tcpflags = {
			0x01:'fin',
			0x02:'syn',
			0x04:'rst',
			0x08:'push',
			0x10:'ack',
			0x20:'urg',
			0x40:'ece',
			0x80:'cwr'
		}


	def _init_protocols(self):
		self.proto['ip'] = 0
		self.proto['icmp'] = 1
		self.proto['igmp'] = 2
		self.proto['ggp'] = 3
		self.proto['ipencap'] = 4
		self.proto['st'] = 5
		self.proto['tcp'] = 6
		self.proto['egp'] = 8
		self.proto['igp'] = 9
		self.proto['pup'] = 12
		self.proto['udp'] = 17
		self.proto['hmp'] = 20
		self.proto['xns-idp'] = 22
		self.proto['rdp'] = 27
		self.proto['iso-tp4'] = 29
		self.proto['xtp'] = 36
		self.proto['ddp'] = 37
		self.proto['idpr-cmtp'] = 38
		self.proto['ipv6'] = 41
		self.proto['ipv6-route'] = 43
		self.proto['ipv6-frag'] = 44
		self.proto['idrp'] = 45
		self.proto['rsvp'] = 46
		self.proto['gre'] = 47
		self.proto['esp'] = 50
		self.proto['ah'] = 51
		self.proto['skip'] = 57
		self.proto['ipv6-icmp'] = 58
		self.proto['ipv6-nonxt'] = 59
		self.proto['ipv6-opts'] = 60
		self.proto['rspf'] = 73
		self.proto['vmtp'] = 81
		self.proto['eigrp'] = 88
		self.proto['ospf'] = 89
		self.proto['ax.25'] = 93
		self.proto['ipip'] = 94
		self.proto['etherip'] = 97
		self.proto['encap'] = 98
		self.proto['pim'] = 103
		self.proto['ipcomp'] = 108
		self.proto['vrrp'] = 112
		self.proto['l2tp'] = 115
		self.proto['isis'] = 124
		self.proto['sctp'] = 132
		self.proto['fc'] = 133
		self.proto['udplite'] = 136


