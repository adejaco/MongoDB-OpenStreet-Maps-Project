# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 12:49:31 2015

@author: adejaco
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE
    tags_unique = {}
    for event,elem in ET.iterparse(filename):
            if elem.tag not in tags_unique:
                tags_unique[elem.tag] = 1
            else:
                tags_unique[elem.tag] += 1
    return tags_unique
            


def test():

    tags = count_tags('columbus_ohio.osm')
    pprint.pprint(tags)

    

if __name__ == "__main__":
    test()