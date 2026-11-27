## 4.0.0-r0 — 2026-11-27 (test)

- Live Grid: przebudowane główne ekrany, dolny dock, rozdzielone czasy i tytuły EPG, procent postępu audycji.
- Live Center: lokalne informacje o kanale, sygnale, RAM, systemie plików i nagraniach.
- 9 palet × 3 tryby powierzchni, Cinema Glass, OLED Black.
- Poprawki TLS, weryfikacji URL/digestu aktualizacji, zabezpieczenie pliku tymczasowego.
- Bezpieczniejszy fallback listy kanałów, zachowany uchwyt eTimer, poprawiony opis pogody Auto.
- Instalacja nie nadpisuje systemowego bootlogo ani nie restartuje GUI.
- Testy statyczne wykonane; testy na tunerze wymagane.


---

# Changelog

## 3.2.1-r5 — 2026-09-15

- Poprawiono pozostałe błędy widoczne na ekranie **Aktualizacja oprogramowania**: napis „Dostępne aktualizacje” jest teraz jednowierszowy i ma oddzielne miejsce na licznik pakietów.
- **Menedżer urządzeń** działa jako pełnoekranowe okno bez systemowej ramki tytułu, dzięki czemu nie pojawia się drugi, ucięty tytuł przy górnej krawędzi.
- **Flash Online / Systemy OpenATV** ma tylko jeden tytuł. Usunięto dublowanie `T_Title` i dodano nieprzezroczyste tło nagłówka, które zakrywa tytuł poprzedniego ekranu.
- Poszerzono nagłówek ekranów OPEN SOURCE i zmniejszono jego font, aby długie polskie tytuły mieściły się bez nakładania.
- Dodano cztery nowe, mniej typowe palety koloru przewodniego: **Petrol**, **Copper**, **Jade** i **Sakura**. Zachowano dotychczasowe Aurora, Amber i Violet.
- Mechanizm aktualizacji skina pozostaje bez zmian funkcjonalnych i od tej rewizji identyfikuje lokalny pakiet jako `3.2.1-r5`.
- Rewizja pakietu: `3.2.1-r5`; widoczna wersja skina pozostaje `3.2.1`.

## 3.2.1-r4 — 2026-09-14

- Poprawiono zgłoszone przycięcia tekstu w ekranach **Aktualizacja oprogramowania**, **Flash Manager / Systemy OpenATV** oraz **Kalibracja OSD**.
- Ekran Flash Manager otrzymał pełny nagłówek FHD i poprawny osobny obszar opisu, zamiast nakładających się elementów.
- W Kalibracji OSD powiększono obszar instrukcji i przesunięto listę ustawień niżej, aby dłuższy polski tekst nie nachodził na konfigurację.
- W ekranie aktualizacji systemu zwiększono wysokość nagłówka liczby pakietów oraz wysokość pozycji listy, żeby nazwa i opis nie były obcinane.
- Uporządkowano **InfoBar**: opis bieżącego wydarzenia ma własny większy obszar, a pasek postępu i czasy zostały przesunięte niżej, dzięki czemu nie zasłaniają opisu.
- Dodano mechanizm sprawdzania aktualizacji skina w **Wtyczki → AIOHD NEXT — Style**. Sprawdzanie odbywa się w tle przy wejściu do ustawień.
- Gdy GitHub Releases zawiera nowszą stabilną wersję, użytkownik otrzymuje komunikat i sam decyduje, czy ją zainstalować. Aktualizacja nigdy nie jest instalowana automatycznie.
- Po udanej instalacji wtyczka proponuje restart GUI; w czasie nagrywania można go odrzucić i wykonać później.
- Dodano walidację adresu pakietu aktualizacji wyłącznie do oficjalnych wydań `OliOli2013/AIOHD-NEXT-Skin`.
- Rewizja pakietu: `3.2.1-r4`; widoczna wersja skina pozostaje `3.2.1`.

## 3.2.1-r3 — 2026-09-14

