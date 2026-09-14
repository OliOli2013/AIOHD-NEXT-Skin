# -*- coding: utf-8 -*-
"""Four upcoming events for the highlighted service, with bounded shared cache."""
from time import time, localtime, strftime
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from Components.config import config
from enigma import eEPGCache

_CACHE = {}


def upcoming(cache, reference, now):
    key = (reference, int(now) // 15)
    if key in _CACHE:
        return _CACHE[key]
    # One query keeps event IDs, start times, durations and titles together.
    rows = cache.lookupEvent(['IBDT', (reference, 0, int(now), 10080)]) or []
    events, seen = [], set()
    for row in rows:
        if len(row) < 4:
            continue
        event_id, begin, duration, title = row[:4]
        if not isinstance(begin, (int, float)) or begin <= now or not title:
            continue
        identity = (event_id, begin)
        if identity not in seen:
            seen.add(identity)
            events.append((begin, str(title).replace('\n', ' ').strip()))
    events.sort(key=lambda event: event[0])
    result = events[:4]
    if len(_CACHE) >= 32:
        _CACHE.clear()
    _CACHE[key] = result
    return result


class AIONextEvent(Poll, Converter):
    def __init__(self, argument):
        Converter.__init__(self, argument)
        Poll.__init__(self)
        try:
            self.offset = max(1, min(4, int(argument)))
        except (TypeError, ValueError):
            self.offset = 1
        self.poll_interval = 15000
        self.poll_enabled = True

    @cached
    def getText(self):
        try:
            service = getattr(self.source, 'service', None)
            cache = eEPGCache.getInstance()
            if service is None or cache is None:
                return ''
            reference = service.toString()
            if not reference:
                return ''
            now = time()
            events = upcoming(cache, reference, now)
            if len(events) < self.offset:
                if self.offset == 1:
                    return ('Brak kolejnych audycji w EPG' if config.osd.language.value.startswith('pl')
                            else 'No upcoming events in EPG')
                return '\u2014'
            begin, title = events[self.offset - 1]
            fmt = '%H:%M' if localtime(now)[:3] == localtime(begin)[:3] else '%d.%m %H:%M'
            return '%s  %s' % (strftime(fmt, localtime(begin)), title)
        except Exception:
            # Invalid provider EPG must not prevent opening the channel list.
            return ''

    text = property(getText)
