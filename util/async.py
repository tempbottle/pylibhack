#!/usr/bin/env python2
# -*- coding: utf8 -*-

import threading

class AsyncTask(threading.Thread):
	def __init__(self,callback):
		threading.Thread.__init__(self)
		self.callback = callback
		
	def run(self):
		self.callback()
		pass


class Async:
	def __init__(self):
		self.tasks = []
	
	def add(self,callback)
		t = AsyncTask(callback)
		t.join()
		s elf.tasks.append(t)


def test():
	print "lala"

Async(test)

