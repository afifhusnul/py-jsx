#!/usr/bin/python3

import sys
import psycopg2
from os import environ, path
from dotenv import load_dotenv

load_dotenv()
con = None
fout = None

try:

    con = psycopg2.connect(
    database=environ.get('DATABASE_NAME'),
    user=environ.get('DATABASE_USERNAME'),
    password=environ.get('DATABASE_PASSWORD'),
    host=environ.get('DATABASE_HOST'),
    port=environ.get('DATABASE_PORT')
)    

    cur = con.cursor()
    fout = open('dataset/tickers.csv', 'w')
    cur.copy_to(fout, 'stock_master', sep=",")

except psycopg2.DatabaseError as e:

    print(f'Error {e}')
    sys.exit(1)

except IOError as e:

    print(f'Error {e}')
    sys.exit(1)

finally:

    if con:
        con.close()

    if fout:
        fout.close()