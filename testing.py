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

try:
    conn = pymongo.MongoClient()
    print "Successful Connection"
except pymongo.errors.ConnectionFailure, e:
    print "Error During Connection"

db = conn['test']

gp = GooglePlay()
gpInfo = gp.getGPInfo()

db.googleplay.insert(gpInfo)

print conn.database_names()
print db.collection_names()

print db.googleplay.find()[0]