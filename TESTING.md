# Testy AIOHD NEXT 4.0.0-r0

## Automatyczne

`python3 -m unittest discover -s tests -v` i `python3 build.py`.
Nowe testy: składnia XML/Python/applety, rozpoznawanie paneli, granice geometrii, oś EPG, procent EPG, 27 kombinacji stylu, aktualizator, schemat Live Center. Zachowano testy regresji 3.2.1, aktualizując oczekiwania dotyczące zmienionych funkcji.

## Test odbiornika (przed wydaniem stabilnym)

1. OpenATV 7.6 i 8.0, następnie 8.1 beta osobno; ARM i MIPS, jeśli dostępne. Testować na Full HD, nie podczas nagrywania.
2. Instalacja z czystego image i aktualizacja 3.2.1-r5; wybór AIOHD, ręczny restart, brak pętli GUI. Powrót do MetrixHD.
3. InfoBar: SAT/IPTV, brak EPG, polskie i długie nazwy, picon, nagrywanie, SNR/AGC/BER, pogoda. Procent tylko przy poprawnym bieżącym EPG.
4. Lista: trzy rozmiary, tryb dwuliniowy, PiG, 4 audycje (czas i tytuł), długie opisy. Sprawdzić również brak EPG i skrajne długości.
5. SecondInfoBar, Menu, EPGSelection, EventView, MoviePlayer, Volume, FlashOnline, DeviceManager, SoftwareUpdate, OSDCalibration, MessageBox.
6. Style: wszystkie 3 powierzchnie, kilka palet, restart, ponowny zapis, odczyt ustawień. Cinema Glass — czytelność na jasnym obrazie; OLED — kontrast starszych ekranów.
7. Live Center: SAT/IPTV, brak aktywnej usługi, nagrania, czas, odczyt danych systemowych, zamknięcie i ponowne otwarcie; brak błędu i zatrzymanie timera.
8. Aktualizator: brak sieci, błędny certyfikat, odmowa instalacji, poprawny oficjalny pakiet, niezgodny digest, gdy podany. Nie publikować testowego wydania jako stable.
9. Sprawdź wtyczki zewnętrzne, które były stylowane przez MetrixHD. Nie wszystkie kombinacje image/wtyczek mają identyczne komponenty.


---

# Weryfikacja AIOHD NEXT 3.2.1-r3

## Testy automatyczne

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

Testy obejmują m.in.:

- 18/15/14 wierszy listy oraz 10/9/8 w trybie dwuliniowym;
- fonty kanałów 32/38/42 px i brak globalnej ingerencji w inne ServiceList;
- wykrywanie i wybór launcherów pogody;
- niezależny wybór źródła danych inline (`Auto`, OpenATV/MetrixWeather, Weather Plugin);
- fallback Weather Plugin → OpenATV/MetrixWeather oraz czytelny stan przy braku danych;
- obecność bezpiecznych źródeł pogody i renderera ikony;
- wspólny ChannelSelection, MiniTV i cztery następne audycje;
- przewijany opis EPG i kontrast zaznaczenia;
- zachowanie palet oraz bootlogo.

## Test na fizycznym tunerze

Po instalacji sprawdź:

- listę kanałów we wszystkich wariantach i trzy rozmiary czcionki, w tym Standard = 18 kanałów;
- ekran **OpenATV Informacje**: brak nakładania etykiet na wartości przy polskiej wersji językowej i długich danych MultiBoot;
- zaznaczenie, picony i paski postępu;
- PiG 544×306 i poprawną zmianę podglądu po przechodzeniu po kanałach;
- pełny opis EPG po prawej oraz jego automatyczne przewijanie;
- cztery następne audycje;
- InfoBar 240 px: tytuł, dwuwierszowy opis bieżącej audycji, czas, postęp i następna audycja bez obcięć;
- Event Information z długim przewijanym opisem;
- Weather Plugin z feedu OpenATV: skonfigurowana lokalizacja, ikona, miejscowość, temperatura i warunki;
- zachowanie skina bez Weather Plugin oraz po wyłączeniu pogody inline;
- launcher innej zainstalowanej wtyczki pogodowej;
- Aurora / Amber / Violet;
- restart GUI, ponowne wejście do listy i zachowanie ustawień.

Automatyczna walidacja nie zastępuje testu na odbiorniku.

## r4 — dodatkowe testy ręczne

1. Otwórz **Aktualizacja oprogramowania** i sprawdź, czy „Dostępne”/liczba oraz dwie linie pozycji nie są obcięte.
2. Otwórz **Flash Manager / Systemy OpenATV** i sprawdź pełny tytuł oraz listę systemów.
3. Otwórz **Kalibrację OSD** i sprawdź, czy instrukcja nie nachodzi na ustawienia.
4. Na InfoBarze sprawdź długi opis wydarzenia: pasek postępu musi znajdować się pod opisem.
5. Wejdź do **AIOHD NEXT — Style**: status powinien przejść ze „sprawdzanie” na aktualną wersję albo informację o nowszej wersji.
6. Test aktualizacji wykonuj dopiero po opublikowaniu nowszego GitHub Release. Odmowa w oknie Tak/Nie nie może uruchamiać żadnego polecenia instalacyjnego.
