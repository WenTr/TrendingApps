from bs4 import BeautifulSoup
import requests

class Youtube:
    
    def __init__(self):
        pass
    
    def get_video_links(self, soup):
        h3 = soup.find_all('a', {'rel': 'spf-prefetch'})
        y = []
        for i in h3:
            y.append(i.get('href'))
        return y        
        
    def get_title(self, soup):
        title = soup.find_all('span', {'class':'watch-title'})
        x = title[0].text     
        return x.strip()    
        
    def get_user(self, soup):
        user = soup.find_all('div', {'class':'yt-user-info'})
        return user[0].text.strip()
        
    def get_view_count(self, soup):
        view_count = soup.find_all('div', {'class':'watch-view-count'})
        for x in view_count:
            return x.text

    def get_likes(self, soup):
        view_like = soup.find_all('button', {'title':'I like this'})
        return view_like[0].text
        
    def get_dislikes(self, soup):
        view_dislike = soup.find_all('button', {'title':'I dislike this'})
        return view_dislike[0].text
    
    def get_date(self, soup):
        upload_date = soup.find_all('strong', {'class':'watch-time-text'})
        x = upload_date[0].text    
        return x.strip('Published on ')
    
    def get_dictionary_list(self, apps_name_change, apps):
        apps_list = {}
        
        for app in range(len(apps_name_change)):
            search_link = 'https://www.youtube.com/results?search_query=' + apps_name_change[app] +'+app' 
            r1 = requests.get(search_link)    
            soup1 = BeautifulSoup(r1.content)
            links = self.get_video_links(soup1)
            videos = {}

            for a in range(0, 5):    
                vid_link = 'https://www.youtube.com/' + links[a]        
                r2 = requests.get(vid_link)    
                soup2 = BeautifulSoup(r2.content)
                info = {'title':self.get_title(soup2), 'user':self.get_user(soup2), 
                        'views':self.get_view_count(soup2), 'likes':self.get_likes(soup2), 
                        'dislikes':self.get_dislikes(soup2), 'upload_date':self.get_date(soup2)}
                videos['video' + str(a)] = info

            apps_list[apps[app]] = videos

        youtube_info = {'youtube': apps_list}

        return youtube_info
        
#    def get_description(self, soup):
#        description = soup.find_all('p', {'id':'eow-description'})
#        for i in description:    
#            return i.text