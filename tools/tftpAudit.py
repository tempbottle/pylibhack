#!/usr/bin/python
#sha0@badchecksum.net


import sys
sys.path.append('..')
from net.tftp import *

def usage():
	print sys.argv[0]+' <mode s:scan c:check b:bruteforce> <net/host> <wordlist>'
	print ' ej: '+sys.argv[0]+' s 192.168.3 4 30'
	print ' ej: '+sys.argv[0]+' c 192.168.3.44'
	print ' ej: '+sys.argv[0]+' c 192.168.3.44 config'
	print '     '+sys.argv[0]+' b 191.168.3.5 nombreficheros.txt'
	sys.exit(-1)


audit = TftpAudit(1)

if len(sys.argv) >= 2 and len(sys.argv) <= 5:
        if sys.argv[1] == 's':
                ip = sys.argv[2]
                ini = int(sys.argv[3])
                end = int(sys.argv[4])
                if len(sys.argv) == 5:
                        audit.scan(ip,ini,end)
                else:
                        usage()

        elif sys.argv[1] == 'c':
                if len(sys.argv) == 3:
                        audit.check(sys.argv[2])
                elif len(sys.argv) == 4:
                        audit.test(sys.argv[2],sys.argv[3])
                else:
                        usage()

        elif sys.argv[1] == 'b':
                if len(sys.argv) == 4:
                        audit.brute(sys.argv[2],sys.argv[3])
                else:
                        usage()

        else:
                usage()
else:
        usage()


audit.end()

