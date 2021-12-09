#!/usr/bin/bash

THE_USER=msa
THE_DB=amibroker
THE_TABLE3=t_planlist

PSQL=/usr/bin/psql
THE_DIR=/home/$USER/www/python3/py-jsx
THE_FILE3=$THE_DIR/dataset/planlist/Planlist11.txt
loadPlanlist=$THE_DIR/bash/ProcPlanlist.sh

$loadPlanlist

#--\COPY ${THE_TABLE3} FROM '${THE_FILE3}' delimiter '|' csv;
#------------------- Process Table Open
${PSQL} -U ${THE_USER} ${THE_DB} <<OMG
\COPY ${THE_TABLE3} (id_ticker,dt_trx,buy1,buy2,tp1,tp2,stoplost,risk,pattern) FROM '${THE_FILE3}' delimiter '|' csv;
OMG

wc -l $THE_FILE3
cat $THE_FILE3
/usr/bin/rm $THE_FILE3
/home/$THE_USER/www/python3/py-jsx/readPlanlist.py
