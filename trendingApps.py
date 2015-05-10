
from TA_GP import GooglePlay
from youtubeAPI import YoutubeAPI
from twitterDataAcquisition import TwitterDataAcquisition
from twitterScreenScrape import TwitterScreenScrape
import json

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
    twitter = TwitterScreenScrape(app_list)
    return twitter
  
def main():
    apps, gpInfo = google_app_info()   
    youtube_vid_info(apps)
    twitter_info(apps)
    
if __name__ == "__main__":
    main()