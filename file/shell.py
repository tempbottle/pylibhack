from wordlist import *
import os

class Shell:
	def __init__(self,cmd):
		self.cmd = cmd
		self.out = Wordlist()

	def __call__(self, *args, **kwargs):
		params=''
		for a in args:
			params += a+' '
		self.popen(params)

	def popen(self,params):
		pd = os.popen(self.cmd+' '+params,'r')
		self.out.set(pd.readlines())
		pd.close()
		self.out.clean()

