'''
Created on May 30, 2015

@author: Sherry
'''

import pymongo
import numpy
import textblob

import re
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
                
                app_stat_dict['num_tweets'] = self.get_tweet_num(app_name)
                
                rt_list = self.get_retweet_list(app_name)
                rt_list.sort()
                
                if rt_list:
                    app_stat_dict['retweet_mean'] = int(round(numpy.mean(rt_list)))
                    app_stat_dict['retweet_median'] = int(round(numpy.median(rt_list)))
                    app_stat_dict['retweet_mode'] = max(rt_list)
                    app_stat_dict['retweet_standard_deviation'] = int(round(numpy.std(rt_list)))
                    
                    t_list = self.get_tweet_list(app_name)
                    sa_list, sa_avg = self.get_SA(t_list)
                    
                    app_stat_dict['sa_list'] = sa_list
                    app_stat_dict['sa_avg'] = sa_avg
                else:
                    app_stat_dict['retweet_mean'] = 0
                    app_stat_dict['retweet_median'] = 0
                    app_stat_dict['retweet_mode'] = 0
                    app_stat_dict['retweet_standard_deviation'] = 0
                    app_stat_dict['sa_list'] = []
                    app_stat_dict['sa_avg'] = 0     
                    
                
                f_list = self.get_follower_list(app_name)
                f_list.sort()
                
                if rt_list:
                    app_stat_dict['user_mean'] = int(round(numpy.mean(f_list)))
                    app_stat_dict['user_median'] = int(round(numpy.median(f_list)))
                    app_stat_dict['user_mode'] = max(rt_list)
                    app_stat_dict['user_standard_deviation'] = int(round(numpy.std(f_list)))
                else:

                    app_stat_dict['user_mean'] = 0
                    app_stat_dict['user_median'] = 0
                    app_stat_dict['user_mode'] = 0
                    app_stat_dict['user_standard_deviation'] = 0        
                
                stat_dict[app_name] = app_stat_dict
                
        twitter_stat['twitter'] = stat_dict
        #print dumps(twitter_stat, indent = 4)
        return twitter_stat
        
    def get_tweet_num(self, app_name):
        tweet_total = 0;
        
        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            tweet_total = len(tweet_dict[app_name])
            
        return tweet_total
    
    def get_retweet_list(self, app_name):
        rt_count_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, (self.get_tweet_num(app_name) + 1)):
                rt_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['retweet_count']))

        return rt_count_list
    
    def get_tweet_list(self, app_name):
        tweet_list = []

        tweet_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, {str(app_name):1, '_id': 0})
        
        for tweet_dict in tweet_dict_cursor:
            for num in range(1, (self.get_tweet_num(app_name) + 1)):
                text = tweet_dict[app_name]['tweet_' + str(num)]['text']
                tweet_list.append(text.encode('ascii', 'ignore').strip())

        return tweet_list
    
    def get_follower_list(self, app_name):
        f_count_list = []

        user_dict_cursor = self.db.twitter.find({str(app_name): {'$exists': 1}}, {str(app_name): 1, '_id': 0})
        
        for tweet_dict in user_dict_cursor:
            for num in range(1, self.get_tweet_num(app_name)):
                f_count_list.append(int(tweet_dict[app_name]['tweet_' + str(num)]['user']['followers_count']))
        
        return f_count_list
    
    def get_SA(self, tweet_list):
        sa_list = []
        
        for tweet in tweet_list:
            sa_list.append(textblob.TextBlob(tweet).sentiment.polarity)
        
        return sa_list, round(numpy.mean(sa_list), 2)