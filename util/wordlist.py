#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# sha0@badchecksum.net

__version__ = "$Revision: 0004002 $"

'''
	Full featured data container, useful for:
	- loading data
	- saving data
	- altering/converting/transforming data
	- sorting data
	- deleting repeated items
	- filling data
	and so on ...



w = Wordlist()
w.clear()
w.load('/tmp/words')
w.num(99)
w.mins(3)
w.preCut(1)
w.postCut(1)
w.append("/test")
w.prepend("test-")
w.uniq()
w.save('/tmp/newWordlist')
print w[-1]
print w



'''


import re



class Wordlist:					#def
	def __init__(self,file = None):
		self.words = []
		self.__vocales = ['e','a','i','o','u']
		self.__vocales_upp = ['E','A','I','O','U']
		if file:
			self.load(file)
			

	def __del__(self):
		del self.words			#quitar listas grandes de memoria

	def __len__(self):
		return len(self.words)

	def __iter__(self):
		for w in self.words:
			yield w

	def __contains__(self,w):
		return w in self.words

	def __getitem__(self,i):
		return self.words[i]

	#def __setitem__(self,wl):
		#self.words = wl

	def __str__(self):
		out = ''
		for w in self.words:
			out += str(w)+'\n'
		return out

	def __eq__(self,wl):
		if len(wl) < self.words:
			return False

		for i in range(0,self.size()):
			if self.words[i] != wl[i]:
				return False

		return True

	def __lt__(self,wl):
		if self.size() < len(wl):
			return True
		return False

	def __gt__(self,wl):
		if self.size() > len(wl):
			return True
		return False


	def __call__(self, *args, **kwargs):
		pass

	#def __getattr__(self,k):
	#def __and__(self,wl): # interseccion
	#def __or__(self,wl): # union

	def add(self,w):
		self.words.append(w)

	def set(self,wl):
		self.words = wl

	def sort(self):
		self.words.sort()

	def uniq(self):
		prev=''
		new = []
		self.words.sort()
		for i in self.words:
			if i != prev:
				new.append(i)
			prev=i
		self.words = new

	def sub(self,pattern,replacement):
		self.regReplace(pattern,replacement)

	def regReplace(self,pattern,replacement):
		r = re.compile(pattern)
		ww=[]
		for i in self.words:
			ww.append(r.sub(replacement,i))
		self.words = ww

	def upto(self,w):	#elimina suprime de la palabra w para arriba
		try:
			pos = self.words.index(w)
			w = []
			for i in range(pos+1,len(self.words)):
				w.append(self.words[i])
			self.words = w
			return len(self.words) 
		except:
			return 0
		
	def hexa(self):
		self.nums(9)
		self.words += ['a','b','c','d','e','f']
		
	def hexaUpper(self):
		self.nums(9)
		self.words += ['A','B','C','D','E','F']

	def vocales(self):
		self.words += self.__vocales

	def vocalesUpper(self):
		self.words += self.__vocales_upp


	def consonantes(self):
		for m in range(97,123):
			if chr(m) not in self.__vocales: 
				self.words.append(chr(m))
			
	
	def mins(self,l,w = None):
		if not w:
			w = ''
		for m in range(97,123):
			if l==1:
				self.words.append(w+chr(m))
			else:
				self.mins(l-1, w+chr(m))

	def mays(self,l,w = None):
		if not w:
			w = ''
		for m in range(65,91):
			if l==1:
				self.words.append(w+chr(m))
			else:
				self.mays(l-1, w+chr(m))

	def nums(self,l):
		for i in range(0,l+1):
			self.words.append(str(i))

	def size(self):
		return len(self.words)

	def count(self):
		return len(self.words)

	def clear(self):
		self.words=[]

	def clean(self):
		self.sub('(\r|\n)','')

	def preCut(self,n):
		for i in range(0,len(self.words)):
			t = self.words[i]
			self.words[i] = t[n:]

	def postCut(self,n):
		for i in range(0,len(self.words)):
			t = self.words[i]
			self.words[i] = t[:-n]

	def prepend(self,w):
		for i in range(0,len(self.words)):
			self.words[i] = w+self.words[i]

	def append(self,w):
		for i in range(0,len(self.words)):
			self.words[i] = self.words[i]+w

#	def fuzz(self):
#		self.load('/opt/pipper/all.wl')

	def load(self,file):
		try:
			fd = open(file,'r')
		except:
			print "cannot open "+file
			return
		w = fd.readlines()
		fd.close()
		for i in w:
			self.words.append(re.compile('\r|\n').sub('',i))
		print "%d words loaded." % len(self.words)

	def save(self,file):
		fd = open(file,'w')
		for w in self.words:
			fd.write(w+'\n')
		fd.close()
