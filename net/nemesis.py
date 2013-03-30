#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import os
import re

class Nemesis:
	def __init__(self):
		self.db = {}
		self.base = '/usr/bin/nemesis'

	def clear(self):
		pass	

	def parse(self,resp):
		pass

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

	def raw(self,params):
		hping = self.base+params+' 2>/dev/null'
		self.run(hping)
