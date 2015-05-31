import pymongo
import numpy
from collections import Counter
from textblob import TextBlob

class YoutubeStats:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['trendingapps']
        self.ycollec = self.db['youtube']
        self.query = self.ycollec.find({}, {'_id': 0})

    def get_lists(self):
        clw_list = []
        for count in self.query:        
            comments_count = []
            likes_list = []
            views_list = []
            comment_lists = []
            comments = {}            
            for x in range(len(count)-1):
                comments_count.append(int(count['video_' + str(x)]['comment_count']))
                likes_list.append(int(count['video_' + str(x)]['likes']))
                views_list.append(int(count['video_' + str(x)]['views']))
                
                if int(count['video_' + str(x)]['comment_count']) != 0:            
                    for comment in range(len(count['video_' + str(x)]['comments'])):
                        comment_str = count['video_' + str(x)]['comments']['comment_' + str(comment)].encode('ascii', 'ignore')
                        if comment_str != "":
                            if comment_str.isspace() == False:                       
                                comment_lists.append(comment_str)
                           
            comments_count.sort()
            likes_list.sort()
            views_list.sort()
            
            app_dict = {}
            app_dict['appName'] = count['appName']
            app_dict['comment_count'] = comments_count            
            app_dict['likes'] = likes_list
            app_dict['views'] = views_list
            app_dict['comments_sent'] = comment_lists
            clw_list.append(app_dict)
   
        return clw_list
     
    def get_stats(self):
        clw_list = self.get_lists()  
        stats_list = []
        
        for app in clw_list:
            app_stats = {}
            app_stats['appName'] = app['appName']
            
            comment_count_list = app['comment_count']
            comment_mean = round(numpy.mean(comment_count_list), 1)
            comment_median = numpy.median(comment_count_list)
            x = Counter(comment_count_list).most_common(1)            
            comment_mode = x[0][0]  
            comment_sd = round(numpy.std(comment_count_list), 1)
            app_stats['comment_count'] = {'mean': comment_mean, 'median': comment_median, 'mode': comment_mode, 'standard_deviation': comment_sd}
            
            likes_list = app['likes']
            likes_mean = round(numpy.mean(likes_list), 1)
            likes_median = numpy.median(likes_list)
            y = Counter(likes_list).most_common(1)            
            likes_mode = y[0][0]  
            likes_sd = round(numpy.std(likes_list), 1)
            app_stats['likes'] = {'mean': likes_mean, 'median': likes_median, 'mode': likes_mode, 'standard_deviation': likes_sd}
            
            views_list = app['views']
            views_mean = round(numpy.mean(views_list), 1)
            views_median = numpy.median(views_list)
            z = Counter(views_list).most_common(1)            
            views_mode = z[0][0]  
            views_sd = round(numpy.std(views_list), 1)
            app_stats['views'] = {'mean': views_mean, 'median': views_median, 'mode': views_mode, 'standard_deviation': views_sd}
            
            comments_polarity = []
            comments = {}
            comments_pol = {}
            comment_list = app['comments_sent']
            for comment in comment_list:
                sent_analysis = TextBlob(comment)    
                if sent_analysis.sentiment.polarity != 0:
                    comments_polarity.append(sent_analysis.sentiment.polarity)
            
            for comment in range(len(comment_list)):
                comments['comment_' + str(comment)] = comment_list[comment]                                
                
            for (comment_num, text) in comments.items():
                sent = TextBlob(text)    
                if sent_analysis.sentiment.polarity != 0:
                    comments_pol[comment_num] = sent.sentiment.polarity                    
                
            sent_mean = round(numpy.mean(comments_polarity), 1)        
            app_stats['sentimental_analysis'] = {'mean': sent_mean, 'comment_polarity': comments_pol}    
            
            stats_list.append(app_stats)
            
        return stats_list