- Naprawiono ekran **OpenATV Informacje**: kolumny etykiet i wartości są fizycznie rozdzielone (`splitSeparated`), z większym odstępem i bez nachodzenia tekstu.
- Dostosowano szerokość kolumn i font informacji do długich polskich opisów oraz dłuższych wartości MultiBoot.
- Dodano trzeci rozmiar listy kanałów **Standard**: 18 kanałów, nazwy 32 px, opis 26 px.
- Tryb dwuliniowy dla Standard używa 10 wierszy; Duża/Bardzo duża pozostają bez zmian (15/14 oraz 9/8).
- Zachowano pogodę, InfoBar, MiniTV i układ EPG z `r2` bez zmian funkcjonalnych.
- Rewizja pakietu: `3.2.1-r3`; widoczna wersja skina pozostaje `3.2.1`.

## 3.2.1-r2 — 2026-09-14

- Naprawiono pusty panel pogody: tryb Auto nie traktuje już wyboru launchera jako interfejsu danych.
- Dodano dwa rzeczywiste backendy inline: skonfigurowany `Weather Plugin` oraz aktualny OpenATV `MetrixWeather / Tools.Weatherinfo`.
- Gdy klasyczny Weather Plugin nie odpowiada, Auto przechodzi do backendu OpenATV; dodano timeout i czytelne stany zamiast pustego prostokąta.
- W ustawieniach rozdzielono **źródło danych inline** od **wtyczki otwieranej jako launcher**.
- InfoBar nadal ma 240 px, ale pokazuje teraz dwuwierszowy `FullDescription` bieżącej audycji między tytułem a paskiem postępu.
- Pełny przewijany opis pozostaje w Event Information.
- Rewizja pakietu: `3.2.1-r2`; widoczna wersja skina pozostaje `3.2.1`.

## 3.2.1-r1 — 2026-09-14

- Przebudowany prawy panel ChannelSelection: podgląd 544×306, więcej miejsca na EPG.
- Wielowierszowy `FullDescription` z automatycznym pionowym przewijaniem dłuższej treści.
- Zachowane cztery następne audycje w czytelniejszym układzie.
- Nazwy kanałów zwiększone do 38/42 px (`NextBold`) bez zwiększania samych odstępów.
- InfoBar zmniejszony do 240 px i uporządkowany wokół bieżącej/następnej audycji.
- Pełny opis pozostaje w przewijanym Event Information.
- Dodano pogodę inline: miejscowość, temperatura, warunki i ikona.
- Preferowanym dostawcą danych inline jest OpenATV Weather Plugin, jeśli jest dostępny i skonfigurowany.
- Inne wykryte dodatki pogodowe nadal mogą działać jako launchery.
- Dodano renderer `AIONextWeatherPixmap` i bezpieczne źródła sesji pogody.
- `AIOHD_VERSION` poprawiono z nieaktualnego `3.1.2-r0` do `3.2.1`.
- Rewizja pakietu IPK: `3.2.1-r1`; widoczna wersja skina pozostaje `3.2.1`.

## 3.2.1-r0 — 2026-09-14

- Naprawiono wykrywanie wtyczek pogody przez `PluginDescriptor.function`.
- Dodano ręczny wybór launcherów oraz żółty przycisk pokazujący wszystkie zarejestrowane dodatki.
- Pogrubione nazwy kanałów 36/40 px, opisy 30/32 px.
- 15/14 wierszy oraz 9/8 w trybie dwuliniowym.
- Ustawienia fontu odporne na kolejne wywołania `setFontsize`.
- Bootlogo z numerem 3.2.1 i bezpieczna aktualizacja systemowego bootlogo tylko przy aktywnym AIOHD.

## 3.2.0 — 2026-09-14

- Większa typografia listy kanałów i tryb bardzo dużej czcionki.
- Lokalne sterowanie wysokością wiersza bez zmiany globalnych ustawień ServiceList.
- Mocniejsze zaznaczenie aktywnego kanału w trzech paletach.
- Opcjonalny launcher pogody.
- MiniTV i cztery przyszłe audycje.
- Pełne źródła, builder IPK, testy oraz GitHub Actions.

## 3.1.3

Poprawki EventView, komunikatów, InfoBar, wspólnego ChannelSelection oraz logiki przyszłych pozycji EPG.
