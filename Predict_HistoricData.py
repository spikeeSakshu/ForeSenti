# -*- coding: utf-8 -*-
"""
Created on Mon Nov  23 22:07:02 2019

@author: Spikee
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score

from keras.models import Sequential
import keras.backend as K
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.layers import Dense
from keras.layers import LSTM

import import_ipynb
from GetHistoricalData import find_data


def processing(data):
    # selecting Feature Columns
    feature_columns=['Prev Close','Open', 'High', 'Low', 'Volume', 'Turnover']
    scaler = MinMaxScaler()
    feature_minmax_transform_data = scaler.fit_transform(data[feature_columns])
    feature_minmax_transform = pd.DataFrame(columns=feature_columns, data=feature_minmax_transform_data, index=data.index)
    return feature_minmax_transform

def split_data(data, target):
    ts_split= TimeSeriesSplit(n_splits=10)
    for train_index, test_index in ts_split.split(data):
        X_train, X_test = data[:len(train_index)], data[len(train_index): (len(train_index)+len(test_index))]
        y_train, y_test = target[:len(train_index)].values.ravel(), target[len(train_index): (len(train_index)+len(test_index))].values.ravel()
        
    return [X_train, X_test, y_train, y_test]

def build_model(X_train):
    K.clear_session()

    model_lstm = Sequential()
    model_lstm.add(LSTM(16, input_shape=(1, X_train.shape[1]), activation='relu', return_sequences=False))
    model_lstm.add(Dense(1))
    
    model_lstm.compile(loss='mean_squared_error', optimizer='adam')
    
    return model_lstm
    
    
def call(symbol):
    find_data(symbol, 0)
    df = pd.read_csv('Data'+symbol+".csv",na_values=['null'],index_col='Date',parse_dates=True,infer_datetime_format=True)
    columns=['Prev Close','Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']
    df_final= df[columns]
    test = df_final

    target = pd.DataFrame(test['Close'])
    
    feature_minmax_transform= processing(test)
    
    # Shift target array because we want to predict the n + 1 day value
    target = target.shift(-1)
    
    X_train, X_test, y_train, y_test= split_data(feature_minmax_transform, target)
    
    X_train =np.array(X_train)
    X_test =np.array(X_test)
    
    X_tr_t = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_tst_t = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
    
    
    model= build_model(X_tr_t)
    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)
    
    history_model_lstm = model.fit(X_tr_t, y_train, validation_data=(X_tst_t,y_test), epochs=200, batch_size=8, verbose=1, shuffle=False, callbacks=[early_stop])
    
    y_pred_test_LSTM= model_lstm.predict(X_tst_t)
    
    return [y_pred_test_LSTM[-1], y_test, y_pred_test_LSTM]