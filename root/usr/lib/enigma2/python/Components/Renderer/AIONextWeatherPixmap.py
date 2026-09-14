# -*- coding: utf-8 -*-
"""Pixmap renderer for an icon path supplied by AIOHD NEXT weather sources."""
import os

from Components.Renderer.Renderer import Renderer
from Tools.LoadPixmap import LoadPixmap
from enigma import ePixmap, BT_SCALE, BT_KEEP_ASPECT_RATIO


class AIONextWeatherPixmap(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self._filename = ''

    def changed(self, what):
        if not self.instance:
            return
        if what[0] == self.CHANGED_CLEAR:
            self._set_pixmap('')
            return
        filename = str(getattr(self.source, 'text', '') or '')
        self._set_pixmap(filename)

    def _set_pixmap(self, filename):
        if filename == self._filename:
            return
        self._filename = filename
        if not filename or not os.path.exists(filename):
            try:
                self.instance.setPixmap(None)
            except Exception:
                pass
            return
        try:
            pixmap = LoadPixmap(filename)
            try:
                self.instance.setPixmapScale(BT_SCALE | BT_KEEP_ASPECT_RATIO)
            except Exception:
                self.instance.setScale(1)
            self.instance.setPixmap(pixmap)
        except Exception:
            try:
                self.instance.setPixmap(None)
            except Exception:
                pass
