#!/usr/bin/env python
# -*- coding: utf-8 -*-
# base85.py: ASCII-85 encoding/decoding.
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# MIT License
# -----------
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the  Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
:module: mom.codec.base85
:synopsis: Adobe-modified ASCII-85 encoding and decoding functions.
:see: http://en.wikipedia.org/wiki/Ascii85

Functions
---------
.. autofunction:: b85encode
.. autofunction:: b85decode
"""

from __future__ import absolute_import, division

from struct import unpack, pack
from mom._compat import range


__all__ = [
    "b85encode",
    "b85decode",
]


def b85encode(raw_bytes, padding=False):
    """
    ASCII-85 encodes a sequence of raw bytes.

    If the number of raw bytes is not divisible by 4, the byte sequence
    is padded with up to 3 null bytes before encoding. After encoding,
    as many bytes as were added as padding are removed from the end of the
    encoded sequence if ``padding`` is ``False`` (default).

    :param raw_bytes:
        Raw bytes.
    :param padding:
        ``True`` if padding should be included; ``False`` (default) otherwise.
    :returns:
        ASCII-85 encoded bytes.
    """
    length = len(raw_bytes)

    # We need chunks of 32-bit (4 bytes chunk size) unsigned integers,
    # which means the length of the byte sequence must be divisible by 4.
    # Ensures length by appending additional padding zero bytes if required.
    # ceil_div(length, 4).
    num_uint32, remainder = divmod(length, 4)
    if remainder:
        padding_size = 4 - remainder
        raw_bytes += '\x00' * padding_size
        #length = length + padding_size
        num_uint32 += 1
    else:
        padding_size = 0

    ascii_chars = []
    # Ascii85 uses a big-endian convention.
    # See: http://en.wikipedia.org/wiki/Ascii85
    for x in unpack('>' + 'L' * num_uint32, raw_bytes):
        remainders = list(range(5))
        for i in reversed(remainders):
            remainders[i] = (x % 85) + 33
            x //= 85
        ascii_chars.extend(map(chr, remainders))
        # Above loop unrolled:
#        ascii_chars.extend((
#            chr((x // 52200625) + 33),      # 85**4 = 52200625
#            chr(((x // 614125) % 85) + 33), # 85**3 = 614125
#            chr(((x // 7225) % 85) + 33),   # 85**2 = 7225
#            chr(((x // 85) % 85) + 33),     # 85**1 = 85
#            chr((x % 85) + 33),             # 85**0 = 1
#        ))
    if not padding:
        ascii_chars = ascii_chars[:-padding_size]
    return ''.join(ascii_chars)


def b85decode(encoded):
    pass