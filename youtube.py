from bs4 import BeautifulSoup

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

    def get_description(self, soup):
        description = soup.find_all('p', {'id':'eow-description'})
        for i in description:    
            return i.text