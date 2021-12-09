#!/usr/bin/python3

import statistics
import pandas as pd
import subprocess
import connectPg

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()

# --- Clear screen & get Ticker input
subprocess.run("clear ",  shell=True)
dtPlan = input("Input date : ")

# Use a list here to insert query parameters into the query string.
#query = """SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc FROM stock_trx_jsx WHERE id_ticker = '""" + ticker + """' AND dt_trx >= '"""+ dt1 +"""' AND dt_trx <= '""" +dt2 +"""' """

query = """
  SELECT id_ticker,dt_trx,buy1,buy2,tp1,tp2,stoplost,risk,pattern
  FROM t_planlist
  WHERE
  dt_trx = '"""+ dtPlan +"""'   
  ORDER by buy1 DESC
  """
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
with open('dataset/read_'+dtPlan+'.csv', 'w') as f:
  cur.copy_expert(outputquery, f)

 
# subprocess.run("ls -l dataset ",  shell=True)

#---Load Dataset
# Load the Stock dataset
df = pd.read_csv('dataset/read_'+dtPlan+'.csv', sep=',')

# #add new column to represent sales differences between each row
#df['tHigh_vs_pClose'] = (df['high_prc'] - df['close_prc'].shift(-1)).fillna(0).astype(int)
#df['tLow_vs_pClose'] = (df['low_prc'] - df['close_prc'].shift(-1)).fillna(0).astype(int)
#df['tHigh_vs_tOpen'] = (df['high_prc'] - df['open_prc']).fillna(0).astype(int)
#df['tOpen_vs_tClose'] = (df['close_prc'] - df['open_prc']).fillna(0).astype(int)

print(df.head(n=100))

#--- get data Max,Min,Avg for only last 5 Days

#print("Total GAP for last 30 days : ", sum(df['tHigh_vs_pClose']))
#print("Total GAP for last 5 days : ", sum(df['tHigh_vs_pClose'][+0:][:5]))
#print("Average for last 5 days : ", statistics.mean(df['tHigh_vs_pClose'][+0:][:5]))
#print("Max High : ", max(df['tHigh_vs_pClose'][+0:][:5]))
#print("Min High : ", min(df['tHigh_vs_pClose'][+0:][:5]))


cur.close()
conn.close()

#--- Remove existing ticker dataframe
subprocess.run('rm dataset/read_'+dtPlan+'.csv',  shell=True)