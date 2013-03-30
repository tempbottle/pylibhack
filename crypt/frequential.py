#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net




import sys

class Frequential:
	def __init__(self):
		self.numbers = range(0x30,0x3a)
		self.lower = range(0x61,0x7b)
		self.upper = range(0x41,0x5b)
		self.sign = range(0x21,0x30)
		self.sign2 = range(0x3a,0x41)
		self.sign3 = range(0x5b,0x61)
		self.sign4 = range(0x7b,0x7f)
		self.null = [0x00]
		self.tab = [0x09]
		self.ret = [0x0a,0x0d]
		self.hidden = [1,2,3,4,5,6,7,8,16,17,18,19,20,21,22,23,24,25,26,28,29,39,31,0x7f]
		self.space = [32]
		self.esc = [0x1b]
		self.txt = ''

	def load(self,filename):
		fd = open(filename,'rb')
		self.txt = fd.read()
		fd.close()
		

	def parse_summary(selft):
		data = ''
		last = 0
		for i in range(0,len(self.txt)):
			c = self.txt[i]
			if c in self.numbers:
				if last != 1:
					data+='[num]'
				last = 1	
			if c in self.lower:
				if last != 2:	
					data+='[low]'
				last = 2	
			if c in self.upper:
				if last != 3:
					data+='[up]'
				last = 3	
			if c in self.sign or c in self.sign2 or c in self.sign3 or c in self.sign4:
				if last != 4:
					data+='[sign]'
				last = 4	
			if c in self.null:
				if last != 5:
					data+='[null]'
				last = 5	
			if c in self.tab:
				if last != 6:
					data+='[tab]'
				last = 6	
			if c in self.ret:
				if last != 7:
					data+='[ret]'
				last = 7	
			if c in self.hidden:
				if last != 8:
					data+='[hidden]'
				last = 8	
			if c in self.space:
				if last != 9:
					data+='[spc]'
				last = 9	
			if c in self.esc:
				if last != 10:
					data+='[esc]'
				last = 10	
		print(data)


	
	def parse_all(self):
		data = ''
		for i in range(0,len(self.txt)):
			c = self.txt[i]
			if c in self.numbers:
					data+='9'
			if c in self.lower:
					data+='a'
			if c in self.upper:
					data+='A'
			if c in self.sign or c in self.sign2 or c in self.sign3 or c in self.sign4:
					data+='.'
			if c in self.null:
					data+='0'
			if c in self.tab:
					data+='t'
			if c in self.ret:
					data+='/'
			if c in self.hidden:
					data+='?'
			if c in self.space:
					data+=' '
			if c in self.esc:
					data+='X'
		print(data)


		
			

f = Frequential()	
f.load(sys.argv[1])
f.parse_all()
