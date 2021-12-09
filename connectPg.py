"""Load config from environment variables."""
import configparser
import psycopg2
from os import environ, path
from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# SQL queries
SQL_QUERIES_FOLDER = 'sql'

def connect():
    # return MySQLdb.connect(host = config['mysqlDB']['host'],
    #                        user = config['mysqlDB']['user'],
    #                        passwd = config['mysqlDB']['pass'],
    #                        db = config['mysqlDB']['db'])

    return psycopg2.connect(
                      database=environ.get('DATABASE_NAME'),
                      user=environ.get('DATABASE_USERNAME'),
                      password=environ.get('DATABASE_PASSWORD'),
                      host=environ.get('DATABASE_HOST'),
                      port=environ.get('DATABASE_PORT')
                  )