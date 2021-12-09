#!/usr/bin/bash
#
##--------- Define today's date
todayDt=`date '+%Y-%m-%d'`
baseFolder=/home/$USER/www/python3/py-jsx


filePlan=$baseFolder/dataset/planlist/Planlist.txt
filePlan0=$baseFolder/dataset/planlist/Planlist0.txt
filePlan1=$baseFolder/dataset/planlist/Planlist1.txt
filePlan2=$baseFolder/dataset/planlist/Planlist2.txt
filePlan3=$baseFolder/dataset/planlist/Planlist3.txt
filePlan4=$baseFolder/dataset/planlist/Planlist4.txt
filePlan5=$baseFolder/dataset/planlist/Planlist5.txt
filePlan6=$baseFolder/dataset/planlist/Planlist6.txt
filePlan7=$baseFolder/dataset/planlist/Planlist7.txt
filePlan8=$baseFolder/dataset/planlist/Planlist8.txt
filePlan9=$baseFolder/dataset/planlist/Planlist9.txt
filePlan10=$baseFolder/dataset/planlist/Planlist10.txt
filePlan11=$baseFolder/dataset/planlist/Planlist11.txt


/usr/bin/sed 's/\*)//g' $filePlan > $filePlan1 && /usr/bin/rm $filePlan
/usr/bin/sed 's/BUY1: /|'$todayDt'|/g' $filePlan1 > $filePlan2 && /usr/bin/rm $filePlan1
/usr/bin/sed 's/BUY2: /|/g' $filePlan2 > $filePlan3 && /usr/bin/rm $filePlan2
/usr/bin/sed 's/TP1: /|/g' $filePlan3 > $filePlan4 && /usr/bin/rm $filePlan3
/usr/bin/sed 's/TP2: /|/g' $filePlan4 > $filePlan5 && /usr/bin/rm $filePlan4
/usr/bin/sed 's/SL: /|/g' $filePlan5 > $filePlan6 && /usr/bin/rm $filePlan5
/usr/bin/sed 's/RISK: /|/g' $filePlan6 > $filePlan7 && /usr/bin/rm $filePlan6
/usr/bin/sed 's/PATTERN: /|/g' $filePlan7 > $filePlan8 && /usr/bin/rm $filePlan7
cat $filePlan8 | /usr/bin/sed ':a; N; $!ba; s/\n/,/g' > $filePlan9  && /usr/bin/rm $filePlan8
/usr/bin/sed -e $'s/,,/\\\n/g' $filePlan9 > $filePlan10 && /usr/bin/rm $filePlan9
/usr/bin/sed 's/,//g' $filePlan10 > $filePlan11 && /usr/bin/rm $filePlan10
