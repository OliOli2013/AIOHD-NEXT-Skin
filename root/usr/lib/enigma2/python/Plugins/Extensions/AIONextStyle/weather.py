# -*- coding: utf-8 -*-
"""Weather integration for AIOHD NEXT.

The skin always owns its session sources, so missing third-party weather plugins
cannot break InfoBar or ChannelSelection.  If OpenATV's Weather Plugin is
installed and configured, its public configuration/data API is used for the
inline city, temperature, condition and icon.  Other installed weather plugins
remain available as launchers from AIOHD NEXT settings.
"""
import os

from Components.PluginComponent import plugins
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from enigma import eTimer

from .settings import settings, tr

WORDS = ('weather', 'pogoda', 'foreca', 'wetter', 'meteo')
SOURCE_CITY = 'AIONextWeatherCity'
SOURCE_TEMP = 'AIONextWeatherTemp'
SOURCE_CONDITION = 'AIONextWeatherCondition'
SOURCE_ICON = 'AIONextWeatherIcon'


def launcher(descriptor):
    # Current OpenATV uses .function, older forks may expose .fnc or __call__.
    for attr in ('function', 'fnc', '__call__'):
        value = getattr(descriptor, attr, None)
        if callable(value):
            return value
    return None


def weather_plugins(show_all=False):
    found = {}
    locations = set((
        PluginDescriptor.WHERE_PLUGINMENU,
        PluginDescriptor.WHERE_EXTENSIONSMENU,
        getattr(PluginDescriptor, 'WHERE_MAINMENU', PluginDescriptor.WHERE_PLUGINMENU),
    ))
    for where in locations:
        for descriptor in plugins.getPlugins(where):
            name = str(getattr(descriptor, 'name', ''))
            path = str(getattr(descriptor, 'path', '') or '')
            fnc = launcher(descriptor)
            module = str(getattr(fnc, '__module__', ''))
            identity = (name + ' ' + path + ' ' + module).lower()
            if 'aionextstyle' in identity or name.startswith('AIOHD NEXT'):
                continue
            if not callable(fnc):
                continue
            if not show_all and not any(word in identity for word in WORDS):
                continue
            key = path + '|' + name
            found.setdefault(key, (name, descriptor, identity))
    return [(key, value[0], value[1]) for key, value in sorted(found.items(), key=lambda x: x[1][0].lower())]


def preferred_weather_key(entries=None):
    """Prefer OpenATV/OE-Alliance Weather Plugin, then another weather plugin."""
    entries = entries if entries is not None else weather_plugins()
    if not entries:
        return ''
    for key, name, descriptor in entries:
        fnc = launcher(descriptor)
        identity = ('%s %s %s' % (name, getattr(descriptor, 'path', '') or '', getattr(fnc, '__module__', '') or '')).lower()
        if 'weatherplugin' in identity or name.strip().lower() == 'weather plugin':
            return key
    return entries[0][0]


def open_weather(session, key=None):
    if key is None:
        if not settings.weatherEnabled.value:
            session.open(MessageBox, tr('Włącz skrót pogody w ustawieniach AIOHD NEXT.', 'Enable the weather shortcut in AIOHD NEXT settings.'), MessageBox.TYPE_INFO)
            return
        key = settings.weatherPlugin.value or preferred_weather_key()
    selected = next((p for p in weather_plugins(show_all=True) if p[0] == key), None)
    if selected is None:
        session.open(MessageBox, tr(
            'Nie znaleziono wybranej wtyczki pogody. Zainstaluj z feedu OpenATV „Weather Plugin” albo wybierz inną zainstalowaną wtyczkę.',
            'The selected weather plugin is unavailable. Install “Weather Plugin” from the OpenATV feed or select another installed weather plugin.'
        ), MessageBox.TYPE_INFO)
        return
    try:
        selected[2](session=session)
    except Exception as error:
        session.open(MessageBox, tr('Nie udało się otworzyć wtyczki pogody: ', 'Could not open the weather plugin: ') + str(error), MessageBox.TYPE_ERROR)


def _set_text(source, value):
    value = value or ''
    try:
        source.setText(value)
    except Exception:
        source.text = value


