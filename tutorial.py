#!/usr/bin/python3

#-----------Penting to prevent BAD INTERPRETER --> sed -i -e 's/\r$//' <script>

import connectPg

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

# load_dotenv()
#--- Connect DB
conn = connectPg.connect()
  
# Creating a cursor object
cur = conn.cursor()

#excute query
cur.execute("select * from stock_master")
rows = cur.fetchall()
for r in rows:
  print (f"{r[0]} {r[1]}")

#commit the transcation 
# con.commit()

#close the cursor
cur.close()

#close the connection
conn.close()