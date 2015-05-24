# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:39:32 2015

@author: Wendy Tran
"""
'''
Sources:
http://stackoverflow.com/questions/252703/python-append-vs-extend
'''
from collections import Counter
import pymongo
import re
import math
#import json

conn = pymongo.MongoClient()
db = conn['trendingapps']
gcollec = db['googleplay']

class GooglePlayStats:

    def __init__(self):
        pass

def getMean(self, appRatings):
    for (appName, ratingList) in appRatings.items():
        #print appName
        appMean = ( 1.0*sum(ratingList) )/len(ratingList)
        return round(appMean, 1)
        
def getMedian(self, appRatings):
    for (appName, ratingList) in appRatings.items():
        mid = len(ratingList)/2
        return (1.0*( ratingList[mid] + ratingList[mid-1] ))/2
        
def getMode(self, appRatings):
    for (appName, ratingList) in appRatings.items():
        return Counter(ratingList).most_common(1)[0][0]

def getStDev(self, appRatings):
    for (appName, ratingList) in appRatings.items():
        #numerator
        squaredList = [r**2 for r in ratingList]
        sumSquaredList = sum(squaredList)
        x = len(ratingList)*sumSquaredList - sum(ratingList)**2

        #denominator
        d = len(ratingList)*( len(ratingList)-1 )
        
        variance = (1.0*x)/d
        sD = round(math.sqrt(variance), 1)
        return sD
    
def getReviewRatings(self):
    appRatings = {}
    appStats = {}    
    
    for num in range(1, 11):        
        appList = []
    
        appDict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, str(num) + '.reviews': 1, '_id': 0})[0]
        #print appDict[str(num)]['title']        
        for reviewNum in range(0, 40):
            appList.append(int(re.findall('\d', str(appDict[str(num)]['reviews']['review_'+str(reviewNum)]['rating']))[0]))
            
        appList.sort()   
        appRatings[str(appDict[str(num)]['title'])] = appList
        #print appRatings
        appStats[str(appDict[str(num)]['title'])] = {'mean':self.getMean(appRatings), 'median':self.getMedian(appRatings), 'mode':self.getMode(appRatings), 'sd':self.getStDev(appRatings)}
        
    return appStats