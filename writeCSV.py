#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import unicodecsv
import codecs

'''
created.csv
'''
def writeCreated(file_in,file_out):
	CREATED= [ 'uid','user', 'changeset', 'timestamp', 'version']
	with codecs.open(file_out,'w','utf_8_sig') as csvfile:
		l=[]
		with open(file_in,'rb') as f:
			for line in f.readlines():
				line=json.loads(line)
				if line['created']:
					l.append(line['created'])
		fieldnames = CREATED
		writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(l)
	return 



# writeCreated('updated.txt', 'created.csv')

'''
amenity.csv
'''
def writeAmenity(file_in,file_out):
	AMENITY=[ 'uid','user','lan','lon','type','amenity','name','street','housenumber']
	with codecs.open(file_out,'w','utf_8_sig') as csvfile:
		l=[]
		with open(file_in,'rb') as f:
			for line in f.readlines():
				line=json.loads(line)
				d={}
				if line.get('amenity'):
					for word in AMENITY:
						if word in ('uid','user'):
							d[word]=line['created'][word]
						else:
							d[word]=line.get(word,'null')
						if line.get('pos'):
							d['lan']=line['pos'][0]
							d['lon']=line['pos'][1]						
				if len(d)>0:
					l.append(d)
		fieldnames = AMENITY
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(l)
	return 

# writeAmenity('updated.txt', 'amenity.csv')









