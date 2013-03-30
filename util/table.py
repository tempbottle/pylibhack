'''
	TODO: analyze files and interpret table estructures

'''

class Row:
	def __init__(self,row):
		self.row = row


class Table:
	def __init__(self,cols):
		self.cols  = cols
		self.db = []

	def __del__(self):
		del self.db

	def __str__(self):
		out = ''
		for row in self.db:
			out += '\n--------------------\n|'
			for col in row:
				out += str(col) + ' | '
		out += '\n--------------------'
		print out

	def __iter__(self):
		for row in self.db:
			yield row

	def __getitem__(self,rowid):
		return self.db[rowid]


	def add(self,row):
		self.addRow(row)

	def addRow(self,row):
		self.db.append(row)


	def load(self,filename):
		pass

