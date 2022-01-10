import socket
import select
import threading
import hashlib
import time
import json
import re
import os
import random
import configparser
import sys
import gc
import mmap
from typing import List
from _thread import *
from datetime import datetime


Slownik_hasel = {}
"""Hasła trzymane są w shadow.txt w postaci hashy"""
#'123123':'96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e' #haslo 123123
#'000001': 'a7fda0b61e2047f0f1057d1f5f064c272fd5d490961c531f4df64b0dd354683a' #haslo 000001


DO_KONCA_GRY = 100
WSKAZNIK = 0
ILOSC_RUND = 10
MIN_UZYTKOWNIKOW = 2
MAX_UZYTKOWNIKOW = 10
NIESKONCZONOSC_POLACZEN = 100
CZAS_NA_WPROWADZENIE_SLOWA = 2
ILE_MAX_ROZGRYWEK = 2
Ilosc_graczy = 0
Numery_gier = 0
Slownik_nazwa_klient = {} #stałe
Kolejka_graczy = []
Kolejka_zapisu = []
Czas_do_rundy = 30
Slownik_slow = {}
Slownik_punktow = {} #ilosc punktow rundy
Slownik_punktow_plik = {} #z pliku ogólna ilosc punktow
Slownik_gier = {} # id_gry:1 - zgadnieto slowo/ 0-niezgadnieto CZYSCIC!!!!! <-> czyszczone po zapisie
Slownik_logow = {} #id_gry:tresc CZYSIC!!!!! <-> czyszczone po zapisie
Slownik_nazwa_gra = {} #nazwa_uzy:id_gry stałe
Slownik_id_gracze = {} #{id_gry:[nazwa_uzy1, nazwa_uzy2]}
Slownik_barier = {} #{id_gry:bariera_id}
Slownik_nazwa_ilosc_gier = {} #nazwa_uzy:ilosc_rozegranych_gier TODO
Lista_slow_do_losowania = [] #uzywana do przetasowania tablicy nastepnie usuwana <-> RAM friendly


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
    """Tworzy plik z 5 lub więcej literowymi słowami dla mmapa oraz tasuje liste do zapisu 3 razy"""
    global Lista_slow_do_losowania

    print("Rozpoczynam tasowanie słów do tablicy...")
    for i in range(3):
        random.shuffle(Lista_slow_do_losowania)
    print("Potasowanych słów: " + str(len(Lista_slow_do_losowania)))

    print("Zapisuje do pliku...")
    file = open("/home/Balalaika/slowa_mini.txt", "w")
    for slowo in Lista_slow_do_losowania:
        file.write(slowo + "\n")
    file.close()

    print("Usuwam liste słow...")
    del Lista_slow_do_losowania
    gc.collect()


