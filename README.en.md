# AIOHD NEXT 3.2.1

Modern Full HD skin for **OpenATV / Enigma2 (Python 3)**.
AIOHD NEXT modifications by **Paweł Pawełek**, based on MetrixHD by iMaxxx / OpenATV.

## Highlights

- Three channel-list sizes with strong selection: **Standard 32 px / 18 channels**, **Large 38 px / 15 channels**, and **Extra large 42 px / 14 channels**.
- Rebuilt right panel with a smaller **544×306 16:9 MiniTV**, current event, time/progress, multi-line EPG description and **four upcoming events**.
- Long descriptions auto-scroll vertically only when needed.
- Compact **240 px** InfoBar with channel, current title, a **two-line current-event description**, progress/time and next event.
- Full long EPG text remains available in the scrollable **Event Information** screen.
- Inline weather: **icon, city, temperature and condition**.
- Inline data provider is separate from the launcher. **Auto** uses a configured Weather Plugin first and falls back to the current **OpenATV / MetrixWeather / Tools.Weatherinfo** backend.
- Other installed weather plugins can still be selected as full-screen launchers; they do not all expose a common inline-data API.
- Aurora, Amber and Violet palettes.
- The **OpenATV Information** screen uses separated label/value columns, preventing long labels from overlapping values.
- Visible skin version stays **3.2.1**; `r3` is the IPK package revision only.

## Install

Copy the IPK to `/tmp` and run:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_3.2.1-r4_all.ipk
```

Select **AIOHD** in the skin selector and restart the GUI from the receiver menu.
Dependencies: `enigma2`, `python3-core`, `enigma2-plugin-skins-metrix-atv`.

## AIOHD NEXT settings

Open **Plugins → AIOHD NEXT — Style**.

- Standard: 32 px / 18 rows.
- Large: 38 px / 15 rows.
- Extra large: 42 px / 14 rows.
- Two-line mode: 10 / 9 / 8 rows.
- Inline weather is enabled by default for the new configuration key.
- The full weather-plugin shortcut remains optional.
- Yellow shows a broader launcher list; blue opens the selected plugin.

## In-plugin updates

Since `3.2.1-r4`, opening **Plugins → AIOHD NEXT — Style** starts a non-blocking check of the official GitHub Releases feed. If a newer stable package is available, the user gets a Yes/No prompt. Nothing is installed automatically; the IPK is downloaded and passed to `opkg` only after explicit confirmation. The package URL is restricted to the official `OliOli2013/AIOHD-NEXT-Skin` release path.

`r4` also fixes text clipping in Software Update, Flash Manager and OSD Calibration, and separates the InfoBar description from the progress bar.

## Inline weather

AIOHD NEXT owns the weather session sources, so a missing provider should not break InfoBar or ChannelSelection or leave an unexplained blank weather panel.

In **Automatic (OpenATV)** mode the skin first uses a configured OpenATV **Weather Plugin**. If it is missing, not configured or times out, AIOHD NEXT falls back to the current **OpenATV / MetrixWeather / Tools.Weatherinfo** backend. Either backend can also be forced in AIOHD NEXT settings.

The **Weather plugin** selector remains a separate full-screen launcher. Foreca and other plugins can be launched there, but they do not all expose a common data API and therefore cannot automatically feed the inline panel.

## Build

```sh
python3 -m unittest discover -s tests -v
python3 build.py
```

The IPK and SHA256 file are generated in `dist/`. The builder validates Python, XML/applets and package checksums. GitHub Actions runs the same checks on push and pull requests.

## Compatibility

OpenATV / Python 3. Keep the inherited MetrixHD licensing notices. Automated tests do not replace receiver testing.

When reporting an issue, include receiver model, OpenATV version, skin version, screenshot and a sanitized crashlog.

Author website: https://olioli2013.github.io/aio-iptv-projekt/
