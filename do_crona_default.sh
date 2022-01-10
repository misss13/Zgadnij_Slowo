#!/bin/sh

screen -X -S serwer_nowy quit && echo "[SUCCESS] closed screen" || echo "[ERROR] nothing to close"

killall screen &>/dev/null

cd /home/Balalaika/domains/balalaika.ct8.pl/public_html/
sleep 3
screen -S serwer_nowy -d -m python serwer_nowy.py ser && echo "[ONLINE] serwer_nowy.py" || echo "[ERROR]"
echo "ahoj_default" > status
touch status