#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node:
	def __init__(self, parent, value=None):
		self.parent = parent
		self.son1 = None
		self.son2 = None
		self.priority = 0
		self.value = value



class Tree:					#def
	def __init__(self):
		self.root = Node(self,'root')
		self.root.parent = self.root
		self.stack = []
		self.found = 0
		self.h = 5
		self.draw = ''
		
	def show(self):
		self._dps(self.root)

	def _dps(self,x):
		print x.value

		if x.son1:
			x = self._dps(x.son1)

		if x.son2:
			x = self._dps(x.son2)

		print "up"
		return x.parent

	def add(self,val,l):
		x = self._bpsE(self.root,l)	
		y = Node(x,val)
		if x.son1:
			x.son2 = y
		else:
			x.son1 = y	

	def add(self,l):
		x = self.root
		y = Node(x,val)

		while 1:
			if not x.son1 or not x.son2:
				return x
			
			if l:
				x = x.son1
			else:
				x = x.son2
