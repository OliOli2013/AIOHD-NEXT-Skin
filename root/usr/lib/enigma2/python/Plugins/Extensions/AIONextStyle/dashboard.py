# -*- coding: utf-8 -*-
"""Read-only live receiver information; no external processes, no network."""
from time import time, strftime, localtime
from os import statvfs
from enigma import eTimer
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from .settings import tr


def memory_snapshot(path='/proc/meminfo'):
    values = {}
    with open(path, 'r') as handle:
        for line in handle:
            name, _, value = line.partition(':')
            if name in ('MemTotal', 'MemAvailable', 'MemFree', 'Buffers', 'Cached'):
                values[name] = int(value.split()[0])
    total = values['MemTotal']
    free = values.get('MemAvailable', sum(values.get(k, 0) for k in ('MemFree', 'Buffers', 'Cached')))
    return max(0, total - free) // 1024, total // 1024


def disk_snapshot(path):
    fs = statvfs(path)
    return fs.f_bavail * fs.f_frsize / (1024 ** 3), fs.f_blocks * fs.f_frsize / (1024 ** 3)


class AIONextDashboard(Screen):
    skin = '''<screen name="AIONextDashboard" position="center,center" size="1500,850" title="AIOHD NEXT / Live Center" flags="wfNoBorder" backgroundColor="#000B111A">
      <eLabel position="0,0" size="1500,5" backgroundColor="#0034D6CF" />
      <eLabel text="NEXT / LIVE CENTER" position="38,28" size="970,68" font="Regular;42" foregroundColor="#00F2F5FA" backgroundColor="#000B111A" />
      <widget name="clock" position="1030,28" size="430,68" font="Regular;32" halign="right" foregroundColor="#0034D6CF" backgroundColor="#000B111A" />
      <eLabel position="38,118" size="920,300" backgroundColor="#00141E2A" zPosition="-1" />
      <eLabel text="01 / LIVE" position="64,136" size="860,40" font="Regular;24" foregroundColor="#0034D6CF" backgroundColor="#00141E2A" />
      <widget name="channel" position="64,184" size="860,54" font="Regular;36" foregroundColor="#00F2F5FA" backgroundColor="#00141E2A" noWrap="1" />
      <widget name="event" position="64,248" size="860,72" font="Regular;29" foregroundColor="#00F2F5FA" backgroundColor="#00141E2A" />
      <widget name="next" position="64,334" size="860,62" font="Regular;23" foregroundColor="#00ADBACA" backgroundColor="#00141E2A" />
      <eLabel position="978,118" size="484,300" backgroundColor="#00141E2A" zPosition="-1" />
      <eLabel text="02 / SIGNAL" position="1004,136" size="432,40" font="Regular;24" foregroundColor="#0034D6CF" backgroundColor="#00141E2A" />
      <widget name="signal" position="1004,186" size="432,200" font="Regular;30" foregroundColor="#00F2F5FA" backgroundColor="#00141E2A" />
      <eLabel position="38,438" size="920,300" backgroundColor="#00141E2A" zPosition="-1" />
      <eLabel text="03 / SYSTEM" position="64,456" size="860,40" font="Regular;24" foregroundColor="#0034D6CF" backgroundColor="#00141E2A" />
      <widget name="system" position="64,512" size="860,200" font="Regular;30" foregroundColor="#00F2F5FA" backgroundColor="#00141E2A" />
      <eLabel position="978,438" size="484,300" backgroundColor="#00141E2A" zPosition="-1" />
      <eLabel text="04 / MEDIA" position="1004,456" size="432,40" font="Regular;24" foregroundColor="#0034D6CF" backgroundColor="#00141E2A" />
      <widget name="media" position="1004,512" size="432,200" font="Regular;28" foregroundColor="#00F2F5FA" backgroundColor="#00141E2A" />
      <widget name="hint" position="38,772" size="1424,48" font="Regular;24" foregroundColor="#00ADBACA" backgroundColor="#000B111A" />
    </screen>'''

    def __init__(self, session):
        Screen.__init__(self, session)
        for name in ('clock', 'channel', 'event', 'next', 'signal', 'system', 'media'):
            self[name] = Label('—')
        self['hint'] = Label(tr('EXIT / Zamknij     •     OK / Odśwież     •     Dane aktualizowane co 5 sekund', 'EXIT / Close     •     OK / Refresh     •     Data refreshes every 5 seconds'))
        self['actions'] = ActionMap(['OkCancelActions'], {'cancel': self.close, 'ok': self.refresh}, -1)
        self.timer = eTimer()
        try:
            self.connection = self.timer.timeout.connect(self.refresh)
        except AttributeError:
            self.timer.callback.append(self.refresh)
        self.onShown.append(self.start)
        self.onHide.append(self.stop)
        self.onClose.append(self.stop)

    def start(self):
        self.refresh()
        self.timer.start(5000, False)

    def stop(self):
        self.timer.stop()

    def refresh(self):
        self['clock'].setText(strftime('%d.%m.%Y  %H:%M'))
        channel = event = next_event = signal = '—'
        try:
            service = self.session.nav.getCurrentService()
            if service is not None:
                info = service.info()
                if info is not None:
                    channel = info.getName() or '—'
                    current = info.getEvent(0)
                    if current:
                        event = current.getEventName() or '—'
                        duration = current.getDuration()
                        if duration > 0:
                            remaining = max(0, int((current.getBeginTime() + duration - time()) / 60))
                            event += '\n' + tr('Pozostało: %d min', 'Remaining: %d min') % remaining
                    following = info.getEvent(1)
                    if following:
                        next_event = strftime('%H:%M', localtime(following.getBeginTime())) + '  ' + following.getEventName()
                frontend = service.frontendInfo()
                if frontend is not None:
                    data = {}
                    try:
                        result = frontend.getFrontendStatus(data)
                    except TypeError:
                        result = frontend.getFrontendStatus()
                    if isinstance(result, dict):
                        data = result
                    if not isinstance(data, dict):
                        data = {}
                    # Frontend status SNR/AGC are native 16-bit values when available.
                    fields = []
                    for key, alias, title in (('tuner_signal_quality', 'snr', 'SNR'), ('tuner_signal_power', 'agc', 'AGC'), ('tuner_bit_error_rate', 'ber', 'BER')):
                        v = data.get(key, data.get(alias))
                        if isinstance(v, int) and v >= 0:
                            fields.append('%s   %s' % (title, str(v) if key == 'ber' else '%d%%' % min(100, v * 100 // 65535)))
                    if fields:
                        signal = '\n'.join(fields)
        except Exception:
            pass
        self['channel'].setText(channel)
        self['event'].setText(event)
        self['next'].setText(next_event)
        self['signal'].setText(signal if signal != '—' else tr('Brak danych DVB / IPTV', 'No DVB signal data / IPTV'))
        try:
            used, total = memory_snapshot()
            free, capacity = disk_snapshot('/')
            system = 'RAM   %d / %d MiB\nFLASH / ROOT   %.1f / %.1f GiB %s' % (used, total, free, capacity, tr('wolne', 'free'))
        except (OSError, ValueError, KeyError, IndexError):
            system = tr('Dane niedostępne', 'Data unavailable')
        self['system'].setText(system)
        try:
            count = len(self.session.nav.getRecordings())
            media = tr('Nagrania aktywne: %d', 'Active recordings: %d') % count
        except Exception:
            media = '—'
        self['media'].setText(media)
