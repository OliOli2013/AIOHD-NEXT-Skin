# AIOHD NEXT 4.0 — Live Grid

**Test build 4.0.0-r0** · Full HD 1920×1080 · OpenATV / Python 3.

AIOHD NEXT modifications by Paweł Pawełek. Based on MetrixHD by iMaxxx / the OpenATV Team. Original licensing and attribution retained.

[Polski](README.md) · [Changelog](CHANGELOG.md) · [Testing](TESTING.md)

- Redesigned bottom TV dock with programme details, EPG progress percentage, next event, weather and DVB signal.
- Channel browser with 528×297 preview, four upcoming events in separate time/title columns and three text sizes.
- SecondInfoBar with a dedicated upcoming-events timeline; redesigned menu, EPG, event information, movie player and volume overlay.
- Live Center extension: current service, EPG, signal when available, memory usage, root filesystem capacity and active recordings. Local refresh every five seconds only while visible.
- Nine accent palettes and three surface profiles: Studio, OLED Black and Cinema Glass.
- Weather Plugin first, then OpenATV/MetrixWeather in Auto mode; full-screen launcher is independent.
- Official GitHub release updater with verified TLS, asset SHA-256 when provided by GitHub and explicit installation consent.

## Installation

Back up settings and avoid installation during recording. Copy the IPK to `/tmp` and run:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_4.0.0-r0_all.ipk
```

Select AIOHD and restart the GUI manually. Plugins → AIOHD NEXT — Style provides colour, surface, channel typography and weather settings. System bootlogo is not overwritten.

Dependencies: `enigma2`, `enigma2-plugin-skins-metrix-atv`, `python3-core`. OpenATV only, in accordance with the base skin licence. Physical receiver validation is still required.

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```
