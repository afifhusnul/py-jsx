#!/usr/bin/python3

import os, pandas

def is_consolidating(df, percentage=2):
    recent_candlesticks = df[-15:]
    
    max_close_prc = recent_candlesticks['close_prc'].max()
    min_close_prc = recent_candlesticks['close_prc'].min()

    threshold = 1 - (percentage / 100)
    if min_close_prc > (max_close_prc * threshold):
        return True        

    return False

def is_breaking_out(df, percentage=2.5):
    last_close_prc = df[-1:]['close_prc'].values[0]

    if is_consolidating(df[:-1], percentage=percentage):
        recent_close_prcs = df[-16:-1]

        if last_close_prc > recent_close_prcs['close_prc'].max():
            return True

    return False

for filename in os.listdir('dataset/daily'):
    df = pandas.read_csv('dataset/daily/{}'.format(filename))
    print(df.head(n=1))
    #print df['tHigh_vs_pClose'] = (df['high_prc'] - df['close_prc'].shift(-1)).fillna(0).astype(int)
    #if is_consolidating(df, percentage=2.5):
    #    print("{} is consolidating".format(filename))

    #if is_breaking_out(df):
    #    print("{} is breaking out".format(filename))
