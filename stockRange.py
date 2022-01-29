#!/usr/bin/python3
import sys
import statistics
import pandas as pd
import subprocess
import connectPg
from pathlib import Path
from datetime import datetime
now = datetime.now()

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()
curTime = now.strftime("%Y%m%d%H%M%S")
# --- Clear screen & get Ticker input
subprocess.run("clear ",  shell=True)
if len(sys.argv) < 2:
# if len(sys.argv[1]) == 0 and len(sys.argv[2]) == 0:
  prc1 = input("Input Price Range-1 : ")
  prc2 = input("Input Price Range-2 : ")
  sort = input("Sort by (Close Prc or High Prc")
  if len(prc1) < 1 and len(prc2) < 1 and len(sort) < 1:
    print("No Input then Exit")
    quit()
else:
  prc1 = sys.argv[1]
  prc2 = sys.argv[2]
  sort = sys.argv[3]

# Use a list here to insert query parameters into the query string.

# def readStock(Ticker):
query = """
  SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
  FROM stock_trx_jsx
  WHERE
  close_prc BETWEEN '"""+ prc1 +"""' AND '"""+ prc2 +"""'
  AND open_prc > 0
  AND volume_trx >= 1000
  AND dt_trx = (select dt_trx from bajul where row_number = 1)
  ORDER by close_prc DESC
  """
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
with open('dataset/rangeStock_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', 'w') as f:
  cur.copy_expert(outputquery, f)

# subprocess.run("ls -l dataset ",  shell=True)
# Load the  dataset
df = pd.read_csv('dataset/rangeStock_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', sep=',')
df['tClose_vs_tOpen'] = (df['close_prc'] - df['open_prc']).fillna(0).astype(int)
df['tHigh_vs_tOpen'] = (df['high_prc'] - df['open_prc']).fillna(0).astype(int)
if (sort == 'C') :
  df_sort = df.sort_values(by='tClose_vs_tOpen', ascending=False)
else :
  df_sort = df.sort_values(by='tHigh_vs_tOpen', ascending=False)
  
print(df_sort.head(n=50))
cur.close()
conn.close()


#--- Remove existing ticker dataframe
subprocess.run('rm dataset/rangeStock_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv',  shell=True)
