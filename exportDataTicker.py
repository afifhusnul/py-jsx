#!/usr/bin/python3

import sys, csv, pwd
import subprocess
import psycopg2
from psycopg2 import sql
from os import environ, path
from dotenv import load_dotenv

load_dotenv()
  
# connection establishment
#--- Connect DB
conn = psycopg2.connect(
    database=environ.get('DATABASE_NAME'),
    user=environ.get('DATABASE_USERNAME'),
    password=environ.get('DATABASE_PASSWORD'),
    host=environ.get('DATABASE_HOST'),
    port=environ.get('DATABASE_PORT')
)

cursor = conn.cursor()
subprocess.run("clear ",  shell=True)


dbcopy_f = open('dataset/master.csv','wb')
dt1 = "2021-11-01"
dt2 = "2021-11-06"




with open('dataset/master.csv') as f:
    for line in f:
      if "," not in line:
          continue
      symbol = line.split(",")[0]
      print(symbol)
      # data = yf.download(symbol, start=dt1, end=dt2)
      query = """SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc FROM stock_trx_jsx WHERE id_ticker = '""" + symbol + """' AND dt_trx >= '"""+ dt1 +"""' AND dt_trx <= '""" +dt2 +"""' """
      outputquery = "COPY ({0}) TO STDOUT WITH CSV ".format(query)
      with open('dataset/daily/{}.csv', 'r') as f_output:
        cur.copy_expert(outputquery, f_output)
        # cur.to_csv('datasets/daily/{}.csv'.format(symbol))
      # cur.copy_expert(outputquery,
          # outputquery.to_csv('datasets/daily/{}.csv'.format(symbol))


# copy_sql = 'COPY stock_master TO STDOUT WITH CSV'
# cursor.copy_expert(copy_sql, dbcopy_f)

# with open('dataset/symbols.csv') as f:
#   for line in f:
#       if "," not in line:
#           continue
#       symbol = line.split(",")[0]
#       print(symbol)
      # for r in symbol:
        # print(r[0])
      # # data = yf.download(symbol, start="2020-01-01", end="2020-08-01")
      # sql_select = ("""
      #       SELECT * 
      #       FROM stock_trx_jsx
      #       WHERE id_ticker = %s
      #       AND dt_trx >= %s
      #       AND dt_trx <= %s;
      #       """,
      #       (symbol,dt1,dt2)
      #       )
      
      # data = cursor.execute(sql_select)
      # dbcopy_f = open('dataset/daily/{}.csv','wb')
      # cursor.copy_expert(data, dbcopy_f)

      # rows = cur.fetchall()
      # for r in rows:
      #   print (f"{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}|{r[5]}|{r[6]}|{r[7]}")


      # dbcopy_f = open('dataset/symbols.csv','wb')
      # data.to_csv('dataset/daily/{}.csv'.format(symbol))
      # cursor.copy_expert(copy_sql, dbcopy_f)

subprocess.run("ls -l dataset/daily ",  shell=True)

#close the cursor
cursor.close()

# Closing the connection
conn.close()