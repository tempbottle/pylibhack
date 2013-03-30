#!/usr/bin/env python

import sys
sys.path.append("..")
from web.searchEngines import *

#g = Google()
i = IXQuick()
kw = sys.argv[1]

print kw+" . . ."
i.search(kw)
fd2 = open('/home/sha0/emails','a')
for m in i.emails:
	print '\t- '+m
	fd2.write(m+"\n")
fd2.close()


