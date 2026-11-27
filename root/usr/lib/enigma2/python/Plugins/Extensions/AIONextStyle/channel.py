# -*- coding: utf-8 -*-
"""Large, readable channel-list typography restricted to this screen instance."""
from types import MethodType
from enigma import eSize, gFont
from Components.config import config
from .settings import settings

# rows, two-line rows, channel font, event font, number font
SIZES = {'standard': (18, 10, 32, 26, 26), 'large': (15, 9, 38, 30, 30), 'xlarge': (14, 8, 42, 32, 32)}


def configure_channel_list(screen):
    try:
        service_list = screen['list']
    except (KeyError, TypeError):
        return
    if not all(hasattr(service_list, key) for key in ('ServiceNameFontName', 'setItemsPerPage', 'setFontsize', 'setMode', 'l', 'listHeight', 'listWidth', 'instance', 'mode')):
        return

    def set_rows(instance):
        size = SIZES.get(settings.listSize.value, SIZES['large'])
        rows = size[1] if getattr(getattr(config.usage, 'servicelist_twolines', None), 'value', False) else size[0]
        height = max(1, instance.listHeight // rows)
        instance.ItemHeight = height
        instance.l.setItemHeight(height)
        instance.instance.resize(eSize(instance.listWidth, rows * height))

    def set_fonts(instance):
        size = SIZES.get(settings.listSize.value, SIZES['large'])
        for field, family, points in (
            ('ServiceName', 'NextBold', size[2]),
            ('ServiceInfo', 'Next', size[3]),
            ('ServiceNumber', 'Next', size[4]),
        ):
            setattr(instance, field + 'FontName', family)
            setattr(instance, field + 'FontSize', points)
            setattr(instance, field + 'Font', gFont(family, points))
        instance.progressInfoFontName = 'Next'
        instance.progressInfoFontSize = 24
        instance.ProgressInfoFont = gFont('Next', 24)
        instance.l.setElementFont(instance.l.celServiceName, instance.ServiceNameFont)
        instance.l.setElementFont(instance.l.celServiceInfo, instance.ServiceInfoFont)
        instance.l.setElementFont(instance.l.celServiceNumber, instance.ServiceNumberFont)

    original_rows = service_list.setItemsPerPage
    original_fonts = service_list.setFontsize
    try:
        service_list.setItemsPerPage = MethodType(set_rows, service_list)
        service_list.setFontsize = MethodType(set_fonts, service_list)
        service_list.setFontsize()
        service_list.setMode(service_list.mode)
    except Exception as exc:
        service_list.setItemsPerPage = original_rows
        service_list.setFontsize = original_fonts
        try:
            original_fonts()
            service_list.setMode(service_list.mode)
        except Exception:
            pass
        print('[AIOHD NEXT] Native channel list fallback: %s' % exc)
