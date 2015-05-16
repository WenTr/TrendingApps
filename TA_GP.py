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
http://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling
http://stackoverflow.com/questions/23380171/using-beautifulsoup-extract-text-without-tags
http://stackoverflow.com/questions/1024847/add-key-to-a-dictionary-in-python
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://docs.python.org/2/library/uuid.html
https://github.com/behackett/presentations/blob/master/pycon_2012/Lesson%201.1:%20Getting%20Started.ipynb
http://stackoverflow.com/questions/12309269/write-json-data-to-file-in-python
'''

import requests
#import pprint
import json
import uuid
from bs4 import BeautifulSoup

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
            #print links[x].text.split()[0].replace('.', '')            
            #appInfo[(links[x].get('title').encode('ascii', 'ignore'))] = {'AppLink':'https://play.google.com/'+links[x].get('href'), 'Rank':links[x].text.split()[0].replace('.', '')}
            appInfo[links[x].text.split()[0].replace('.', '')] = {'title':links[x].get('title').encode('ascii', 'ignore'), 'appLink':'https://play.google.com/'+links[x].get('href')}
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
    def getDescription(self, aC): 
        def getNumOfReviewers(self, aC):
        appDesc = aC.find_all('div', {'class': 'id-app-orig-desc'})
        for a in appDesc:
            return str(a.text)
    '''        
    
    def getReviews(self, aC):
        reviewDict = {}      
        reviewInfo = {}        

        singleReviews = aC.findAll('div', {'class': 'single-review'})
        for eachReview in singleReviews:
            reviewInfo['user'] = eachReview.find('span', {'class': 'author-name'}).text
            reviewInfo['date'] = eachReview.find('span', {'class': 'review-date'}).text
            reviewInfo['rating'] = eachReview.find('div', {'class': 'tiny-star star-rating-non-editable-container'})['aria-label']
            reviewInfo['title'] = eachReview.find('span', {'class': 'review-title'}).text
            reviewInfo['comment'] = eachReview.find('span', {'class': 'review-title'}).next_sibling
            #print reviewInfo
            reviewDict[str(uuid.uuid4())] = reviewInfo
            reviewInfo = {}
        #print json.dumps(reviewDict, indent=4)
        return reviewDict
    
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
        
        allAppInfo[appKey]['company'] = self.getCompanies(aC)
        allAppInfo[appKey]['genre'] = self.getGenre(aC)
        allAppInfo[appKey]['starRating'] = self.getStarRating(aC)
        allAppInfo[appKey]['numOfReviewers'] = self.getNumOfReviewers(aC)
        allAppInfo[appKey]['lastUpdated'] = self.getLastUpdated(aC)
        allAppInfo[appKey]['numOfInstalls'] = self.getNumOfInstalls(aC)
        allAppInfo[appKey]['androidOSReq'] = self.getAndrOSReq(aC)
        allAppInfo[appKey]['contentRating'] = self.getContentRating(aC)
        allAppInfo[appKey]['inAppPurchases'] = self.getInAppPurch(aC)
        allAppInfo[appKey]['reviews'] = self.getReviews(aC)
        return allAppInfo
        
    def printToJson(self, gpDict):
        with open('gp.txt', 'w') as outfile:
            json.dump(gpDict, outfile)
    
    def getGPInfo(self):
        urlPage = 'https://play.google.com/store/apps/collection/topselling_free?hl=en'
        webContent = self.visitWebPage(urlPage)
        wC = BeautifulSoup(webContent.content)
        
        appTitles = []
        allAppInfo = {}
        topApps = {}
        
        titles = self.getTitleOfApps(wC)
        
        #=============
        #---> List of Title of Apps: Send to all Other Classes to Search <---
        appTitles = titles[0]
        #=============
        
        allAppInfo = titles[1]
        
        #loops through all the apps to get app Info
        for appKey in allAppInfo.keys():
            allAppInfo = self.getAppInfo(appKey, allAppInfo[appKey]['appLink'], allAppInfo)
            
        #################################
        #########Test Value##############
        #allAppInfo = self.getAppInfo('Criminal Case', allAppInfo['Criminal Case']['AppLink'], allAppInfo)
        #################################
    
        topApps['googlePlay'] = allAppInfo
        #self.printToJson(topApps)
        #print json.dumps(topApps, indent=4)
        return topApps
