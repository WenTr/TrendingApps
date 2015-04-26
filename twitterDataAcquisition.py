'''
Created on Apr 24, 2015

@author: Sherry

Resources:
Twitter API: https://dev.twitter.com/overview/documentation
TwitterSearch External Library: https://github.com/ckoepp/TwitterSearch
'''

from TwitterSearch import *
import time

from json import dumps

class TwitterDataAcquisition:
    
    consumer_key = ""
    consumer_secret = ""
    
    access_token = ""
    access_secret = ""
    
    dynAppsList = ["Messenger", "Criminal Case", "Facebook", "Pandora Radio", 
                   "Instagram", "Snapchat", "Dubsmash",
                   "Super-Bright LED Flashlight", "Spotify Music",
                   "Clean Master (Speed Booster)"]
        
    jsonKeysList = ["created_at", "text", "retweet_count", "source", "user"]
    
    userJsonKeysList = ["name", "screen_name", "location", "followers_count", 
                        "friends_count", "created_at", "time_zone"]
    
    infoDict = {}        
    
    def __init__(self):
        self.getTwitterData()
    
    def getTwitterData(self):
        auth = TwitterSearch(self.consumer_key, self.consumer_secret, 
                             self.access_token, self.access_secret)
                
        appsDict = {}
            
        tweetDict = self.searchTweets(auth, ["facebook app"])
        appsDict["facebook app"] = tweetDict
                    
        self.infoDict["twitter"] = appsDict
        
        
        '''
        for app in self.dynAppsList:
            time.sleep(30)
            appsDict = {}
            
            tweetDict = self.searchTweets(auth, [app + " app"])
            appsDict[app] = tweetDict
                    
        self.infoDict["twitter"] = appsDict
        
        return self.infoDict
        '''
    def searchTweets(self, auth, keyword):
        tweetID = 0
        tweetDict = {}
        
        searchQuery = TwitterSearchOrder()
        searchQuery.set_keywords(keyword)
        searchQuery.set_count(1)
        
        for tweet in auth.search_tweets_iterable(searchQuery):
            time.sleep(5)
            tweetDict["tweetID"] = tweetID + 1
            for jsonKey in self.jsonKeysList:
                if jsonKey == "user":
                    userDict = {}
                    for userKey in self.userJsonKeysList:
                        userDict[userKey] = tweet["user"][userKey]
                    
                    tweetDict[jsonKey] = userDict
                elif jsonKey == "source":                    
                    sourceString = tweet[jsonKey]
                    tweetDict[jsonKey] = sourceString.strip("\\")
                else:
                    tweetDict[jsonKey] = tweet[jsonKey]
        
        return tweetDict
    
def main():
    twitterData = TwitterDataAcquisition()
        
    #jsonFile = ("twitter_data.json", "w")
    #jsonFile.write(str(twitterData))
    #jsonFile.close()
    
    print dumps(twitterData)

if __name__ == '__main__':
    main()