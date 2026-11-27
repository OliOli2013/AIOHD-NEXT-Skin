# AIOHD NEXT 4.0 — Live Grid

**Wersja testowa 4.0.0-r0** · Full HD 1920×1080 · OpenATV / Python 3

Autor modyfikacji: Paweł Pawełek. Baza: MetrixHD autorstwa iMaxxx / zespołu OpenATV. Zachowano oryginalną licencję i informacje o autorach.

[English](README.en.md) · [Historia zmian](CHANGELOG.md) · [Testy](TESTING.md) · [Wydanie](RELEASE-4.0.0.md)

## Live Grid

- Nowy InfoBar: wszystkie moduły w dolnej strefie, bieżąca/następna audycja, opis, pasek i procent EPG, sygnał DVB oraz pogoda.
- Lista kanałów: panel podglądu 528×297, cztery kolejne audycje z rozdzielonymi kolumnami czasu i tytułu, trzy rozmiary listy (18/15/14 wierszy, 10/9/8 w trybie dwuliniowym).
- SecondInfoBar: pełny przewijany opis i osobna oś kolejnych audycji.
- Główne menu oraz EPG: nawigacja po lewej, kontekst po prawej. Odświeżone okna informacji o wydarzeniach, odtwarzacza i głośności.
- Live Center w menu rozszerzeń: bieżący kanał i EPG, dane DVB (jeśli dostępne), wykorzystanie RAM, miejsce w głównym systemie plików i aktywne nagrania. Lokalny odczyt co 5 sekund podczas wyświetlania okna.
- Dziewięć akcentów: Aurora, Amber, Violet, Petrol, Copper, Jade, Sakura, Ice, Lime. Trzy tryby powierzchni: Studio, OLED Black, Cinema Glass (przezroczysty dock TV).
- Pogoda: Auto korzysta najpierw z Weather Plugin, następnie z OpenATV / MetrixWeather. Launcher pełnego ekranu jest niezależny.
- Aktualizacje: wyłącznie oficjalne GitHub Releases, TLS z weryfikacją certyfikatów i SHA-256, jeśli GitHub zwraca digest zasobu. Instalacja wyłącznie za zgodą użytkownika.

## Instalacja i ustawienia

Najpierw wykonaj kopię ustawień, nie instaluj podczas nagrania. Przenieś IPK do `/tmp` odbiornika i wykonaj:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_4.0.0-r0_all.ipk
```

Wybierz AIOHD w selektorze skina. Restart GUI wykonaj ręcznie. Wtyczki → AIOHD NEXT — Style pozwala zmieniać paletę, tryb powierzchni, wielkość listy i pogodę. Zmiana stylu wymaga restartu GUI. Pakiet nie podmienia systemowego bootlogo.

Zależności: `enigma2`, `enigma2-plugin-skins-metrix-atv`, `python3-core`. Pozostałe odziedziczone ekrany mogą wymagać odpowiednich wtyczek. Projekt przeznaczony dla OpenATV zgodnie z licencją bazy. Nie deklarujemy potwierdzonej zgodności z innymi image ani z wszystkimi wydaniami OpenATV.

## Budowanie

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

Wyniki: `dist/`. Testy statyczne nie zastępują fizycznego testu odbiornika. Wydanie testowe, nie oznaczać jako stabilne przed weryfikacją.
