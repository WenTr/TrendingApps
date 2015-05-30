import urllib2
import json
import requests
from bs4 import BeautifulSoup

class YoutubeAPI:
    def __init__(self):
        self.api_key = 'AIzaSyCnW1CtS2RHZuv07N3gfW4geD0e2kYcA9w'
    
    def get_video_id_list(self, app):
        apps_name_change = app
        if ' ' in apps_name_change:
            apps_name_change.replace(' ', '+')
            
        search_link = 'https://www.youtube.com/results?search_query=' + apps_name_change +'+app' 
        search_link2 = 'https://www.youtube.com/results?search_query=' + apps_name_change +'+app&page=2'        
        search_link3 = 'https://www.youtube.com/results?search_query=' + apps_name_change +'+app&page=3'
        search_link4 = 'https://www.youtube.com/results?search_query=' + apps_name_change +'+app&page=4'
        search_link5 = 'https://www.youtube.com/results?search_query=' + apps_name_change +'+app&page=5'        
        
        r = requests.get(search_link)
        r2 = requests.get(search_link2)
        r3 = requests.get(search_link3)
        r4 = requests.get(search_link4)
        r5 = requests.get(search_link5)

        soup = BeautifulSoup(r.content)    
        soup2 = BeautifulSoup(r2.content)
        soup3 = BeautifulSoup(r3.content)    
        soup4 = BeautifulSoup(r4.content)
        soup5 = BeautifulSoup(r5.content)    
    
        h = soup.find_all('a', {'rel': 'spf-prefetch'})
        h2 = soup2.find_all('a', {'rel': 'spf-prefetch'})
        h3 = soup3.find_all('a', {'rel': 'spf-prefetch'})
        h4 = soup4.find_all('a', {'rel': 'spf-prefetch'})
        h5 = soup5.find_all('a', {'rel': 'spf-prefetch'})
        
        vid_id_list = []
    
        for i in h:
            vid_id_list.append(i.get('href'))
        
        for j in h2:
            vid_id_list.append(j.get('href'))
        
        for k in h3:
            vid_id_list.append(k.get('href'))
        
        for L in h4:
            vid_id_list.append(L.get('href'))        
        
        for m in h5:
            vid_id_list.append(m.get('href'))
                
        
        for video in range(len(vid_id_list)):
            actual_id = vid_id_list[video]
            vid_id_list[video] = actual_id[9:]
    
        return vid_id_list

    def get_vid_info(self, url_video):
        response = urllib2.urlopen(url_video)
    
        video = json.load(response)
    
        info_dict = {}    
        for vid_info in video['items']:
            info_dict['title'] = vid_info['snippet']['title']
            info_dict['uploader'] = vid_info['snippet']['channelTitle']
            info_dict['views'] = vid_info['statistics']['viewCount']
            info_dict['likes'] = vid_info['statistics']['likeCount']
            info_dict['dislikes'] = vid_info['statistics']['dislikeCount']
            info_dict['comment_count'] = vid_info['statistics']['commentCount']    
            
            upload_date = vid_info['snippet']['publishedAt']
            info_dict['uploadDate'] = upload_date[0:10]
    
        return info_dict

    def get_comments(self, url_comments):
        comment_list = []
        comment_dict = {}
        
        try:        
            response = urllib2.urlopen(url_comments)
        except urllib2.HTTPError, e:
            print 'HTTPError:', e.code            
            return comment_dict
            
        comments = json.load(response)
        
        for comment in comments['items']:
            comment_list.append(comment['snippet']['topLevelComment']['snippet']['textDisplay'])
        
        for x in range(len(comment_list)):
            comment_dict['comment_' + str(x)] = comment_list[x]
    
        return comment_dict

  
    def get_all_info(self, apps_list):
        video_id = ''
        youtube_vid_dict = []
        for app in range(len(apps_list)): 
            video_id_list = self.get_video_id_list(apps_list[app])        
            
            video_dict = {}
            video_dict['appName'] = apps_list[app]
            print apps_list[app]
            
            for video_id in range(len(video_id_list)):
                url_comments = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=50&videoId=' + video_id_list[video_id] + '&key=' + self.api_key
                url_video = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2C+statistics&id=' + video_id_list[video_id] + '&key=' + self.api_key
                
                print video_id_list[video_id]
                
                vid_comments = self.get_comments(url_comments)
                video_info = self.get_vid_info(url_video)
                video_info['comments'] = vid_comments
                video_dict['video_' + str(video_id)] = video_info
        
            youtube_vid_dict.append(video_dict)

        return youtube_vid_dict       