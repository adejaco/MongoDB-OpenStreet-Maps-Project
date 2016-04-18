# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:16:01 2015

@author: adejaco
"""

#!/usr/bin/env python
"""
Use an aggregation query to answer the following question.:
Find an address from a position and conversely find position information from 
an address.   This program uses 
 2201 Neil Avenue Columbus OH 43201 (a house in the database from a way that has no address).
 I looked up the lat and long for this address and got:
     lat = 40.006700
     long = -83.014451
Then I built the queries to perform the desired functions

"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():

#Andy's house:
#    lat = 40.150035
#    long = -83.157755
#Andy's business:  40.112522,-83.087457
  #  lat = 40.112522
  #  long = -83.087457
  #  region = .0005

#    2201 Neil Avenue Columbus OH 43201 (a house in the database)
    lat = 40.006700
    long = -83.014451
    region = .0001
#u'id': u'571690081'
# u'id': u'571690084

    pipeline = [{"$match" : { "pos.0" : {"$gt" : lat - region, "$lt" : lat + region},
                              "pos.1" : {"$gt" : long-region, "$lt" : long+region }, "type":"node"}}#.

                      #  {"$group": {"_id":"$type",
                      #   "count":{"$sum":1}}}           
                        ]
          
   # pipeline = [{"$match" : {"pos"[0]:{"$gt": 10.10}, "pos"[0]:{"$lt": 50.12}}}]
     #                     "pos[1]":{"$lt": -83}  }}]
  #  pipeline = [{"$match" : {"type":"way"}}]
    return pipeline

def aggregate(db, pipeline):
    result = db.mystreets.aggregate(pipeline)
    return result

if __name__ == '__main__':
    # The following statements will be used to test your code by the grader.
    # Any modifications to the code past this point will not be reflected by
    # the Test Run.
    db = get_db('columbus_ohio')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    node = result.next()
    nid = node["id"]
    print " The node and the Node id found at that location is ",node, nid
# now find "ways" that contains that nid    
    
    pipeline2 = [{"$match" : { "node_refs" : {"$in" : [nid]}, "address" : {"$exists" :1}}},
                 {"$group": {"_id":"$type",
                        "count":{"$sum":1}}}]
    #.
    result = aggregate(db, pipeline2)
    print "************************"
    print "number of documents with that Node ID =", result.next()["count"]
   
    pipeline3 = [{"$match" : { "node_refs" : {"$in" : [nid]},"address" : {"$exists" :1}}}]
    print "Here's the location address ", aggregate(db, pipeline3).next()["address"]
    

# now find lat and lon from address
    house = "2201"
    street = "Neil Avenue"
    zipcode = "43201"
    pipeline6 = [{"$match" : { "address.housenumber" : house, "address.street":street,
                                "address.postcode": zipcode}}]
    node_ref = aggregate(db, pipeline6).next()["node_refs"][0] 
    print "************************"
    print "node reference number for the address is =",node_ref   
    pipeline7 = [{"$match" : { "id" : node_ref}}] 
    position = aggregate(db, pipeline7).next()["pos"]   
    print "************************"
    print "The lat and lon of the address requested is = ",position
    pass
 
 