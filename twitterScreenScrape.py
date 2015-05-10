'''
Created on May 8, 2015

@author: Sherry

Beutiful Soup External Library: http://www.crummy.com/software/BeautifulSoup/
'''

from bs4 import *
import requests
import re
from json import dumps

class TwitterScreenScrape:
    
    consumer_key = ''
    consumer_secret = ''
    
    access_token = ''
    access_secret = ''
        
    def __init__(self, app_list):
        self.app_list = app_list
        self.get_twitter_data(app_list)
        
    def get_twitter_data(self, app_list):
        twitter_dict = {}
        app_dict = {}
        
        for app in app_list:
            tweet_dict = self.search_tweet(app)
            app_dict[app] = tweet_dict
            
        twitter_dict['twitter'] = app_dict
        
        return twitter_dict 
    
    def search_tweet(self, app_name):
        tweet_dict = {}
        info_dict = {}
        tweet_ID = 0   
        #url_file = requests.get('https://twitter.com/search?f=realtime&q=' + str.lower(app) + '%20app&src=typd')
        url_file = requests.get('https://twitter.com/search?q=' + str.lower(app_name) + '%20app&src=typd')
        b_soup = BeautifulSoup(url_file.content)
            
        for tweet in b_soup.find_all('div', {'data-follows-you': 'false'}):
        #for tweet in b_soup.find_all('div', {'class': 'tweet'}):
            if tweet:
                date = tweet.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})
                info_dict['created_at'] = re.findall('\d\s\w\w\w\s\d\d\d\d', str(date.get('title')))[0] if date else ''
                    
                text = tweet.find('p', {'class': 'TweetTextSize  js-tweet-text tweet-text'})
                info_dict['text'] = text.text if text else ''
                    
                source = tweet.get('data-permalink-path')
                info_dict['source'] = ('http://twitter.com' + source) if source else ''
                
                user_URL = requests.get(info_dict['source'])
                b_soup_2 = BeautifulSoup(user_URL.content)
                
                retweet = b_soup_2.find('a', {'class': 'request-retweeted-popup'})
                info_dict['retweet_count'] = retweet.get('data-tweet-stat-count') if retweet else 0
                                                            
                for username_list in tweet.find_all('span', {'class': 'username js-action-profile-name'}):
                    user_dict = {}
                    
                    username = username_list.find('b').text
                    user_dict['screen_name'] = username if username else ''
                        
                    user_URL = requests.get('https://twitter.com/' + username)
                    b_soup_3 = BeautifulSoup(user_URL.content)
                        
                    name = b_soup_3.find('a', {'class': 'ProfileHeaderCard-nameLink'})
                    user_dict['name'] = name.text if name else ''
                        
                    location = b_soup_3.find('span', {'class': 'ProfileHeaderCard-locationText'})
                    user_dict['location'] = location.text.strip() if location else ''
                        
                    followers = b_soup_3.find('a', {'data-nav': 'followers'})
                    user_dict['followers_count'] = ((followers.get('title')).strip(' Followers')).replace(',', '') if str(followers.text) != "" else 0
                        
                    user_date = b_soup_3.find('span', {'class': 'ProfileHeaderCard-joinDateText'})
                    user_dict['created_at'] = re.findall('\d\s\w\w\w\s\d\d\d\d', str(user_date.get('title')))[0] if user_date else ''
                
                    info_dict['user'] = user_dict
                
                tweet_dict['tweet_' + str(tweet_ID)] = info_dict
                
                '''
                print ('-' * 5), 'Tweet ', tweet_ID, ('-' * 5)
                print info_dict['created_at']
                print info_dict['text']
                print info_dict['retweet_count']
                print info_dict['source']
                print user_dict['screen_name']
                print user_dict['name']
                print user_dict['location']
                print user_dict['followers_count']
                print user_dict['created_at']
                '''                
                tweet_ID += 1
        
        return tweet_dict