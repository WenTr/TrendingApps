# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 22:04:10 2015

@author: WT
Sources:
http://altons.github.io/python/2013/01/21/gentle-introduction-to-mongodb-using-pymongo/
http://stackoverflow.com/questions/9822575/how-to-check-in-pymongo-if-collection-exists-and-if-exists-empty-remove-all-fro
"""

from TA_GP import GooglePlay
import pymongo
import json
import pprint


try:
    conn = pymongo.MongoClient()
    print "Successful Connection"
except pymongo.errors.ConnectionFailure, e:
    print "Error During Connection"

db = conn['test2']


gp = GooglePlay()
gpInfo = gp.getGPInfo()
appTitles = gpInfo[0]
appInfo = gpInfo[1]


db.googleplay.insert(appInfo)

print conn.database_names()
print db.collection_names()

a = db.googleplay.find_one()
for b in a:   
    print b
#print pprint(a)
#print json.dumps(a, indent = 4)