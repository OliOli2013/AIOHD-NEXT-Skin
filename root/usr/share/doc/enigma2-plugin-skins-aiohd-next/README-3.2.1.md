# AIOHD NEXT 3.2.1

Skin Full HD dla **OpenATV / Enigma2, Python 3**, autor modyfikacji: **Paweł Pawełek**.
Na bazie MetrixHD autorstwa iMaxxx / zespołu OpenATV.

[English](README.en.md) · [Historia zmian](CHANGELOG.md) · [Testy na tunerze](TESTING.md)

## Co oferuje

- Czytelny infobar: picon, nazwa kanału i audycji, opis, postęp, następna audycja, SNR/AGC.
- Lista kanałów z podglądem TV i czterema następnymi audycjami zaznaczonego kanału.
- Duża czcionka domyślnie: 15 wierszy, nazwy 36 px pogrubione; opcja bardzo dużej: 14 wierszy, nazwy 40 px pogrubione.
- Tryb dwuliniowy: 9 lub 8 wierszy. Ustawienie działa lokalnie w obsługiwanej liście klasycznej.
- Mocne zaznaczenie aktywnego kanału, biały tekst i kontrastowy pasek postępu.
- Trzy palety: Aurora, Amber, Violet.
- Pełny opis wydarzenia EPG oraz komunikaty z obsługą długiego tekstu.
- Opcjonalne uruchamianie zainstalowanej wtyczki pogody.

## Instalacja

Pobierz IPK z wydania repozytorium, gdy zostanie opublikowane, i prześlij go do `/tmp` tunera.

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_3.2.1-r0_all.ipk
```

Wybierz **AIOHD** w ustawieniach skina i wykonaj restart GUI z menu tunera.
Nie restartuj interfejsu w trakcie ważnego nagrania.
Zależności pakietu: `enigma2`, `python3-core`, `enigma2-plugin-skins-metrix-atv`.
Nie używaj wymuszania instalacji przy brakujących zależnościach.

## Większa lista i pogoda

Otwórz **Wtyczki → AIOHD NEXT — Style**:

1. Wybierz kolor przewodni oraz czcionkę: **Duża** lub **Bardzo duża**.
2. Opcjonalnie włącz skrót pogody i wybierz wykrytą wtyczkę.
3. Niebieski przycisk otwiera wybraną pogodę; zielony zapisuje ustawienia. Żółty pokazuje wszystkie zarejestrowane wtyczki, jeśli pogodowa ma nietypową nazwę.
4. Zmiana wielkości listy działa po jej ponownym otwarciu. Kolory i dodanie/usunięcie skrótu pogody wymagają restartu GUI.

Pogoda korzysta z już zainstalowanej wtyczki, nie z nowego serwisu pogodowego.
Wykrywane są dostępne do uruchomienia wpisy menu o nazwie/ścieżce zawierającej
`weather`, `pogoda`, `foreca`, `wetter` lub `meteo`. Przykładami są WeatherPlugin,
Foreca i MSNweather, o ile rejestrują standardową funkcję uruchamiania w menu.
Nie każdy wariant tych wtyczek został przetestowany. Własną miejscowość, źródło
danych i ikony ustawia się w wybranej wtyczce. Ta wersja nie dodaje własnych
animowanych ikon ani pogody do infobara. Bez zainstalowanej wtyczki pojawia się
czytelny komunikat; nic nie jest automatycznie pobierane ani instalowane.
Po włączeniu skrót **AIOHD NEXT — Pogoda** jest dostępny w menu rozszerzeń.

## Budowanie i testy

Na Linux Mint/Ubuntu wystarczy Python 3; kompilator dla tunera nie jest potrzebny.

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

Wynik trafia do `dist/`, obok sumy SHA256. Skrypt sprawdza XML, składnię Python
oraz sumy plików. GitHub Actions wykonuje te same polecenia i udostępnia artefakt.

## Struktura

- `root/` — komplet plików instalowanych na tunerze, w tym grafiki, fonty, XML i moduły Python.
- `control/` — metadane i skrypt instalacyjny IPK.
- `build.py` — samodzielne budowanie pakietu.
- `tests/` — testy logiki z atrapami API Enigma2.
- `.github/workflows/build.yml` — automatyczne testowanie i budowanie.
- `GITHUB-START.md` — instrukcja utworzenia i wypełnienia repozytorium.

## Zgodność i zgłoszenia

Nie deklarujemy zgodności ze wszystkimi obrazami Enigma2. Wymagany jest OpenATV,
zgodnie z bazą techniczną i zachowaną informacją licencyjną MetrixHD.
W nowych implementacjach list opartych na innych szablonach może być potrzebne
dodatkowe dopasowanie; liczba wierszy jest sterowana lokalnie dla klasycznej ServiceList.
Testy automatyczne nie zastępują testu na fizycznym tunerze. Nowa wersja 3.2.1
nie była jeszcze uruchomiona na urządzeniu w ramach przygotowania tego pakietu.

W zgłoszeniu podaj model tunera, wersję OpenATV, wersję skina, tryb listy,
wybrany rozmiar czcionki, zdjęcie problemu i log błędu, jeśli wystąpił.
Usuń z logu hasła i dane dostępowe.

Strona autora: https://olioli2013.github.io/aio-iptv-projekt/

## Bootlogo 3.2.1

Pakiet zawiera zaktualizowany plik MPEG Full HD i podgląd PNG. Jeśli AIOHD jest
już aktywnym skinem, instalator aktualizuje także `/usr/share/bootlogo.mvi`,
zachowując wcześniejszy plik jako `/usr/share/bootlogo.mvi.before-aiohd-next`.
Systemowego logo nie zmienia, jeśli aktywny jest inny skin.
