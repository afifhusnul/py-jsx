#!/usr/bin/python3

import subprocess
import connectPg

# --- Clear screen
subprocess.run("clear ",  shell=True)

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()

#----------- Export data into csv
with open('dataset/master.csv') as f:
      for line in f:
        if "," not in line:
          continue
        Stock = line.split(",")[0]
          # data = yf.download(symbol, start="2021-01-01", end="2021-12-28")
          # data.to_csv('datasets/daily/{}.csv'.format(symbol))
        query = """
          SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc
          FROM stock_trx_jsx 
          WHERE
          id_ticker = '"""+ Stock.upper() +"""' 
          AND dt_trx IN (SELECT dt_trx FROM bajul WHERE row_number BETWEEN 1 AND 100)
          AND volume_trx >= 10000
          ORDER by dt_trx DESC
          """

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
        with open('dataset/daily/'+Stock.upper()+'.csv', 'w') as f:
          cur.copy_expert(outputquery, f)
          print("Export data for "+Stock.upper()+" Done")


# dbcopy_f = open('dataset/master.csv','wb')
# copy_sql = 'COPY stock_master TO STDOUT WITH CSV'
# cur.copy_expert(copy_sql, dbcopy_f)

#close the cursor
cur.close()

# Closing the connection
conn.close()
