#!/usr/bin/python3

import subprocess
import connectPg

# --- Clear screen
subprocess.run("clear ",  shell=True)

# connection establishment
conn = connectPg.connect()    
cur = conn.cursor()

dbcopy_f = open('dataset/tickers.csv','wb')
copy_sql = 'COPY stock_master TO STDOUT WITH CSV'
cur.copy_expert(copy_sql, dbcopy_f)

#close the cursor
cur.close()

# Closing the connection
conn.close()