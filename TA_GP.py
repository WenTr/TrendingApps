# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 01:49:42 2015

@author: Wendy Tran
"""
'''
Sources:
https://docs.python.org/2/howto/urllib2.html
http://stackoverflow.com/questions/16870648/python-read-website-data-line-by-line-when-available
http://stackoverflow.com/questions/12943819/how-to-python-prettyprint-a-json-file
http://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
http://www.crummy.com/software/BeautifulSoup/
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
http://stackoverflow.com/questions/5041008/handling-class-attribute-in-beautifulsoup

'''

import requests
from bs4 import BeautifulSoup


webContent = requests.get('https://play.google.com/store/apps/collection/topselling_free?hl=en')

'''
#html = response.read()
for eachLine in webContent:
    print eachLine
'''    
'''
http = urllib2.Http()
status, response = http.request('https://play.google.com/store/apps/collection/topselling_free?hl=en')

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_attr('href'):
        print link['href']
'''


#for eachLine in BeautifulSoup(webContent.content):
#    print eachLine
 

wC = BeautifulSoup(webContent.content)

for links in wC.find_all('a', {'class' : 'title'}):
    print links.text
    
