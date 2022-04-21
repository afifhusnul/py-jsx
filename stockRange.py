#!/usr/bin/python3
import sys
import statistics
import pandas as pd
import subprocess
import connectPg
# from IPython.core.display import display, HTML
from pathlib import Path
from datetime import datetime
now = datetime.now()

a_number = 1 / 3
pd.options.display.float_format = '{:,.2f}'.format
#---------Execute ./stockRange.py <hrgRendah> <hrgTinggi> <dateRow> <Sort Close/High>
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
  dt   = input("Input Date Row/Trx Date : ")
  sort = input("Sort by (Close Prc or High Prc")
  if len(prc1) < 1 and len(prc2) < 1 and len(dt) < 1 and len(sort) < 1:
    print("No Input then Exit")
    quit()
else:
  prc1 = sys.argv[1]
  prc2 = sys.argv[2]
  dt   = sys.argv[3]
  sort = sys.argv[4]

# Use a list here to insert query parameters into the query string.

# def readStock(Ticker):
query = """
  SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
  FROM stock_trx_jsx
  WHERE
  close_prc BETWEEN '"""+ prc1 +"""' AND '"""+ prc2 +"""'
  AND open_prc > 0
  AND volume_trx >= 100000
  AND dt_trx = (select dt_trx from bajul where row_number = '"""+ dt +"""')
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
# df['gapHigh'] = ((df['close_prc'] / df['open_prc'].sum()) * 100).map('{:,.2f}'.format)
df['gapHigh'] = (((df['close_prc'] - df['open_prc']) / df['open_prc'])*100)

if (sort.upper() == 'C') :
  df_sort = df.sort_values(by='tClose_vs_tOpen', ascending=False)
else :
  #df_sort = df.sort_values(by='tHigh_vs_tOpen', ascending=False)
  df_sort = df.sort_values(by='gapHigh', ascending=False)
  # df_sort.style.hide_index()
  # print(df_sort.head(n=50))
  print(df_sort.to_string(index=False))
cur.close()
conn.close()


#--- Remove existing ticker dataframe
subprocess.run('rm dataset/rangeStock_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv',  shell=True)
