# AIOHD NEXT 3.2.1

Nowoczesny skin Full HD dla **OpenATV / Enigma2 (Python 3)**.
Modyfikacje AIOHD NEXT: **Paweł Pawełek**. Baza: MetrixHD autorstwa iMaxxx / zespołu OpenATV.

[English](README.en.md) · [Historia zmian](CHANGELOG.md) · [Testy](TESTING.md)

## Najważniejsze funkcje

- Czytelna lista kanałów z trzema rozmiarami: **Standard 32 px / 18 kanałów**, **Duża 38 px / 15 kanałów** i **Bardzo duża 42 px / 14 kanałów**, z mocnym zaznaczeniem aktywnej pozycji.
- Prawy panel listy: mniejszy podgląd TV **544×306 (16:9)**, nazwa kanału, bieżąca audycja, czas, postęp, wielowierszowy opis EPG oraz **4 następne audycje**.
- Długi opis EPG przewija się pionowo tylko wtedy, gdy nie mieści się w polu.
- Kompaktowy InfoBar o wysokości **240 px**: kanał, tytuł, opis bieżącej audycji, postęp, czas i następna audycja. W `r4` opis ma osobny obszar, a pasek postępu nie nachodzi już na tekst.
- Pełny opis pozostaje dostępny w przewijanym oknie **Event Information**.
- Pogoda bezpośrednio w skinie: **ikona, miejscowość, temperatura i warunki**.
- Pogoda inline ma osobne źródło danych: **Auto** korzysta z skonfigurowanego Weather Plugin, a w razie braku/błędu przechodzi do aktualnego backendu **OpenATV / MetrixWeather / Tools.Weatherinfo**.
- Wybór Foreca, MSNWeather i innych pozycji w polu „Wtyczka pogody” dotyczy launchera pełnego ekranu; nie każda wtyczka udostępnia wspólne API danych dla skina.
- Trzy palety: **Aurora, Amber, Violet**.
- Ekran **OpenATV Informacje** ma rozdzielone kolumny etykiet i wartości, a `r4` dodatkowo poprawia przycinanie w Aktualizacji oprogramowania, Flash Managerze i Kalibracji OSD.
- Widoczna wersja skina jest spójna: **3.2.1**. `r4` oznacza wyłącznie rewizję pakietu IPK.

## Instalacja

Pobierz plik IPK z wydania GitHub, prześlij go do `/tmp` tunera i wykonaj:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_3.2.1-r5_all.ipk
```

Następnie wybierz **AIOHD** w ustawieniach skina i uruchom ponownie GUI z menu tunera.
Nie restartuj GUI w czasie ważnego nagrania.

Zależności pakietu:

- `enigma2`
- `python3-core`
- `enigma2-plugin-skins-metrix-atv`

## Ustawienia AIOHD NEXT

Otwórz **Wtyczki → AIOHD NEXT — Style**.

- **Czcionka listy kanałów**: Standard = 32 px / 18 wierszy, Duża = 38 px / 15 wierszy, Bardzo duża = 42 px / 14 wierszy.
- W trybie dwuliniowym: odpowiednio 10, 9 lub 8 wierszy.
- **Pogoda bezpośrednio w skinie**: domyślnie włączona dla nowego klucza konfiguracji.
- **Skrót do pełnej wtyczki pogody**: opcjonalny launcher z menu rozszerzeń.
- Żółty przycisk pokazuje szerszą listę zainstalowanych launcherów; niebieski otwiera wybraną wtyczkę.
- Po wejściu do ustawień wtyczka **w tle sprawdza GitHub Releases**. Jeśli pojawi się nowsza stabilna rewizja, pokaże informację i zapyta o zgodę na instalację.

## Aktualizacje z poziomu wtyczki

W `3.2.1-r5` wybór koloru przewodniego został rozszerzony o palety **Petrol**, **Copper**, **Jade** i **Sakura**.

Od `3.2.1-r4` AIOHD NEXT ma własny, opcjonalny mechanizm aktualizacji. Po otwarciu **AIOHD NEXT — Style** status aktualizacji pojawia się pod listą ustawień. Sprawdzanie nie blokuje interfejsu.

Jeżeli dostępne jest nowsze stabilne wydanie w oficjalnym repozytorium GitHub, wtyczka wyświetla okno **Tak/Nie**. Dopiero po wybraniu **Tak** pobierany jest oficjalny pakiet IPK i uruchamiana instalacja `opkg`. Po powodzeniu użytkownik może od razu zrestartować GUI albo zrobić to później.

Mechanizm nie instaluje aktualizacji bez zgody i akceptuje wyłącznie pakiety z oficjalnej ścieżki wydań `OliOli2013/AIOHD-NEXT-Skin`.

## Pogoda inline

AIOHD NEXT tworzy własne, bezpieczne źródła sesji, dlatego brak dostawcy danych nie powinien powodować błędu skina ani pustego, niewyjaśnionego panelu.

W trybie **Automatycznie (OpenATV)** skin najpierw korzysta ze skonfigurowanego **Weather Plugin** z feedu OpenATV. Gdy go nie ma, nie jest skonfigurowany albo nie odpowie w wyznaczonym czasie, następuje przejście do aktualnego backendu **OpenATV / MetrixWeather / Tools.Weatherinfo**. Można też wymusić jeden z tych backendów w ustawieniach AIOHD NEXT.

Pole **Wtyczka pogody** służy niezależnie jako launcher pełnego ekranu. Foreca i inne dodatki mogą być uruchamiane, ale nie wszystkie mają wspólne API danych, więc sam wybór launchera nie może być traktowany jako źródło pogody inline.

## Budowanie

Wymagany jest Python 3; pakiet nie wymaga kompilatora dla tunera.

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

Gotowy IPK i plik `.sha256` trafiają do `dist/`. `build.py` sprawdza składnię Python, XML, applety oraz sumy plików. GitHub Actions wykonuje te same testy przy push/pull request.

## Struktura repozytorium

- `root/` — pliki instalowane na tunerze.
- `control/` — metadane i skrypt instalacyjny IPK.
- `build.py` — budowanie pakietu.
- `tests/` — testy regresji.
- `.github/workflows/build.yml` — CI GitHub Actions.

## Zgodność

Projekt jest przygotowany dla **OpenATV / Python 3** i zachowuje informacje licencyjne MetrixHD. Testy automatyczne nie zastępują testów na fizycznym tunerze.

Przy zgłoszeniu problemu podaj model odbiornika, wersję OpenATV, wersję skina, zdjęcie ekranu i crashlog po usunięciu haseł oraz danych dostępowych.

Strona autora: https://olioli2013.github.io/aio-iptv-projekt/
