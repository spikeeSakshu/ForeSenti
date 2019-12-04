# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:56:01 2019

@author: Sakshu
"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit

from sklearn import linear_model,svm, preprocessing

import import_ipynb
from GetHistoricalData import find_data
from SentimentData.GetSentimentData import senti_data


def processing(data):
    # selecting Feature Columns
    feature_columns=['Prev Close','Open', 'High', 'Low', 'Volume', 'Turnover', 'Score']
    scaler = MinMaxScaler()
    feature_minmax_transform_data = scaler.fit_transform(data[feature_columns])
    feature_minmax_transform = pd.DataFrame(columns=feature_columns, data=feature_minmax_transform_data, index=data.index)
    return feature_minmax_transform

def split_data(data, target):
    ts_split= TimeSeriesSplit(n_splits=2)
    for train_index, test_index in ts_split.split(data):
        X_train, X_test = data[:len(train_index)], data[len(train_index): (len(train_index)+len(test_index))]
        y_train, y_test = target[:len(train_index)].values.ravel(), target[len(train_index): (len(train_index)+len(test_index))].values.ravel()
        
    return [X_train, X_test, y_train, y_test]

def build_model(X_train, y_train):
    lm = svm.SVR(max_iter=20,C=0.1)
    model_SVM= lm.fit(X_train, y_train)
    return model_SVM
    
    
def call_senti(symbol):
#    symbol= 'RELIANCE'
    find_data(symbol, '2019-11-05')
    
    senti_data(symbol)
    
    df = pd.read_csv('Data/'+symbol+"_merged_Data.csv",na_values=['null'],index_col='Date',parse_dates=True,infer_datetime_format=True)   
    columns=['Prev Close','Open', 'High', 'Low', 'Close', 'Volume', 'Turnover', 'Score']
    df_final= df[columns]
    test = df_final

    target = pd.DataFrame(test['Close'])
    
    feature_minmax_transform= processing(test)
    
    # Shift target array because we want to predict the n + 1 day value
    target = target.shift(-1)
    
    X_train, X_test, y_train, y_test= split_data(feature_minmax_transform, target)
    
    
    model= build_model(X_train, y_train)
    
    y_pred= model.predict(X_test)
 
    
    return y_pred[-1]