def Losuj_slowo():
    """Losowanie slowa bez uzycia RAM-u"""
    global WSKAZNIK

    with open("/home/Balalaika/slowa_mini.txt", mode="r", encoding="utf-8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            text = mmap_obj.readline()
            for i in range(WSKAZNIK):
                text = mmap_obj.readline()
            WSKAZNIK += 1
            if WSKAZNIK >= 3045268:
                WSKAZNIK%=3045268
            return text.decode().replace("\n", "")


def Czy_zgadnieto_slowo(id_gry):
    """Funkcja sprawdza czy w grze o podanym id zostało zgadnięte słowo. True - zgadnięto; False - nie; (-1) - błąd"""
    global Slownik_gier
    try:
        if Slownik_gier[id_gry] == 1:
            return True
        else:
            return False
    except:
        print("Brak gry o podanym id, albo slownik wybuchł")
        return (-1)


def Prasowanie():
    """Co kilka s aktualizowana jest zawartosc ustawien"""
    global ILOSC_RUND
    global DO_KONCA_GRY
    global CO_ILE_POLACZENIE
    global CZAS_NA_WPROWADZENIE_SLOWA
    global MAX_UZYTKOWNIKOW
    global ILE_MAX_ROZGRYWEK
    global MIN_UZYTKOWNIKOW
    global Slownik_logow
    global Slownik_gier
    global Slownik_punktow
    global Czas_do_rundy


    config = configparser.ConfigParser()
    config.read('ustawienia.ini')
    try:
        ILOSC_RUND = int(config['serwer']['ilosc_rund'])
        Czas_do_rundy = int(config['serwer']['czas_do_rundy'])
        CZAS_NA_WPROWADZENIE_SLOWA = int(config['serwer']['czas_na_slowo'])
        MAX_UZYTKOWNIKOW = int(config['serwer']['max_uzytkownikow'])
        czyszczacz = int(config['serwer']['czyszczacz'])
        uzytkownik = int(config['serwer']['uzytkownik'])
        DO_KONCA_GRY = int(config['serwer']['do_konca_gry'])
        CO_ILE_POLACZENIE = float(config['serwer']['co_ile_polaczenie'])
        ILE_MAX_ROZGRYWEK = int(config['serwer']['ile_max_rozgrywek'])
        MIN_UZYTKOWNIKOW = int(config['serwer']['min_uzytkownikow'])
    except:
        print("Błąd w parsowaniu")
        return False
    if czyszczacz == 1: #czysci pamiec
        print("Wyczyszczono pamiec")
        Slownik_logow.clear()
        Slownik_gier.clear()
        gc.collect()

    if uzytkownik != 0: #usuwanie komus punktow o wielkosc uzytkownik_usuwanie
        try:
            Slownik_punktow[uzytkownik] = 0
        except:
            print("błąd w usuwaniu punktów")


def Zapisz_logi_gry(id_gry):
    """Zapisuje logi danej gry do pliku z logami gier. Zwraca True gdy powiódł się zapis"""
    global Slownik_logow
    tresc = Slownik_logow[id_gry]
    try:
        a = datetime.now().strftime("%d-%m-%Y_%H:%M:%S_")
        sciezka_zapisu = "./logi_gry"
        nazwa_gry = a + str(id_gry) + ".log"
        lokalizacja = os.path.join(sciezka_zapisu, nazwa_gry)
        plik = open(lokalizacja, "w")
        plik.write(tresc)
        plik.close()
        return True
    except:
        print("Błąd przy zapisie - Zapisz_logi_gry")
        return False


def Usun_logi_gry_i_slownik_gier(id_gry):
    """Usuwa logi danej gry ze słownika z logami gier. Zwraca True gdy powiódł się zapis"""
    global Slownik_logow
    global Slownik_gier
    try:
        del Slownik_logow[id_gry]
        del Slownik_gier[id_gry]
        gc.collect()
    except:
        print("Blad usuwania logow gry albo slownika - gra o ponadym id nie istnieje")


def Kolejka_graczy_json():
    """Parsuje kolejke bieżących graczy tak by można było ją zapisać do jsona. True - zapisano/False - nie"""
    global Kolejka_graczy
    do_zapisu = []
    try:
        if Kolejka_graczy == []:
            do_zapisu = [["e m p t y"]]
            json.dump(do_zapisu, open("kolejka.json", 'w'))
        else:
            for gracz in Kolejka_graczy:
                do_zapisu.append([ gracz ]) #zgodnie z kolejnością
            json.dump(do_zapisu, open("kolejka.json", 'w'))
        return True
    except:
        print("Błąd zapoisu - Kolejka_graczy_json")
        return False


"""Słownik na hinty"""
Slownik_hint = { 
    'a':1,
    'ą':1,
    'b':3,
    'c':1,
    'ć':1,
    'd':3,
    'e':1,
    'ę':1,
    'f':4,
    'g':2,
    'h':3,
    'i':1,
    'j':2,
    'k':3,
    'l':3,
    'ł':3,
    'm':1,
    'n':1,
    'ń':1,
    'o':1,
    'ó':1,
    'p':2,
    'q':2,
    'r':1,
    's':1,
    'ś':1,
    't':3,
    'u':1,
    'v':1,
    'w':1,
    'x':1,
    'y':2,
    'z':1,
    'ź':1,
    'ż':1
}


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


def Update_Slownik_hasel():
    global Slownik_hasel
    Slownik_hasel = json.load(open("shadow.txt"))


def Update_ilosc_gier():
    """Wczytuje ilość rozegranych gier graczy do słownika"""
    global Slownik_nazwa_ilosc_gier
    Slownik_nazwa_ilosc_gier = json.load(open("ilosc_gier_graczy.txt"))


def Rozlacz_ladnie(client, nazwa):
    """Rozlaczanie i usuwanie ze slownika uzytkowikow:klientow"""
    """try: TODO
        Slownik_nazwa_klient.pop(nazwa)
    except:
        print("Niematakiego usera"+str(nazwa))"""
    try:
        client.close()
    except:
        print("połączenie zakończono")


def Polacz_ladnie(client, nazwa):
    """Dodawanie bierzacych uzytkowikow do ich listy"""
    global Slownik_nazwa_klient
    Slownik_nazwa_klient[nazwa]=client


def Uwierzytelnienie(polaczenie):
    """Uwierzytelnienie(client) - zajmuje sie logowaniem uzytkownika zwraca +/- do klienta gdzie: '+' True, '-' False """
    #patrze sie czy gracza nie ma w kolejce <=> żeby nie był w jendej rundzie!! moze grac 2 rundy naraz ale różne
    global Kolejka_graczy
    global Slownik_hasel
    global Slownik_nazwa_ilosc_gier
    global ILE_MAX_ROZGRYWEK

    try:
        nazwa_uzy = polaczenie.recv(2048)
        nazwa_uzy = str(nazwa_uzy.decode())
        nazwa_uzy = nazwa_uzy.replace("\0", "\n")
        nazwa_uzy = nazwa_uzy.rstrip()
    except error:
        print("Uwierzytelnienie -nazwa- blad z decode() albo polaczeniem - zakanczam je")
        return False, "none"
    try:
        haslo_uzy = polaczenie.recv(2048)
        haslo_uzy = haslo_uzy.decode()
        haslo_uzy = haslo_uzy.replace("\0", "\n")
        haslo_uzy = haslo_uzy.rstrip()
    except:
        print("Uwierzytelnienie -haslo- blad z decode() albo polaczeniem - zakanczam je")
        return False, nazwa_uzy

    haslo_uzy=str(hashlib.sha256(haslo_uzy.encode()).hexdigest())

    Update_Slownik_hasel()
    #funkcja updejtujaca baze danych urzytkownikow z pliku
    if nazwa_uzy not in Slownik_nazwa_ilosc_gier:
        Slownik_nazwa_ilosc_gier[nazwa_uzy] = 0

    if (nazwa_uzy not in Slownik_hasel) or (Slownik_hasel[nazwa_uzy] != haslo_uzy):
        polaczenie.send(str.encode('-\n'))
        return False, nazwa_uzy
    else:
        if nazwa_uzy in Kolejka_graczy:  #bylo Slownik_nazwa_klient
            """Zeby nie bylo sytuacji ze ktos sie łączy i gra sam ze sobą nabija sb punkty"""
            polaczenie.send(str.encode('-\n'))
            return False, nazwa_uzy
        elif Slownik_nazwa_ilosc_gier[nazwa_uzy] >= ILE_MAX_ROZGRYWEK:
            """Każdy gracz powinien odbyć taką samą liczbę rozgrywek"""
            polaczenie.send(str.encode('-\n'))
            print("Gamon " + str(nazwa_uzy) + " już grał")
            return False, nazwa_uzy
        else:

            Polacz_ladnie(polaczenie, nazwa_uzy)
            polaczenie.send(str.encode('+1\n'))
            return True, nazwa_uzy


def Wprowadz_dane(e, client):
    """Sprawdza wprowadzone słowo od klienta"""
    try:
        p = time.time()
        slowo = client.recv(2048)
        slowo = str(slowo.decode())
        slowo = slowo.lower()
        #print(slowo)
        k = time.time() 
        return str(slowo) +":"+ str(k-p)
    except:
        print("blad przy przesylaniu slowa")
        return str("0:11")


def Obsluga_klienta(client, adres):
    """Obsluga_klienta(client) - nowy watek komunikuje sie z klientem"""
    global Ilosc_graczy
    global Kolejka_graczy
    global Slownik_slow
    global Slownik_punktow
    global Slownik_nazwa_gra
    global Slownik_gier
    global Slownik_logow
    global Slownik_id_gracze
    global Slownik_barier
    global Slownik_nazwa_klient
    global Slownik_nazwa_ilosc_gier
    global ILOSC_RUND

    czy_uwierzytelniony, nazwa_uzy = Uwierzytelnienie(client)
    if (czy_uwierzytelniony == False):
        client.close()
    else:
        Kolejka_graczy.append(nazwa_uzy)
        Ilosc_graczy +=1
        Slownik_slow[nazwa_uzy] = ""

        while(True):
            if(Slownik_slow[nazwa_uzy] != ""):
                break
            time.sleep(2)
        
        #zwiekszam ilosc rozegranych gier
        if nazwa_uzy not in Slownik_nazwa_ilosc_gier:
            Slownik_nazwa_ilosc_gier[nazwa_uzy] = 1
        else:
            Slownik_nazwa_ilosc_gier[nazwa_uzy] += 1
        
        #id_gry do ktorej nalezy klient
        id_gry = Slownik_nazwa_gra[nazwa_uzy]
        Slownik_punktow[id_gry][nazwa_uzy] = 0 

        #tego uzywam do zliczania punktow ze slowa
        slowo = Slownik_slow[nazwa_uzy]
        nie_odgadniete_literki = slowo

        #10 rund
        for runda in range(ILOSC_RUND):
            #zgadnieto slowo w poprzedniej rundzie
            if Czy_zgadnieto_slowo(id_gry) == 1:
                print("tak w poprzedniej rundzie")
                try:
                    client.send(str.encode(str(Slownik_slow[nazwa_uzy]) + "\n"))
                    client.send(str.encode(str(Slownik_punktow[id_gry][nazwa_uzy]) + "\n"))
                    client.send(str.encode("?\n"))
                except:
                    print("błąd - nie można wysłać - punlktow - klient rozłączony: " + str(nazwa_uzy))
                #time.sleep(2) #czekam az Gra() wysle slowo/npunkty/n?
                break

            e = threading.Event()
            t = ThreadWithReturnValue(target=Wprowadz_dane, args=(e,client))
            t.start()
            parse = t.join(10)
            if parse != None:
                #ktos wyslal stringa z wiecej niz jednym znakiem :
                if parse.count(":") > 1:
                    print("Jakis gamoń mi to chce popsuć - rozłączam")
                    try:
                        Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        Update_barier(id_gry)
                        return False
                    except:
                        print("błąd w obsłudze klienta - rozlacz ladnie")
                    return False
                parse = parse.replace("\0", "\n")
                parse = parse.replace("\n","")
                parse = parse.rstrip()
                parse = parse.split(":")
                wprowadzone_dane, czas = parse[0], parse[1]
            if t.is_alive():
                #jeszcze nie skonczono wpisywania <-> kończe wątek i wyrzucam gracza
                e.set()
                Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " rozłączam minęło 10s\n"
                try:
                    #rozlaczam po 10s 
                    Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                    Rozlacz_ladnie(client, nazwa_uzy)
                    Update_barier(id_gry)
                    return False
                except:
                    Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ "błąd - klient rozłączony\n"
                    print("błąd w obsłudze klienta - rozlacz ladnie - rozłączony albo słownik wybuchł")
                    return False
            else:
                #skonczono wpisywanie
                if Wprowadz_dane == "0" and czas == "11":
                    #nastąpił błąd w funkcji wprowadzania <-> rozłączam
                    Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " błąd w funkcji wprowadź dane - rozłączam" +"\n"
                    print("blad w funkcji Wprowadz_dane")
                    try:
                        Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        Update_barier(id_gry)
                        return False
                    except:
                        print("błąd w obsłudze klienta - rozlacz ladnie - Wprowadz dane - rozłączony albo słownik wybuchł")
                        return False

                if float(czas) > float(CZAS_NA_WPROWADZENIE_SLOWA):
                    #odpowiedz po 2s
                    Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " odpowiedź po: "+ str("{:.2f}".format(float(czas))) +"s ignoruję gracza"+"\n"
                    try:
                        client.send(str.encode("#\n"))
                        #continue
                    except:
                        #klient rozłączony <-> rozłączam go ładnie
                        Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        try:
                            Update_barier(id_gry)
                        except:
                            print("Odpowiedz po 2s i błąd bariery przy rozłączaniu")
                        return False

                if (len(wprowadzone_dane)>=1) and ("=" == wprowadzone_dane[0]):
                    #zgadywanie slowa
                    if slowo == wprowadzone_dane[1:]:
                        try:
                            client.send(str.encode("=\n"))
                            Slownik_punktow[id_gry][nazwa_uzy] += 5
                            client.send(str.encode(str(Slownik_punktow[id_gry][nazwa_uzy])+"\n"))
                            client.send(str.encode("?\n"))
                            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " zgadł słowo - dostaje 5 punktów" +"\n"
                            bariera = Slownik_barier[id_gry] #synchronizacja klientów po rundzie
                            try:
                                bariera.wait()
                                Slownik_gier[id_gry] = 1 #zgadnięto słowo 
                            except:
                                print("Błąd z synchronizacją u zwycięzcy")
                            Slownik_gier[id_gry] = 1
                            try:
                                Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                                Update_barier(id_gry)
                            except:
                                print("Boze ile bledow")
                            return True
                        except:
                            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ "błąd - klient rozłączony\n"
                            print("Jakis blad przy zgadywaniu slowa")
                            try:
                                Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                                Update_barier(id_gry)
                            except:
                                print("Boze ile bledow")
                            return False
                    else:
                        #niepoprawne słowo
                        Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " nie zgadł słowa, wprowadził: "+ str(wprowadzone_dane[1:]) +"\n"
                        try:
                            client.send(str.encode("!\n"))
                            #continue
                        except:
                            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ "błąd - klient rozłączony\n"
                            print("Jakis blad przy zgadywaniu slowa - klient prawdopodobnie rozlaczony")
                            try:
                                Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                                Update_barier(id_gry)
                            except:
                                print("Boze ile bledow")
                            return False

                elif (len(wprowadzone_dane)>=2) and ("+" == wprowadzone_dane[0]):
                    #zgadywanie litery
                    literka = wprowadzone_dane[1]
                    if literka in nie_odgadniete_literki:
                        try:
                            slowo_tymczasowe = slowo #je wysle uzytkownikowi
                            client.send(str.encode("=\n"))
                            licznik_punktow = nie_odgadniete_literki.count(literka)
                            Slownik_punktow[id_gry][nazwa_uzy] += licznik_punktow
                            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " odgadł literkę: "+ literka+" dostał punktów: "+str(licznik_punktow)+"\n"
                            #wyrzucam wszystkie zgadniete literki
                            nie_odgadniete_literki = nie_odgadniete_literki.replace(literka, "")
                            #zamiana na 0/1 ciąg 1-zgadnieta literka reszte rzeczy wyrzucam ze stringa
                            slowo_tymczasowe = slowo_tymczasowe.replace(literka, "1")
                            slowo_tymczasowe = re.sub(re.compile("[a-z2-9ęóąśłżźćń]"), '0', slowo_tymczasowe)
                            #jak klient wysle jakis syf (np.: +_=-!@$@$#%^$%)to jego problem
                            client.send(str.encode(str(slowo_tymczasowe)+"\n"))
                            #continue
                        except:
                            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ "błąd - klient rozłączony\n"
                            print("Klient rozlaczony albo cos nei tak z moim regexem")
                            try:
                                Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                                Update_barier(id_gry)
                            except:
                                print("Boze ile bledow w literkach")
                            return False
                    else:
                        Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " wybrał literkę: "+ literka+ " nie dostał punktów\n"
                        #brak takiej literki (znaku/cyfry) jak ktos cos nieladnego wpisal w slowie
                        try:
                            client.send(str.encode("!\n"))
                            #continue
                        except:
                            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ "błąd - klient rozłączony\n"
                            print("Jakis blad przy zgadywaniu slowa - klient prawdopodobnie rozlaczony")
                            try:
                                Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                                Update_barier(id_gry)
                            except:
                                print("Boze ile bledow - brak literki znaku cyfry")
                            return False

                else:
                    #niespodziewana odpowiedz
                    Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gracz: " +str(nazwa_uzy)+ " wprowadził niespodziewaną odpowiedź - rozłączam:"+ str(wprowadzone_dane)+"\n"
                    try:
                        client.send(str.encode("?\n"))
                        Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        Update_barier(id_gry)
                        return False
                    except:
                        try:
                            Slownik_id_gracze[id_gry].remove(nazwa_uzy)
                            Rozlacz_ladnie(client, nazwa_uzy)
                            Update_barier(id_gry)
                        except:
                            print("Boze ile bledow nie moge wyslac ?")
                        print("wprowadzono niezrozumianą sekwencje - dodatkowo błąd z wysyłaniem ?")
                        return False
            #print(Slownik_barier[id_gry])
            bariera = Slownik_barier[id_gry] #synchronizacja klientów po rundzie
            try:
                bariera.wait()
            except:
                print("Błąd z synchronizacją klienta - nieaktualna bariera użyta :<")
            time.sleep(0.2)
        #koniec rundy
        #Koniec obsługi <-> koniec połączenia klienta wracam do Gry
        Rozlacz_ladnie(client, nazwa_uzy)
        Slownik_id_gracze[id_gry].remove(nazwa_uzy)
        return True


def Wez_slownik_punkty():
    """Bierze aktualne wyniki z pliku"""
    global Slownik_punktow_plik
    Slownik_punktow_plik = json.load(open("punkty.txt"))


def Zapisz_slownik_nazwa_ilosc_gier():
    """Zapisuje akualną ilość gier do pliku"""
    global Slownik_nazwa_ilosc_gier
    do_zapisu = []
    try:
        json.dump(Slownik_nazwa_ilosc_gier, open("ilosc_gier_graczy.txt", 'w'))
        for nazwa_uzy in Slownik_nazwa_ilosc_gier:
            do_zapisu.append([ nazwa_uzy, Slownik_nazwa_ilosc_gier[nazwa_uzy] ])
        json.dump(do_zapisu, open("ilosc_gier_graczy.json", 'w'))
    except:
        print("Błąd w zapisie punktów, slownik się posypoał")


def Zapis_slownika_punkty():
    """Zapisuje aktualne wyniki do plików, punkty.txt oraz punkty.json"""
    global Slownik_punktow_plik
    do_zapisu = []
    try:
        json.dump(Slownik_punktow_plik, open("punkty.txt", 'w'))
        for nazwa_uzy in Slownik_punktow_plik:
            do_zapisu.append([ nazwa_uzy, Slownik_punktow_plik[nazwa_uzy] ])
        json.dump(do_zapisu, open("punkty.json", 'w'))
    except:
        print("Błąd w zapisie punktów, slownik się posypoał")


def Czasomierz():
    """Oblicza czas między rundami oraz sprawdza ilosc graczy w kolejce - jeśli 10 rozpoczyna gre albo czas"""
    global Ilosc_graczy
    global Kolejka_graczy
    global Czas_do_rundy
    global Kolejka_zapisu
    global Slownik_nazwa_klient
    global MAX_UZYTKOWNIKOW
    global MIN_UZYTKOWNIKOW

    Wez_slownik_punkty()
    Update_ilosc_gier()
    print("|#####################|")
    i=0
    ile_razy_kratka = 1
    trwanie_do_rundy = round(Czas_do_rundy / 2)
    animacja = round(Czas_do_rundy/30)
  
    while True:
        Prasowanie()
        #wyrzucanie gracza z kolejki
        for pedent in Kolejka_graczy:
            klient = Slownik_nazwa_klient[pedent]
            rs, _, _ = select.select([klient], [], [], 0.01)
            if len(rs) != 0:
                Ilosc_graczy -= 1
                Kolejka_graczy.remove(pedent)
                Rozlacz_ladnie(klient, pedent)

        trwanie_do_rundy = round(Czas_do_rundy / 2)
        animacja = round(Czas_do_rundy/30)
        #rysowanie pasku ładowania do kolejnej gry (jesli zbierze sie odp ilosc graczy)
        if i%animacja == 0:
            print("|" + "#"*ile_razy_kratka + (16-ile_razy_kratka)*" " + "|" + str(Ilosc_graczy))
            print(Kolejka_graczy)
            ile_razy_kratka += 1

        if (Ilosc_graczy >= MAX_UZYTKOWNIKOW) or (i>=trwanie_do_rundy):
            i=0
            ile_razy_kratka=1
            if(Ilosc_graczy <= MIN_UZYTKOWNIKOW-1):
                continue
            print("Nowa runda")
            Bierzaca_gra_gracze = []
            liczba_graczy = min(Ilosc_graczy, MAX_UZYTKOWNIKOW)
            for j in range(liczba_graczy):
                gracz = Kolejka_graczy.pop(0)
                Bierzaca_gra_gracze.append(gracz)
            Ilosc_graczy -= liczba_graczy
            time.sleep(0.5) #GRY BEDĄ DZIAŁAŁY ASYNCHRONICZNIE ALE ZEBY NIE BYŁO PROBLEMU Z R/W DO PLIKU
            gra_watek = threading.Thread(target=Gra, args=(Bierzaca_gra_gracze, liczba_graczy), daemon=True) #funkcja zarządzająca barierami
            gra_watek.start()
        time.sleep(2)
        i += 1
        Kolejka_graczy_json() #tylko ta funkcja zarządza kolejką klientów

        #sprawdza czy jest cos do zapisu <-> zapis wszystkiego naraz żeby nie uszkodzic plików <-> zapis w tym samym czasie z dwóch wątków
        if len(Kolejka_zapisu) >= 1:
            Zapis_slownika_punkty()
            Zapisz_slownik_nazwa_ilosc_gier()
            Kolejka_zapisu = []


def Przetlumacz_na_hinta(slowo: str):
    """Zamienia słowo na postać cyfrową tak jak podano w poleceniu z urzyciem słownika"""
    hint = ""
    for i in slowo:
        hint += str(Slownik_hint[i])
    return hint

def Broadcast_hinta(tablica_klientow, hint: str):
    """Wysyłanie do wszystkich wiadomości z hasłem"""
    for klient in tablica_klientow:
        try:
            klient.send(str.encode(hint + "\n")) #niewiem czy ma byc koniec linii 
        except:
            print("błąd - Broadcast_hinta")
            continue


def Update_barier(id_gry):
    """Funkcja zajmująca się odświeżaniem barier dla każdej gry o zadanym id"""
    global Slownik_id_gracze
    global Slownik_barier

    if len(Slownik_id_gracze[id_gry]) > 0:
        try:
            Slownik_barier[id_gry] = threading.Barrier(len(Slownik_id_gracze[id_gry]), timeout=3)
        except:
            print("błąd - Update_barier - coś nie tak")
            return False
    return True


def Gra(Bierzaca_gra_gracze, Ilosc_w_grze):
    """dostaje liste 10-2 graczy z kolejki odsługuje wszystkich naraz a później się wyłącza"""
    global Slownik_slow
    global Slownik_punktow
    global Slownik_punktow_plik
    global Slownik_nazwa_klient
    global Numery_gier
    global Slownik_gier
    global Kolejka_zapisu
    global Slownik_logow
    global Slownik_nazwa_gra
    global Slownik_id_gracze
    global Slownik_barier
    global DO_KONCA_GRY

    #id_gry
    id_gry = Numery_gier
    Numery_gier+=1
    Slownik_punktow[id_gry] = {}
    Slownik_id_gracze[id_gry] = []

    Slownik_gier[id_gry] = 0 
    Slownik_logow[id_gry] = "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Zaczęto grę o id: " + str(id_gry) +"\n"

    #DEBUG_ZONE
    #print(Bierzaca_gra_gracze)
    #print(Slownik_id_gracze)
    #print(Slownik_logow)
    #print(Slownik_nazwa_klient)

    #klienci_gry
    tablica_klientow = []
    for i in range(Ilosc_w_grze):
        try:
            tablica_klientow.append(Slownik_nazwa_klient[Bierzaca_gra_gracze[i]])
            Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Dodano gracza: " + str(Bierzaca_gra_gracze[i]) +"\n"
            Slownik_id_gracze[id_gry].append(Bierzaca_gra_gracze[i])
        except:
            print("Nie udało się dodać gracza nr: " + str(i))

    #Wybranie Słowa
    slowo = Losuj_slowo()
    print("Wybrano słowo: " + slowo)
    Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Wybrano słowo: "+ slowo +"\n"
    hint = Przetlumacz_na_hinta(slowo)
    Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " +"Przetłumaczone słowo: "+ hint +"\n"
    Broadcast_hinta(tablica_klientow, hint)
    print("Wysłano hint: " + hint)

    #wysyłam klientom slowa gdy beda nie puste rozpocznie sie runda oraz id_gry do zbierania logów
    for nazwa_uzy in Bierzaca_gra_gracze:
        Slownik_slow[nazwa_uzy] = slowo
        Slownik_nazwa_gra[nazwa_uzy] = id_gry

    Slownik_barier[id_gry] = threading.Barrier(len(Slownik_id_gracze[id_gry]), timeout=10) #bo po 10s ma klienta rozłączać
 
    #obsluga 10 rund po stronie klienta
    do_konca = 0
    DO_KONCA_GRY_PRZEZ_2 = round(DO_KONCA_GRY/2)
    while True:
        if do_konca >= DO_KONCA_GRY_PRZEZ_2:
            break
        if len(Slownik_id_gracze[id_gry]) == 0:
            time.sleep(3) #na spokojnie żeby wszystkie wątki się skończyły
            break
        if Czy_zgadnieto_slowo(id_gry) == (-1):
            #błąd slownika
            print("Błąd słownika - Gra")
            break
        print(Slownik_id_gracze[id_gry], end =" ")
        print(id_gry)
        do_konca+=1    
        time.sleep(2)

    print("Koniec gry")
    for nazwa_uzy in Slownik_punktow[id_gry]:
        Slownik_logow[id_gry] += "["+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "] " + "Gra dla "+str(nazwa_uzy)+" zakończona wynikiem: " + str(Slownik_punktow[id_gry][nazwa_uzy]) +"\n"

    Zapisz_logi_gry(id_gry)
    Usun_logi_gry_i_slownik_gier(id_gry) #mniej użycia ramu

    for nazwa_uzy in Bierzaca_gra_gracze: #jeden gracz w jednej grze po jej zakonczeniui tak musi czekac w kolejce 2s
        if nazwa_uzy not in Slownik_punktow_plik:
            Slownik_punktow_plik[nazwa_uzy] = 0
        try:
            Slownik_punktow_plik[nazwa_uzy] += Slownik_punktow[id_gry][nazwa_uzy]
        except:
            print("brak uzytkownika: " + str(nazwa_uzy) + "w slowniku punktow - pomijam")
            continue
    print("id_gry" + str(id_gry))
    print(Slownik_punktow_plik)
    print(Slownik_punktow[id_gry])

    for nazwa_uzy in Bierzaca_gra_gracze: # RAM friendly
        try:
            del Slownik_punktow[id_gry][nazwa_uzy]
        except:
            print("brak uzytkownika: " + str(nazwa_uzy) + "w slowniku punktow - pomijam")
            continue
    del Slownik_punktow[id_gry]
    del Slownik_id_gracze[id_gry]
    del Slownik_barier[id_gry]
    #nawet jesli uzytkownik sie rozłączy punkty zostaną dodane
    #aktualizacja slownika dla kazdego gracza w grze <-> dodaje do kolejki zapisu
    Kolejka_zapisu.append(id_gry)
    #zapis w funkcji Czasomierz()


if __name__=="__main__":
    if (len(sys.argv)-1) < 1:
        print("python serwer_nowy.py [lok/ser]")
        quit()
    ktore = sys.argv[1]
    if ktore == "lok":
        print("Serwer działa na loopbacku")
        host = '127.0.0.1'
        port = 12345 
    else:
        print("Serwer działa na stronce")
        host = '136.243.156.120'
        port = 12186
    ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    ServerSocket.listen(NIESKONCZONOSC_POLACZEN)

    print("Serwer up")
    Zaladuj_slowa()
    Zapisz_slowa_mini()
    czasomierz_watek = threading.Thread(target=Czasomierz, args=(), daemon=True)
    czasomierz_watek.start()
    while True:
        client, adres = ServerSocket.accept()
        print (adres[0] + " połączony")
        klient_wontek = threading.Thread(target=Obsluga_klienta, args=(client, adres), daemon=True)
        klient_wontek.start()
        time.sleep(0.05)
client.close()
ServerSocket.close() 