import matplotlib.pyplot as plt
import numpy as np
import pymongo
import re
from collections import Counter

conn = pymongo.MongoClient()
db = conn['trendingapps']
ycollec = db['youtube']
tcollec = db['twitter']
gcollec = db['googleplay']
y_stats = db['youtube_stats']
gp_stats = db['googleplay_stats']
t_stats = db['twitter_stats']
query = y_stats.find({}, {"_id": 0})

def youtube_graphs():
    color_list = ['b','g','r','c','m','y','k','b' ,'m' ,'r']    
    a = 0
    for stat in query:
        stats = {}                
        for sent in range(len(stat['sentimental_analysis']['comment_polarity'])):
            stats[sent] = stat['sentimental_analysis']['comment_polarity']['comment_'+str(sent)]
        
        x = stats.keys()
        y = stats.values()
        half = len(y)/ 2
        plt.scatter(x, y, s= 5, color = color_list[a])
        plt.scatter(half, stat['sentimental_analysis']['mean'], s= 50, color = color_list[9-a])
        plt.title('Sentimental Analysis')
        plt.ylabel('Polarity')
        plt.xlabel('Comment_ID')    
        plt.savefig('yt_scatter_' + stat['appName'])
        plt.close()
        a += 1
      
    b = 0    
    for stat2 in query:
        stats = {}  
        stats[0.5] = 0
        stats[1] = stat2['likes']['mean']
        stats[1.5] = 0
        x2 = stats.keys()
        y2 = stats.values()
        plt.bar(x2, y2, color = color_list[b], align='center')
        plt.title('Average Likes')
        plt.ylabel('Likes')
        plt.xlabel(stat2['appName'])
        plt.text(0.2, 20, 'Mean: ' + str(stats[1]))
        plt.savefig('yt_likesbar_' + stat2['appName'])
        plt.close()
        b += 1
       
    b = 0    
    for stat2 in query:
        stats = {}
        stats[0.5] = 0        
        stats[1] = stat2['views']['mean']
        stats[1.5] = 0
        x2 = stats.keys()
        y2 = stats.values()
        plt.bar(x2, y2, color = color_list[b], align='center')
        plt.title('Average Views')
        plt.ylabel('Views')
        plt.xlabel(stat2['appName'])
        plt.text(0.1, 20, 'Mean: ' + str(stats[1]))
        plt.savefig('yt_viewsbar_' + stat2['appName'])
        plt.close()
        b += 1

def google_graphs():
    color_list = ['b','g','r','c','m','y','k','b' ,'m' ,'r']
    titleDict = {}
    starRatingDict = {}
    sRD = {}
    for num in range(1, 11):
        titleDict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
        starRatingDict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.starRating': 1, '_id': 0})[0]   
        sRD[titleDict[str(num)]['title']] = float(starRatingDict[str(num)]['starRating'])
    
    rates = {}
    app_number = {}
    number_app = {}    
    a = 1    
    for (key,value) in sRD.items():
        rates[a] = value
        app_number[key] = a
        a += 1
    for (key2, value2) in app_number.items():
        number_app[value2] = str(key2)
    
    print number_app    
    x = app_number.values()
    y = rates.values()
    x.sort()
    y.sort()
    
    plt.bar(x,y, color='r')
    plt.title('App Ratings')
    plt.xlabel('App Names')
    plt.ylabel('Rating')
    plt.savefig('g_main')
    plt.close()
    apps = {}    
    polarList = []
    appPolarDict = {}   
    sent_mean = {}
    apps = gp_stats.find({'appNames':{'$exists': 1}}, {'appNames':1, '_id':0})[0]
    for a in apps['appNames']:
        tempDict = gp_stats.find({'appNames': {'$exists':1}}, {'appNames.'+a:1, '_id':0})[0]
        for n in range(0, 40):
            polarList.append(tempDict['appNames'][a]['SentimentalAnalysis']['review_' + str(n)])
        appPolarDict[a] = polarList
        sent_mean[a] = tempDict['appNames'][a]['meanOfPolarity']
        polarList = []
    
    b = 0    
    for (app, pol_list) in appPolarDict.items():
        pol_dict = {}        
        for pol in range(len(pol_list)):
            pol_dict[pol] = pol_list[pol]
        
        x = pol_dict.keys()
        y = pol_dict.values()
        plt.scatter(x, y, s=20, color = color_list[b])
        plt.scatter(20, sent_mean[app], s = 100, color = color_list[9 - b])        
        plt.title('Sentimental Analysis')
        plt.ylabel('Polarity')
        plt.xlabel('Review_ID')    
        plt.savefig('g_scatter_' + app)
        plt.close()
        b += 1
    ratingDict = {}
    for num in range(1, 11):
        appList = []
        appDict = db.googleplay.find({str(num):{'$exists':1}}, {str(num)+'.title':1, str(num)+'.reviews':1, '_id':0})[0]
        for reviewNum in range(0, 40):
            appList.append(int(re.findall('\d', str(appDict[str(num)]['reviews']['review_'+str(reviewNum)]['rating']))[0]))
                   
        ratingDict[appDict[str(num)]['title']] = appList
        appList = []
    
    a = 0
    for (app, rate) in ratingDict.items():
        plt.hist(rate, 5, histtype='bar', color=color_list[a], align='mid', range=(1,5))
        plt.title('Ratings')
        plt.ylabel('Rate Frequency')
        plt.xlabel('Rating Scale')
        plt.savefig('g_hist_' + app)
        plt.close()
        a += 1
 
