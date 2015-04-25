import requests
from bs4 import BeautifulSoup
from youtube import Youtube

def main():
    apps = ['Messenger', 'Criminal Case', 'Facebook', 'Pandora® Radio', 'Instagram', 
            'Snapchat', 'Dubsmash','Super-Bright LED Flashlight', 'Spotify Music',
            'Clean Master (Speed Booster)']   
    
    for x in range(len(apps)):
        if ' ' in apps[x]:
            a = apps[x].replace(' ', '+')
            apps[x] = a    
    
    for app in range(len(apps)):
        search_link = 'https://www.youtube.com/results?search_query=' + apps[app] +'+app' 
        r1 = requests.get(search_link)    
        soup1 = BeautifulSoup(r1.content)
        yt = Youtube()    
        links = yt.get_video_links(soup1)
    
        vid_info = []
        for a in range(0, 5):    
            vid_link = 'https://www.youtube.com/' + links[a]        
            r2 = requests.get(vid_link)    
            soup2 = BeautifulSoup(r2.content)
            info = [yt.get_title(soup2), yt.get_view_count(soup2), yt.get_likes(soup2),
                    yt.get_dislikes(soup2), yt.get_date(soup2), yt.get_description(soup2)]
            vid_info.append(info)
        for b in vid_info:
            for c in b:
                print c
            print ''
        
if __name__ == "__main__":
    main()