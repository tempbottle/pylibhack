

class Cache

	def __init__(self,filename,autosync=True):
		self.filename = filename
		self.data = []
		self.autosync = autosync

	def __del__(self):
		self.sync()

	def load(self):
		self.data = []
		try:
			for l in open(self.filename,'r').readlines():
				self.data.append(l.replace('\r','').replace('\n',''))
		except:
			pass

	def getData(self):
		return self.data

	def pop(self):
		p = self.data.pop()
		if self.autosync:
			self.sync()
		return p

	def size(self):
		return self.count()

	def count(self):
		return len(self.data)

	def add(self,item):
		self.data.append(item)
		if self.autosync:
			self.sync()

	def sync(self):
		try:
			fd = open(self.filename,'w')
			for l in self.data:
				fd.write(l+'\n')
			fd.close()
		except:
			print "Error syncing."