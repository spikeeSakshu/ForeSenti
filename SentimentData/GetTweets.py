# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 12:41:30 2019

@author: Sakshu
"""

import urllib
from urllib import parse
import json
import datetime
import os
from datetime import timedelta
import oauth2
import csv
import time
from datetime import date

global csvWriter

class TwitterData:
    #start __init__
    def __init__(self,givenDate):
        self.currDate = datetime.datetime.strptime(givenDate,'%Y-%m-%d')
       
        self.weekDates = []
        
        self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))
        #parse date in this format
        
        for i in range(1,20):
            dateDiff = datetime.timedelta(days=-i)
            newDate = self.currDate + dateDiff
            self.weekDates.append(newDate.strftime("%Y-%m-%d"))
        # end loop
#        print("New Week Dates =",self.weekDates)
    # end

    # start getWeeksData
    def getTwitterData(self, keyword):
        self.weekTweets = {}
        print('weeks')
        
        for i in range(0,10):
            params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
            self.weekTweets[i] = self.getData(keyword, params)
            #print(self.weekTweets[i])
            # end loop
        return self.weekTweets

    # end

    def parse_config(self):
        config = {}
      # Get credential from JSON file
        if os.path.exists('SentimentData/twitter_credentials.json'):
            with open('SentimentData/twitter_credentials.json') as f:
                config.update(json.load(f))
#        print(config)
        return config

    def oauth_req(self, url, http_method="GET", post_body='',
              http_headers=None):
        config = self.parse_config()
        consumer = oauth2.Consumer(key=config.get('CONSUMER_KEY'), secret=config.get('CONSUMER_SECRET'))
        token = oauth2.Token(key=config.get('ACCESS_KEY'), secret=config.get('ACCESS_SECRET'))
        client = oauth2.Client(consumer, token)
#        print('token accepted')
        resp, content = client.request(url,method=http_method,body=bytes('', 'utf-8'),headers=http_headers)

        return content

    # start getTwitterData
    def getData(self, keyword, params = {}):
        maxTweets = 200
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        data = {'q': keyword, 'lang': 'en', 'result_type': 'mixed', 'since_id': 2018,'count': maxTweets, 'include_entities': 0}
       # print('hello')
        # Add if additional params are passed
        if params:
            for key, value in params.items():
                data[key] = value
        url += urllib.parse.urlencode(data)

        response = self.oauth_req(url)
        jsonData = json.loads(response)
        tweets = []
        if 'errors' in jsonData:
            print ("API Error")
            print(jsonData['errors'])
        else:
            for item in jsonData['statuses']:
                #print item['created_at']
                d = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                date= str(d).split()
                
                csvWriter.writerow([item['user']['screen_name'], item['text'].encode('utf-8'), 'Company', date[0], date[1]])
                
        return tweets
    
def tweets(symbol):
    # Open/Create a file to append data
    csvFile = open('Data/'+symbol+'_Tweets.csv', 'w', newline='')
    #Use csv Writer
    global csvWriter
    csvWriter= csv.writer(csvFile)
    csvWriter.writerow(["Username", "Tweet",  'Company', "Date", 'Time'])
    
    if symbol=='RELIANCE':
        q='@RELIANCE OR @jio OR #Reliance OR #RELIANCE OR RELIANCE JIO OR Reliance Industries OR RCOM OR Reliance Industries OR RELCAPITAL'
    else:
        q='#'+symbol
    
    twitterData = TwitterData(str(date.today()))
    twitterData.getTwitterData(q)
    print('Tweets Scrapped')

    
    