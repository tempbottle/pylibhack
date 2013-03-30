#!/usr/bin/env python

import sys
sys.path.append("..")
from web.bruter import *


if __name__ == '__main__':
	if len(sys.argv) != 3 and len(sys.argv) != 4:
		print "usage: %s 'wrong password' 'http://lalala.com/a.php?id=#' 'pass=#'" % sys.argv[0]
		sys.exit(1)

	wb = WebBruter()
	wb.numthreads = 8
	wb.badguy =  sys.argv[1]
	wb.load('/home/sha0/audit/wordlist/s1-3')
	if len(sys.argv) == 3:
		wb.scan(sys.argv[2])
	elif len(sys.argv) == 4:
		wb.scan(sys.argv[2],sys.argv[3])




