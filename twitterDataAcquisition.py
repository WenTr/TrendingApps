'''
Created on Apr 24, 2015

@author: Sherry
'''

from urllib import urlopen
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

#Comsumer key/secret hidden
consumer_key = ""
consumer_secret = ""

#Access key/secret hidden
access_token = ""
access_secret = ""

def main():
    authTwitter()
    # Test URL: "https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&result_type=popular&count=1");
     
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth, l)
    stream.filter(track=["basketball"])

def authTwitter():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_secret)

    api = API(auth)
    print(api.me().name)

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        #jsonFile = ("/twitter.txt", "w")
        #jsonFile.write(data)
        #jsonFile.close()
        
        #for line in data:
            #jsonFile = ("twitter.txt", "w")
            #jsonFile.write(line)
            #jsonFile.close()
        
        return True

    def on_error(self, status):
        print(status)

def passURL(urlString):
    pass

if __name__ == '__main__':
    main()
