# AIOHD NEXT 3.2.1

Full HD skin for **OpenATV / Enigma2, Python 3**.
AIOHD NEXT modifications by **Paweł Pawełek**, based on MetrixHD by iMaxxx / OpenATV.

## Features

- Clear infobar with picon, event description, progress, next event and SNR/AGC.
- Mini TV preview and four upcoming events for the highlighted channel.
- Bold 36 / 40 px channel fonts: 15 / 14 rows in supported legacy lists.
- Two-line lists use 9 / 8 rows. Other template implementations retain native sizing.
- Strong selection highlight matched to Aurora, Amber or Violet.
- Scrollable EPG details and paginated long messages.
- Optional launcher for an installed weather plugin.

## Install

Copy the IPK to `/tmp` and run:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_3.2.1-r0_all.ipk
```

Select **AIOHD** in the skin selector and restart the GUI through the receiver menu.
Dependencies: Enigma2, Python 3 core and `enigma2-plugin-skins-metrix-atv`.

## Settings and weather

Open **Plugins → AIOHD NEXT — Style**. Select the accent palette and list font.
Enable the optional weather shortcut and choose an installed weather launcher.
Blue previews weather; green saves. Reopen the channel list to apply font sizing.
Palette changes and adding/removing the Extensions weather entry require a GUI restart.

Weather detection checks registered Plugin/Extensions menu launchers for weather,
pogoda, foreca, wetter or meteo in their identity. It does not install plugins,
access weather APIs, add animated icons, or show weather in the infobar.
Location and icon settings belong to the selected weather plugin. Specific
versions of third-party weather plugins have not been hardware-tested.
Unavailable or removed plugins produce an information message.

## Build

Python 3 standard library only:

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

The IPK and SHA256 are generated in `dist/`. GitHub Actions runs tests and builds.
The source tree includes all packaged assets and modules.

## Scope

OpenATV only; retain the inherited MetrixHD licensing notice in `LICENSE` and
`skin.xml`. No blanket MIT/GPL licence is assigned to third-party assets.
Tests use mocked Enigma2 APIs; version 3.2.1 still requires physical receiver
validation. Include receiver model, OpenATV version and screenshots in reports.

Author's website: https://olioli2013.github.io/aio-iptv-projekt/

Yellow in the settings screen lists all registered launchers for manual selection.
The corrected detector supports OpenATV PluginDescriptor.function.
Bootlogo now displays 3.2.1. If AIOHD is the active skin during installation,
the system bootlogo is updated with a backup of the previous file.
