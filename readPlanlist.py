#!/usr/bin/python3
import sys
import statistics
import pandas as pd
import subprocess
import connectPg

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()

# --- Clear screen & get Date input
subprocess.run("clear ",  shell=True)

if len(sys.argv) < 2:
  dtPlan = input("Input date : ")  
  if len(dtPlan) < 1 :
    print("No Input then Exit")
    quit()
else:
  dtPlan = sys.argv[1]

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

 
#---Load Dataset
df = pd.read_csv('dataset/read_'+dtPlan+'.csv', sep=',')
print(df.head(n=100))

cur.close()
conn.close()

#--- Remove existing ticker dataframe
subprocess.run('rm dataset/read_'+dtPlan+'.csv',  shell=True)