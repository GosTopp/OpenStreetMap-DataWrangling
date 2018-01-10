#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from pprint import pprint
import re

'''
remove elements which are not in shanghai 
'''

def excepted(addrs): # addrds: a list of addr
	count=0
	for addr in addrs:
	    if re.search('shang\s*hai|上海',addr,re.I):
	        i=True      
	    else:
	        i=False
	    count=count+i
	if count>0:
		value=False
	else:
		value=True
	return value





def whether_in_shanghai(element):
	k=['addr:city']
	kv_values={}
	check_v=[]
	if element.find('tag')==None:
		in_shanghai=True
	else:
		for tag_elem in element.findall('tag'):
			kv_values[tag_elem.get('k')]=tag_elem.get('v')
		l=kv_values.keys()		
		intersection=list(set(l).intersection(k))
		if intersection==[]:
			in_shanghai=True
		else:
			for i in intersection:
				check_v.append(kv_values[i])
			if excepted(check_v):
				in_shanghai=False
			else:
				in_shanghai=True			
	return in_shanghai


def withoutNoise(osm_file,tags=('node','way','relation')):
	for _, elem in ET.iterparse(osm_file):
		if elem.tag in tags:
			if whether_in_shanghai(elem):
				yield elem
				elem.clear()




def updatedData(file_in,file_out):
    with open(file_out,'wb') as output:
        output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write(b'<osm>\n ')
        for elem in withoutNoise(file_in,tags=('node','way','relation')):
            output.write(ET.tostring(elem, encoding='utf-8'))
        output.write(b'</osm>')

				
updatedData('shanghai_china.osm','updated.osm')

