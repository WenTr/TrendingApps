from TA_GP import GooglePlay
from youtubeAPI import YoutubeAPI
from twitter_api import Twitter_API
from googleplayStats import GooglePlayStats
from twitterStats import TwitterStats
from youtubeStats import YoutubeStats
from json import dumps
import pymongo

conn = pymongo.MongoClient()
db = conn['trendingapps']
ycollec = db['youtube']
tcollec = db['twitter']
gcollec = db['googleplay']
y_stats = db['youtube_stats']
gp_stats = db['googleplay_stats']
t_stats = db['twitter_stats']

def youtube_vid_info(apps):   
    youtube = YoutubeAPI()
    vid_dict = youtube.get_all_info(apps)
    return vid_dict
    
def google_app_info():
    google = GooglePlay()
    app_list = google.getGPInfo()
    return app_list
    
def twitter_info(app_list):
    twitter = Twitter_API()
    return twitter.get_tweets(app_list)

def insert_DB():
    apps, gpInfo = google_app_info()   
    yt = youtube_vid_info(apps)
    tw = twitter_info(apps)
    
    for docu in yt:
        ycollec.insert(docu)
    
    for (tkey, tvalue) in tw['twitter'].items():
        tcollec.insert( {tkey:tvalue} )

    for (gkey, gvalue) in gpInfo['googlePlay'].items():
        gcollec.insert( {gkey:gvalue} )

def find_DB():
    for num in range(1, 11):
        appDict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
        
        for appTitle in appDict.keys():
            appName = appDict[appTitle]['title']
            
            for num2 in range(1, 6):
                tweetInfo = db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                
                for info in tweetInfo:
                    print dumps(info, indent = 4)
                          
            query = ycollec.find({'appName': appName}, {"appName": 1, "video_0" : 1, "video_1" : 1, 
                                 "_id" : 0})
                
            for app in query:
                    print dumps(app, indent = 4) 

def get_stats():
    gp = GooglePlayStats()
    t = TwitterStats()
    yt = YoutubeStats()
    
    gpl_stats =  gp.getReviewRatings()
    tw_stats = t.get_twitter_stats()
    yt_stats = yt.get_stats()
    
    gp_stats.insert(gpl_stats)
    t_stats.insert(tw_stats['twitter'])
    
    for document in yt_stats:
        y_stats.insert(document)
        
  
def main():             
#    find_DB()
    insert_DB()
#   get_stats()
        
if __name__ == "__main__":
    main()