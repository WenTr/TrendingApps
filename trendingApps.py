
from TA_GP import GooglePlay
from youtubeAPI import YoutubeAPI
#from twitterDataAcquisition import TwitterDataAcquisition
from twitterScreenScrape import TwitterScreenScrape
import json
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
    
    apps, gpInfo = google_app_info()   
    yt = youtube_vid_info(apps)
    tw = twitter_info(apps)
    
    ycollec = db['youtube']
    tcollec = db['twitter']
    gcollec = db['googleplay']
    
    for docu in yt:
        ycollec.insert(docu)
    
    for (tkey, tvalue) in tw['twitter'].items():
        tcollec.insert( {tkey:tvalue} )
    
    for (gkey, gvalue) in gpInfo['googlePlay'].items():
        gcollec.insert( {gkey:gvalue} )
    
    print db.youtube.find_one()
    print
    print db.twitter.find_one()
    print
    print db.googleplay.find_one()
    
if __name__ == "__main__":
    main()