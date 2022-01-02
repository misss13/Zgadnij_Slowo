#!/bin/sh

killall screen
kill `ps aux | grep serwer_nowy_dzialajacy.py | cut -d" " -f2 | head -n 1` || echo "[DOWN] serwer_nowy.py"
kill `ps aux | grep serwer_nowy.py | cut -d" " -f2 | head -n 1` || echo "[DOWN] serwer_nowy.py"
cd /home/Balalaika/domains/balalaika.ct8.pl/public_html/
screen -t python-serwer -d -m python serwer_nowy.py ser
echo "ahoj_default" > status
touch status