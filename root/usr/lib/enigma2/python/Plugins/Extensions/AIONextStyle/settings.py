# -*- coding: utf-8 -*-
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigYesNo, ConfigText

if not hasattr(config.plugins, 'aionext'):
    config.plugins.aionext = ConfigSubsection()
settings = config.plugins.aionext
if not hasattr(settings, 'listSize'):
    settings.listSize = ConfigSelection(default='large', choices=[('large', 'Large'), ('xlarge', 'Extra large')])
# Keep the launcher for users who want to open the complete weather plugin.
if not hasattr(settings, 'weatherEnabled'):
    settings.weatherEnabled = ConfigYesNo(default=True)
if not hasattr(settings, 'weatherInline'):
    settings.weatherInline = ConfigYesNo(default=True)
# r2: inline data provider is deliberately separate from the launcher selection.
# Auto prefers the current OpenATV/Metrix weather backend and falls back to the
# classic Weather Plugin when available/configured.
if not hasattr(settings, 'weatherProvider'):
    settings.weatherProvider = ConfigSelection(default='auto', choices=[
        ('auto', 'Auto (OpenATV)'),
        ('metrix', 'OpenATV / MetrixWeather'),
        ('weatherplugin', 'Weather Plugin'),
    ])
if not hasattr(settings, 'weatherPlugin'):
    settings.weatherPlugin = ConfigText(default='', fixed_size=False)


def tr(pl, en):
    return pl if config.osd.language.value.startswith('pl') else en
