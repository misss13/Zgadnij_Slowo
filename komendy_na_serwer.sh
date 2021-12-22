#!/bin/sh

cd /home/Balalaika/Zgadnij_Slowo
git pull
cp slowa.txt /home/Balalaika/domains/balalaika.ct8.pl/public_html
cp serwer_nowy.py /home/Balalaika/domains/balalaika.ct8.pl/public_html
cp shadow.txt /home/Balalaika/domains/balalaika.ct8.pl/public_html
cp ustawienia.ini /home/Balalaika/domains/balalaika.ct8.pl/public_html
cp punkty.txt /home/Balalaika/domains/balalaika.ct8.pl/public_html
cd /home/Balalaika/domains/balalaika.ct8.pl/public_html
screen