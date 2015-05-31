'''
Created on May 30, 2015

@author: Sherry
'''

import pymongo
import numpy
from json import dumps

class TwitterStats():
    conn = pymongo.MongoClient()
    db = conn['trendingapps']
    
    def  __init__(self):
        pass
    
    def get_twitter_stats(self):
        twitter_stat = {}
        stat_dict = {}
        
        for num in range(1, 11):
            app_dict = self.db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
            
            for app_title in app_dict.keys():
                app_stat_dict = {}
                
                app_name = app_dict[app_title]['title']
                                
                app_stat_dict['retweet_mean'] = self.get_retweet_mean(app_name)
                app_stat_dict['retweet_median'] = self.get_retweet_median(app_name)
                app_stat_dict['retweet_mode'] = self.get_retweet_mode(app_name)
                app_stat_dict['retweet_standard_deviation'] = self.get_retweet_SD(app_name)
                
                app_stat_dict['user_mean'] = self.get_user_mean(app_name)
                app_stat_dict['user_median'] = self.get_user_median(app_name)
                app_stat_dict['user_mode'] = self.get_user_mode(app_name)
                app_stat_dict['user_standard_deviation'] = self.get_user_SD(app_name)
                
                stat_dict[app_name] = app_stat_dict
                
        twitter_stat['twitter'] = stat_dict

        return twitter_stat
        
    def get_retweet_mean(self, app_name):
        rt_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                rt_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['retweet_count']))
        
        if rt_count_list:
            return int(round(numpy.mean(rt_count_list)))
        else:
            return 0
            
    def get_retweet_median(self, app_name):
        rt_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                rt_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['retweet_count']))
        
        if rt_count_list:
            rt_count_list.sort()
            return int(round(numpy.median(rt_count_list)))
        else:
            return 0
            
    def get_retweet_mode(self, app_name):
        rt_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                rt_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['retweet_count']))
        
        if rt_count_list:
            return max(rt_count_list)
        else:
            return 0
            
    def get_retweet_SD(self, app_name):
        rt_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                rt_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['retweet_count']))
        
        if rt_count_list:
            return int(round(numpy.std(rt_count_list)))
        else:
            return 0
    
    def get_user_mean(self, app_name):
        f_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                f_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['user']['followers_count']))
        
        if f_count_list:
            return int(round(numpy.mean(f_count_list)))
        else:
            return 0
            
    def get_user_median(self, app_name):
        f_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                f_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['user']['followers_count']))
        
        if f_count_list:
            f_count_list.sort()
            return int(round(numpy.median(f_count_list)))
        else:
            return 0
            
    def get_user_mode(self, app_name):
        f_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                f_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['user']['followers_count']))
                
        if f_count_list:
            return max(f_count_list)
        else:
            return 0
            
    def get_user_SD(self, app_name):
        f_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, 
                                          {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, len(tweet_dict[app_name])):
                f_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['user']['followers_count']))
        
        if f_count_list:
            return int(round(numpy.std(f_count_list)))
        else:
            return 0