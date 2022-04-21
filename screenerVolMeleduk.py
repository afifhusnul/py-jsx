#!/usr/bin/python3
import os
import pandas as pd
import subprocess
import numpy as np
import glob
from tabulate import tabulate
# import sys
# import statistics
# import connectPg
from pathlib import Path


# --- Clear screen & setting file
subprocess.run("clear ",  shell=True)
filepath = Path('dataset/meledukOut.csv') 
joined_files = os.path.join("dataset", "meledukAll.csv")
# joined_list = glob.glob(joined_files)

def is_breakVol(df):
    # last_vol = df[-1:]['volume_trx'].values[0]
    # last_2vol = df[-2:]['volume_trx'].values[0]
    ijo = df['tC_pC'].values[0]
    bengkak = df['breakVol'].values[0]

    if ( ijo > 0 and
        (((df['volume_trx'] - df['volume_trx'].shift(-1)) / df['volume_trx'].shift(-1))*100).values[0] > 100
        # (df['close_prc'] - df['close_prc'].shift(-1)).values[0] > 1
        # (df['volume_trx'] / df['volume_trx'].shift(-1).sum()).values[0] > 1 and
        # df['volume_trx'].shift(-1).values[0] > 10000
      ):
    # if ijo >= 1 and bengkak >= 1 :
      # df['gapVol'] = df['gapVol'].map('{:,.0f}'.format)
      # print(df.head(n=2))
      return True   

    return False

for filename in os.listdir('dataset/daily'):
    df = pd.read_csv('dataset/daily/{}'.format(filename))
    df['tC_pC'] = (((df['close_prc'] - df['close_prc'].shift(-1)) / df['close_prc'].shift(-1))*100).fillna(0).astype(int)
    df['gapVol'] = (df['volume_trx'] - df['volume_trx'].shift(-1)).fillna(0).astype(int)
    df['breakVol'] = (((df['volume_trx'] - df['volume_trx'].shift(-1)) / df['volume_trx'].shift(-1))*100)
    # df['breakVol'] = ((df['volume_trx'] / df['volume_trx'].shift(-1).sum())).fillna(0).astype(int)
    # df['breakVol'] = ((df['volume_trx'] / df['volume_trx'].shift(-1).sum()) ).map('{:,.2f}'.format)
    # df.sort_values(by=['breakVol'], inplace=True, ascending=False)

    if is_breakVol(df):      
      df_t = df.head(1)
      # df.sort_values(by=['breakVol'], inplace=True, ascending=False)      
      # print("{} is IJO ".format(filename))
      print(tabulate(df.head(1), tablefmt='github', showindex=False))
      
      # df_t.to_csv(filepath, sep='|', index=False, header=False)
      # df_t.to_csv(filepath, sep='|', index=False)
      # joined_list = glob.glob(joined_files)
      # dfJadi = pd.read_csv('dataset/joined_files.csv', sep='|')
      # dfGabung = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
      # dfJadi.sort_index(axis=1, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True)
      # print(dfJadi.head(20))

      # df.to_csv(filepath) 
      # print((df_t.to_string(index=False, header=None)))