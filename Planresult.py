#!/usr/bin/python3
import sys
import statistics
import pandas as pd
import subprocess
import connectPg

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()

# --- Clear screen & get Ticker input
subprocess.run("clear ",  shell=True)

if len(sys.argv) < 2:
# if len(sys.argv[1]) == 0 and len(sys.argv[2]) == 0:
  dt1 = input("Input date-1 : ")
  dt2 = input("Input date-2 : ")
  if len(dt1) < 1 and len(dt2) < 1:
    print("No Input then Exit")
    quit()
else:
  dt1 = sys.argv[1]
  dt2 = sys.argv[2]


# Use a list here to insert query parameters into the query string.
query = """
  SELECT *
  FROM f_planlist (
  (select dt_trx from bajul where row_number = '"""+ dt1 +"""'), 
  (select dt_trx from bajul where row_number = '"""+ dt2 +"""')
  )  
  """
outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
with open('dataset/planresult_'+dt1+'.csv', 'w') as f:
  cur.copy_expert(outputquery, f)


#---Load Dataset
df = pd.read_csv('dataset/planresult_'+dt1+'.csv', sep=',')
print(df.head(n=100))
cur.close()
conn.close()

#--- Remove existing ticker dataframe
subprocess.run('rm dataset/planresult_'+dt1+'.csv',  shell=True)