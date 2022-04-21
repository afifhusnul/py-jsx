#!/usr/bin/python3
import os, pandas
import subprocess
# import sys
# import statistics
# import connectPg
# from pathlib import Path

# --- Clear screen & get Ticker input
subprocess.run("clear ",  shell=True)

def is_consolidating(df, percentage=2):
    recent_candlesticks = df[-10:]
    
    max_close = recent_candlesticks['close_prc'].max()
    min_close = recent_candlesticks['close_prc'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True        

    return False

def is_breaking_out(df, percentage=3):
    last_close = df[-1:]['close_prc'].values[0]

    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-10:-1]

        if last_close > recent_closes['close_prc'].max():
            print(df.head(n=2))
            return True

    return False

for filename in os.listdir('dataset/daily'):
    df = pandas.read_csv('dataset/daily/{}'.format(filename))
    df['tC_pC'] = (df['close_prc'] - df['close_prc'].shift(-1)).fillna(0).astype(int)    
    
    # if is_consolidating(df, percentage=2.5):
        # print("{} is consolidating".format(filename))

    if is_breaking_out(df):
        print("{} is breaking out".format(filename))