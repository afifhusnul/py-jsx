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
if len(sys.argv) < 4:
# if len(sys.argv[1]) == 0 and len(sys.argv[2]) == 0:
  prc1 = input("Input Price Range-1 : ")
  prc2 = input("Input Price Range-2 : ")
  dt   = int(input("Input Date Row/Trx Date : "))
  sort = input("Sort by (Close Prc or High Prc")
  if len(prc1) < 1 and len(prc2) < 1 and len(dt) < 1 and len(sort) < 1 :
    print("No Input then Exit or input is not complete")
    quit()
else:
  prc1 = sys.argv[1]
  prc2 = sys.argv[2]
  dt   = sys.argv[3]
  sort = sys.argv[4]
  if (int(dt) <= 1):
    dt2 = int(dt)
  else :
    dt2 = int(dt)-int(1)


# Use a list here to insert query parameters into the query string.

# def readStock(Ticker):
# 
#------StockMuncrat
queryMuncrat = """
  SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
  FROM stock_trx_jsx
  WHERE
  close_prc BETWEEN '"""+ prc1 +"""' AND '"""+ prc2 +"""'
  AND open_prc > 0
  AND volume_trx >= 100000
  AND dt_trx = (select dt_trx from bajul where row_number between '"""+ str(dt2) +"""' and '"""+ dt +"""')
  ORDER by close_prc DESC
  """
outputqueryMuncrat = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(queryMuncrat)
with open('dataset/rangeStockMuncrat_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', 'w') as f:
  cur.copy_expert(outputqueryMuncrat, f)

#------Query Now
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

#------Query PrevDay
queryPrev = """
  SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
  FROM stock_trx_jsx
  WHERE
  close_prc BETWEEN '"""+ prc1 +"""' AND '"""+ prc2 +"""'
  AND open_prc > 0
  AND volume_trx >= 100000
  AND dt_trx = (select dt_trx from bajul where row_number = '"""+ str(dt2) +"""')
  ORDER by close_prc DESC
  """
outputqueryPrev = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(queryPrev)
with open('dataset/rangeStockPrev_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', 'w') as f:
  cur.copy_expert(outputqueryPrev, f)  

# Load the  dataset
df = pd.read_csv('dataset/rangeStock_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', sep=',')
df2 = pd.read_csv('dataset/rangeStockPrev_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', sep=',')
dfMuncrat = pd.read_csv('dataset/rangeStockMuncrat_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv', sep=',')

# df['tClose_vs_tOpen'] = (df['close_prc'] - df['open_prc']).fillna(0).astype(int)
# df['tHigh_vs_tOpen'] = (df['high_prc'] - df['open_prc']).fillna(0).astype(int)
# df['gapHigh'] = ((df['high_prc'] / df['open_prc'].sum()) * 100).map('{:,.2f}'.format)

# dfCombine = df.loc[df['id_ticker'].isin(df2['id_ticker'])]
# dfCombine['tVol_pVol'] = (dfCombine['volume_trx'] - dfCombine['volume_trx'].shift(-1)).fillna(0).astype(int)
# 
# 
dfMuncrat['tClose_vs_tOpen'] = (dfMuncrat['close_prc'] - dfMuncrat['open_prc']).fillna(0).astype(int)
dfMuncrat['tHigh_vs_tOpen'] = (dfMuncrat['high_prc'] - dfMuncrat['open_prc']).fillna(0).astype(int)
dfMuncrat['gapHigh'] = ((dfMuncrat['high_prc'] / dfMuncrat['open_prc'].sum()) * 100).map('{:,.2f}'.format)
dfMuncrat['tVol_pVol'] = (dfMuncrat['volume_trx'] - dfMuncrat['volume_trx'].shift(-1)).fillna(0).astype(int)

if (sort.upper() == 'C') :
  df_sort = dfMuncrat.sort_values(by='tVol_pVol', ascending=False)
else :
  df_sort = dfMuncrat.sort_values(by='tVol_pVol', ascending=False)

print(df_sort.head(n=50))
cur.close()
conn.close()


#--- Remove existing ticker dataframe
subprocess.run('rm dataset/rangeStock_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv',  shell=True)
subprocess.run('rm dataset/rangeStockPrev_'+prc1+'_TO_'+prc2+'_'+curTime+'.csv',  shell=True)
