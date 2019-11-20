import argparse
import urllib
from urllib import parse
#import urllib2
import json
import datetime
import random
import os
import pickle
from datetime import timedelta

import oauth2
# from dateutil import parser

class TwitterData:
    #start __init__
    def __init__(self,givenDate):
        self.currDate = datetime.datetime.strptime(givenDate,'%Y-%m-%d')
        #get date in this format
        # self.currDate = datetime.datetime.now()
        # print type(self.currDate)
        # print self.currDate
        # print type(y)
        # print y
        self.weekDates = []
        print('poorvi')
        self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))
        #parse date in this format
        for i in range(1,20):
            dateDiff = datetime.timedelta(days=-i)
            newDate = self.currDate + dateDiff
            self.weekDates.append(newDate.strftime("%Y-%m-%d"))
        # end loop
        print("New Week Dates =",self.weekDates)
    # end

    # start getWeeksData
    def getTwitterData(self, keyword, time):
        self.weekTweets = {}
        print('poorvi1')
        if(time == 'lastweek'):
            for i in range(0,19):
                params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
                self.weekTweets[i] = self.getData(keyword, params)
            # end loop

            # Write data to a pickle file
            filename = 'Data/weekTweets_'+urllib.parse.unquote(keyword.replace("+", " "))+'_'+str(int(random.random()*10000))+'.txt'
            outfile = open(filename, 'wb')
            pickle.dump(self.weekTweets, outfile)
            outfile.close()
        elif(time == 'today'):
            print('poorvi2')
            for i in range(0,1):
                params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
                # params = {'since': self.weekDates[i]}
                self.weekTweets[i] = self.getData(keyword, params)
            # end loop
        return self.weekTweets
    '''
        inpfile = open('data/weekTweets/weekTweets_obama_7303.txt')
        self.weekTweets = pickle.load(inpfile)
        inpfile.close()
        return self.weekTweets
    '''
    # end

    def parse_config(self):
      config = {}
      # from file args
      if os.path.exists('config.json'):
          with open('config.json') as f:
              config.update(json.load(f))
    #   else:
    #       args_ = parser.parse_args()
    #       def val(key):
    #         return config.get(key)\
    #                or getattr(args_, key)\
    #                or raw_input('Your developper `%s`: ' % key)
    #       config.update({
    #         'consumer_key': val('consumer_key'),
    #         'consumer_secret': val('consumer_secret'),
    #         'access_token': val('access_token'),
    #         'access_token_secret': val('access_token_secret'),
    #       })
      # should have something now
      return config
#
#    def oauth_req(self, url, http_method="GET", post_body=None,
#                  http_headers=None):
#      config = self.parse_config()
#      print(config.get('consumer_key'))
#      consumer = oauth2.Consumer(key=config.get('consumer_key'), secret=config.get('consumer_secret'))
#      token = oauth2.Token(key=config.get('access_token'), secret=config.get('access_token_secret'))
#      client = oauth2.Client(consumer, token)
#      print('token accepted')
#      resp, content = client.request(url,method=http_method,body=post_body or '',headers=http_headers)
#      return content
  
   def oauth_req(self, url, http_method="GET", post_body=None,
                  http_headers=None):
      config = self.parse_config()
      consumer = oauth2.Consumer(key=config.get('consumer_key'), secret=config.get('consumer_secret'))
      token = oauth2.Token(key=config.get('access_token'), secret=config.get('access_token_secret'))
      client = oauth2.Client(consumer, token)

      resp, content = client.request(
          url,
          method=http_method,
          body=post_body or '',
          headers=http_headers
      )
      return content
  
    

    # start getTwitterData
    def getData(self, keyword, params = {}):
        maxTweets = 200
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        data = {'q': keyword, 'lang': 'en', 'result_type': 'mixed', 'since_id': 2019,'count': maxTweets, 'include_entities': 0}
        print('hello')
        # Add if additional params are passed
        if params:
            for key, value in params.iteritems():
                data[key] = value
        print(url)
        url += urllib.parse.urlencode(data)
        #url=urllib.parse.urlencode(url)
        print(type(url))
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
                str = d.strftime('%Y-%m-%d')+" | "+item['text'].replace('\n', ' ')
                # dt = parser.parse(item['created_at'])
                # tweets.append(item['text'])
                tweets.append(str)
        return tweets
    # end

# end class
obj=TwitterData('2019-11-18')
obj.getData('stock')