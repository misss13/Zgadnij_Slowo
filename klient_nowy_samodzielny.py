import socket
import time
import sys
from random import choice

"""Inicjacja klienta"""
Lista_slow_do_losowania = [] #zawiera słowa losowane przez użytkowników

if (len(sys.argv)-1) < 3:
    print("python client.py [lok/ser] [login] [haslo]")
ktore = sys.argv[1]
login = sys.argv[2]
haselo = sys.argv[3]
if ktore == "lok":
    IP = '127.0.0.1'
    PORT = 12345
else:
    IP = '136.243.156.120'
    PORT = 12186 

"""Slownik alfabetu"""
alfabet = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e','ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ż', 'ź']



def Zaladuj_slowa():
    """Ładuje 5 lub więcej literowe słowa do tablicy Lista_slow_do_losowania, zabiera ok 200Mb ramu i trwa 4s"""
    global Lista_slow_do_losowania

    print("Rozpoczynam ładowanie słów do tablicy...")
    with open("slowa.txt") as file:
        while (line := file.readline().rstrip()):
            if len(line) >= 5:
                Lista_slow_do_losowania.append(line)
    print("Zakonczono ładowanie słów do tablicy")


def Zgadnij_slowo():
    """Losuje slowo z tablicy Lista_slow_do_losowania"""
    global Lista_slow_do_losowania

    if len(Lista_slow_do_losowania) < 1:
        return "anananas"
    else:
        return choice(Lista_slow_do_losowania)


def Otrzymaj(client):
    """Otrzymuje wiadomosc dekoduje i usuwa znaki konca linii"""
    try:
        response = client.recv(2048)
        response = response.decode()
        response = response.rstrip()
        czy_same_litery = 1 #tak
        for lit in response:
            if lit not in alfabet:
                czy_same_litery = 0
                break
        if len(response) >=2 and (czy_same_litery == 1):
            #otrzymano słowo <-> odczytuje reszte i kończe grę
            print("Slowo zgadnięte: "+response) #slowo
            response = client.recv(2048)
            response = response.decode()
            response = response.rstrip()
            print("Zebranych punktów: "+response) #punkty
            response = client.recv(2048)
            response = response.decode()
            response = response.rstrip()
            print("Kończe połączenie - " + response) #punkty
            client.close()
            return False
        return response
    except:
        #klient chyba się rozłączył dla pewności rozłączam
        Rozlacz_ladnie(client)
        return False

def Rozlacz_ladnie(client):
    """Rozłącz klienta"""
    client.close()


def Zgadnij_literke():
    global alfabet
    """Funckja zwraca literke"""
    return choice(alfabet)

    
def Logowanie(klient):
    """Funkcja loguje klienta na serwer"""
    global login
    global haselo
    
    time.sleep(0.2)
    index = login
    try:    
        klient.send(str.encode(index+"\n"))
    except:
        #klient chyba się rozłączył dla pewności rozłączam
        Rozlacz_ladnie(klient)
        return False
    time.sleep(0.2)
    haslo = haselo
    try:
        klient.send(str.encode(haslo+"\n"))
    except:
        #klient chyba się rozłączył dla pewności rozłączam
        Rozlacz_ladnie(klient)
        return False
    return True


Zaladuj_slowa()
print(Zgadnij_slowo())
print(Zgadnij_literke())


