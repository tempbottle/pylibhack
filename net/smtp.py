
from net.conn import *

class Smtp(Conn):
	def __init__(self):
		Conn.__init__(self)
		self.banner = ''

	def attach(self,target):
		if self.connect(target,25):
			self.banner = self.read()
			print self.banner
		else:
			print 'cannot connect'
	
