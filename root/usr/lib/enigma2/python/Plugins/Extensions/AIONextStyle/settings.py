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
# New in 3.2.1-r1: weather data is shown directly in the skin.
# This is a new key, therefore upgrades get the requested enabled-by-default behaviour.
if not hasattr(settings, 'weatherInline'):
    settings.weatherInline = ConfigYesNo(default=True)
if not hasattr(settings, 'weatherPlugin'):
    settings.weatherPlugin = ConfigText(default='', fixed_size=False)


def tr(pl, en):
    return pl if config.osd.language.value.startswith('pl') else en
