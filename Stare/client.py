import socket
import time
from random import randrange

"""IP = '127.0.0.1' #'136.243.156.120' #IP SERWERA
PORT = 12345 #12186 #PORT
"""

IP = '136.243.156.120' #IP SERWERA '127.0.0.1' #'
PORT = 12186 #PORT 12345 #

"""Slownik alfabetu"""
alfabet = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e','ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ż', 'ź']

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
	time.sleep(2)
	client.close()

def Zgadnij_slowo():
	"""Funkcja zwraca dowolne słowo"""
	file = open('slowa.txt', 'r')
	a = randrange(200)
	i=0
	lines = file.readlines()
	for i, slowo in enumerate(lines):
		if i == a:
			return slowo.rstrip()
		i+=1
	file.close()

def Zgadnij_literke():
	global alfabet
	"""Funckja zwraca literke"""
	a = randrange(35)
	return alfabet[a]

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
	index = input("Podaj nr indexu: ")
	try:	
		client.send(str.encode(index+"\n"))
	except:
		#klient chyba się rozłączył dla pewności rozłączam
		Rozlacz_ladnie(client)
		continue
	
	haslo = input("Podaj hasło: ")
	try:
		client.send(str.encode(haslo+"\n"))
	except:
		#klient chyba się rozłączył dla pewności rozłączam
		Rozlacz_ladnie(client)
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
		Rozlacz_ladnie(client)
		continue

	response = Otrzymaj(client)
	if response == False:
		continue
	print(response)
	
	if response == "@":
		#Jeśli gracz będzie wybierał słowo
		slowo_do_wisielca = input("Podaj słowo które pozostali muszą zgadnąć: ")
		try:
			client.send(str.encode(slowo_do_wisielca + "\n"))
			response = Otrzymaj(client)
			print(response)
		except:
			Rozlacz_ladnie(client)
		print("Wybrano slowo zamykam klienta - 2s spania")
		time.sleep(2)
		continue
	else:
		if response == "?":
			#gracza wyrzucilo
			Rozlacz_ladnie(client)
			continue
		else:
			#gracz dostal hint
			Slowo_hint = list(response)
			dlugosc_slowa = len(response)
			slowa_zgadywane = ['_'] * dlugosc_slowa
			print(response)
			print(slowa_zgadywane)
	
#TODO
	#zgadywanie słowa w 10 rundach
	for i in range(10):
		print("Runda: %d" %i)
		literka = ""
		slowko = ""
		znak = input("Podaj literke [+] [enter] [literka]/ slowo [=] [enter] [slowo]: ")
		tresc = input()
		if znak[0] == "+": 
			czy_litera = 1 #literka
			literka = tresc
		else:
			czy_litera = 0 #nie, slowo
			slowko = tresc

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
				#zla literka
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
				for i in range(len(alfabet_gra)):
					if alfabet_gra[i] == literka:
						alfabet_gra.pop(i)
						break
				czy_koniec = 0 
				for i in range(dlugosc_slowa):
					if slowa_zgadywane[i] == "_":
						czy_koniec = 1
						break
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
					if response == False:
						break
					print("Koniec gry! - 2s czekam")
					time.sleep(2)
					break
				else:
					#nie
					print("Literki niezgadnięte: ")
					print(alfabet_gra)
				continue
		else:
			#jakis niezrozumialy ciąg rozłączam
			Rozlacz_ladnie(client)
			break

	continue
	client.close()
