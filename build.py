#!/usr/bin/env python3
"""Build a portable opkg IPK using only the Python standard library."""
import ast
import gzip
import hashlib
import io
from pathlib import Path
import tarfile
import textwrap
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'root'
CONTROL = BASE / 'control'


def archive(folder, extra=None):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.GNU_FORMAT) as tar:
        for path in sorted(folder.rglob('*')):
            if '__pycache__' in path.parts or path.suffix == '.pyc' or path.name == 'md5sums':
                continue
            name = './' + path.relative_to(folder).as_posix()
            if extra and path.name in extra:
                continue
            info = tar.gettarinfo(str(path), arcname=name)
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = 'root'
            if path.is_dir():
                info.mode = 0o755
            else:
                info.mode = 0o755 if path.name in ('postinst', 'preinst', 'prerm', 'postrm') else 0o644
            if path.is_file():
                with path.open('rb') as stream:
                    tar.addfile(info, stream)
            else:
                tar.addfile(info)
        for name, payload in (extra or {}).items():
            info = tarfile.TarInfo('./' + name)
            info.size = len(payload)
            info.mode = 0o644
            info.uname = info.gname = 'root'
            tar.addfile(info, io.BytesIO(payload))
    return gzip.compress(buffer.getvalue(), mtime=0)


def build():
    for path in ROOT.rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    for path in ROOT.rglob('*.xml'):
        root = ET.parse(path).getroot()
        for applet in root.iter('applet'):
            compile(textwrap.dedent(applet.text or '').strip(), str(path), 'exec')
    control = (CONTROL / 'control').read_text()
    fields = dict(line.split(': ', 1) for line in control.splitlines() if ': ' in line and not line.startswith(' '))
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    sums = ''.join(hashlib.md5(p.read_bytes()).hexdigest() + '  ' + p.relative_to(ROOT).as_posix() + '\n' for p in files)
    control = '\n'.join(line for line in control.splitlines() if not line.startswith('Installed-Size:')) + '\n'
    control += 'Installed-Size: %d\n' % ((sum(p.stat().st_size for p in files) + 1023) // 1024)
    members = [('debian-binary', b'2.0\n'), ('control.tar.gz', archive(CONTROL, {'control': control.encode(), 'md5sums': sums.encode()})), ('data.tar.gz', archive(ROOT))]
    output = BASE / 'dist' / ('%s_%s_%s.ipk' % (fields['Package'], fields['Version'], fields['Architecture']))
    output.parent.mkdir(exist_ok=True)
    with output.open('wb') as stream:
        stream.write(b'!<arch>\n')
        for name, data in members:
            header = '%-16s%-12s%-6s%-6s%-8s%-10s`\n' % (name + '/', '0', '0', '0', '100644', str(len(data)))
            stream.write(header.encode('ascii')); stream.write(data)
            if len(data) % 2:
                stream.write(b'\n')
    with tarfile.open(fileobj=io.BytesIO(members[2][1]), mode='r:gz') as tar:
        for line in sums.splitlines():
            digest, name = line.split('  ', 1)
            assert hashlib.md5(tar.extractfile('./' + name).read()).hexdigest() == digest
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix('.ipk.sha256').write_text(digest + '  ' + output.name + '\n')
    print(output)
    print('Verified %d file checksums; SHA256 %s' % (len(files), digest))
    return output


if __name__ == '__main__':
    build()
