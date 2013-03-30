#!/usr/bin/python
from irc import *
import re
import sys
import time

#Config
#pwd = 'juasss'
server = 'irc.blessed.net'
port = 6667
ssl = False
ident = 'lol'
nick = 'Bugu_Bot33'
keywords = ['']
inside = False 

def callback(data):
	if not inside:
		bot.join('buguroo')


bot = IRC(server,port,ssl)
bot.ident = ident
bot.output = True
bot.connect(nick)
bot.callback = callback
bot.log = True
bot.logfile = 'bugubot.txt'
bot.listen()



while 1:
	pass

