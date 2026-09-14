# AIOHD NEXT 3.2.1-r1 — przebudowany ChannelSelection, InfoBar i pogoda inline

Rewizja `r1` aktualizuje pakiet 3.2.1 bez zmiany widocznego numeru skina.

## Najważniejsze zmiany

- mniejszy podgląd TV 544×306 i większy obszar danych po prawej stronie listy kanałów;
- bieżący tytuł, czas, postęp, wielowierszowy opis i cztery kolejne audycje;
- pogrubione nazwy kanałów 38/42 px;
- InfoBar zmniejszony do 240 px, bez obcinanego długiego opisu;
- pełny opis dostępny w przewijanym Event Information;
- pogoda bezpośrednio w skinie: ikona, miejscowość, temperatura i warunki;
- OpenATV Weather Plugin preferowany jako dostawca danych inline;
- inne wtyczki pogodowe zachowane jako wybieralne launchery;
- `AIOHD_VERSION` i pozostałe widoczne oznaczenia ujednolicone do 3.2.1.

## Pakiet

`enigma2-plugin-skins-aiohd-next_3.2.1-r1_all.ipk`

Po instalacji wybierz AIOHD i wykonaj restart GUI z menu tunera. Ustawienia pogody i czcionki: **Wtyczki → AIOHD NEXT — Style**.

Przed publikacją zalecany jest test na fizycznym tunerze OpenATV, szczególnie ChannelSelection/PiG, przewijania EPG i Weather Plugin.
