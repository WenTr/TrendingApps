from youtube import Youtube
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
#    f = open('youtube.json', 'w')    
#    f.write(str(youtube_info))
#    f.close()
    print json.dumps(youtube_info, indent=4)
    
def google_app_info():
    pass    

def twitter_info():
    pass
  
def main():
    apps = ['Messenger', 'Criminal Case', 'Facebook', 'Pandora® Radio', 'Instagram', 
            'Snapchat', 'Dubsmash','Super-Bright LED Flashlight', 'Spotify Music',
            'Clean Master (Speed Booster)']    
    youtube_vid_info(apps)
    
if __name__ == "__main__":
    main()