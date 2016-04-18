# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 14:51:57 2015

@author: adejaco
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["type"] = element.tag
        node["created"] = {}
        first = True
        for key in element.attrib:
            if key in CREATED:
                node["created"][key] = element.attrib[key]
                continue
            if key == "lat":
                if first == True:
                    node["pos"] = [None,None]
                    first = False
                node["pos"][0] = float(element.attrib[key]) 
                continue
            if key == "lon":
                if first == True:
                    node["pos"] = [None,None]
                    first = False
                node["pos"][1] = float(element.attrib[key]) 
                continue
            node[key] = element.attrib[key]
                
        for tag in element.iter("tag"):  # check addreses
                process_address_tag(tag.attrib['k'],tag.attrib['v'],node) #tag.attrib['k'] is just a string to appy rules to
        
        for ref in element.iter("nd"):  # append references to way
    
                try:
                    node["node_refs"].append(ref.attrib['ref'])
                   
                except:
                    node["node_refs"]= []
                    node["node_refs"].append(ref.attrib['ref'])
                  
            #check for special attributes
            
            
        return node
    else:
        return None
        
def process_address_tag(address,value,node):
    if problemchars.search(address) != None:
            return node  #if contains probem character don't add tag 
    if address.find("addr:")== 0:
        if address.find("addr:street:")== 0:
            return node # ignore tag
        if address.find("addr:street")== 0: 
            value = update_street(value)# clean street value 
        try:
            node["address"][address[5:]] =  value
            return node
        except:
            node["address"]={}
            node["address"][address[5:]] =  value
            return node
                
    node[address] =  value
    return node
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]
expectedfix_2 = ["Ste","SR","Rt","St.Rt.","Rd","St"]
expectedfix_3 = ["Rd","E","W","N","S","E.","W.","N.","S."]

# UPDATE THIS VARIABLE
mapping = {  "St": "Street", 
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
def update_street(street_name):
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
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []

    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            
            if el:
              # Don't need to create the data file list: data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.

    data = process_map('columbus_ohio.osm', pretty=False)
    #pprint.pprint(data)
 
 
    pass

if __name__ == "__main__":
    test()