#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004000 $"

import re


class Color:					#def
        def __init__(self):
                self.red = "\x1b[31;01m"
                self.green = "\x1b[32;02m"
                self.yellow = "\x1b[33;01m"
                self.blue = "\x1b[34;01m"
                self.magenta = "\x1b[35;01m"
                self.cyan = "\x1b[36;01m"
                self.white = "\x1b[37;00m"

class Festival:
	def __init__(self):
		self.festival = None
		fd = os.popen('which festival','r')
		f = fd.readlines()
		fd.close()
		if not f:
			print "Festival not installed"
		else:
			self.festival = f[0][:-1]

	def say(self,msg):
		if self.festival:
			fd = os.popen('echo %s | %s --tts' % (msg, self.festival), 'r')
			fd.close()



class Date:			#def
        def __init__(self):
                self.year = self.date('Y')
                self.day = self.date('d')
                self.mon = self.date('m')

        def setDate(self,d,m,y):
                self.year = y
                self.day = d
                self.mon = m

        def date(self,fmt):
                o = os.popen('date +%'+fmt,'r')
                year = o.read()[:-1]
                o.close()
                return year

	def tstamp(self):
		return int(time.time())

        def cal(self,year):
                os.popen('cal '+year,'r')


class File: 					#def
	def load(self,file):
		bad = re.compile('\n|\r')
		f = open(file,'r')
		data = f.readlines()
		f.close()
		data2=[]
		for d in data:
			data2.append(bad.sub('',d))
		return data2

	def save(self,data,file):
		f = open(file,'w')
		for d in data:
			f.write(d+'\n')
		f.close()
