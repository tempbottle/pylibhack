import xml.etree.ElementTree as ET
from util import File
import re, sys

#Para hacer cosas simples está bien.

class XmlDict(File):
	def __init__(self):
		self.xml = ''
		self.tree = {}
		self.subdict = {}
		self.level = 0
		self.where = [] # 0 -> root
		self.r_tab = re.compile('\t')

	def xml2dict(self, xml_filename):
		self.tree = {}
		self.xml = ''.join(self.load(xml_filename))
		self.xml = self.r_tab.sub('',self.xml)
		root = ET.fromstring(self.xml)
		self._xml2dict(root)
		return self.tree

	def _xml2dict(self, node):
		t = self.tree
		for k in self.where:
			t = t[k]

		if node.text:
			t.update({node.tag:node.text})	
		else:
			t.update({node.tag:{}})

		for (name,value) in node.items():
			t[node.tag].update({name:value})

		self.where.append(node.tag)

		for child in node.getchildren():
			self._xml2dict(child)

		self.where.pop()

	def dict2xml(self, dict, xml_filename):
		self._dict2xml(dict)	
		self.save(self.xml,xml_filename)

	def _dict2xml(self, map):
	        if (str(type(map)) == "<class 'object_dict.object_dict'>" or str(type(map)) == "<type 'dict'>"):
			for key, value in map.items():
                		if (str(type(value)) == "<class 'object_dict.object_dict'>" or str(type(value)) == "<type 'dict'>"):
                    			if(len(value) > 0):
                        			self.xml += "\t"*self.level
                        			self.xml += "<%s>\n" % (key)
                        			self.level += 1
                        			self._dict2xml(value)
                        			self.level -= 1
                        			self.xml += "\t"*self.level
                        			self.xml += "</%s>\n" % (key)
                    			else:
                        			self.xml += "\t"*(self.level)
                        			self.xml += "<%s></%s>\n" % (key,key)
                		else:
                    			self.xml += "\t"*(self.level)
                    			self.xml += "<%s>%s</%s>\n" % (key,value, key)
        	else:
			self.xml += "\t"*self.level
			self.xml += "<%s>%s</%s>\n" % (key,value, key)

