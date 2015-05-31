'''
Created on May 23, 2015

@author: Sherry

Twitter Search API: https://dev.twitter.com/rest/public/search
TwiiterSearch External Library: https://github.com/geduldig/TwitterAPI/blob/master/examples/api_test.py
'''

from TwitterAPI import *

from json import dumps

class Twitter_API:
    
    consumer_key = 'AQOeMUImTqcPLm1KS847pdo6Y'
    consumer_secret = 'FNFXTMjfyABt57UHaxstz2p8juasQRBenulQqGhqo85T1KxhCK'
    
    access_token = '313601183-CQKz2PLX8ohQZyaLDyQ64Vvp2Z3Q1Eq4CkbDtc8O'
    access_secret = '1NbqrzmR7JaWKewqAVRXrk7FgJklGDpvrmpyONtuAqYbP'
            
    def __init__(self):
        #Purposely empty
        pass
    
    def get_tweets(self, app_list):
        twitter_dict = {}
        app_dict = {}
        
        auth = self.auth_lib()
        
        for app in app_list:          
            app_tweet_dict = self.search_tweets_lib(auth, '\"' + app + '\" app OR \"' + app + ' app\"')

            app_dict[app] = app_tweet_dict
                            
        twitter_dict['twitter'] = app_dict
        
        return twitter_dict
    
    def auth_lib(self):
        auth = TwitterAPI(self.consumer_key, self.consumer_secret, 
                         self.access_token, self.access_secret)
        
        return auth
        
    def search_tweets_lib(self, auth, keyword):
        tweet_ID = 0
        tweet_group_dict = {}
                
        for tweet in auth.request('search/tweets', {'q': keyword, 'count': 100, 'lang': 'en'}):
            tweet_dict = {}
            tweet_ID += 1
                        
            json_keys_list = ['created_at', 'text', 'retweet_count', 'user']
    
            user_json_keys_list = ['name', 'screen_name', 'location', 'followers_count', 'friends_count', 'created_at', 'time_zone']
            
            for tweet_key in json_keys_list:
                if tweet_key == 'user':
                    user_dict = {}
                    
                    for user_key in user_json_keys_list:
                        user_dict[user_key] = tweet['user'][user_key]
                    
                    tweet_dict[tweet_key] = user_dict
                else:
                    tweet_dict[tweet_key] = tweet[tweet_key]
            
            tweet_group_dict['tweet_' + str(tweet_ID)] = tweet_dict   
            '''
            print '-' * 20
            print 'Date: ' + tweet_dict['created_at']
            print 'Tweet: ' + tweet_dict['text']
            print 'Retweets: ' + str(tweet_dict['retweet_count'])
            print 'Favorited: ' + str(tweet_dict['favorite_count'])
            print 'Name: ' + user_dict['name']
            print 'Screen Name: ' + user_dict['screen_name']
            print 'Location: ' + user_dict['location']
            print 'Followers Count: ' + str(user_dict['followers_count'])
            print 'Created At: ' + user_dict['created_at']
            '''
        #print keyword, len(tweet_group_dict)
        return tweet_group_dict