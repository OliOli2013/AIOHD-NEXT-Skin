# -*- coding: utf-8 -*-
"""GitHub Release updater used by the AIOHD NEXT settings plugin.

The updater never installs anything automatically. It only reports a newer
stable release to the UI; installation starts after explicit user approval.

Important: the installed package version is read from opkg on every check.
This prevents a just-installed release from being offered again while Enigma2
is still running in the same GUI session.
"""
from __future__ import absolute_import

import json
import re
import shlex
import ssl
import subprocess

try:
    from urllib.request import Request, urlopen
except ImportError:  # pragma: no cover - AIOHD NEXT requires Python 3
    from urllib2 import Request, urlopen

PACKAGE_NAME = 'enigma2-plugin-skins-aiohd-next'
CURRENT_PACKAGE_VERSION = '3.2.1-r5'  # safe fallback if opkg status is unavailable
RELEASES_API = 'https://api.github.com/repos/OliOli2013/AIOHD-NEXT-Skin/releases/latest'
DOWNLOAD_PREFIX = 'https://github.com/OliOli2013/AIOHD-NEXT-Skin/releases/download/'
_PACKAGE_RE = re.compile(r'^enigma2-plugin-skins-aiohd-next_([0-9]+\.[0-9]+\.[0-9]+-r[0-9]+)_all\.ipk$')
_VERSION_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-?r(\d+))?$')
_OPKG_VERSION_RE = re.compile(r'^Version:\s*(\S+)\s*$', re.MULTILINE)


def version_tuple(value):
    """Return a comparable (major, minor, patch, revision) tuple."""
    match = _VERSION_RE.match((value or '').strip())
    if not match:
        raise ValueError('unsupported version: %s' % value)
    major, minor, patch, revision = match.groups()
    return int(major), int(minor), int(patch), int(revision or 0)


def installed_version():
    """Read the version actually installed by opkg, with a safe fallback."""
    try:
        output = subprocess.check_output(
            ['opkg', 'status', PACKAGE_NAME],
            stderr=subprocess.STDOUT,
            timeout=4,
        )
        if not isinstance(output, str):
            output = output.decode('utf-8', 'replace')
        match = _OPKG_VERSION_RE.search(output)
        if match:
            value = match.group(1).strip()
            version_tuple(value)  # accept only the version syntax understood here
            return value
    except Exception:
        pass
    return CURRENT_PACKAGE_VERSION


def is_newer(candidate, current=None):
    if current is None:
        current = installed_version()
    return version_tuple(candidate) > version_tuple(current)


def _read_json(context=None, timeout=8):
    current = installed_version()
    request = Request(RELEASES_API, headers={
        'User-Agent': 'AIOHD-NEXT/%s' % current,
        'Accept': 'application/vnd.github+json',
        'Cache-Control': 'no-cache',
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
    """Return {'version', 'url', 'name'} only for a genuinely newer release."""
    try:
        data = _read_json(timeout=timeout)
    except Exception:
        # Some older Enigma2 images have an outdated CA store. GitHub download
        # URLs are still restricted below to this project's exact release path.
        data = _read_json(context=ssl._create_unverified_context(), timeout=timeout)

    if data.get('draft') or data.get('prerelease'):
        return None

    tag = str(data.get('tag_name') or '').strip()
    current = installed_version()
    if not tag:
        return None
    try:
        if version_tuple(tag) <= version_tuple(current):
            return None
    except ValueError:
        return None

    for asset in data.get('assets') or []:
        name = str(asset.get('name') or '')
        url = str(asset.get('browser_download_url') or '')
        match = _PACKAGE_RE.match(name)
        if not match:
            continue
        asset_version = match.group(1)
        # The release tag and the IPK filename must describe exactly the same
        # version. This also prevents a stale/mismatched asset from being offered.
        if version_tuple(asset_version) != version_tuple(tag):
            continue
        if url.startswith(DOWNLOAD_PREFIX) and url.endswith('/' + name):
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
