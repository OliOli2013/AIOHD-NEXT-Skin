# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.config import ConfigSelection, ConfigYesNo, getConfigListEntry, configfile
from .theme import current_palette, apply_palette
from .settings import settings, tr
from .weather import weather_plugins, preferred_weather_key, open_weather, start_weather_sources

SKIN_PATH = '/usr/share/enigma2/AIOHD/skin.xml'


class AIONextStyle(Screen, ConfigListScreen):
    skin = '''<screen name="AIONextStyle" position="center,center" size="1360,800" title="AIOHD NEXT 3.2.1" backgroundColor="#000B111A">
      <eLabel position="0,0" size="1360,6" backgroundColor="#0034D6CF" />
      <widget name="heading" position="44,30" size="1272,56" font="Regular;36" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
      <widget name="config" position="44,122" size="1272,348" itemHeight="56" font="Regular;30" backgroundColor="#00141E2A" foregroundColor="#00F2F5FA" backgroundColorSelected="#00007678" foregroundColorSelected="#00FFFFFF" scrollbarMode="showOnDemand" />
      <widget name="description" position="44,488" size="1272,182" font="Regular;24" foregroundColor="#00ADBACA" backgroundColor="#000B111A" />
      <eLabel position="44,714" size="6,30" backgroundColor="#00FF5A68" />
      <widget name="key_red" position="62,704" size="280,48" font="Regular;27" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
      <eLabel position="362,714" size="6,30" backgroundColor="#006BE3A2" />
      <widget name="key_green" position="380,704" size="280,48" font="Regular;27" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
      <eLabel position="998,714" size="6,30" backgroundColor="#004CA3FF" />
      <widget name="key_blue" position="1016,704" size="280,48" font="Regular;27" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
      <eLabel position="680,714" size="6,30" backgroundColor="#00F6C56C" />
      <widget name="key_yellow" position="698,704" size="292,48" font="Regular;25" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
    </screen>''' 

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setTitle('AIOHD NEXT 3.2.1')
        self['heading'] = Label(tr('AIOHD NEXT — wygląd i pogoda', 'AIOHD NEXT — appearance and weather'))
        self['key_red'] = Label(tr('Anuluj', 'Cancel'))
        self['key_green'] = Label(tr('Zapisz', 'Save'))
        self.showAllPlugins = False
        self['key_yellow'] = Label(tr('Wszystkie wtyczki', 'All plugins'))
        self['key_blue'] = Label(tr('Otwórz pogodę', 'Open weather'))
        self['description'] = Label(tr(
            'Duża: pogrubione nazwy 38 px, 15 wierszy. Bardzo duża: 42 px, 14 wierszy.\nPogoda inline: Auto najpierw używa aktualnego backendu OpenATV / MetrixWeather, potem Weather Plugin.\nWybrana niżej wtyczka jest skrótem do pełnego ekranu i nie musi być źródłem danych inline.',
            'Large: bold 38 px channel names, 15 rows. Extra large: 42 px, 14 rows.\nInline weather: Auto first uses the current OpenATV / MetrixWeather backend, then Weather Plugin.\nThe plugin selected below is a launcher for its full screen and does not have to be the inline data provider.'))
        self.palette = ConfigSelection(default=current_palette(SKIN_PATH), choices=[('aurora', 'Aurora'), ('amber', 'Amber'), ('violet', 'Violet')])
        self.listSize = ConfigSelection(default=settings.listSize.value, choices=[('large', tr('Duża', 'Large')), ('xlarge', tr('Bardzo duża', 'Extra large'))])
        self.weatherInline = ConfigYesNo(default=settings.weatherInline.value)
        self.weatherProvider = ConfigSelection(default=settings.weatherProvider.value, choices=[
            ('auto', tr('Automatycznie (OpenATV)', 'Automatic (OpenATV)')),
            ('metrix', 'OpenATV / MetrixWeather'),
            ('weatherplugin', 'Weather Plugin'),
        ])
        self.weatherEnabled = ConfigYesNo(default=settings.weatherEnabled.value)
        found = weather_plugins()
        if settings.weatherPlugin.value and settings.weatherPlugin.value not in [p[0] for p in found]:
            found.extend(p for p in weather_plugins(show_all=True) if p[0] == settings.weatherPlugin.value)
        choices = [(key, name) for key, name, descriptor in found]
        if not choices:
            choices = [('', tr('Brak zainstalowanej wtyczki pogody', 'No installed weather plugin found'))]
        default = settings.weatherPlugin.value or preferred_weather_key(found)
        if default and default not in [key for key, name in choices]:
            choices.append((default, tr('Poprzednio wybrana — niedostępna', 'Previously selected — unavailable')))
        self.weatherPlugin = ConfigSelection(default=default if default in [key for key, name in choices] else choices[0][0], choices=choices)
        ConfigListScreen.__init__(self, [
            getConfigListEntry(tr('Kolor przewodni', 'Accent colour'), self.palette),
            getConfigListEntry(tr('Czcionka listy kanałów', 'Channel list font'), self.listSize),
            getConfigListEntry(tr('Pogoda bezpośrednio w skinie', 'Inline weather in skin'), self.weatherInline),
            getConfigListEntry(tr('Źródło danych pogody', 'Inline weather provider'), self.weatherProvider),
            getConfigListEntry(tr('Skrót do pełnej wtyczki pogody', 'Weather plugin shortcut'), self.weatherEnabled),
            getConfigListEntry(tr('Wtyczka pogody', 'Weather plugin'), self.weatherPlugin)
        ], session=session)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.close, 'red': self.close, 'green': self.saveStyle, 'ok': self.saveStyle, 'blue': self.previewWeather, 'yellow': self.togglePluginList}, -2)

    def togglePluginList(self):
        self.showAllPlugins = not self.showAllPlugins
        selected = self.weatherPlugin.value
        entries = weather_plugins(show_all=self.showAllPlugins)
        choices = [(key, name) for key, name, descriptor in entries]
        if not choices:
            choices = [('', tr('Brak dostępnych wtyczek', 'No available plugins'))]
        self.weatherPlugin.setChoices(choices, default=selected if selected in [x[0] for x in choices] else choices[0][0])
        self['key_yellow'].setText(tr('Tylko pogodowe', 'Weather only') if self.showAllPlugins else tr('Wszystkie wtyczki', 'All plugins'))
        self['config'].invalidateCurrent()

    def previewWeather(self):
        open_weather(self.session, self.weatherPlugin.value)

    def saveStyle(self):
        # Missing weather software must never block saving unrelated skin options.
        # The inline sources stay empty until a supported provider is configured.
        restart_needed = (self.weatherEnabled.value != settings.weatherEnabled.value or
                          self.weatherInline.value != settings.weatherInline.value or
                          self.weatherProvider.value != settings.weatherProvider.value)
        try:
            restart_needed = apply_palette(SKIN_PATH, self.palette.value) or restart_needed
            settings.listSize.value = self.listSize.value
            settings.weatherInline.value = self.weatherInline.value
            settings.weatherProvider.value = self.weatherProvider.value
            settings.weatherEnabled.value = self.weatherEnabled.value
            settings.weatherPlugin.value = self.weatherPlugin.value
            settings.save()
            configfile.save()
        except Exception as error:
            self.session.open(MessageBox, tr('Nie udało się zapisać ustawień: ', 'Could not save settings: ') + str(error), MessageBox.TYPE_ERROR)
            return
        if restart_needed:
            self.session.openWithCallback(self.restart, MessageBox, tr('Ustawienia zapisane. Uruchomić ponownie GUI?\nW czasie nagrywania wybierz Nie.', 'Settings saved. Restart the GUI?\nChoose No while recording.'), MessageBox.TYPE_YESNO, default=False)
        else:
            self.close()

    def restart(self, answer):
        if answer:
            self.session.open(TryQuitMainloop, 3)
        self.close()


def main(session, **kwargs):
    session.open(AIONextStyle)


def weather_main(session, **kwargs):
    open_weather(session)


def sessionstart(reason, **kwargs):
    if reason == 0:
        start_weather_sources(kwargs.get('session'))


def Plugins(**kwargs):
    result = [
        PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart),
        PluginDescriptor(name='AIOHD NEXT — Style', description=tr('Wygląd, większe czcionki i pogoda', 'Appearance, larger fonts and weather'), where=PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main),
    ]
    if settings.weatherEnabled.value:
        result.append(PluginDescriptor(name=tr('AIOHD NEXT — Pogoda', 'AIOHD NEXT — Weather'), description=tr('Otwórz wybraną wtyczkę pogody', 'Open selected weather plugin'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=weather_main))
    return result
