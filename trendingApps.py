from TA_GP import GooglePlay
from youtube import Youtube
from twitterDataAcquisition import TwitterDataAcquisition
import json

def youtube_vid_info(apps):   
    apps_name_change = []
    for x in range(len(apps)):
        if ' ' in apps[x]:
            a = apps[x].replace(' ', '+')
            apps_name_change.append(a)    
        else:
            apps_name_change.append(apps[x])
    yt = Youtube()
    youtube_info = yt.get_dictionary_list(apps_name_change, apps)
    #f = open('youtube.json', 'w')    
    #f.write(json.dumps(youtube_info, indent=4))
    #f.close()
    print json.dumps(youtube_info, indent=4)
    
def google_app_info():
    google = GooglePlay()
    app_list = google.getGPInfo()    
    return app_list
    
def twitter_info(app_list):
    twitter = TwitterDataAcquisition(app_list)
    return twitter
  
def main():
    apps = google_app_info()    
    youtube_vid_info(apps)
    twitter_info(apps)
    
if __name__ == "__main__":
    main()