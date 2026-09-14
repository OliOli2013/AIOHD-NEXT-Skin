# -*- coding: utf-8 -*-
"""Discover registered weather launchers; never import or execute arbitrary files."""
from Components.PluginComponent import plugins
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from .settings import settings, tr

WORDS = ('weather', 'pogoda', 'foreca', 'wetter', 'meteo')


def launcher(descriptor):
    # Current OpenATV uses .function, older forks may expose .fnc or __call__.
    for attr in ('function', 'fnc', '__call__'):
        value = getattr(descriptor, attr, None)
        if callable(value):
            return value
    return None


def weather_plugins(show_all=False):
    found = {}
    for where in set((PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU, getattr(PluginDescriptor, 'WHERE_MAINMENU', PluginDescriptor.WHERE_PLUGINMENU))):
        for descriptor in plugins.getPlugins(where):
            name = str(getattr(descriptor, 'name', ''))
            path = str(getattr(descriptor, 'path', '') or '')
            fnc = launcher(descriptor)
            module = str(getattr(fnc, '__module__', ''))
            if 'aionextstyle' in (path + module).lower() or name.startswith('AIOHD NEXT'):
                continue
            if not callable(fnc):
                continue
            # Match identity rather than generic descriptions of multi-tools.
            if not show_all and not any(word in (name + ' ' + path + ' ' + module).lower() for word in WORDS):
                continue
            key = path + '|' + name
            found.setdefault(key, (name, descriptor))
    return [(key, value[0], value[1]) for key, value in sorted(found.items(), key=lambda x: x[1][0].lower())]


def open_weather(session, key=None):
    if key is None:
        if not settings.weatherEnabled.value:
            session.open(MessageBox, tr('Włącz pogodę w ustawieniach AIOHD NEXT.', 'Enable weather in AIOHD NEXT settings.'), MessageBox.TYPE_INFO)
            return
        key = settings.weatherPlugin.value
    selected = next((p for p in weather_plugins(show_all=True) if p[0] == key), None)
    if selected is None:
        session.open(MessageBox, tr('Wybrana wtyczka pogody nie jest dostępna. Wybierz zainstalowaną wtyczkę w ustawieniach AIOHD NEXT.', 'The selected weather plugin is unavailable. Select an installed plugin in AIOHD NEXT settings.'), MessageBox.TYPE_INFO)
        return
    try:
        selected[2](session=session)
    except Exception as error:
        session.open(MessageBox, tr('Nie udało się otworzyć wtyczki pogody: ', 'Could not open the weather plugin: ') + str(error), MessageBox.TYPE_ERROR)
