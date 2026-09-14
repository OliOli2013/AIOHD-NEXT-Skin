# AIOHD NEXT 3.2.1

Modern Full HD skin for **OpenATV / Enigma2 (Python 3)**.
AIOHD NEXT modifications by **Paweł Pawełek**, based on MetrixHD by iMaxxx / OpenATV.

## Highlights

- Bold **38 px / 42 px** channel names with a strong active-row highlight.
- Rebuilt right panel with a smaller **544×306 16:9 MiniTV**, current event, time/progress, multi-line EPG description and **four upcoming events**.
- Long descriptions auto-scroll vertically only when needed.
- Compact **240 px** InfoBar focused on channel, current event, progress/time and next event.
- Full long EPG text remains available in the scrollable **Event Information** screen.
- Inline weather: **icon, city, temperature and condition**.
- Preferred inline provider: **Weather Plugin from the OpenATV feed**, when installed and configured.
- Other installed weather plugins can still be selected as launchers.
- Aurora, Amber and Violet palettes.
- Visible skin version stays **3.2.1**; `r1` is the IPK package revision only.

## Install

Copy the IPK to `/tmp` and run:

```sh
opkg install /tmp/enigma2-plugin-skins-aiohd-next_3.2.1-r1_all.ipk
```

Select **AIOHD** in the skin selector and restart the GUI from the receiver menu.
Dependencies: `enigma2`, `python3-core`, `enigma2-plugin-skins-metrix-atv`.

## AIOHD NEXT settings

Open **Plugins → AIOHD NEXT — Style**.

- Large: 38 px / 15 rows.
- Extra large: 42 px / 14 rows.
- Two-line mode: 9 / 8 rows.
- Inline weather is enabled by default for the new configuration key.
- The full weather-plugin shortcut remains optional.
- Yellow shows a broader launcher list; blue opens the selected plugin.

## Inline weather

AIOHD NEXT owns the weather session sources, so a missing external weather plugin should not break InfoBar or ChannelSelection.

When the OpenATV **Weather Plugin** is installed and configured, AIOHD NEXT uses its data for city, temperature, condition and icon. Location and units remain configured in Weather Plugin itself.

Other weather plugins can still be used as launchers, but third-party plugins do not expose one common data API, so selecting another launcher does not automatically make it an inline data provider.

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
