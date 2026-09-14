"""Local, atomic palette updates; no network requests or background services."""
import os
import re
import tempfile
import xml.etree.ElementTree as ET

PALETTES = {
    'aurora': ('#0034D6CF', '#00195759'),
    'amber': ('#00F6C56C', '#0060441F'),
    'violet': ('#00BCABFF', '#00483C70'),
}
ACCENTS = {'nextAccent', 'infobaraccent1', 'infobarprogress', 'layer-a-accent1',
           'layer-b-accent1', 'layer-a-progress', 'layer-a-underline',
           'scrollbarSlidercolor', 'layer-a-channelselection-progressbar'}
STRONG_SELECTIONS = {'aurora': '#00007678', 'amber': '#00805412', 'violet': '#006C4A9A'}
SELECTIONS = {'nextAccentDim', 'layer-a-selection-background',
              'layer-b-selection-background'}

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

def apply_palette(path, key):
    if key not in PALETTES:
        raise ValueError('Unknown palette')
    with open(path, 'rb') as stream:
        original = stream.read()
    root = ET.fromstring(original)
    if root.tag != 'skin' or root.find("./colors/color[@name='nextAccent']") is None:
        raise ValueError('AIOHD NEXT 3.1 skin.xml is required')
    accent, selected = PALETTES[key]
    text = original.decode('utf-8')
    changes = [0]
    def replace(match):
        tag = match.group(0)
        item = ET.fromstring(tag)
        name = item.get('name')
        new = STRONG_SELECTIONS[key] if name == 'nextSelection' else accent if name in ACCENTS else selected if name in SELECTIONS else None
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
