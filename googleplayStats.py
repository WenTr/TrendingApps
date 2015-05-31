# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:39:32 2015

@author: Wendy Tran
"""
'''
Sources:
http://stackoverflow.com/questions/252703/python-append-vs-extend
http://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html
http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
'''
from collections import Counter
import pymongo
import re
import math
import numpy as np
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import json

conn = pymongo.MongoClient()
db = conn['trendingapps']
gcollec = db['googleplay']

class GooglePlayStats:

    def __init__(self):
        pass

    def getMean(self, appRatings):
        for (appName, ratingList) in appRatings.items():
            #print appName
            #appMean = ( 1.0*sum(ratingList) )/len(ratingList)
            appMean = np.mean(ratingList)
            return round(appMean, 1)
            
    def getMedian(self, appRatings):
        for (appName, ratingList) in appRatings.items():
            #mid = len(ratingList)/2
            #return (1.0*( ratingList[mid] + ratingList[mid-1] ))/2
            return np.median(ratingList)            
            
    def getMode(self, appRatings):
        for (appName, ratingList) in appRatings.items():
            return Counter(ratingList).most_common(1)[0][0]
    
    def getStDev(self, appRatings):
        for (appName, ratingList) in appRatings.items():
#            #numerator
#            squaredList = [r**2 for r in ratingList]
#            sumSquaredList = sum(squaredList)
#            x = len(ratingList)*sumSquaredList - sum(ratingList)**2
#    
#            #denominator
#            d = len(ratingList)*( len(ratingList)-1 )
#            
#            variance = (1.0*x)/d
#            sD = round(math.sqrt(variance), 1)
            sD = np.std(ratingList)
            return sD

    def getSentiAnaly(self, appNum):
        sentianaly = {}
        reviews = {}
        meanOfPolar = 0.0
        sentiList = []
        
        for reviewNum in range(0, 40):
            rev = gcollec.find({str(appNum): {'$exists': 1}}, {str(appNum) + '.reviews.review_'+str(reviewNum)+'.comment': 1, '_id': 0})[0]
            #the comment
            r = rev[str(appNum)]['reviews']['review_'+str(reviewNum)]['comment']
            
            #sentimental analysis on the comment
            r2 = TextBlob(r.encode('ascii', 'ignore'))
            polar = r2.sentiment[0]
            
            #adding the comment into the dictionary and list
            sentianaly['review_'+str(reviewNum)] = round(polar, 5)
            sentiList.append(polar)
        reviews['SentimentalAnalysis'] = sentianaly
        
        #finding the mean of the polarity
        meanOfPolar = np.mean(sentiList)
        reviews['meanOfPolarity'] = round(meanOfPolar, 5)
                
        #print json.dumps(reviews, indent=4)
        return reviews
        
    def getReviewRatings(self):
        appRatings = {}
        appStats = {}
        appStatsTemp = {}
        apps = {}
        sa = {}
        
        for num in range(1, 11):        
            appList = []
        
            appDict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, str(num) + '.reviews': 1, '_id': 0})[0]
            #print appDict[str(num)]['title']        
            for reviewNum in range(0, 40):
                appList.append(int(re.findall('\d', str(appDict[str(num)]['reviews']['review_'+str(reviewNum)]['rating']))[0]))
                
            appList.sort()   
            appRatings[str(appDict[str(num)]['title'])] = appList
            #print appRatings
            appStatsTemp['stats'] = {'mean':self.getMean(appRatings), 'median':self.getMedian(appRatings), 'mode':self.getMode(appRatings), 'sd':self.getStDev(appRatings)}
            sa = self.getSentiAnaly(num)
            temp = appStatsTemp.copy()
            temp.update(sa)
            appStats[str(appDict[str(num)]['title'])] = temp
            apps['appNames'] = appStats
        return apps