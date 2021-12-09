#!/usr/bin/python3

import subprocess
import connectPg

#--- Connect DB
conn = connectPg.connect()
cur = conn.cursor()


# --- Clear screen & get Ticker input
subprocess.run("clear ",  shell=True)