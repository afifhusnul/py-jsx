#!/usr/bin/python3
import sys, csv, pwd
import subprocess
import psycopg2
import connectPg
from psycopg2 import sql
from os import environ, path
# from dotenv import load_dotenv

# load_dotenv()
  
# connection establishment
#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()

subprocess.run("clear ",  shell=True)
# dbcopy_f = open('dataset/master.csv','wb')

if len(sys.argv) < 2:

# if len(sys.argv[1]) == 0 and len(sys.argv[2]) == 0:
  dt1   = input("Input Date -1 : ")
  dt2   = input("Input Date -2 : ")
  if len(dt1) < 1 and len(dt2) < 1 :
    print("No Input then Exit or input is not complete")
    quit()
else:
  dt1 = sys.argv[1]
  dt2 = sys.argv[2]  


# dtx1 = "2022-01-01"
# dtx2 = "2022-01-31"


with open('dataset/master.csv') as f:
  for line in f:
    if "," not in line:
        continue
    symbol = line.split(",")[0]
    # print(symbol)
    query = """
      SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
      FROM stock_trx_jsx
      WHERE
      id_ticker = '"""+ symbol +"""'
      AND dt_trx >= (select dt_trx from bajul where row_number = '"""+ dt1 +"""')
      AND dt_trx <= (select dt_trx from bajul where row_number = '"""+ dt2 +"""')
      ORDER by dt_trx DESC
      """
    outputquery = "COPY ({}) TO STDOUT WITH CSV HEADER".format(query)
    with open('dataset/daily/'+symbol+'.csv', 'wb') as f:
      cur.copy_expert(outputquery, f)
      print("Export data for "+symbol+" Done")
          
subprocess.run("ls -l dataset/daily ",  shell=True)

#close the cursor
cur.close()

# Closing the connection
conn.close()