while(True):
    slowa_zgadywane = []
    alfabet_gra = alfabet
    Slowo_odgadniete = []
    Slowo_hint  = []
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    #logowanie
    if Logowanie(client) == False:
        continue


    # Czy zalogowano
    czy_zalogowano = Otrzymaj(client)
    if czy_zalogowano == False:
        continue
    print(czy_zalogowano)
    if(czy_zalogowano == "+1"):
        print("logowanie powiodło się")
    else:
        print("logowanie nie powiodło się - czekam 2s i próbuje się znowu połączyć")
        time.sleep(2)
        Rozlacz_ladnie(client)
        continue

    response = Otrzymaj(client)
    if response == False:
        continue
    print(response)
    
    if response == "?":
        #serwer wyrzucił gracza
        Rozlacz_ladnie(client)
        continue
    else:
        #gracz dostal hint
        Slowo_hint = list(response)
        dlugosc_slowa = len(response)
        slowa_zgadywane = ['_'] * dlugosc_slowa
        print(response)
        print(slowa_zgadywane)
    
 
    #zgadywanie słowa w 10 rundach
    for i in range(10):
        print("Runda: %d" %i)
        literka = ""
        slowko = ""
        print("Podaj literke [+] [enter] [literka]/ slowo [=] [enter] [slowo]: ")
        time.sleep(0.2)
        znak = choice(["+", "-"])
        if znak == "+":
            czy_litera = 1 #literka
            tresc = Zgadnij_literke()
            literka = tresc
            znak = "+"
        else:
            czy_litera = 0 #nie, slowo
            tresc = Zgadnij_slowo()
            slowko = tresc
            znak = "="
        print()
        print("Wysyłam: " + str(znak) + str(tresc)+ "\n")
        time.sleep(0.2)
        try:
            client.send(str.encode(znak + "\n" + tresc+ "\n"))
        except:
            Rozlacz_ladnie(client)
            break

        response = Otrzymaj(client)
        print(response)
        if response == False:
            print("Wystąpił błąd")
            break
        
        if response == "":
            response = Otrzymaj(client)
            if response == False:
                    print("Wystąpił błąd")
                    break
            if response == "":
                #zostalam rozlaczona
                break

        if response[0] == "?":
            #cos zle wyslalam serwerowi
            Rozlacz_ladnie(client)
            break
        elif response[0] == "#":
            print("Zostłaś zignorowana")
            continue
        elif response[0] == "!":
            #zle slowo
            if czy_litera == 0:
                print("Niepoprawne slowo!")

            else:
                #zla literka usuwam z alfabetu a jak już była no to nie usuwam
                if literka in alfabet_gra:
                    alfabet_gra.remove(literka)
                print("Niepoprawna litera!")
                print(alfabet_gra)
            continue

        elif response[0] == '=':
            if czy_litera == 0:
                print("Poprawne slowo!")
                #punkty
                response = Otrzymaj(client)
                if response == False:
                    break
                print("Liczba zdobytych punktów: ", response)

                #znak końca linii
                response = Otrzymaj(client)
                if response == False:
                    break
                print("Koniec gry! - 2s czekam")
                time.sleep(2)
                break
            else:
                print("Poprawna litera!")
                #hint - wysylanie liter
                response = Otrzymaj(client)
                if response == False:
                    break
                #zamiana ciagu na zgadniete literki
                for i in range(dlugosc_slowa):
                    print(response[i])
                    if(response[i] == "1"):
                        slowa_zgadywane[i] = literka
                print(slowa_zgadywane)
                if literka in alfabet_gra:
                    alfabet_gra.remove(literka) #nie powinno być takiej sytuacji ale just in case
                    print("SERWER POPSUTY")
    
                #sprawdzam czy znalazłam wszystkie literki
                czy_koniec = 0
                if "_" in slowa_zgadywane:
                    czy_koniec = 1
                if czy_koniec == 0:
                    #tak
                    print("Poprawne slowo!")
                    #punkty
                    response = Otrzymaj(client)
                    if response == False:
                        break
                    print("Liczba zdobytych punktów: ", response)

                    #znak ? i końca linii
                    response = Otrzymaj(client)
                    print(response)
                    if response == False:
                        break
                    print("Koniec gry! - 2s czekam")
                    time.sleep(1)
                    break
                else:
                    #nie
                    print("Literki niezgadnięte: ")
                    print(alfabet_gra)
                    time.sleep(0.2)
                continue
        else:
            #jakis niezrozumialy ciąg rozłączam
            Rozlacz_ladnie(client)
            break
    client.close()
    del client
    continue
