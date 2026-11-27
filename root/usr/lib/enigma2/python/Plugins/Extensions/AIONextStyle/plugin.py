# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.config import ConfigSelection, ConfigYesNo, getConfigListEntry, configfile
from threading import Thread
from twisted.internet import reactor
from .theme import PALETTE_CHOICES, current_palette, current_surface, apply_palette
from .settings import settings, tr
from .weather import weather_plugins, preferred_weather_key, open_weather, start_weather_sources
from .updater import CURRENT_PACKAGE_VERSION, fetch_latest, installer_command, installed_version

SKIN_PATH = '/usr/share/enigma2/AIOHD/skin.xml'


class AIONextStyle(Screen, ConfigListScreen):
    skin = '''<screen name="AIONextStyle" position="center,center" size="1360,800" title="AIOHD NEXT 4.0.0" backgroundColor="#000B111A">
      <eLabel position="0,0" size="1360,6" backgroundColor="#0034D6CF" />
      <widget name="heading" position="44,30" size="1272,56" font="Regular;36" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
      <widget name="config" position="44,122" size="1272,336" itemHeight="48" font="Regular;30" backgroundColor="#00141E2A" foregroundColor="#00F2F5FA" backgroundColorSelected="#00007678" foregroundColorSelected="#00FFFFFF" scrollbarMode="showOnDemand" />
      <widget name="update_status" position="44,470" size="1272,38" font="Regular;22" foregroundColor="#006BE3A2" backgroundColor="#000B111A" />
      <widget name="description" position="44,520" size="1272,150" font="Regular;23" foregroundColor="#00ADBACA" backgroundColor="#000B111A" />
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
        self.setTitle('AIOHD NEXT 4.0.0')
        self['heading'] = Label(tr('AIOHD NEXT — wygląd i pogoda', 'AIOHD NEXT — appearance and weather'))
        self['key_red'] = Label(tr('Anuluj', 'Cancel'))
        self['key_green'] = Label(tr('Zapisz', 'Save'))
        self.showAllPlugins = False
        self['key_yellow'] = Label(tr('Wszystkie wtyczki', 'All plugins'))
        self['key_blue'] = Label(tr('Otwórz pogodę', 'Open weather'))
        self['update_status'] = Label(tr('Aktualizacja: sprawdzanie…', 'Update: checking…'))
        self._update_check_started = False
        self._offered_release = None
        self._closed = False
        self['description'] = Label(tr(
            'Standard: 32 px / 18 kanałów. Duża: 38 px / 15 kanałów. Bardzo duża: 42 px / 14 kanałów.\nPogoda inline: Auto: Weather Plugin, następnie OpenATV / MetrixWeather. Cinema Glass zmienia przezroczystość paneli TV.\nWybrana niżej wtyczka jest skrótem do pełnego ekranu i nie musi być źródłem danych inline.',
            'Standard: 32 px / 18 channels. Large: 38 px / 15 channels. Extra large: 42 px / 14 channels.\nInline weather: Auto: Weather Plugin, then OpenATV / MetrixWeather. Cinema Glass changes TV dock opacity.\nThe plugin selected below is a launcher for its full screen and does not have to be the inline data provider.'))
        self.palette = ConfigSelection(default=current_palette(SKIN_PATH), choices=PALETTE_CHOICES)
        self.surface = ConfigSelection(default=current_surface(SKIN_PATH), choices=[('studio', 'Studio'), ('oled', 'OLED Black'), ('cinema', 'Cinema Glass')])
        self.listSize = ConfigSelection(default=settings.listSize.value, choices=[('standard', tr('Standard — 18 kanałów', 'Standard — 18 channels')), ('large', tr('Duża — 15 kanałów', 'Large — 15 channels')), ('xlarge', tr('Bardzo duża — 14 kanałów', 'Extra large — 14 channels'))])
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
            getConfigListEntry(tr('Tryb powierzchni', 'Surface mode'), self.surface),
            getConfigListEntry(tr('Czcionka listy kanałów', 'Channel list font'), self.listSize),
            getConfigListEntry(tr('Pogoda bezpośrednio w skinie', 'Inline weather in skin'), self.weatherInline),
            getConfigListEntry(tr('Źródło danych pogody', 'Inline weather provider'), self.weatherProvider),
            getConfigListEntry(tr('Skrót do pełnej wtyczki pogody', 'Weather plugin shortcut'), self.weatherEnabled),
            getConfigListEntry(tr('Wtyczka pogody', 'Weather plugin'), self.weatherPlugin)
        ], session=session)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.close, 'red': self.close, 'green': self.saveStyle, 'ok': self.saveStyle, 'blue': self.previewWeather, 'yellow': self.togglePluginList}, -2)
        self.onLayoutFinish.append(self._start_update_check)
        self.onClose.append(self._mark_closed)

    def _mark_closed(self):
        self._closed = True

    def _start_update_check(self):
        if self._update_check_started:
            return
        self._update_check_started = True
        Thread(target=self._update_worker, name='AIONextUpdateCheck', daemon=True).start()

    def _update_worker(self):
        try:
            release = fetch_latest()
            error = None
        except Exception as exc:
            release = None
            error = str(exc)
        try:
            reactor.callFromThread(self._finish_update_check, release, error)
        except Exception:
            # The screen is still fully usable if the network/update check fails.
            pass

    def _finish_update_check(self, release, error=None):
        if self._closed:
            return
        if error:
            self['update_status'].setText(tr(
                'Aktualizacja: nie udało się sprawdzić (ustawienia działają normalnie)',
                'Update: check failed (settings still work normally)'))
            return
        if not release:
            self['update_status'].setText(tr(
                'Aktualizacja: masz najnowszą wersję %s' % installed_version(),
                'Update: you have the latest version %s' % installed_version()))
            return
        self._offered_release = release
        self['update_status'].setText(tr(
            'Dostępna aktualizacja: %s' % release['version'],
            'Update available: %s' % release['version']))
        self.session.openWithCallback(
            self._update_answer,
            MessageBox,
            tr(
                'Dostępna jest aktualizacja AIOHD NEXT %s.\nZainstalować ją teraz?\n\nPo instalacji wymagany będzie restart GUI.' % release['version'],
                'AIOHD NEXT %s is available.\nInstall it now?\n\nA GUI restart will be required after installation.' % release['version']),
            MessageBox.TYPE_YESNO,
            default=False)

    def _update_answer(self, answer):
        if self._closed or not answer or not self._offered_release:
            return
        try:
            command = installer_command(self._offered_release['url'], self._offered_release.get('digest'))
        except Exception as exc:
            self.session.open(MessageBox, tr('Nieprawidłowe dane aktualizacji: ', 'Invalid update data: ') + str(exc), MessageBox.TYPE_ERROR)
            return
        self['update_status'].setText(tr('Aktualizacja: instalowanie…', 'Update: installing…'))
        self.session.openWithCallback(
            self._after_update_command,
            Console,
            title=tr('Aktualizacja AIOHD NEXT', 'AIOHD NEXT update'),
            cmdlist=[command],
            closeOnSuccess=True)

    def _after_update_command(self):
        if self._closed:
            return
        status = ''
        try:
            with open('/tmp/aiohd-next-update.status', 'r') as handle:
                status = handle.read().strip()
        except Exception:
            pass
        if status == 'OK':
            self['update_status'].setText(tr('Aktualizacja: zainstalowana — wymagany restart GUI', 'Update: installed — GUI restart required'))
            self.session.openWithCallback(
                self._restart_after_update,
                MessageBox,
                tr('Aktualizacja AIOHD NEXT została zainstalowana.\nUruchomić ponownie GUI teraz?', 'AIOHD NEXT update was installed.\nRestart the GUI now?'),
                MessageBox.TYPE_YESNO,
                default=False)
        else:
            self['update_status'].setText(tr('Aktualizacja: instalacja nie powiodła się', 'Update: installation failed'))
            self.session.open(MessageBox, tr('Aktualizacja nie została zainstalowana. Sprawdź wynik w oknie poleceń.', 'The update was not installed. Check the command window for details.'), MessageBox.TYPE_ERROR)

    def _restart_after_update(self, answer):
        if answer:
            self.session.open(TryQuitMainloop, 3)

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
        restart_needed = (self.listSize.value != settings.listSize.value or
                          self.weatherEnabled.value != settings.weatherEnabled.value or
                          self.weatherInline.value != settings.weatherInline.value or
                          self.weatherProvider.value != settings.weatherProvider.value)
        try:
            restart_needed = apply_palette(SKIN_PATH, self.palette.value, self.surface.value) or restart_needed
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


def dashboard_main(session, **kwargs):
    from .dashboard import AIONextDashboard
    session.open(AIONextDashboard)


def weather_main(session, **kwargs):
    open_weather(session)


def sessionstart(reason, **kwargs):
    if reason == 0:
        start_weather_sources(kwargs.get('session'))


def Plugins(**kwargs):
    result = [
        PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart),
        PluginDescriptor(name='AIOHD NEXT — Live Center', description=tr('Kanał, EPG i stan odbiornika', 'Channel, EPG and receiver status'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=dashboard_main),
        PluginDescriptor(name='AIOHD NEXT — Style', description=tr('Wygląd, większe czcionki i pogoda', 'Appearance, larger fonts and weather'), where=PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main),
    ]
    if settings.weatherEnabled.value:
        result.append(PluginDescriptor(name=tr('AIOHD NEXT — Pogoda', 'AIOHD NEXT — Weather'), description=tr('Otwórz wybraną wtyczkę pogody', 'Open selected weather plugin'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=weather_main))
    return result
