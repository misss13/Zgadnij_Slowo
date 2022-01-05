<div id="top"></div>


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL3 License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Zgadnij Slowo</h3>

  <p align="center">
    v2.2.1
    <br />
    <a href="https://github.com/misss13/Zgadnij_Slowo/wiki"><strong>Dla piszących klienta »</strong></a>
    <br />
    <br />
    <a href="https://github.com/misss13/Zgadnij_Slowo/issues">Zgłoś błąd</a>
    ·
    <a href="https://github.com/misss13/Zgadnij_Slowo/issues">Nowy ficzer</a>
  </p>
</div>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/misss13/Zgadnij_Slowo.svg?style=for-the-badge
[contributors-url]: https://github.com/misss13/Zgadnij_Slowo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/misss13/Zgadnij_Slowo.svg?style=for-the-badge
[forks-url]: https://github.com/misss13/Zgadnij_Slowo/network/members
[stars-shield]: https://img.shields.io/github/stars/misss13/Zgadnij_Slowo.svg?style=for-the-badge
[stars-url]: https://github.com/misss13/Zgadnij_Slowo/stargazers
[issues-shield]: https://img.shields.io/github/issues/misss13/Zgadnij_Slowo.svg?style=for-the-badge
[issues-url]: https://github.com/misss13/Zgadnij_Slowo/issues
[license-shield]: https://img.shields.io/github/license/misss13/Zgadnij_Slowo.svg?style=for-the-badge
[license-url]: https://github.com/misss13/Zgadnij_Slowo/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/zuzanna-konopek

## Opis
Gra pisana jako projekt na przedmiot Systemy Operacyjne. Na początku jej pliki znajdowały się w moim repo Systemy Operacyjne. Razem z dość sporą zmianą w treści polecenia postanowiłam, że czas na osobne repozytorium. Zasady dotyczące protokołu zdnajdują się tutaj [Zgadnij słowo - zasady](https://docs.google.com/document/d/1-8pCYH72MZ9gG4ABTg2KkhmAc4gaL6aznOohr4Zht9c). Gra pomimo użycia około 3mil słów nie potrzebuje dużo RAMu ok 100mb, używam mmap do chodzenia po pliku ze słowami.

## Spis treści
* [Wymagania do włączenia serwera](#wymagania-do-włączenia-serwera)
* [Strona](#strona)
* [TODO](#todo)
## Wymagania do włączenia serwera
 - Python 3.10.1
 - ``python serwer_nowy.py [ser/lok]`` gdzie odpowiednio ``ser`` - z moimi danymi serwera ``lok`` na loopbacku
### Pliki potrzebne
 - serwer_nowy.py - kod serwera
 - slowa.txt - zestaw słów z których losuje słowo
 - shadow.txt - słownik użytkowników i hashy ich haseł(protokół nie uwzględnia szyfrowania więc hashe będą publiczne)
 - ustawienia.ini - ustawienia serwera(czas trwania gry, czas do nowej gry, itd)
 - punkty.txt - słownik punktów graczy
### Pliki opcjonalne
 - punkty.json - na strone do tabelki
 - kolejka.json - na strone do tabelki
## Strona
 - stronka.html - aktualnie wyświetlana
 - index.js - używam jsGrid do zarządzania wyświetlaniem tabeli
## TODO
 - [x] Serwer sam wybiera słowo
 - [x] Gry odbywają się asynchronicznie
 - [x] Rundy odbywają się synchronicznie
 - [ ] Opis do odpalenia klienta
 - [ ] Szybszy czas rund
 - [ ] Sprawdzanie czy gracz czeka w kolejce <wyrzucanie po ns>
 - [ ] Slownik klientów
 - [ ] Optymalizacja pamięci
