#!/usr/bin/bash

THE_USER=msa
THE_PASS=digi123
THE_DB=amibroker
THE_TABLE=stock_master

PSQL=/usr/bin/psql
THE_DIR=/home/$USER/www/python3/py-jsx
THE_FILE=$THE_DIR/dataset/$1.csv

#--- Extract data
cat <<SQL | tr -d '\n'  | \psql -U ${THE_USER} ${THE_DB}
\COPY (
  SELECT id_ticker, nm_ticker FROM ${THE_TABLE}   
  ORDER BY id_ticker ASC
) TO ${THE_FILE} DELIMITER ','
SQL