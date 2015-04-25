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

consumer_key = "AQOeMUImTqcPLm1KS847pdo6Y"
consumer_secret = "FNFXTMjfyABt57UHaxstz2p8juasQRBenulQqGhqo85T1KxhCK"

access_token = "313601183-CQKz2PLX8ohQZyaLDyQ64Vvp2Z3Q1Eq4CkbDtc8O"
access_secret = "1NbqrzmR7JaWKewqAVRXrk7FgJklGDpvrmpyONtuAqYbP"

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