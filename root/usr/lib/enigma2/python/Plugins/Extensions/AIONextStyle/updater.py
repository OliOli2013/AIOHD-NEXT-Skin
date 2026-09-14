# -*- coding: utf-8 -*-
"""Small GitHub Release updater used by the AIOHD NEXT settings plugin.

The updater never installs anything automatically.  It only returns a newer
release to the UI; installation starts after an explicit Yes/No confirmation.
"""
from __future__ import absolute_import

import json
import re
import shlex
import ssl

try:
    from urllib.request import Request, urlopen
except ImportError:  # pragma: no cover - AIOHD NEXT itself requires Python 3
    from urllib2 import Request, urlopen

CURRENT_PACKAGE_VERSION = '3.2.1-r4'
RELEASES_API = 'https://api.github.com/repos/OliOli2013/AIOHD-NEXT-Skin/releases/latest'
DOWNLOAD_PREFIX = 'https://github.com/OliOli2013/AIOHD-NEXT-Skin/releases/download/'
_PACKAGE_RE = re.compile(r'^enigma2-plugin-skins-aiohd-next_[0-9]+\.[0-9]+\.[0-9]+-r[0-9]+_all\.ipk$')
_VERSION_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-?r(\d+))?$')


def version_tuple(value):
    """Return a comparable (major, minor, patch, revision) tuple."""
    match = _VERSION_RE.match((value or '').strip())
    if not match:
        raise ValueError('unsupported version: %s' % value)
    major, minor, patch, revision = match.groups()
    return int(major), int(minor), int(patch), int(revision or 0)


def is_newer(candidate, current=CURRENT_PACKAGE_VERSION):
    return version_tuple(candidate) > version_tuple(current)


def _read_json(context=None, timeout=8):
    request = Request(RELEASES_API, headers={
        'User-Agent': 'AIOHD-NEXT/%s' % CURRENT_PACKAGE_VERSION,
        'Accept': 'application/vnd.github+json',
    })
    response = urlopen(request, timeout=timeout, context=context) if context is not None else urlopen(request, timeout=timeout)
    try:
        raw = response.read(262144)
    finally:
        try:
            response.close()
        except Exception:
            pass
    if not isinstance(raw, str):
        raw = raw.decode('utf-8', 'replace')
    return json.loads(raw)


def fetch_latest(timeout=8):
    """Return {'version', 'url', 'name'} for a newer stable release or None."""
    try:
        data = _read_json(timeout=timeout)
    except Exception:
        # Older Enigma2 images occasionally have an outdated CA store.  GitHub
        # is still pinned below by exact host/path validation before install.
        data = _read_json(context=ssl._create_unverified_context(), timeout=timeout)

    if data.get('draft') or data.get('prerelease'):
        return None
    tag = str(data.get('tag_name') or '').strip()
    if not tag or not is_newer(tag):
        return None

    for asset in data.get('assets') or []:
        name = str(asset.get('name') or '')
        url = str(asset.get('browser_download_url') or '')
        if _PACKAGE_RE.match(name) and url.startswith(DOWNLOAD_PREFIX) and url.endswith('/' + name):
            return {'version': tag, 'url': url, 'name': name}
    return None


def installer_command(url):
    """Build the only shell command accepted by the updater."""
    url = str(url or '').strip()
    name = url.rsplit('/', 1)[-1]
    if not url.startswith(DOWNLOAD_PREFIX) or not _PACKAGE_RE.match(name):
        raise ValueError('unexpected update URL')
    quoted = shlex.quote(url)
    status = '/tmp/aiohd-next-update.status'
    return (
        'rm -f {status} /tmp/aiohd-next-update.ipk; '
        'wget -q --no-check-certificate {url} -O /tmp/aiohd-next-update.ipk '
        '&& opkg install /tmp/aiohd-next-update.ipk '
        '&& rm -f /tmp/aiohd-next-update.ipk '
        '&& echo OK > {status} '
        '|| {{ rc=$?; rm -f /tmp/aiohd-next-update.ipk; echo FAIL:$rc > {status}; exit $rc; }}'
    ).format(status=status, url=quoted)
