# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 01:49:42 2015

@author: Wendy Tran
"""
'''
Sources:
https://play.google.com/store
https://docs.python.org/2/howto/urllib2.html
http://stackoverflow.com/questions/16870648/python-read-website-data-line-by-line-when-available
http://stackoverflow.com/questions/12943819/how-to-python-prettyprint-a-json-file
http://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
http://www.crummy.com/software/BeautifulSoup/
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
http://stackoverflow.com/questions/5041008/handling-class-attribute-in-beautifulsoup
http://stackoverflow.com/questions/18851325/adding-more-values-on-existing-python-dictionary-key
'''

import requests
import pprint
import json
from bs4 import BeautifulSoup 
'''
def getListOfApps(wC):
    allLinks = []
    links = wC.find_all('a', {'class' : 'title'})
    for link in range(len(links)):
        a = links[link].text.encode('ascii', 'ignore')
        x = link+1        
        a.strip(str(x) + '.' + ' ')
        allLinks.append(a)
    return allLinks
'''

class GooglePlay:
    
    def __init__(self):
        pass
    
    def visitWebPage(self, urlPage):
        webInfo = requests.get(urlPage)
        return webInfo
    
    def getTitleOfApps(self, wC):
        titles = []
        appInfo = {}
        links = wC.find_all('a', {'class' : 'title'})
        #top 10 apps
        for x in range(0, 10):
            titles.append(links[x].get('title').encode('ascii', 'ignore'))
            appInfo[(links[x].get('title').encode('ascii', 'ignore'))]= {'appLink':'https://play.google.com/'+links[x].get('href')}
        return (titles, appInfo)
        
    def getCompanies(self, aC):
        companies = aC.find_all('span', {'itemprop': 'name'})
        for a in companies:
            return str(a.text)
        
    def getGenre(self, aC):
        genres = aC.find_all('span', {'itemprop': 'genre'})
        for a in genres:
            return str(a.text)
    
    def getStarRating(self, aC):
        starRating = aC.find_all('div', {'class': 'score'})
        for a in starRating:
            return str(a.text)
    
    def getNumOfReviewers(self, aC):
        numOfReviews = aC.find_all('span', {'class': 'reviews-num'})
        for a in numOfReviews:
            return str(a.text)
            
    '''    
    def getDescription():
        
    def getReviews():
    '''
    
    def getLastUpdated(self, aC):
        lastUpdated = aC.find_all('div', {'itemprop': 'datePublished'})
        for a in lastUpdated:
            return str(a.text)
        
    def getNumOfInstalls(self, aC):
        numDownloads = aC.find_all('div', {'itemprop': 'numDownloads'})
        for a in numDownloads:
            return str(a.text)
        
    def getAndrOSReq(self, aC):
        AndroidReq = aC.find_all('div', {'itemprop': 'operatingSystems'})
        for a in AndroidReq:
            return str(a.text)
            
    def getContentRating(self, aC):
        contentRating = aC.find_all('div', {'itemprop': 'contentRating'})
        for a in contentRating:
            return str(a.text)
            
    def getInAppPurch(self, aC):
        inAppPurch = aC.find_all('div', {'class': 'inapp-msg'})
        for a in inAppPurch:
            return str(a.text)
    
    def getAppInfo(self, appKey, appURL, allAppInfo):
        appContent = self.visitWebPage(appURL)
        aC = BeautifulSoup(appContent.content)  
        
        allAppInfo[appKey]['Company'] = self.getCompanies(aC)
        allAppInfo[appKey]['Genre'] = self.getGenre(aC)
        allAppInfo[appKey]['StarRating'] = self.getStarRating(aC)
        allAppInfo[appKey]['NumOfReviewers'] = self.getNumOfReviewers(aC)
        allAppInfo[appKey]['LastUpdated'] = self.getLastUpdated(aC)
        allAppInfo[appKey]['NumOfInstalls'] = self.getNumOfInstalls(aC)
        allAppInfo[appKey]['AndroidOSReq'] = self.getAndrOSReq(aC)
        allAppInfo[appKey]['ContentRating'] = self.getContentRating(aC)
        allAppInfo[appKey]['InAppPurchases'] = self.getInAppPurch(aC)
        return allAppInfo
    
    def getGPInfo(self):
        urlPage = 'https://play.google.com/store/apps/collection/topselling_free?hl=en'
        webContent = self.visitWebPage(urlPage)
        wC = BeautifulSoup(webContent.content)
        
        appTitles = []
        allAppInfo = {}
        topApps = {}
        
        #=============
        #---> List of Title of Apps: Send to all Other Classes to Search <---
        appTitles = self.getTitleOfApps(wC)[0]
        #=============
        
        allAppInfo = self.getTitleOfApps(wC)[1]
        
        for appKey in allAppInfo.keys():
            allAppInfo = self.getAppInfo(appKey, allAppInfo[appKey]['appLink'], allAppInfo)
    
        topApps['GooglePlay'] = allAppInfo
        print json.dumps(topApps, indent=4)