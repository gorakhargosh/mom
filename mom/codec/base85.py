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
from mom.builtins import b
from mom.codec import long_to_bytes
from mom.functional import chunks


__all__ = [
    "b85encode",
    "b85decode",
]

def base85_chr(value):
    return chr(value + 33)

def base85_ord(char):
    return ord(char) - 33


def b85encode(raw_bytes, padding=False, base85_chr=base85_chr):
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

    # We need chunks of 32-bit (4 bytes chunk size) unsigned integers,
    # which means the length of the byte sequence must be divisible by 4.
    # Ensures length by appending additional padding zero bytes if required.
    # ceil_div(length, 4).
    num_uint32, remainder = divmod(len(raw_bytes), 4)
    if remainder:
        padding_size = 4 - remainder
        raw_bytes += '\x00' * padding_size
        num_uint32 += 1
    else:
        padding_size = 0

    ascii_chars = []
    # Ascii85 uses a big-endian convention.
    # See: http://en.wikipedia.org/wiki/Ascii85
    for x in unpack('>' + 'L' * num_uint32, raw_bytes):
#        chars = list(range(5))
#        for i in reversed(chars):
#            chars[i] = base85_chr(x % 85)
#            x //= 85
#        ascii_chars.extend(chars)
        # Above loop unrolled:
        ascii_chars.extend((
            base85_chr(x // 52200625),      # 85**4 = 52200625
            base85_chr((x // 614125) % 85), # 85**3 = 614125
            base85_chr((x // 7225) % 85),   # 85**2 = 7225
            base85_chr((x // 85) % 85),     # 85**1 = 85
            base85_chr(x % 85),             # 85**0 = 1
        ))
    if padding_size and not padding:
        ascii_chars = ascii_chars[:-padding_size]
    return ''.join(ascii_chars)



def b85decode(encoded, base85_ord=base85_ord):
    # We want 5-tuple chunks, so pad with as many 'u' characters as
    # required to fulfill the length.
    remainder = len(encoded) % 5
    if remainder:
        padding_size = 5 - remainder
        encoded += 'u' * padding_size
    else:
        padding_size = 0

    raw_bytes = b('')
    for chunk in chunks(encoded, 5):
        uint32_value = 0
        for char in chunk:
            uint32_value = uint32_value * 85 + base85_ord(char)
        raw_bytes += long_to_bytes(uint32_value)

    if padding_size:
        raw_bytes = raw_bytes[:-padding_size]
    return raw_bytes
