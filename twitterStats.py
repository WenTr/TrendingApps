'''
Created on May 23, 2015

@author: Sherry
'''

import pymongo
from json import dumps
from math import sqrt

class TwitterStats():
    conn = pymongo.MongoClient()
    db = conn['trendingapps']
    
    def  __init__(self):
        pass
    
    def get_twitter_stats(self):
        stat_dict = {}
        stat_dict['mean'] = self.get_mean()
        stat_dict['median'] = self.get_median()
        stat_dict['mode'] = self.get_mode()
        stat_dict['standard_deviation'] = self.get_SD()
        
        return stat_dict
    
    def get_mean(self):
        mean_dict = {}
        
        for num in range(1, 11):
            appDict = self.db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
                
            for appTitle in appDict.keys():
                total_retweets = 0;
                appName = appDict[appTitle]['title']
    
                if appName == 'Criminal Case':
                    for num2 in range(0, 11):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            total_retweets += int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                    
                    mean_dict[appName] = str(total_retweets/11)
                elif appName == 'WhatsApp Messenger':
                    for num2 in range(0, 14):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            total_retweets += int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                    
                    mean_dict[appName] = str(total_retweets/14)
                elif appName == 'Super-Bright LED Flashlight':
                    for num2 in range(0, 12):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            total_retweets += int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                    
                    mean_dict[appName] = str(total_retweets/12)
                else:
                    for num2 in range(0, 18):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            total_retweets += int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                    
                    mean_dict[appName] = str(total_retweets/18)
        
        return mean_dict
    
    def get_median(self):
        median_dict = {}
        
        for num in range(1, 11):
            appDict = self.db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
                
            for appTitle in appDict.keys():
                most_retweet = 0
                appName = appDict[appTitle]['title']
    
                if appName == 'Criminal Case':
                    median_list = []
                    for num2 in range(0, 11):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            median_list.append(int(info[appName]['tweet_' + str(num2)]['retweet_count']))
                            
                    median_list.sort()
                    median_dict[appName] = median_list[len(median_list)/2]
                elif appName == 'WhatsApp Messenger':
                    median_list = []
                    for num2 in range(0, 14):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                median_list.append(int(info[appName]['tweet_' + str(num2)]['retweet_count']))
                            
                        median_list.sort()
                        median_dict[appName] = median_list[len(median_list)/2]            
                elif appName == 'Super-Bright LED Flashlight':
                    median_list = []
                    for num2 in range(0, 12):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                median_list.append(int(info[appName]['tweet_' + str(num2)]['retweet_count']))
                            
                    median_list.sort()
                    median_dict[appName] = median_list[len(median_list)/2]
                else:
                    median_list = []
                    for num2 in range(0, 18):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                median_list.append(int(info[appName]['tweet_' + str(num2)]['retweet_count']))
                            
                    median_list.sort()
                    median_dict[appName] = median_list[len(median_list)/2]
    
        return median_dict
    
    def get_mode(self):
        mode_dict = {}
        
        for num in range(1, 11):
            appDict = self.db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
                
            for appTitle in appDict.keys():
                most_retweet = 0
                appName = appDict[appTitle]['title']
    
                if appName == 'Criminal Case':
                    for num2 in range(0, 11):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                most_retweet = retweet
                            
                    mode_dict[appName] = most_retweet
                elif appName == 'WhatsApp Messenger':
                    for num2 in range(0, 14):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                most_retweet = retweet
                                
                    mode_dict[appName] = most_retweet
                elif appName == 'Super-Bright LED Flashlight':
                    for num2 in range(0, 12):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                most_retweet = retweet
                                
                    mode_dict[appName] = most_retweet
                else:
                    for num2 in range(0, 18):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            
                            if retweet > most_retweet:
                                most_retweet = retweet
                    
                    mode_dict[appName] = most_retweet
    
        return mode_dict
    
    def get_SD(self):
        sd_dict = {}
        
        for num in range(1, 11):
            appDict = self.db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
                
            for appTitle in appDict.keys():
                sq_retweet = 0
                total_retweet = 0
                
                appName = appDict[appTitle]['title']
    
                if appName == 'Criminal Case':
                    for num2 in range(0, 11):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            sq_retweet += retweet ** 2
                            total_retweet += retweet
                    
                    sd_dict[appName] = round(sqrt(((11*sq_retweet) - (total_retweet ** 2))/(11 * 10)), 1)
                elif appName == 'WhatsApp Messenger':
                    for num2 in range(0, 14):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            sq_retweet += retweet ** 2
                            total_retweet += retweet
                    
                    sd_dict[appName] = round(sqrt(((14*sq_retweet) - (total_retweet ** 2))/(14 * 13)), 1)
                elif appName == 'Super-Bright LED Flashlight':
                    for num2 in range(0, 12):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            sq_retweet += retweet ** 2
                            total_retweet += retweet
                    
                    sd_dict[appName] = round(sqrt(((12*sq_retweet) - (total_retweet ** 2))/(12 * 11)), 1)
                else:
                    for num2 in range(0, 18):
                        tweet_dict = self.db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                            
                        for info in tweet_dict:
                            retweet = int(info[appName]['tweet_' + str(num2)]['retweet_count'])
                            sq_retweet += retweet ** 2
                            total_retweet += retweet
                    
                    sd_dict[appName] = round(sqrt(((18*sq_retweet) - (total_retweet ** 2))/(18 * 17)), 1)
        
        return sd_dict