#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"


class Sing:
	def __init__(self):
		self.flags={
			'filter':'2>/dev/null | grep -v SING | grep -v statistics',
			'base':'sing -v -c 1 -n -t 30 -T 1 ',
			'size':' -s ',
			'type9':' -rta X ',
			'type8':' -rte X ',
			'type12':' -rts ', #tipo10 tambien rts??
			'type15':' -info ',
		}

	def parse(self,data):
		print data
		#TODO: parse data to own structs

	def send(target,type,size=None):
		params = self.flags['base'] + self.flags[type] 
		if size:
			params += self.flags['size'] + size
		params += target + self.flags[filer]
		o = so.popen(params,'r')
                resp = o.readline()
		o.close()
		self.parse(resp)

