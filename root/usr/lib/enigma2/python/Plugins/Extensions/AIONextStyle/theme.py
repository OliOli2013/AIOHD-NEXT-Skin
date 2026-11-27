"""Local, atomic palette updates; no network requests or background services."""
import os
import re
import tempfile
import xml.etree.ElementTree as ET

PALETTES = {
    'aurora': ('#0034D6CF', '#00195759'),
    'amber': ('#00F6C56C', '#0060441F'),
    'violet': ('#00BCABFF', '#00483C70'),
    # Less common palettes chosen to stay readable on dark OpenATV layers.
    'petrol': ('#0020B7A6', '#00184346'),
    'copper': ('#00D99058', '#004A2D21'),
    'jade': ('#0059D39A', '#001C4A37'),
    'sakura': ('#00E07BA4', '#00472B38'),
    'ice': ('#008ACBFF', '#00243E59'),
    'lime': ('#00C8E879', '#003D4A24'),
}
PALETTE_CHOICES = [
    ('aurora', 'Aurora'),
    ('amber', 'Amber'),
    ('violet', 'Violet'),
    ('petrol', 'Petrol'),
    ('copper', 'Copper'),
    ('jade', 'Jade'),
    ('sakura', 'Sakura'),
    ('ice', 'Ice'),
    ('lime', 'Lime'),
]
ACCENTS = {'nextAccent', 'infobaraccent1', 'infobarprogress', 'layer-a-accent1',
           'layer-b-accent1', 'layer-a-progress', 'layer-a-underline',
           'scrollbarSlidercolor', 'layer-a-channelselection-progressbar'}
STRONG_SELECTIONS = {
    'aurora': '#00007678',
    'amber': '#00805412',
    'violet': '#006C4A9A',
    'petrol': '#00505F5B',
    'copper': '#00713E22',
    'jade': '#002E6B50',
    'sakura': '#00733B52',
    'ice': '#003D6085',
    'lime': '#00515D22',
}
SELECTIONS = {'nextAccentDim', 'layer-a-selection-background',
              'layer-b-selection-background'}

SURFACES = {
    'studio': ('#000B111A', '#00141E2A', '#00192330', '#00141E2A'),
    'oled': ('#00000000', '#00090909', '#00121212', '#00090909'),
    'cinema': ('#000B111A', '#00141E2A', '#00192330', '#60101824'),
}
SURFACE_NAMES = ('nextBg', 'nextCard', 'nextCardHi', 'nextDock')


def current_surface(path):
    try:
        root = ET.parse(path).getroot()
        values = tuple(root.find("./colors/color[@name='%s']" % name).get('value').upper() for name in SURFACE_NAMES)
        for key, palette in SURFACES.items():
            if values == palette:
                return key
    except (OSError, ET.ParseError, AttributeError):
        pass
    return 'studio'


def current_palette(path):
    try:
        root = ET.parse(path).getroot()
        value = root.find("./colors/color[@name='nextAccent']").get('value').upper()
        for key, pair in PALETTES.items():
            if pair[0].upper() == value:
                return key
    except (OSError, ET.ParseError, AttributeError):
        pass
    return 'aurora'

def atomic_write(path, payload, mode=0o644):
    directory = os.path.dirname(os.path.abspath(path))
    fd, temp = tempfile.mkstemp(prefix='.aio-next-', dir=directory)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)

def apply_palette(path, key, surface=None):
    if key not in PALETTES:
        raise ValueError('Unknown palette')
    with open(path, 'rb') as stream:
        original = stream.read()
    root = ET.fromstring(original)
    if root.tag != 'skin' or root.find("./colors/color[@name='nextAccent']") is None:
        raise ValueError('AIOHD NEXT 4.0.0 skin.xml is required')
    accent, selected = PALETTES[key]
    surfaces = dict(zip(SURFACE_NAMES, SURFACES[surface or current_surface(path)]))
    if (surface or current_surface(path)) == 'oled':
        surfaces.update({'background': '#00000000', 'layer-a-background': '#00000000', 'layer-b-background': '#00090909', 'title-background': '#00090909'})
    elif surface:
        surfaces.update({'background': '#000B111A', 'layer-a-background': '#000B111A', 'layer-b-background': '#00141E2A', 'title-background': '#000E1C2C'})
    text = original.decode('utf-8')
    changes = [0]
    def replace(match):
        tag = match.group(0)
        item = ET.fromstring(tag)
        name = item.get('name')
        new = STRONG_SELECTIONS[key] if name == 'nextSelection' else accent if name in ACCENTS else selected if name in SELECTIONS else None
        new = surfaces.get(name, new)
        if new is None:
            return tag
        changes[0] += 1
        return re.sub(r'value\s*=\s*([\"\']).*?\1', 'value="%s"' % new, tag)
    changed = re.sub(r'<color\b[^<>]*/>', replace, text)
    ET.fromstring(changed)
    if changes[0] < 2:
        raise ValueError('Palette entries not found')
    payload = changed.encode('utf-8')
    if payload == original:
        return False
    # The previous XML is recoverable even if writing the new one fails.
    atomic_write(path + '.before-style', original)
    atomic_write(path, payload)
    return True
