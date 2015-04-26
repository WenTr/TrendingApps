import requests
from bs4 import BeautifulSoup
from youtube import Youtube

def main():
    apps = ['Messenger', 'Criminal Case', 'Facebook', 'Pandora® Radio', 'Instagram', 
            'Snapchat', 'Dubsmash','Super-Bright LED Flashlight', 'Spotify Music',
            'Clean Master (Speed Booster)']   
    apps_name_change = []
    for x in range(len(apps)):
        if ' ' in apps[x]:
            a = apps[x].replace(' ', '+')
            apps_name_change.append(a)    
        else:
            apps_name_change.append(apps[x])
    apps_list = {}
    
    for app in range(len(apps_name_change)):
        search_link = 'https://www.youtube.com/results?search_query=' + apps_name_change[app] +'+app' 
        r1 = requests.get(search_link)    
        soup1 = BeautifulSoup(r1.content)
        yt = Youtube()   
        links = yt.get_video_links(soup1)
        videos = {}
        for a in range(0, 10):    
            vid_link = 'https://www.youtube.com/' + links[a]        
            r2 = requests.get(vid_link)    
            soup2 = BeautifulSoup(r2.content)
            info = {'title':yt.get_title(soup2), 'user':yt.get_user(soup2), 
                    'views':yt.get_view_count(soup2), 'likes':yt.get_likes(soup2), 
                    'dislikes':yt.get_dislikes(soup2), 'upload_date':yt.get_date(soup2)}
            videos['video' + str(a)] = info
        apps_list[apps[app]] = videos
    youtube_info = {'youtube': apps_list}
    
    f = open('youtube.json', 'w')    
    f.write(str(youtube_info))
    f.close()

if __name__ == "__main__":
    main()