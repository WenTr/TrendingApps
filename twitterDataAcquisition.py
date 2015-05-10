'''
Created on Apr 24, 2015

@author: Sherry

Resources:
Twitter API: https://dev.twitter.com/overview/documentation
TwitterSearch External Library: https://github.com/ckoepp/TwitterSearch
'''

from TwitterSearch import *
import time
import json

class TwitterDataAcquisition:
    
    consumer_key = ''
    consumer_secret = ''
    
    access_token = ''
    access_secret = ''
        
    jsonKeysList = ["created_at", "text", "retweet_count", "source", "user"]
    
    userJsonKeysList = ["name", "screen_name", "location", "followers_count", 
                        "friends_count", "created_at", "time_zone"]
    
    infoDict = {}        
    dynAppsList = []
    
    def __init__(self, dynAppsList):
        self.dynAppsList = dynAppsList
        self.getTwitterData()
    
    def getTwitterData(self):
        auth = TwitterSearch(self.consumer_key, self.consumer_secret, 
                             self.access_token, self.access_secret)

        for app in self.dynAppsList:
            appsDict = {}

            tweetDict = self.searchTweets(auth, [app + " app"])
            appsDict[app] = tweetDict
                    
        self.infoDict["twitter"] = appsDict
        
        return self.infoDict
        
    def searchTweets(self, auth, keyword):
        tweetID = 0
        tweetDict = {}
        tweetCounter = 0
        print keyword
        searchQuery = TwitterSearchOrder()
        searchQuery.set_keywords(keyword)
        searchQuery.set_count(1)
        
        for tweet in auth.search_tweets_iterable(searchQuery):
            if tweetCounter == 175:
                tweetCounter = 0
                time.sleep(60)
                
            tweetCounter += 1
                        
            tweetID += 1
            tweetDict["tweetID"] = tweetID
            for jsonKey in self.jsonKeysList:
                if jsonKey == "user":
                    userDict = {}
                    for userKey in self.userJsonKeysList:
                        userDict[userKey] = tweet["user"][userKey]
                    
                    tweetDict[jsonKey] = userDict
                elif jsonKey == "source":                    
                    sourceString = tweet[jsonKey]
                    tweetDict[jsonKey] = sourceString.replace('\\', '')
                else:
                    tweetDict[jsonKey] = tweet[jsonKey]
        
        print json.dumps(tweetDict, indent = 4)
 
        return tweetDict