#!/usr/bin/env python
# -*- coding: utf-8 -*-
# base85.py: ASCII-85 encoding/decoding.
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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

from struct import unpack
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



def b85decode(encoded, ignore_whitespace=True, base85_ord=base85_ord):
    # We want 5-tuple chunks, so pad with as many 'u' characters as
    # required to fulfill the length.
    if ignore_whitespace:
        import re
        pattern = re.compile(r'(\s)*', re.MULTILINE)
        encoded = re.sub(pattern, '', encoded)

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
