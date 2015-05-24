import pymongo
from math import sqrt
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
            mean = (1.0*sum(value)) / len(value)
            comment_mean[key] = round(mean, 1)
   
        for (key2, value2) in like_dict.items():         
            mean = 1.0*sum(value2) / len(value2)
            like_mean[key2] = round(mean, 1)
       
        for (key3, value3) in view_dict.items():         
            mean = 1.0*sum(value3) / len(value3)
            view_mean[key3] = round(mean, 1)
       
        return comment_mean, like_mean, view_mean    

    def find_median(self, comment_dict, like_dict, view_dict):
        comment_median = {}
        like_median = {}
        view_median = {}    
        
        for (app1, comment_count_list) in comment_dict.items():
            if len(comment_count_list) % 2 != 0:        
                median1 = len(comment_count_list) / 2
                comment_median[app1] = comment_count_list[median1] 
        
            elif len(comment_count_list) % 2 == 0:
                med1 = len(comment_count_list) / 2     
                med2 = med1 - 1
                median2 = 1.0 * (comment_count_list[med1] + comment_count_list[med2]) / 2            
                comment_median[app1] = median2            
    
        for (app2, likes_list) in like_dict.items():
            if len(likes_list) % 2 != 0:        
                median3 = len(likes_list) / 2
                like_median[app2] = likes_list[median3] 
        
            elif len(likes_list) % 2 == 0:
                med3 = len(likes_list) / 2     
                med4 = med1 - 1
                median4 = 1.0 * (likes_list[med3] + likes_list[med4]) / 2            
                like_median[app2] = median4        
            
        for (app3, view_list) in view_dict.items():
            if len(view_list) % 2 != 0:        
                median5 = len(view_list) / 2
                view_median[app3] = comment_count_list[median5] 
        
            elif len(view_list) % 2 == 0:
                med5 = len(view_list) / 2     
                med6 = med1 - 1
                median6 = 1.0 * (view_list[med5] + view_list[med6]) / 2            
                view_median[app3] = median6
    
        return comment_median, like_median, view_median

    def find_mode(self, comment_dict, like_dict, view_dict):
        comment_mode = {}
        likes_mode = {}    
        views_mode = {}    
        for (app, comment_lists) in comment_dict.items():
            x = Counter(comment_lists).most_common(1)   
            comment_mode[app] = {'comment_mode': x[0][0], 'counter':x[0][1]}

        for (app, likes_lists) in like_dict.items():
            y = Counter(likes_lists).most_common(1)   
            likes_mode[app] = {'likes_mode': y[0][0], 'counter':y[0][1]}
    
        for (app, views_lists) in view_dict.items():
            z = Counter(views_lists).most_common(1)   
            views_mode[app] = {'views_mode': z[0][0], 'counter':z[0][1]}
    
        return comment_mode, likes_mode, views_mode
    
    def find_standard_deviation(self, comment_dict, like_dict, view_dict):
        comment_sd = {}
        like_sd = {}
        view_sd = {}
    
        for (app, comment_lists) in comment_dict.items():
            square_list = [x**2 for x in comment_lists]
            sum1 = sum(square_list) * len(comment_lists)
            sum2 = sum(comment_lists) ** 2
            subt = sum1 - sum2
            lendenom = len(comment_lists) * (len(comment_lists) - 1)
            variance = subt/lendenom
            sd = round(sqrt(variance), 1)    
            comment_sd[app] = sd
    
        for (app, likes_lists) in like_dict.items():
            square_list = [x**2 for x in likes_lists]
            sum1 = sum(square_list) * len(likes_lists)
            sum2 = sum(likes_lists) ** 2
            subt = sum1 - sum2
            lendenom = len(likes_lists) * (len(likes_lists) - 1)
            variance = subt/lendenom
            sd = round(sqrt(variance), 1)    
            like_sd[app] = sd
    
        for (app, views_lists) in view_dict.items():
            square_list = [x**2 for x in views_lists]
            sum1 = sum(square_list) * len(views_lists)
            sum2 = sum(views_lists) ** 2
            subt = sum1 - sum2
            lendenom = len(views_lists) * (len(views_lists) - 1)
            variance = subt/lendenom
            sd = round(sqrt(variance), 1)    
            view_sd[app] = sd
        
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