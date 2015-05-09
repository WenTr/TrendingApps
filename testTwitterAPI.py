'''
Created on Apr 25, 2015

@author: Sherry
'''

from json import dumps

from twitterDataAcquisition import TwitterDataAcquisition

def main():
    twitterData = TwitterDataAcquisition()
        
    #jsonFile = ("twitter_data.json", "w")
    #jsonFile.write(str(twitterData))
    #jsonFile.close()
    
    print dumps(twitterData)

if __name__ == '__main__':
    main()