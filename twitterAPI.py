import tweepy                  
import json
import csv
from datetime import date
from datetime import datetime
import time
import pandas as pd

######################################################################################

def getApi():
    with open('twitterkeys.json') as server_file:
        datatwitter = json.load(server_file)

    configtwitter = {
        "consumer_key" : datatwitter['consumer_key'],
        "consumer_secret" : datatwitter['consumer_secret'],
        "access_token_key": datatwitter['access_token_key'],
        "access_token_secret": datatwitter['access_token_secret']
                    }
        
    auth = tweepy.OAuthHandler(configtwitter["consumer_key"], configtwitter["consumer_secret"])
    auth.set_access_token(configtwitter["access_token_key"],configtwitter["access_token_secret"])
    #apitweepy = tweepy.API(auth)
    #apitweepy = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True,parser=tweepy.parsers.JSONParser())
    apitweepy = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    try:
        apitweepy.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")  

    return apitweepy

######################################################################################
    
def get_friends_ids(idUserNode):
    api=getApi()
    ids = []
    try:
        for page in tweepy.Cursor(api.friends_ids, id=idUserNode, count=5000).pages():
            #print 'Getting page {} for friends ids'.format(i)
            #print('ids.extend(page)')
            ids.extend(page)
            #print(ids)
    except tweepy.error.TweepError as e:
        print('error: ',e)
       # print (e.message)        
    return ids 

######################################################################################

def get_timeline(idUserNode):
    api=getApi()
    tweets = []
    try:
        tweetsaux=api.user_timeline( id=idUserNode, count=200,include_rts = True)
        
        for status in tweetsaux:
            user_mentions=status._json['entities']['user_mentions']
            if(len(user_mentions)>0):
                for tw in user_mentions:
                    item ={
                        "screen_name" : tw['screen_name'],
                        "name" : tw['name'],
                        "id" : tw['id'],
                        "id_str" : tw['id_str']
                    }
                    tweets.append(item)

    except tweepy.error.TweepError as e:
        print('error: ',e)
        #print (e.message)        
    return GetUniqueListFromList(tweets) 
    
##############################################

def countItemsAndRemoveDuplicates():
    frequency = {}
    for item in list:
        if(item in frequency):
            frequency[item] += 1
    else:
        frequency[item] = 1
    for key, value in frequency.items():
        print("% s -> % d" % (key, value))

##############################################

def GetUniqueListFromList(ListVar):
    d_unique = pd.DataFrame(ListVar).drop_duplicates().to_dict('records')
    return d_unique

