# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:16:01 2015

@author: adejaco
"""

#!/usr/bin/env python
"""
Use an aggregation query to answer the following question. 

Which Region in India has the largest number of cities with longitude between 75 and 80?

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation 
pipeline that can be passed to the MongoDB aggregate function. As in our examples in this lesson, 
the aggregation pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you want to run this 
code locally on your machine, you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a smaller version of the twitter dataset used in 
examples in this lesson. If you attempt some of the same queries that we looked at in the lesson 
examples, your results will be different.
"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


def aggregate(db, pipeline):
    result = db.mystreets.aggregate(pipeline)
    return result

if __name__ == '__main__':
    # The following statements will be used to test your code by the grader.
    # Any modifications to the code past this point will not be reflected by
    # the Test Run.
    db = get_db('columbus_ohio')

    #find the number of nodes that contain an address field
   

    pipeline4 = [{"$match" : { "address" : {"$exists" :1}, "type":"node"}},
                  {"$group": {"_id":"$type",
                       "count":{"$sum":1}}}]
    result = aggregate(db, pipeline4) 
    address_num = result.next()["count"]                   
    print "number of nodes that have address fields =", address_num
    
    pipeline5 = [{"$match" : { "address" : {"$exists" :1}, "type":"node"}}]
    result = aggregate(db, pipeline5)
    # print first 5 addresses  
    for i in range(5):
        print result.next()["address"]
    
    #find the number of ways that contain an address field
   

    pipeline4 = [{"$match" : { "address" : {"$exists" :1}, "type":"way"}},
                  {"$group": {"_id":"$type",
                       "count":{"$sum":1}}}]
    result = aggregate(db, pipeline4) 
    address_num = result.next()["count"]                   
    print "number of ways that have address fields =", address_num
    
    pipeline5 = [{"$match" : { "address" : {"$exists" :1}, "type":"way"}}]
    result = aggregate(db, pipeline5)
    # print first 5 addresses  
    for i in range(5):
        print result.next()["address"]
     #find the number of nodes that contain an "pos" field
   

    pipeline4 = [{"$match" : { "pos" : {"$exists" :1}, "type":"node"}},
                  {"$group": {"_id":"$type",
                       "count":{"$sum":1}}}]
    result = aggregate(db, pipeline4) 
    pos_num = result.next()["count"]                   
    print "number of nodes that have a position field =", pos_num
    
 
    #find the number of ways that contain an "pos" field
   

    pipeline4 = [{"$match" : { "pos" : {"$exists" :1}, "type":"way"}},
                  {"$group": {"_id":"$type",
                       "count":{"$sum":1}}}]
    result = aggregate(db, pipeline4)
    try:
        pos_num = result.next()["count"]                   
        print "number of ways that have address fields =", pos_num
    except:
        print "No ways have position fields"
    
 
 
 