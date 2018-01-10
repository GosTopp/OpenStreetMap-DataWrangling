#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from pprint import pprint
import json
import re
import codecs

def count_items(file):
    '''
    print counts of tags, attibutes and 'k' to see 
    if there are any problematic items.
    '''
    context=ET.iterparse(file)
    count_tags={}
    count_attributes={}
    count_k={}
    
    for event, elem in context:

        # count tags
        if elem.tag in count_tags.keys():
            count_tags[elem.tag]+=1
        else:
            count_tags[elem.tag]=1

        # count attr
        for i in elem.keys():
            if i in count_attributes.keys():
                count_attributes[i]+=1
            else:
                count_attributes[i]=1

        # count k
        if elem.get('k'):
            if elem.get('k') in count_k.keys():
                count_k[elem.get('k')]+=1
            else:
                count_k[elem.get('k')]=1
        elem.clear()

    print ('count_tag: ')
    pprint(sorted(count_tags.items(),key=lambda k:k[1],reverse=True))
    print ('count_attributes  : ')
    pprint(sorted(count_attributes.items(),key=lambda k:k[1],reverse=True))
    print ('count_k: ')
    pprint(sorted(count_k.items(),key=lambda k:k[1],reverse=True))

# count_items('sample.osm')
# count_items('shanghai_china.osm')

def get_kv_values(file):
    '''
    Return a dictionary containing tags as keys 
    and the sets of all possible values in the file as values.
    '''
    check_KV={}
    for event ,elem in ET.iterparse(file):
        if elem.tag=='tag':
            # if elem.get('k') in tag_names:
            if elem.get('k') in check_KV.keys():
                check_KV[elem.get('k')].add(elem.get('v'))
            else:
                check_KV[elem.get('k')]=set([elem.get('v')])
        elem.clear()
    return check_KV

# pprint(get_kv_values('updated.osm'))


'''
transform XML to json-like file. The output should be a list of dictinaries 
that look like this:

'''
postcode = re.compile(r'^\d{6}$', re.I)

mapping={
    "St": "Street",
    "St.": "Street",
    "Jie":"Street",
    "Lu":"Road",
    "Rd":"Road",
    "Rd.":"Road",
    "(N.)":"North",
    "(S.)":"South",
    "(W.)":"West",
    "(E.)":"East",
    "N.":"North",
    "N":"North",
    "S.":"South",
    "S":"South",
    "W.":"West",
    "W":"West",
    "E.":"East",
    "E":"East"
    }

def update_street_name(st,mapping):
    st=st.split(' ')
    for i, word in enumerate(st):
        if len(word)==1:
            word=word.upper()
        elif len(word)>1:
            word=word[0].upper()+word[1:]
        st[i]=word
    return ' '.join([mapping.get(e,e) for e in st])


def clean_element(element):
    if element.tag in ('node','way','relation'):
        for tag in element.iter('tag'):

             # remove problematic poscodes
            if tag.get('k')=='addr:postcode':
                tag.attrib['v']=tag.get('v').replace('上海','')
                if postcode.match(tag.attrib['v'].strip())==None:
                    element.remove(tag)

             # update street name
            elif tag.get('k')=='addr:street':
                st=tag.attrib['v']
                st=update_street_name(st,mapping)
    return element
    

def shape_element(element):
    # transform XML to JSON
    node={}
    CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
    
    if element.tag in ('node','way'):
        node['type']=element.tag
        for attr in element.attrib.keys():
            if attr in CREATED:
                if 'created' in node.keys():
                    node['created'][attr]=element.attrib[attr]
                else:
                    node['created']={attr:element.attrib[attr]}
            elif attr in ['lon','lat']:
                node['pos']=[float(element.attrib['lat']), float(element.attrib['lon'])]
       
        for child in element.iter():
            if child.tag=='nd':
                if 'nd_refs' in node.keys():
                    node['nd_refs'].append(child.attrib['ref'])
                else:
                    node['nd_refs']=[child.attrib['ref']]
            if child.tag=='tag':
                tag_name=child.attrib['k']
                if tag_name in ('type','address'):
                    pass
                elif tag_name[:5]=='addr:':
                    if tag_name.count(':')>1:
                        pass
                    else:
                        key=tag_name.split(':')[-1]
                        if 'address' in node.keys():
                            node['address'][key]=child.attrib['v']
                        else:
                            node['address']={key:child.attrib['v']}
                else:
                    node[tag_name] = child.attrib['v']
        return node
    else:
        return None


def writeCleanedData(file_in,file_out):
    with codecs.open (file_out,'wb') as output:
        output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write(b'<osm>\n  ')
        for i, element in ET.iterparse(file_in):
            element = clean_element(element)
            output.write(ET.tostring(element, encoding='utf-8'))
            element.clear()
        output.write(b'</osm>')


# writeCleanedData('updated.osm', 'cleaned.osm')

def outputJSON(file_in, file_out, pretty = False):
    # file_out="{0}.txt".format(file)
    with codecs.open(file_out, "w",'utf_8_sig') as fo:
        context=ET.iterparse(file_in)
        _, root =next(context)
        for _, element in context:
            if element.tag in ['node','way']:
                element = clean_element(element)
                el = shape_element(element)
                if el:
                    # data.append(el)
                    if pretty:
                      fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                      fo.write(json.dumps(el,ensure_ascii=False) + "\n")
                    element.clear()
            
    return 

outputJSON('sample_updated.osm','sample_updated_test.txt')
# outputJSON('updated.osm','updated.txt')












