#!/usr/bin/python3
import sys
import statistics
import pandas as pd
import subprocess
import connectPg
from pathlib import Path

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()

# --- Clear screen & get Ticker input
subprocess.run("clear ",  shell=True)
if len(sys.argv) < 2:
  Stock = input("Input a ticker : ")
  # readStock(Stock)
  if len(Stock) < 1:
    print("No Input then Exit")
    quit()
else:
  Stock = sys.argv[1]
  # readStock(Stock)


#Stock = input("Input a ticker : ")

# Use a list here to insert query parameters into the query string.
#query = """SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc FROM stock_trx_jsx WHERE id_ticker = '""" + ticker + """' AND dt_trx >= '"""+ dt1 +"""' AND dt_trx <= '""" +dt2 +"""' """

# def readStock(Ticker):
query = """
  SELECT dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
  FROM stock_trx_jsx 
  WHERE
  id_ticker = '"""+ Stock.upper() +"""' 
  AND dt_trx IN (SELECT dt_trx FROM bajul WHERE row_number BETWEEN 1 AND 30)
  ORDER by dt_trx DESC
  """
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
with open('dataset/read_'+Stock.upper()+'.csv', 'w') as f:
  cur.copy_expert(outputquery, f)

 
# subprocess.run("ls -l dataset ",  shell=True)

#---Load Dataset
# Load the Stock dataset
df = pd.read_csv('dataset/read_'+Stock.upper()+'.csv', sep=',')

# #add new column to represent sales differences between each row
df['tHigh_vs_pClose'] = (df['high_prc'] - df['close_prc'].shift(-1)).fillna(0).astype(int)
#df['tLow_vs_pClose'] = (df['low_prc'] - df['close_prc'].shift(-1)).fillna(0).astype(int)
df['tHigh_vs_tOpen'] = (df['high_prc'] - df['open_prc']).fillna(0).astype(int)
df['tOpen_vs_tClose'] = (df['close_prc'] - df['open_prc']).fillna(0).astype(int)
df['gapHigh'] = ((df['high_prc'] / df['open_prc'].sum()) * 100).map('{:,.2f}'.format)

print(df.head(n=30))

#--- get data Max,Min,Avg for only last 5 Days
print("Ticker ID ", Stock.upper())
print("Total GAP for last 30 days : ", sum(df['tHigh_vs_pClose']))
print("Total GAP for last 5 days : ", sum(df['tHigh_vs_pClose'][+0:][:5]))
print("Average for last 5 days : ", statistics.mean(df['tHigh_vs_pClose'][+0:][:5]))
print("Max High : ", max(df['tHigh_vs_pClose'][+0:][:5]))
print("Min High : ", min(df['tHigh_vs_pClose'][+0:][:5]))
print("==================")
print("Average Volume Trx for last 5 days :", '{:,}'.format(statistics.mean(df['volume_trx'][+0:][:5]/100)),"Lot")
print("Average Value Trx for last 5 days :", '{:,}'.format(statistics.mean(df['value_prc'][+0:][:5]/1000)),"M")

cur.close()
conn.close()

#--- Remove existing ticker dataframe
subprocess.run('rm dataset/read_'+Stock.upper()+'.csv',  shell=True)
