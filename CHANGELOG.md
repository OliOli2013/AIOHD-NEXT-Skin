# Changelog

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
