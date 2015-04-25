'''
Created on Apr 24, 2015

@author: Sherry
'''

'''
- created_at
- text
- retweet count
- source (remove \'s and other fomatting)
- user
    - name
    - screen_name
    - location
    - followers_count
    - friends_count
    - created_at
    - time_zone
'''    

from urllib import urlopen
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

<<<<<<< HEAD
'''
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
'''

consumer_key = "AQOeMUImTqcPLm1KS847pdo6Y"
consumer_secret = "FNFXTMjfyABt57UHaxstz2p8juasQRBenulQqGhqo85T1KxhCK"

access_token = ""
access_secret = ""

appsList = ["basketball"]
=======
#Comsumer key/secret hidden
consumer_key = ""
consumer_secret = ""

#Access key/secret hidden
access_token = ""
access_secret = ""
>>>>>>> origin/twitter


def main():
    #authTwitter()
    searchKeywords(appsList)

def authTwitter():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_secret)

    api = API(auth)
    print(api.me().name)

class TweetListener(StreamListener):
    print("reached here...")
    
    def on_data(self, data):
        print("got here...")
        jsonFile = open("twitter.json", "w")
        
        '''
        for line in data:
            jsonFile.write(line)
            print(line)
        '''
        jsonFile.close()
        
        return True

    def on_error(self, status):
        print("failed")
        print(status)

def searchKeywords(keywordList):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    tl = TweetListener()

    for keyword in keywordList:
        stream = Stream(auth, tl)
        stream.filter(track = [keyword])

if __name__ == '__main__':
    main()
