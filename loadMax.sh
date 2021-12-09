#!/usr/bin/bash

/usr/bin/clear
THE_USER=msa
THE_DB=amibroker
THE_TABLE3=stock_trx_jsx

PSQL=/usr/bin/psql
THE_DIR=/home/$USER/www/express-nextjs/jsx/data-jsx
THE_FILE3=$THE_DIR/Planlist11.txt


#------------------- Process Table Open
${PSQL} -U ${THE_USER} ${THE_DB} <<OMG
SELECT MAX(dt_trx) FROM stock_trx_jsx;
OMG
