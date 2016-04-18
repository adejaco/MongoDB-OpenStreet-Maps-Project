# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 14:49:39 2015

@author: adejaco
"""

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

OSMFILE = "columbus_ohio.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]
expectedfix_2 = ["Ste","SR","Rt","St.Rt.","Rd","St"] # 2nd last word to fix
expectedfix_3 = ["Rd","E","W","N","S","E.","W.","N.","S."] # 3rd last word to fix

# UPDATE THIS VARIABLE
mapping = { "St": "Street", 
            "St.": "Street",
           "Ave":"Avenue",
           "Ave.":"Avenue",
           "Rd.":"Road",
           "Rd":"Road",
           "rd":"Road",
           "Blvd":"Boulevard",
           "Blvd.":"Boulevard",
           "Cir": "Circle",
           "Ct":"Court",
           "Dr":"Drive",
           "dr":"Drive",
           "E.":"East",
           "E":"East",
           "Ln":"Lane",
           "N":"North",
           "N.":"North",
           "Parkwa":"Parkway",
           "Pk":"Pike",
           "Pkwy":"Parkway",
           "Pky":"Parkway",
           "Pl":"Place",
           "S":"South",
           "S.":"South",
           "SE":"Southeast",
           "Ste":"Suite",
           "SR": "State Route",
           "Rt":"Route",
           "St.Rt.":"State Route",
            "SW":"Southwest",
            "Sw":"Southwest",
            "W":"West",
            "W.":"West"
            
           }


def audit_street_type(street_types, street_name):
 
#After iterating on this audit, I wanted to correct abbreviations in the last 3 words
#in the street name.  Note that for the last word I'm looking for expected word and for the 2nd 
#and 3rd last I'm looking for expected mistakes 
 
    street_words = street_name.split()
    street_type = street_words[-1] # pick off the last word as the street type
    if street_type not in expected:
       street_types[street_type].add(street_name)
    if len(street_words) >= 2:
       street_type_2 = street_words[-2]
       if street_type_2 in expectedfix_2:
           street_types[street_type_2].add(street_name)   
    if len(street_words) >= 3:
       street_type_3 = street_words[-3]
       if street_type_3 in expectedfix_3:
           street_types[street_type_3].add(street_name)   
 

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set) 
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(street_name, mapping):

       #split up street name and fix each of last 3 words individually
    
    street_words = street_name.split()
    street_type_1 = street_words[-1]
    if street_type_1 in mapping:
        street_words[-1] = mapping[street_type_1]# pick off the last word as the street type
       
    if len(street_words) >= 2:
        street_type_2 = street_words[-2]
        if street_type_2 in mapping:
            street_words[-2] = mapping[street_type_2]  
     
    if len(street_words) >= 3:
        street_type_3 = street_words[-3]
        if street_type_3 in mapping:
            street_words[-3] = mapping[street_type_3] 
      
    #Put the corrected words back into the street name
    new_name = street_words[0]
    if len(street_words) > 1:
        for i in range(1,len(street_words)):
            new_name += " "+ street_words[i]

    return new_name


def test():
    st_types = audit(OSMFILE)
  #  assert len(st_types) == 3
    pprint.pprint(dict(st_types))
    print "***********"
    print "Number of suspicious street name words is ",len(dict(st_types))
    print "***********"
    count = 0
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name != better_name:
                count += 1
    print "***********"       
    print "The number of street names fixed is ", count
 


if __name__ == '__main__':
    test()