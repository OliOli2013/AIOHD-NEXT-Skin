# Utworzenie repozytorium GitHub

Proponowana nazwa: **AIOHD-NEXT-Skin**

Opis repozytorium (pole Description):

> AIOHD NEXT — Full HD skin for OpenATV / Enigma2 with TV preview, upcoming EPG, large channel fonts and optional weather plugin integration.

Website:

> https://olioli2013.github.io/aio-iptv-projekt/

Topics:

`enigma2`, `openatv`, `skin`, `full-hd`, `epg`, `python3`, `aiohd-next`

## Pierwsze wysłanie z Linux Mint

1. Na GitHub utwórz puste repozytorium `AIOHD-NEXT-Skin` na koncie `OliOli2013`.
2. Nie dodawaj automatycznie README, .gitignore ani dodatkowej licencji — pliki są w zestawie.
3. Rozpakuj ZIP i otwórz terminal w folderze zawierającym `README.md` i `build.py`.
4. Uruchom:

```sh
git init -b main
git add .
git commit -m "AIOHD NEXT 3.2.1: initial source release"
git remote add origin https://github.com/OliOli2013/AIOHD-NEXT-Skin.git
git push -u origin main
```

Użyj logowania GitHub obsługiwanego przez swój komputer. Nie wpisuj tokenu do
plików projektu. Jeśli wybierzesz inną nazwę repozytorium, zmień adres `origin`.
Wysyłanie przez Git pozwala zachować cały zestaw ponad 1600 plików i folder `.github`;
nie trzeba dzielić go na porcje w przeglądarce.

## Pierwsze wydanie

1. Otwórz Releases → Draft a new release.
2. Tag: `v3.2.1`, branch: `main`.
3. Tytuł: `AIOHD NEXT 3.2.1`.
4. Treść: skopiuj `RELEASE-3.2.1.md`.
5. Dodaj pliki `dist/enigma2-plugin-skins-aiohd-next_3.2.1-r0_all.ipk`
   i odpowiadający mu `.ipk.sha256` (powstają po `python3 build.py`).
6. Opublikuj wydanie po teście na tunerze; wcześniej można zachować szkic.

Workflow buduje artefakt przy każdym push i pull request. Nie publikuje wydań
ani nie wysyła pakietu na tuner automatycznie.

Repozytorium nie zostało utworzone ani opublikowane przez przygotowanie tego ZIP.
