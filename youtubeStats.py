import pymongo
import numpy
from collections import Counter


class YoutubeStats:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['trendingapps']
        self.ycollec = self.db['youtube']
        self.query = self.ycollec.find({}, {'_id': 0})

    def get_lists(self):
        comment_count_dict = {}
        likes_dict = {}
        views_dict = {}
      
        for count in self.query:        
            comments_count = []
            likes_list = []
            views_list = []
            for x in range(len(count)-1):
                comments_count.append(int(count['video_' + str(x)]['comment_count']))
                likes_list.append(int(count['video_' + str(x)]['likes']))
                views_list.append(int(count['video_' + str(x)]['views']))
       
            comments_count.sort()
            likes_list.sort()
            views_list.sort()
       
            comment_count_dict[str(count['appName'])] = comments_count
            likes_dict[str(count['appName'])] = likes_list
            views_dict[str(count['appName'])] = views_list
   
        return comment_count_dict, likes_dict, views_dict
    
    def find_mean(self, comment_dict, like_dict, view_dict):    
        comment_mean = {}
        like_mean = {}
        view_mean = {}
       
        for (key, value) in comment_dict.items():
            mean = numpy.mean(value)
            comment_mean[key] = round(mean, 1)
       
        for (key2, value2) in like_dict.items():         
            mean = numpy.mean(value2)
            like_mean[key2] = round(mean, 1)
       
        for (key3, value3) in view_dict.items():         
            mean = numpy.mean(value3)
            view_mean[key3] = round(mean, 1)
       
        return comment_mean, like_mean, view_mean    

    def find_median(self, comment_dict, like_dict, view_dict):
        comment_median = {}
        like_median = {}
        view_median = {}    
        
        for (app1, comment_count_list) in comment_dict.items():
            median1 = numpy.median(comment_count_list)
            comment_median[app1] = median1 
    
        for (app2, likes_list) in like_dict.items():
            median2 = numpy.median(likes_list)
            like_median[app2] = median2 
            
        for (app3, view_list) in view_dict.items():
            median3 = numpy.median(view_list)
            view_median[app3] = median3 
                
        return comment_median, like_median, view_median

    def find_mode(self, comment_dict, like_dict, view_dict):
        comment_mode = {}
        likes_mode = {}    
        views_mode = {}    
        for (app, comment_lists) in comment_dict.items():
            x = Counter(comment_lists).most_common(1)   
            comment_mode[app] = x[0][0]

        for (app, likes_lists) in like_dict.items():
            y = Counter(likes_lists).most_common(1)   
            likes_mode[app] = y[0][0]
    
        for (app, views_lists) in view_dict.items():
            z = Counter(views_lists).most_common(1)   
            views_mode[app] = z[0][0]
    
        return comment_mode, likes_mode, views_mode
    
    def find_standard_deviation(self, comment_dict, like_dict, view_dict):
        comment_sd = {}
        like_sd = {}
        view_sd = {}
    
        for (app, comment_lists) in comment_dict.items():
            sd = numpy.std(comment_lists)    
            comment_sd[app] = round(sd, 1)
    
        for (app, likes_lists) in like_dict.items():
            sd = numpy.std(likes_lists)
            like_sd[app] = round(sd, 1)
    
        for (app, views_lists) in view_dict.items():
            sd = numpy.std(views_lists) 
            view_sd[app] = round(sd, 1)
        
        return comment_sd, like_sd, view_sd

    def stats(self):
        comment_dict, like_dict, view_dict = self.get_lists()
   
        comment_mean, like_mean, view_mean = self.find_mean(comment_dict, like_dict, view_dict)
        comment_median, like_median, view_median = self.find_median(comment_dict, like_dict, view_dict)    
        comment_mode, like_mode, view_mode = self.find_mode(comment_dict, like_dict, view_dict)
        comment_sd, like_sd, view_sd = self.find_standard_deviation(comment_dict, like_dict, view_dict)
       
        stats_dict = {}        
        stats_dict['mean'] = {'comment_count': comment_mean, 'likes': like_mean, 'views': view_mean}      
        stats_dict['median'] = {'comment_count': comment_median, 'likes': like_median, 'views': view_median}  
        stats_dict['mode'] = {'comment_count': comment_mode, 'likes': like_mode, 'views': view_mode}
        stats_dict['standard_deviation'] = {'comment_count': comment_sd, 'likes': like_sd, 'views': view_sd}
   
        return stats_dict