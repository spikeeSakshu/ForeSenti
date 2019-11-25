# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:03:18 2019

@author: Sakshu
"""

import pandas as pd
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from nltk import tokenize
import collections
from SentimentData.GetTweets import tweets

def Merge_datasets(symbol, df1):
    
    
    df2=pd.read_csv('Data/'+symbol+'_Week.csv')
    
    df1['date'] = pd.to_datetime(df1.date).dt.strftime('%Y-%m-%d')
    
    # create sets of ids
    id_df1=set(df1['date'].tolist())
    id_df2=set(df2['Date'].tolist())
    
    ids=id_df1.intersection(id_df2)
    
    # copy of ids for 2nd for loop
#    cp_ids = copy.deepcopy(ids)
#    
#    not_present=id_df1-id_df2
    
    # create new df1 with unique rows
    df3=pd.DataFrame()
    c=0
    for i1,r1 in df1.iterrows():
        if r1.date in ids:
            temp=pd.DataFrame({'Date':[r1.date],'Score':[r1.Score]})
            df3=pd.concat([df3,temp])
            c=c+1
            ids.remove(r1.date)
            
    df4=pd.DataFrame()
    c=0
    for i1,r1 in df2.iterrows():
        #print(r1)
        temp=pd.DataFrame({'Date':[r1.Date],'Open':[r1.Open],'Close':[r1.Close], 'High':[r1.High], 'Low':[r1.Low], 'Prev Close':[r1['Prev Close']], 'Turnover': [r1.Turnover], 'Volume':[r1.Volume], 'Date.1':[r1.Date]})
        df4=pd.concat([df4,temp])
        c=c+1

    result= df4.merge(df3, on=['Date'])
    
    return result

def Average_senti(df):
    
    date_list = df.Date.tolist()
#    dates=set(date_list)
    
    cnt = collections.Counter(date_list)
    
    score= dict()
    for k,v in cnt.items():
#        print(k,v)
        score[k]= 0
        
    for i,r in df.iterrows():
        date=str(r.Date)
        
#        date1 = datetime.datetime.strptime(str(r.Date),"%d-%m-%Y") #.strftime("%Y-%m-%d")
#        delta = datetime.timedelta(days = 1)
#        prev_date = date1-delta
    
        score[date] += float(r.sentiment)
    
#    print(score)
    for k,v in cnt.items():
    
        if score[k]!=0:
            score[k]= score[k]/cnt[k]
    
    result = pd.DataFrame()

    for k,v in score.items():
        temp= pd.DataFrame({'Score':[score[k]], 'date':[k]}) 
        result = pd.concat([result,temp])
        
    
    return result

def sentiment_cal(tweet):	
	sia = SentimentIntensityAnalyzer()	
	score= sia.polarity_scores(tweet)	
	score = float(score['compound'])	
	return score
    
def senti_data(symbol):
    
    tweets(symbol)
    df = pd.read_csv('Data/'+symbol+'_Tweets.csv')
    
    
    result = pd.DataFrame()
    for i,r in df.iterrows():
    	score=sentiment_cal(str(r.Tweet))
    	temp=pd.DataFrame({'Username':[r.Username],'Tweet':[r.Tweet],'Company':[r.Company],'sentiment':[score],'Date':[r.Date], 'Time': [r.Time]})
    	result = pd.concat([result,temp])
        
#    result.to_csv('labeled.csv',encoding='utf-8',sep=',')
    
    avg_senti= Average_senti(result)
    
    merged_data= Merge_datasets(symbol, avg_senti)
    
    merged_data.to_csv('Data/'+symbol+'_merged_Data.csv', sep=',', encoding='utf-8')