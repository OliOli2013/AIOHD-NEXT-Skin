# Weryfikacja

## Testy automatyczne

`python3 -m unittest discover -s tests -v`

Osiem testów obejmuje: wysokości listy dla 4 kombinacji rozmiaru i trybu,
brak modyfikacji innych instancji listy, trwałość ustawienia wierszy przy zmianie
trybu, wykrywanie i deduplikację wtyczek pogody, obsługę usunięcia wtyczki,
kontrast białego tekstu zaznaczenia we wszystkich paletach, wspólne panele,
MiniTV i cztery audycje oraz regresje EPG, komunikatów i zapisywania palet.
Testy korzystają z atrap API Enigma2. Budowanie sprawdza także składnię XML,
Python i appletów oraz sumy kontrolne plików w archiwum danych.

## Do sprawdzenia na fizycznym tunerze

- Aktualizacja 3.1.3 → 3.2.1 i restart GUI.
- Strzałki listy, widoczność zaznaczenia i piconów; wszystkie warianty listy.
- Rozmiary Duża / Bardzo duża; tryby jedno- i dwuliniowe.
- Podgląd TV, zmiana zaznaczonego kanału, cztery przyszłe audycje.
- Aurora / Amber / Violet, zapis i restart.
- Brak wtyczki pogodowej, jedna dostępna, kilka dostępnych, usunięta po konfiguracji.
- Niebieski przycisk pogody, powrót do ustawień, skrót w menu rozszerzeń.
- Anulowanie ustawień bez zapisywania.
- Pełny opis EPG, długi komunikat i wybór Tak/Nie.

W przygotowaniu wydania nie wykonano testów na fizycznym odbiorniku.
Zgodność szczególnych wersji wtyczek pogodowych wymaga sprawdzenia na urządzeniu.

Dodatkowo sprawdzono właściwości fontu (NextBold 36/40) po ponownym setFontsize.
Wykrywanie pogody sprawdzono również z rzeczywistą klasą PluginDescriptor
z repozytorium OpenATV, używając dwóch testowych funkcji uruchamiających.
Nie zastępuje to uruchomienia konkretnych wtyczek użytkownika na tunerze.

Test instalacji bootlogo: zachowanie innego aktywnego skina, aktualizacja
przy aktywnym AIOHD i zachowanie pierwotnej kopii przy kolejnej aktualizacji.
