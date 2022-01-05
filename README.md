[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][www.linkedin.com/in/zuzanna-konopek]

# Zgadnij Slowo

## Opis
Gra pisana jako projekt na przedmiot Systemy Operacyjne. Na początku jej pliki znajdowały się w moim repo Systemy Operacyjne. Razem z dość sporą zmianą w treści polecenia postanowiłam, że czas na osobne repozytorium. Zasady dotyczące protokołu zdnajdują się tutaj [Zgadnij słowo - zasady](https://docs.google.com/document/d/1-8pCYH72MZ9gG4ABTg2KkhmAc4gaL6aznOohr4Zht9c). Gra pomimo użycia około 3mil słów nie potrzebuje dużo RAMu ok 100mb, używam mmap do chodzenia po pliku ze słowami.

## Spis treści

## Wymagania do włączenia serwera
 - Python 3.10.1
 - ``bash python serwer_nowy.py [ser/lok]``
### Pliki potrzebne
 - serwer_nowy.py - kod serwera
 - slowa.txt - zestaw słów z których losuje słowo
 - shadow.txt - słownik użytkowników i hashy ich haseł(protokół nie uwzględnia szyfrowania więc hashe będą publiczne)
 - ustawienia.ini - ustawienia serwera(czas trwania gry, czas do nowej gry, itd)
 - punkty.txt - słownik punktów graczy
### Pliki opcjonalne
 - punkty.json - na strone do tabelki
 - kolejka.json - na strone do tabelki
 - 
## Strona
 - stronka.html - aktualnie wyświetlana
 - index.js - używam jsGrid do zarządzania wyświetlaniem tabeli

## TODO
 - [x] Serwer sam wybiera słowo
 - [x] Gry odbywają się asynchronicznie
 - [x] Rundy odbywają się synchronicznie
 - [ ] Szybszy czas rund
 - [ ] Sprawdzanie czy gracz czeka w kolejce <wyrzucanie po ns>
 - [ ] Slownik klientów
 - [ ] Optymalizacja pamięci
 
