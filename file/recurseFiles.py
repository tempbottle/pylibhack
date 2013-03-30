'''
Sample:

class ParseFile(RecurseFiles):

	def parse(self, filename):
		code = self.getCode(filename)

	def getCode(self,filename):
		return open(filename,'r').readlines()
		


pa = ParseFile()
pa.setPath('PortalWEB_Inputs')
pa.addFilter('.cs')
pa.addFilter('.vb')
pa.start()


'''

import os

class RecurseFiles:
	def __init__(self):
		self.path = '.'
		self.filters = []

	def addFilter(self,f):
		self.filters.append(f)

	def setPath(self,path):
		self.path = path

	def parse(self):
		pass #overrideme!!!

	def isFiltered(self,fil):
		if len(self.filters) == 0:
			return False

		for f in self.filters:
			if fil.find(f) >= 0:
				return False

		return True

	def start(self):
		self.recurse(self.path)

	def recurse(self,path):
		for root, dirs, files in os.walk(path):

			for f in files:
				if not self.isFiltered(f):
					self.parse(root+'/'+f)

			for d in dirs:
				self.recurse(d)