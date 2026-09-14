# AIOHD NEXT 3.2.1 — package revision r1

Skin Full HD dla **OpenATV / Enigma2, Python 3**, autor modyfikacji: **Paweł Pawełek**.
Na bazie MetrixHD autorstwa iMaxxx / zespołu OpenATV.

## Najważniejsze elementy

- Lista kanałów: pogrubione nazwy 38 px lub 42 px, mocne zaznaczenie aktywnej pozycji i czytelny postęp.
- Prawy panel listy: mniejszy podgląd TV 16:9, nazwa kanału, tytuł, czas, pełny wielowierszowy opis EPG z automatycznym przewijaniem i cztery kolejne audycje.
- Infobar: wysokość 240 px, bieżąca audycja, postęp i następna audycja bez obcinanego akapitu opisu.
- Event Information: pełny opis EPG pozostaje w dużym natywnie przewijanym polu.
- Pogoda bezpośrednio w skinie: ikona, miejscowość, temperatura i warunki.
- OpenATV **Weather Plugin** jest preferowany jako dostawca pogody inline i jako domyślny launcher, jeśli jest zainstalowany.
- Inne zainstalowane wtyczki pogodowe można nadal wybrać w ustawieniach jako launcher.
- Trzy palety: Aurora, Amber, Violet.
- Widoczny numer wersji jest spójny: **3.2.1**. `r1` jest wyłącznie rewizją pakietu IPK.

## Instalacja

Prześlij IPK do `/tmp` tunera i wykonaj:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_3.2.1-r1_all.ipk
```

Następnie wybierz **AIOHD** w ustawieniach skina i uruchom ponownie GUI. Nie restartuj interfejsu w trakcie ważnego nagrania.

Zależności pakietu: `enigma2`, `python3-core`, `enigma2-plugin-skins-metrix-atv`.

## Pogoda

Otwórz **Wtyczki → AIOHD NEXT — Style**. Opcja **Pogoda bezpośrednio w skinie** jest domyślnie włączona dla nowego klucza konfiguracji.

Dane inline są pobierane przez zainstalowany i skonfigurowany **Weather Plugin** z feedu OpenATV. Lokalizację ustawia się w tej wtyczce. Brak Weather Plugin lub brak lokalizacji nie blokuje działania skina — pola pogodowe pozostają puste albo pokazują prośbę o konfigurację.

Żółty przycisk w ustawieniach może pokazać inne zarejestrowane wtyczki pogodowe. Niebieski uruchamia wybraną pełną wtyczkę. Ponieważ różne dodatki pogodowe nie mają wspólnego API danych, ich wybór jako launchera nie oznacza automatycznie użycia ich danych w polach inline.

## Lista kanałów i EPG

Domyślny wariant **Duża**: 15 wierszy i nazwa kanału 38 px. **Bardzo duża**: 14 wierszy i 42 px. W trybie dwuliniowym stosowane jest odpowiednio 9 lub 8 wierszy.

Opis po prawej korzysta z `FullDescription` i renderera `RunningText`: tekst, który mieści się w polu, stoi nieruchomo; dłuższy opis po krótkim opóźnieniu przewija się pionowo. Cztery kolejne pozycje EPG korzystają z istniejącego konwertera `AIONextEvent`.

## Infobar i Event Information

Infobar celowo nie wyświetla pełnego akapitu opisu. Dzięki temu ma mniejszą wysokość i nie ucina treści. Pełny opis jest dostępny w oknie **Event Information**, którego pole `epg_description` ma przewijanie `showOnDemand`.

## Zgodność

Pakiet przygotowano dla OpenATV / Python 3. XML i składnia Python są sprawdzane przed zbudowaniem IPK, ale test automatyczny nie zastępuje testu na fizycznym tunerze. W przypadku problemu podaj model tunera, wersję OpenATV, zdjęcie ekranu i crashlog bez haseł lub danych dostępowych.

Strona autora: https://olioli2013.github.io/aio-iptv-projekt/
