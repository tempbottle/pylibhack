#!/usr/bin/python
'''
wsdl debugger sha0@badchecksum.net
'''

from net.wsdl import *




def main():
	if len(sys.argv) != 2:
		print 'usage: %s <url>'
		sys.exit(1)

	wsdl = WSDLDebug()
	wrong = 'type h for help!'
	current = ''
	last_execution = ''
	last_cmd = 'nothing'
	id = False
	od = False
	wsdl.load(sys.argv[1])

	while 1:
		sys.stdout.write('%s=>' % current)
		cmd = sys.stdin.readline()[:-1]

		if cmd == '':
			cmd = last_cmd

		if cmd == 'q':
			del wsdl
			print 'CYA!'
			sys.exit(1)

		if cmd == 'h':
			print 'q ________________ quit'
			print 'h ________________ this help'
			print 'u <url> __________ change url of the wsdl'
			print 'c ________________ clear screen'
			print 'l ________________ list methods'
			#print 'lp _______________ list methods and the params of every method (dirty)'
			print 'm <method> _______ work whith a method'
			print 'p ________________ show the params of the working method'
			print 'r ________________ run working method'
			print 's <file> _________ save to file the last response'
			print 'd <file> _________ dictionary attack, mark the fields to attack with ## byte pair'
			print 'b <range> ________ bruteforce attack, ranges: n99 (0 to 99) c3 (a to zzz) C2 (A to ZZ)' # h2 (0 to zz)'
			print 'e ________________ show errors on / off'
			#print 'id _______________ input debugging'
			#print 'od _______________ output debugging'
			#print 'e ________________ eval, for advanced users.'
			print ''

		if cmd[0] == 'c':
			print '\n'*30

		if cmd[0] == 'u':
			if len(cmd)>2:
				wsdl.load(cmd[2:])
			else:
				print wrong

		if cmd[0] == 'l':
			last_execution = wsdl.list()
			print last_execution	


		if cmd[0] == 'm':
			if len(cmd)>2:
				if cmd[2:] in wsdl.methods:
					current = cmd[2:]
			else:
				current = ''

		if cmd[0] == 'p':
			if current != '':
				last_execution = wsdl.listParams(current)
				print last_execution

		if cmd[0] == 'r':
			p = wsdl.promptParams(current)
			last_execution =  wsdl.launch(current,p)
			print last_execution

		if cmd[0] == 's':
			if len(cmd)>2:
				fd = open(cmd[2:],'w')
				fd.write(last_execution)
				fd.close()

		if cmd[0] == 'd':
			if current:
				if len(cmd)>2:
					wl = Wordlist()
					wl.load(cmd[2:])

					print 'Mark the fields to attack with ## byte pair'
					params = wsdl.promptParams(current)

					params_to_brute = []
					for p in range(0,len(params)):
						if params[p][2] == '##':
							params_to_brute.append(p)
				
					last_execution = ''
					for w in wl.words:
						for i in params_to_brute:
							params[i][2] = w 

						z = '\n%s(%s)\n' % (current,params)
						z += wsdl.launch(current,params)
						z += '\n'
						last_execution += z
						print z
			else:
				print wrong

		if cmd[0] == 'b':
			if current:
				if len(cmd)>3:
					wl = Wordlist()
					if cmd[2] == 'h':
						pass		
					elif cmd[2] == 'n':
						wl.nums(int(cmd[3:]))
					elif cmd[2] == 'c':
						wl.mins(int(cmd[3:]))
					elif cmd[2] == 'C':
						wl.mays(int(cmd[3:]))
					else:
						print wrong
						continue

					print 'Mark the fields to attack with ## byte pair'
					params = wsdl.promptParams(current)

					params_to_brute = []
					for p in range(0,len(params)):
						if params[p][2] == '##':
							params_to_brute.append(p)
				
					last_execution = ''
					for w in wl.words:
						for i in params_to_brute:
							params[i][2] = w 

						z = '%s(%s)\n' % (current,params)
						z += wsdl.launch(current,params)
						z += '\n'
						last_execution += z
						print z
			else:
				print wrong

		if cmd[0] == 'e':
			wsdl.showErrors = not wsdl.showErrors
			print 'Show Errors: %s' % wsdl.showErrors
							
		last_cmd = cmd

		'''
		if cmd == 'lp':
			last_execution = wsdl.server.show_methods()
			print last_execution

		if cmd == 'id':
			id = not id
			server.soapproxy.config.dumpSOAPIn = id
			print 'Input Debugging is %s' % id

		if cmd == 'od':
			od = not od
			server.soapproxy.config.dumpSOAPOut = od
			print 'Output Debugging is %s' % od

		if cmd[0] == 'e':
			if len(cmd)>2:
				exec(cmd[2:])	
			else:
				print wrong
		'''

	wsdl.list()


if __name__ == '__main__':
	main()
