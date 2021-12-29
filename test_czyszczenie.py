"""import gc
import time
import json

Slownik_hasel = {"toqqqqqqqqqqqqqk":"10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1", "tokqqw":"10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1", "tossssssk":"10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1", "tosk":"10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1", "tok":"10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1", "kok":"10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1","407045": "10f0c23f1cb5e366035081f153a1bd2704ecc50548c870e8b010adc484011dd1", "406593": "463d4d7cb31ca0b1ab31f99c513454ed213dd91c6d571223fbf00c86439d2216", "123123": "96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e", "000001": "a7fda0b61e2047f0f1057d1f5f064c272fd5d490961c531f4df64b0dd354683a", "1": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", "2": "d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35", "3": "4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce", "4": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a", "5": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d", "6": "e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683", "7": "7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451", "8": "2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3", "9": "19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7"}

def Update_Slownik_hasel():
    global Slownik_hasel
    Slownik_hasel = json.load(open("shadow.txt"))

def Clearr():
    global Slownik_hasel
    Slownik_hasel.clear()

def Czyszczacz():
    del globals()['Slownik_hasel']
    gc.collect()
    global Slownik_hasel
    Slownik_hasel = {}

if __name__=="__main__":
    print(Slownik_hasel)
    print("Test pamieci - czekam 10s")
    print(Slownik_hasel)
    time.sleep(10)
    
    print("Uwalaniam pamiec slownika")
    Clearr()
    time.sleep(10)
    print("Done")

    print("Uwalaniam pamiec slownika")
    Czyszczacz()
    print(Slownik_hasel)
    print("Czekam 10s")
    time.sleep(10)

    print("Nowa zawartosc")
    Update_Slownik_hasel()
    print(Slownik_hasel)
    time.sleep(10)
"""
########################### slownik w slowniku {id_gry:{nazwa_urzy:punkty}}
"""Slownik_punktow = {}
id_gry = 1
id_gry2 = 2

Slownik_punktow[id_gry] = {}
Slownik_punktow[id_gry2] = {}

#gra 1
Slownik_punktow[id_gry]["123"] = 0
Slownik_punktow[id_gry]["123"] += 1
Slownik_punktow[id_gry]["1234"] = 0
Slownik_punktow[id_gry]["1234"] += 1

#gra 2
Slownik_punktow[id_gry2]["123"] = 2

print(Slownik_punktow[id_gry])
print(Slownik_punktow)
del Slownik_punktow[id_gry]["123"]
print(Slownik_punktow)
"""
######################### testowanie funkcji losujacej
import mmap
import time
import random
import gc

Lista_slow_do_losowania = []
WSKAZNIK = 0

def Zaladuj_slowa():
    """Ładuje 5 lub więcej literowe słowa do tablicy Lista_slow_do_losowania, zabiera ok 200Mb ramu i trwa 4s"""
    global Lista_slow_do_losowania

    print("Rozpoczynam ładowanie słów do tablicy...")
    with open("slowa.txt") as file:
        while (line := file.readline().rstrip()):
            if len(line) >= 5:
                Lista_slow_do_losowania.append(line)
    print("Zakonczono ładowanie słów do tablicy")


def Zapisz_slowa_mini():
    """Tworzy plik z 5 lub więcej literowymi słowami dla mmapa oraz losuje słowa 3 razy"""
    global Lista_slow_do_losowania

    print("Rozpoczynam tasowanie słów do tablicy...")
    for i in range(3):
        random.shuffle(Lista_slow_do_losowania)
    print("Potasowanych słów: " + str(len(Lista_slow_do_losowania)))

    print("Zapisuje do pliku...")
    file = open("slowa_mini.txt", "w")
    for slowo in Lista_slow_do_losowania:
        file.write(slowo + "\n")
    file.close()
    
    print("Usuwam liste słow...")
    del Lista_slow_do_losowania
    gc.collect()


def Losuj_slowo():
    """Losowanie slowa bez uzycia RAM-u"""
    global WSKAZNIK

    with open("slowa_mini.txt", mode="r", encoding="utf-8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            text = mmap_obj.readline()
            for i in range(WSKAZNIK):
                text = mmap_obj.readline()
            WSKAZNIK += 1
            if WSKAZNIK >= 3045268:
                WSKAZNIK%=3045268
            print(text.decode().replace("\n", ""))
            return text.decode().replace("\n", "")

Zaladuj_slowa()
Zapisz_slowa_mini()
Losuj_slowo()
print("czekam 10s")
time.sleep(10)
Losuj_slowo()