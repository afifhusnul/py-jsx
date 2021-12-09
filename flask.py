from flask import Flask
import sys, csv, pwd
import subprocess
import psycopg2
from psycopg2 import sql
from os import environ, path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
@app.route("/")

db_conn = psycopg2.connect(
    database=environ.get('DATABASE_NAME'),
    user=environ.get('DATABASE_USERNAME'),
    password=environ.get('DATABASE_PASSWORD'),
    host=environ.get('DATABASE_HOST'),
    port=environ.get('DATABASE_PORT')
)
db_cursor = db_conn.cursor()

ticker = "AALI"
dt1 = "2021-11-01"
dt2 = "2021-11-03"

@app.route("/export")
def csv_export():
    s = "'"
    s += "SELECT id_ticker,dt_trx,open_prc,high_prc,low_prc,close_prc,volume_trx,value_prc"
    s += " FROM "
    s += "stock_trx_jsx"
    s += "WHERE id_ticker = '"+ticker+"'"
    s += "AND dt_trx >= '"+dt1+"'"
    s += "AND dt_trx <= '"+dt2+"'"
    s += "'"

    # set up our database connection.
    # conn = psycopg2.connect...
    # db_cursor = conn.cursor()

    # Use the COPY function on the SQL we created above.
    SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)

    # Set up a variable to store our file path and name.
    t_path_n_file = "dataset/daily/"+ticker+".csv"

    # Trap errors for opening the file
    try:
    WITH Open(t_path_n_file, 'w') as f_output:
        db_cursor.copy_expert(SQL_for_file_output, f_output)
    except psycopg2.Error as e:
        t_message = "Error: " + e + "/n query we ran: " + s + "/n t_path_n_file: " + t_path_n_file
        return render_template("error.html", t_message = t_message)

    # Success!

    # Clean up: Close the database cursor and connection
    db_cursor.close()
    db_conn.close()