# -*- coding: utf-8 -*-
"""
hyper/compat
~~~~~~~~~

Normalizes the Python 2/3 API for internal use.
"""
from contextlib import contextmanager
import sys
import zlib

try:
    from . import ssl_compat
except ImportError:
    # TODO log?
    ssl_compat = None

try:
    from urllib.parse import urlencode, urlsplit
except ImportError:  # pragma: no cover
    from urllib import urlencode
    from urlparse import urlsplit

_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py2_7_9_or_later = _ver[0] >= 2 and _ver[1] >= 7 and _ver[2] >= 9
is_py3 = _ver[0] == 3
is_py3_3 = is_py3 and _ver[1] == 3

@contextmanager
def ignore_missing():
    try:
        yield
    except (AttributeError, NotImplementedError):  # pragma: no cover
        pass

if is_py2:
    if is_py2_7_9_or_later:
        import ssl
    else:
        ssl = ssl_compat

    from urlparse import urlparse

    def to_byte(char):
        return ord(char)

    def decode_hex(b):
        return b.decode('hex')

    # The standard zlib.compressobj() accepts only positional arguments.
    def zlib_compressobj(level=6, method=zlib.DEFLATED, wbits=15, memlevel=8,
                         strategy=zlib.Z_DEFAULT_STRATEGY):
        return zlib.compressobj(level, method, wbits, memlevel, strategy)

elif is_py3:
    from urllib.parse import urlparse

    def to_byte(char):
        return char

    def decode_hex(b):
        return bytes.fromhex(b)

    zlib_compressobj = zlib.compressobj

    if is_py3_3:
        ssl = ssl_compat
    else:
        import ssl
