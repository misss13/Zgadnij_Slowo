#import json
import hashlib

nazwa = input("Podaj nr indexu: ")
haslo = input("Podaj haslo: ")

haslo = str(hashlib.sha256(haslo.encode()).hexdigest())
Slownik_hasel = {}

#Slownik_hasel = json.load(open("shadow.txt"))
Slownik_hasel[nazwa]=haslo
print(Slownik_hasel)
#json.dump(Slownik_hasel, open("shadow.txt",'w'))

#, "000001": "a7fda0b61e2047f0f1057d1f5f064c272fd5d490961c531f4df64b0dd354683a"