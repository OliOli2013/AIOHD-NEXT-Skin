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
