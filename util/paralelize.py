#!/usr/bin/env python

import thread


class Paralelize:
	def __init__(self):
		self.elements = []
		self.mutex = 1
                self.sem = threading.BoundedSemaphore(value=self.mutex)
		self.num_threads = 10
		self.data = []
	
	def launch(self):
                for i in range(0,self.num_threads):
                        th = threading.Thread(target=self._attack, kwargs={})
                        th.start()
                        #th.join()
                        self.threads.append(th)



	

