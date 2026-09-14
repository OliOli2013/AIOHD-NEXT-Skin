# -*- coding: utf-8 -*-
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigYesNo, ConfigText

if not hasattr(config.plugins, 'aionext'):
    config.plugins.aionext = ConfigSubsection()
settings = config.plugins.aionext
if not hasattr(settings, 'listSize'):
    settings.listSize = ConfigSelection(default='large', choices=[('large', 'Large'), ('xlarge', 'Extra large')])
if not hasattr(settings, 'weatherEnabled'):
    settings.weatherEnabled = ConfigYesNo(default=False)
if not hasattr(settings, 'weatherPlugin'):
    settings.weatherPlugin = ConfigText(default='', fixed_size=False)


def tr(pl, en):
    return pl if config.osd.language.value.startswith('pl') else en
