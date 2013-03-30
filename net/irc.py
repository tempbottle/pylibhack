import socket
import select
import threading
import ssl
import re
import time

class Conn:
	def __init__(self,bSSL=False):
		self.presock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.buffer = 100
		self.idle = 2
		if bSSL:
			self.sock = ssl.wrap_socket(self.presock)
		else:

			self.sock = self.presock


	def connectSend(self, ip, port, toSend):
		self.sock.connect(ip,port)
		self.sock.send(toSend)
		self.sock.shutdown(1)
		data = self.sock.recv(self.buffer)
		self.sock.close()
		return data

	def connect(self, ip, port):
		try:
			self.sock.connect((ip,port))
			return 1
		except:
			return 0

	def recv(self):
		return self.sock.recv(self.buffer)
		
		
	def send(self, msg):
		self.sock.send(msg)
		try:
			return self.sock.recv(666)
		except:
			return ''

	def close(self):
		self.sock.close()
		self.presock.close()

	def read(self):
                count=0
                alldata=''
                while 1:
                        count +=1
                        if count > self.idle: break
                        (r,w,e) = select.select([self.sock],[],[self.sock],3)
                        if e: break
                        for rr in r:
                                try:
                                        data = rr.recv(8192)
                                        alldata+=data
                                except:
                                        return ''

		return alldata



class IRC:
	def __init__(self,server,port,bSSL=False):
		self.server = server
		self.port = port
		self.con = Conn(bSSL)
		self.con.buffer = 2048
		self.ident = 'weee'
		self.r_ping = re.compile('PING :([a-zA-Z0-9@._-]+)')
		self.output = True
		self.log = False
		self.logfile = ''
		self.listener = None
		self.running = True

	def __del__(self):
		self.quit()


	def connect(self,user):
		self.con.connect(self.server,self.port)
		self.con.send('USER '+user+' +ixw '+user+' :'+self.ident+'\n')
		self.con.send('NICK '+user+'\n')

	def join(self,chan,passwd=None):
		if passwd:
			self.con.send('JOIN #'+chan+' :'+passwd+'\n')
		else:
			self.con.send('JOIN #'+chan+'\n')
		
	def part(self,chan):
		self.con.send('PART #'+chan+'\n')	

	def kick(self,chan,nick,why):
		self.con.send('KICK #'+canal+' '+nick+' :'+why+'\n')
		
	def msg(self,chan,msg):	
		self.con.send('PRIVMSG '+chan+' :'+msg+'\n')

	def mode(self,chan,mode,nick):
		self.con.send('MODE '+chan+' '+mode+' '+nick+'\n')

	def raw(self,msg):
		self.con.send(msg)

	def pingpong(self,data):
		ping = self.r_ping.findall(data)
		if ping:
			print "pongeando "+ping[0]
			self.con.send('PONG :'+ping[0]+'\n')

	def listen(self):
		self.listener = threading.Thread(target=self.read, kwargs={})
		self.listener.start()
		

	def read(self):
		while self.running:
			try:
				data = self.con.read()
			except:
				data = ''

			if data:
				self.pingpong(data)
				if self.output:
					print data
				if self.log:
					fd = open(self.logfile,'a')
					fd.write(data)
					fd.close()
				if self.callback:
						self.callback(data)
		
	def who(self,name):
		self.con.send('WHO '+name+'\n')


	def quit(self):
		self.con.send('QUIT :bytes\n')
		self.running = False
		time.sleep(2)
		#self.listener.join()
		self.con.close()