class AIONextWeatherManager(object):
    """Refresh inline weather without making skin XML depend on WeatherPlugin."""
    INITIAL_DELAY = 4000
    REFRESH_INTERVAL = 30 * 60 * 1000
    RETRY_INTERVAL = 5 * 60 * 1000

    def __init__(self, session):
        self.session = session
        self.weatherData = None
        self.iconPath = ''
        self.timer = eTimer()
        try:
            self.timer.timeout.connect(self.refresh)
        except Exception:
            self.timer.callback.append(self.refresh)
        self._arm(self.INITIAL_DELAY)

    def _arm(self, milliseconds):
        try:
            self.timer.stop()
        except Exception:
            pass
        self.timer.start(int(milliseconds), True)

    def _source(self, name):
        try:
            return self.session.screen[name]
        except Exception:
            return None

    def _publish(self, city='', temp='', condition='', icon=''):
        for name, value in (
            (SOURCE_CITY, city),
            (SOURCE_TEMP, temp),
            (SOURCE_CONDITION, condition),
            (SOURCE_ICON, icon),
        ):
            source = self._source(name)
            if source is not None:
                _set_text(source, value)

    def _cancel(self):
        if self.weatherData is not None:
            try:
                self.weatherData.cancel()
            except Exception:
                pass
        self.weatherData = None

    def refresh(self):
        self._cancel()
        if not settings.weatherInline.value:
            self._publish()
            self._arm(self.REFRESH_INTERVAL)
            return

        # OpenATV/OE-Alliance Weather Plugin is the primary provider.  Importing
        # its plugin module initializes config.plugins.WeatherPlugin exactly as
        # the installed plugin expects; absence is handled without skin failure.
        try:
            from Plugins.Extensions.WeatherPlugin import plugin as weather_plugin
            from Plugins.Extensions.WeatherPlugin.MSNWeather import MSNWeather
        except Exception:
            self._publish()
            self._arm(self.RETRY_INTERVAL)
            return

        try:
            cfg = weather_plugin.config.plugins.WeatherPlugin
            count = int(cfg.entrycount.value)
            if count < 1 or len(cfg.Entry) < 1:
                self._publish(city=tr('Ustaw pogodę', 'Set weather'))
                self._arm(self.RETRY_INTERVAL)
                return
            entry = cfg.Entry[0]
            city = str(getattr(entry.city, 'value', '') or '')
            self._publish(city=city)
            self.iconPath = ''
            self.weatherData = MSNWeather()
            self.weatherData.getWeatherData(
                entry.degreetype.value,
                entry.weatherlocationcode.value,
                entry.city.value,
                self._weather_result,
                self._weather_icon,
            )
            # This also provides a timeout/retry if a provider request never
            # calls back. A later callback still updates the already-owned sources.
            self._arm(self.REFRESH_INTERVAL)
        except Exception:
            self._publish()
            self._arm(self.RETRY_INTERVAL)

    def _weather_icon(self, index, filename):
        if int(index) != -1:
            return
        self.iconPath = str(filename or '')
        source = self._source(SOURCE_ICON)
        if source is not None:
            _set_text(source, self.iconPath if os.path.exists(self.iconPath) else '')

    def _weather_result(self, result, errortext):
        data = self.weatherData
        if data is None:
            return
        if result != getattr(data, 'OK', 1):
            # Keep the configured city visible but remove stale measurements.
            try:
                city = str(data.city or '')
            except Exception:
                city = ''
            self._publish(city=city)
            self._arm(self.RETRY_INTERVAL)
            return
        try:
            item = data.weatherItems.get('-1')
            if item is None:
                self._arm(self.RETRY_INTERVAL)
                return
            city = str(data.city or '')
            temperature = str(getattr(item, 'temperature', '') or '').strip()
            degree = str(getattr(data, 'degreetype', '') or '').strip()
            temp = ('%s°%s' % (temperature, degree)) if temperature else ''
            condition = str(getattr(item, 'skytext', '') or '').strip()
            icon = str(getattr(item, 'iconFilename', '') or self.iconPath or '')
            if icon and not os.path.exists(icon):
                icon = ''
            self._publish(city=city, temp=temp, condition=condition, icon=icon)
            self._arm(self.REFRESH_INTERVAL)
        except Exception:
            self._arm(self.RETRY_INTERVAL)

    def stop(self):
        try:
            self.timer.stop()
        except Exception:
            pass
        self._cancel()


def start_weather_sources(session):
    """Install safe session sources before skin screens reference them."""
    if session is None or not hasattr(session, 'screen'):
        return
    for name in (SOURCE_CITY, SOURCE_TEMP, SOURCE_CONDITION, SOURCE_ICON):
        if name not in session.screen:
            session.screen[name] = StaticText('')
    manager = getattr(session, '_aioNextWeatherManager', None)
    if manager is None:
        manager = AIONextWeatherManager(session)
        session._aioNextWeatherManager = manager
