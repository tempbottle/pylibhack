
class Chunked:
        def __init__(self):
                self.r_chunked = re.compile('chunked',re.IGNORECASE)
                self.r_hexa = re.compile('([a-zA-Z0-9]+)(\r|\n)')
                self.size = 0
                self.chunked = False

        def check(self,headers):
		print 'chunked!'
                self.chunked = False
                if self.r_chunked.findall(headers):
                        self.chunked = True

                return self.chunked

        def _eraseInitialLinebytes(self,data):
                for i in range(0,len(data)):
                        if data[i] != '\r' and data[i] != '\n':
                                break
                return data[i:]

        def getData(self,data):
                hex = self.r_hexa.findall(data)
                self.size = hex[0][0]
		print  'ChunkSize: '+self.size
                data = re.sub(hex[0][0],'',data)
		
		if data[-1] == '0':
			if data[-2] == '\r' or data[-2] == '\n':
				if data[-3] == '\r' or data[-3] == '\n':
					data = data[:-3]
				else:
					data = data[:-2]
		
                return self._eraseInitialLinebytes(data)



class Proxy:
	def __init__(self,lhost,lport,rhost,rport):
		self.lhost = lhost
		self.lport = lport
		self.rhost = rhost
		self.rport = rport
		self.incommers = 100
		self.idle=2
		self.keepalive = 0
		self.r_rr = re.compile('\r\r')
		self.r_nrnr = re.compile('\n\r\n\r')
		self.r_rnrn = re.compile('\r\n\r\n')
		self.r_keepalive = re.compile('\r\n0')
		self.r_deflate = re.compile('Accept-Encoding:.*',re.IGNORECASE)
		self.desconecta = 0
		self.mutex = 1
		self.sem = threading.BoundedSemaphore(value=self.mutex)
		self.classnum = 1
		self.trapMode = 1

	def log(self,data):
		if not data1:
			return

		self.sem.acquire()
		fd = open('interceptor.log','a')
		#fd.write('---- Class %d ----\n' % self.classnum)
		fd.write(data)
		#fd.write('\n------------------\n\n')
		fd.close()
		#self.classnum += 1
		self.sem.release()
		
	def connect(self):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			s.connect((self.rhost,self.rport))
			s.setblocking(False)
		except:
			print 'Cannot connect!'
			sys.exit(1)
		return s

	def listen(self):
		try:
			listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			listener.bind((self.lhost,self.lport))
			listener.listen(self.incommers)
			return listener
		except:
			print 'Cannot bind port'
			sys.exit(1)

	def readsend(self,toRead,toSend):
		count=0
		alldata=''
		while 1:
			count +=1
			#print 'counter %d' % count
			if count > self.idle: break
			(r,w,e) = select.select([toRead],[],[toRead],3)
			if e: break
			for rr in r:
				#print ':/'
				try:
					data = rr.recv(8192)
					alldata+=data
				except:
					return 1

		if alldata:
			return self.analyze(alldata,toSend)
		else:
			return 0


	def run(self):
		listener = self.listen()
		#try:
		print 'Awaiting connections'
		while 1:
			if self.desconecta:
				listener.close()
				break
			cli, addr = listener.accept()
			cli.setblocking(False)
			th = threading.Thread(target=self.attend, args=[cli])
			th.start()


	def attend(self,*args,**kwargs):
		print 'New communication thread'
		cli = args[0]
		srv = self.connect()
		while 1:
			if self.desconecta:
				cli.close()
				srv.close()
				break

			e = self.readsend(cli,srv)
			if e == 1:
				cli.close()
				break
			if e == 2:
				srv.close()
				srv = self.connect()
				continue

			e = self.readsend(srv,cli)
			if e == 2:
				cli.close()
				break
			if e == 1:
				srv.close()
				srv = self.connect()

	def _send(self,sock,data):
		try:
			sock.send(data)
			print 'Enviado!'
			return 0
		except:
			print 'No se pudo enviar!'
			return 2

	def analyze(self,data,toSend):
		print 'Analyzing'
		if data.startswith('desconecta'):
			print 'Desconectando'
			self.desconecta = 1
			return 0

		if not data:
			return 0
		if len(data) == 0:
			return 0

		data = self.r_rr.sub('\n\n',data)
		data = self.r_nrnr.sub('\n\n',data)
		data = self.r_rnrn.sub('\n\n',data)

		httpdata = data.split('\n\n')
		if not httpdata:
			return 0
		if len(httpdata) < 2:
			return 0

		headers   = httpdata[0]
		post = httpdata[1]

		c = Chunked()
		if c.check(headers):
			postChunked = c.getData(javaobject)
		
		if c.chunked:
			return self._send(toSend,headers+'\r\n\r\n'+str(c.size)+'\r\n'+str(post)+'\r\n0')
		else:
			return self._send(toSend,headers+'\r\n\r\n'+str(post))

	def __del__(self):
		print 'Flushing sockets'
		try: 
			listener.close()
		except: pass
		try: 
			srv.close()
		except: pass
		try: 
			cli.close()
		except: pass



