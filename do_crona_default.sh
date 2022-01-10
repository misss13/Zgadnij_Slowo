#!/bin/sh

screen -X -S serwer_nowy quit && echo "[SUCCESS] closed screen" || echo "[ERROR] can't close"

killall screen
kill `ps aux | grep serwer_nowy_dzialajacy.py | cut -d" " -f2 | head -n 1`  &>/dev/null || echo "[DOWN] serwer_nowy_default.py"
kill `ps aux | grep serwer_nowy.py | cut -d" " -f2 | head -n 1` &>/dev/null || echo "[DOWN] serwer_nowy.py"

cd /home/Balalaika/domains/balalaika.ct8.pl/public_html/
screen -dmS serwer_nowy python serwer_nowy.py lok && echo "[ONLINE] serwer_nowy.py" || echo "[ERROR]"
echo "ahoj_default" > status
touch status