def twitter_graphs():
    color_list = ['b','g','r','c','m','y','k','b' ,'m' ,'r']    
    graph_dict = {}

    for num in range(1, 11):
        app_dict = db.googleplay.find({str(num): {'$exists': 1}}, {str(num) + '.title': 1, '_id': 0})[0]
                
        for app_title in app_dict.keys():
            app_stat_dict = {}
                    
            app_name = app_dict[app_title]['title']
    
            stat_dict_cursor = db.twitter_stats.find({app_name: {'$exists': 1}}, {'_id': 0})
    
            for app in stat_dict_cursor:
                app_stat_dict['retweet_mean'] = app[app_name]['retweet_mean']
                app_stat_dict['user_mean'] = app[app_name]['user_mean']
                app_stat_dict['sa_avg'] = app[app_name]['sa_avg']
                app_stat_dict['sa_list'] = app[app_name]['sa_list']
                
            graph_dict[app_name] = app_stat_dict
    a = 0        
    for (key,value) in graph_dict.items():
        sa_dict = {}
        for sa in range(len(value['sa_list'])):
            sa_dict[sa] = value['sa_list'][sa]    
        x = sa_dict.keys()
        y = sa_dict.values()
        half = len(y)/2
        plt.scatter(x, y, s = 5, color = color_list[a])
        plt.scatter(half, value['sa_avg'], s = 30, color = color_list[9 - a])        
        plt.title('Sentimental Analysis')
        plt.ylabel('Polarity')
        plt.xlabel('Tweet_ID')    
        plt.savefig('tweet_scatter_' + key)
        plt.close()
        a += 1
    b = 0        
    for (key2, value2) in graph_dict.items():
        retweet_bar = {}
        retweet_bar[0.5] = 0
        retweet_bar[1.5] = 0
        retweet_bar[1] = value2['retweet_mean']        
        x2 = retweet_bar.keys()
        y2 = retweet_bar.values()
        plt.bar(x2, y2, color = color_list[b], align='center')
        plt.title('Average Retweets')
        plt.ylabel('Retweets')
        plt.xlabel(key2)
        plt.text(0.2, 20, 'Mean: ' + str(retweet_bar[1]))
        plt.savefig('tweet_retweet_' + key2)
        plt.close()
        b += 1
 
    c = 0        
    for (key3, value3) in graph_dict.items():
        user_bar = {}
        user_bar[0.5] = 0
        user_bar[1.5] = 0
        user_bar[1] = value3['user_mean']        
        x3 = user_bar.keys()
        y3 = user_bar.values()
        plt.bar(x3, y3, color = color_list[c], align='center')
        plt.title('Average Followers')
        plt.ylabel('Followers')
        plt.xlabel(key3)
        plt.text(0.2, 20, 'Mean: ' + str(user_bar[1]))
        plt.savefig('tweet_user_' + key3)
        plt.close()
        c += 1
        
def main():
   google_graphs()

if __name__ == '__main__':
    main()