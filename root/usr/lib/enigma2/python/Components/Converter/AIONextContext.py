# -*- coding: utf-8 -*-
"""EPG progress from actual begin/duration; no network or global hooks."""
from time import time
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached


def event_percent(begin, duration, now):
    if duration <= 0 or now < begin or now >= begin + duration:
        return None
    return max(0, min(100, int((now - begin) * 100 / duration)))


class AIONextContext(Poll, Converter):
    def __init__(self, argument):
        Converter.__init__(self, argument)
        Poll.__init__(self)
        self.poll_interval = 15000
        self.poll_enabled = True

    @cached
    def getText(self):
        try:
            event = self.source.event
            if event is not None:
                value = event_percent(event.getBeginTime(), event.getDuration(), time())
                if value is not None:
                    return '%d%%' % value
        except Exception:
            pass
        return '—'

    text = property(getText)
