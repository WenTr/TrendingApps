'''
Created on Apr 25, 2015

@author: Sherry
'''

from json import dumps

from twitterDataAcquisition import TwitterDataAcquisition
from twitterScreenScrape import TwitterScreenScrape

def main():
    appsList = ["Messenger", "Criminal Case", "Facebook", "Pandora Radio", "Instagram", 
            "Snapchat", "Dubsmash","Super-Bright LED Flashlight", "Spotify Music",
            "Clean Master (Speed Booster)"]
    
    #twitterData = TwitterDataAcquisition()
        
    #jsonFile = ("twitter_data.json", "w")
    #jsonFile.write(str(twitterData))
    #jsonFile.close()
    
    #print dumps(twitterData)
    
    TwitterScreenScrape(appsList)
    #TwitterScreenScrape(["Messenger"])

if __name__ == '__main__':
    main()