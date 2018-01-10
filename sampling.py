#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET 
osm_file='shanghai_china.osm'
sample='sample.osm'

def get_element(osm_file,tags=('node','way','relation')):
    context=ET.iterparse(osm_file)
    for event,elem in context:
        if elem.tag in tags:
            yield elem
            elem.clear()



def sampling(sample_file,osm_file):
    with open(sample_file,'wb') as output:
        output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write(b'<osm>\n ')
        for i,elem in enumerate(get_element(osm_file)):
            if i % 50 ==0:
                output.write(ET.tostring(elem, encoding='utf-8'))
        output.write(b'</osm>')


sampling('sample_updated.osm', 'updated.osm')
