# AIOHD NEXT 3.2.1-r2 — pogoda inline i opis audycji w InfoBar

Rewizja `r2` naprawia dwie rzeczy zgłoszone po teście `r1`, bez zmiany widocznego numeru skina **3.2.1**.

## Zmiany

- pogoda inline nie zależy już od samego wyboru launchera;
- **Auto** korzysta ze skonfigurowanego Weather Plugin i ma fallback do aktualnego backendu OpenATV / MetrixWeather (`Tools.Weatherinfo`);
- dodano timeout/fallback oraz czytelny status, więc panel pogody nie powinien pozostawać pustym prostokątem;
- ustawienia rozdzielają teraz źródło danych pogody od wtyczki otwieranej na pełnym ekranie;
- InfoBar zachowuje wysokość 240 px, ale pod tytułem bieżącej audycji pokazuje dwuwierszowy opis `FullDescription`;
- pasek czasu/postępu i następna audycja zostały zachowane;
- pełny opis nadal jest dostępny w przewijanym Event Information.

## Pakiet

`enigma2-plugin-skins-aiohd-next_3.2.1-r2_all.ipk`

Po instalacji wykonaj restart GUI. W **Wtyczki → AIOHD NEXT — Style** pozostaw źródło danych pogody na **Automatycznie (OpenATV)**, chyba że chcesz wymusić konkretny backend.
