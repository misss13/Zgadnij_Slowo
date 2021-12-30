#!/bin/sh

killall screen
cd /home/Balalaika/domains/balalaika.ct8.pl/public_html/
screen -t python-serwer -d -m python serwer_nowy.py ser
echo "ahoj" > status
