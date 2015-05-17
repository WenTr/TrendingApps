from TA_GP import GooglePlay
from youtubeAPI import YoutubeAPI
#from twitterDataAcquisition import TwitterDataAcquisition
from twitterScreenScrape import TwitterScreenScrape
from json import dumps
import pymongo

def youtube_vid_info(apps):   
    youtube = YoutubeAPI()
    vid_dict = youtube.get_all_info(apps)
    return vid_dict
    
def google_app_info():
    google = GooglePlay()
    app_list = google.getGPInfo()
    return app_list
    
def twitter_info(app_list):
    #twitter = TwitterDataAcquisition(app_list)
    twitter = TwitterScreenScrape()
    return twitter.get_twitter_data(app_list)
  
def main():    
    try:
        conn = pymongo.MongoClient()
        print "Successful Connection"
    except pymongo.errors.ConnectionFailure, e:
        print "Error During Connection"    
    
    db = conn['trendingapps']
	
    '''
    apps, gpInfo = google_app_info()   
    yt = youtube_vid_info(apps)
    tw = twitter_info(apps)
    '''
    ycollec = db['youtube']
    tcollec = db['twitter']
    gcollec = db['googleplay']
    '''
    for docu in yt:
        ycollec.insert(docu)
    
    for (tkey, tvalue) in tw['twitter'].items():
        tcollec.insert( {tkey:tvalue} )
    
    for (gkey, gvalue) in gpInfo['googlePlay'].items():
        gcollec.insert( {gkey:gvalue} )
    '''
    
#    print db.youtube.find_one()
#    print
#    print db.twitter.find_one()
#    print
#    print db.googleplay.find_one()

    query = ycollec.find({'appName': {'$exists': True}}, {'video_0.likes': 1, '_id': 0})


    for num in range(1, 11):
        appDict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
        
        for appTitle in appDict.keys():
            appName = appDict[appTitle]['title']
            
            for num2 in range(1, 6):
                tweetInfo = db.twitter.find({str(appName): {'$exists': 1}}, {str(appName) + '.tweet_' + str(num2): 1, '_id': 0})
                
                for info in tweetInfo:
                    print dumps(info, indent = 4)
                          
            query = ycollec.find({'appName': appName}, {"_id": 0})
                
            for vid in query:
                    print dumps(vid, indent = 4)


if __name__ == "__main__":
    main()