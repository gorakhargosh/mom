#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
:synopsis: ASCII-85 and RFC1924 Base85 encoding and decoding functions.
:see: http://en.wikipedia.org/wiki/Ascii85

Functions
---------
.. autofunction:: b85encode
.. autofunction:: b85decode
.. autofunction:: base85_chr
.. autofunction:: base85_ord
.. autofunction:: ipv6_b85encode
.. autofunction:: ipv6_b85decode
"""

from __future__ import absolute_import, division

import re
from struct import unpack, pack
from mom.functional import chunks


__all__ = [
    "b85encode",
    "b85decode",
    "ADOBE_PREFIX",
    "ADOBE_SUFFIX",
    "WHITESPACE_PATTERN",
    "base85_chr",
    "base85_ord",
    "ipv6_b85encode",
    "ipv6_b85decode",
]


ADOBE_PREFIX = '<~'
ADOBE_SUFFIX = '~>'

WHITESPACE_PATTERN = re.compile(r'(\s)*', re.MULTILINE)


def base85_chr(value):
    """
    Converts an ordinal into its base85 character.

    :param value:
        Ordinal value.
    :returns:
        base85 character.
    """
    return chr(value + 33)


def base85_ord(char):
    """
    Converts a base85 character into its ordinal.

    :param char:
        Base85 character
    :returns:
        Ordinal value.
    """
    return ord(char) - 33


def b85encode(raw_bytes,
              prefix=ADOBE_PREFIX,
              suffix=ADOBE_SUFFIX,
              _padding=False,
              _base85_chr=base85_chr):
    """
    ASCII-85 encodes a sequence of raw bytes.

    If the number of raw bytes is not divisible by 4, the byte sequence
    is padded with up to 3 null bytes before encoding. After encoding,
    as many bytes as were added as padding are removed from the end of the
    encoded sequence if ``padding`` is ``False`` (default).

    Encodes a zero-group (\x00\x00\x00\x00) as 'z' instead of '!!!!!'.

    The resulting encoded ASCII string is *not URL-safe* nor is it
    safe to include within SGML/XML/HTML documents. You will need to escape
    special characters if you decide to include such an encoded string
    within these documents.

    :param raw_bytes:
        Raw bytes.
    :param prefix:
        The prefix used by the encoded text. Defaults to Adobe's prefix.
    :param suffix:
        The suffix used by the encoded text. Defaults to Adobe's suffix.
    :param _padding:
        ``True`` if padding should be included; ``False`` (default) otherwise.
        You should not need to use this--the default value is usually the
        expected value.
    :param _base85_chr:
        A function that converts an ordinal number into its base85 character
        representation.
    :returns:
        ASCII-85 encoded bytes.
    """
    prefix = prefix or ''
    suffix = suffix or ''

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
            _base85_chr(x // 52200625),      # 85**4 = 52200625
            _base85_chr((x // 614125) % 85), # 85**3 = 614125
            _base85_chr((x // 7225) % 85),   # 85**2 = 7225
            _base85_chr((x // 85) % 85),     # 85**1 = 85
            _base85_chr(x % 85),             # 85**0 = 1
        ))
    if padding_size and not _padding:
        ascii_chars = ascii_chars[:-padding_size]
    encoded = ''.join(ascii_chars).replace('!!!!!', 'z')
    return prefix + encoded + suffix


def b85decode(encoded,
              prefix=ADOBE_PREFIX,
              suffix=ADOBE_SUFFIX,
              _ignore_pattern=WHITESPACE_PATTERN,
              _base85_ord=base85_ord):
    """
    Decodes a base85 encoded string into raw bytes.

    :param encoded:
        Encoded ASCII string.
    :param prefix:
        The prefix used by the encoded text. Defaults to Adobe's prefix.
    :param suffix:
        The suffix used by the encoded text. Defaults to Adobe's suffix.
    :param _ignore_pattern:
        By default all whitespace is ignored. This must be an
        ``re.compile()`` instance. You should not need to use this.
    :param _base85_ord:
        A function to convert a base85 character to its ordinal value.
        You should not need to use this.
    :returns:
        Base85-decoded raw bytes.
    """
    prefix = prefix or ""
    suffix = suffix or ""

    # ASCII-85 ignores whitespace.
    if _ignore_pattern:
        encoded = re.sub(_ignore_pattern, '', encoded)

    # Strip the prefix and suffix.
    if prefix and encoded.startswith(prefix):
        encoded = encoded[len(prefix):]
    if suffix and encoded.endswith(suffix):
        encoded = encoded[:-len(suffix)]

    # Replace all the 'z' occurrences with '!!!!!'
    encoded = encoded.replace('z', '!!!!!')

    # We want 5-tuple chunks, so pad with as many 'u' characters as
    # required to satisfy the length.
    num_uint32s, remainder = divmod(len(encoded), 5)
    if remainder:
        padding_size = 5 - remainder
        encoded += 'u' * padding_size
        num_uint32s += 1
    else:
        padding_size = 0

    #raw_bytes = ''
    uint32s = []
    for chunk in chunks(encoded, 5):
        uint32_value = 0
        for char in chunk:
            uint32_value = uint32_value * 85 + _base85_ord(char)
        # Groups of characters that decode to a value greater than 2**32 − 1
        # (encoded as "s8W-!") will cause a decoding error.
        if uint32_value > 4294967295:
            raise OverflowError("Cannot decode chunk `%r`" % chunk)
        #raw_bytes += pack(">L", uint32_value)
        uint32s.append(uint32_value)

    raw_bytes = pack(">" + "L" * num_uint32s, *uint32s)
    if padding_size:
        raw_bytes = raw_bytes[:-padding_size]
    return raw_bytes


# http://tools.ietf.org/html/rfc1924
RFC1924_CHARS = "0123456789" \
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                "abcdefghijklmnopqrstuvwxyz" \
                "!#$%&()*+-;<=>?@^_`{|}~"

RFC1924_CHAR_TO_INT = dict((x, i) for i, x in enumerate(RFC1924_CHARS))


def ipv6_b85encode(uint128, _charset=RFC1924_CHARS):
    """
    Encodes a 128-bit unsigned integer using the RFC 1924 base-85 encoding.

    Can be used to encode IPv6 addresses.

    :param uint128:
        A 128-bit unsigned integer to be encoded.
    :returns:
        RFC1924 Base85-encoded string.
    """
    if uint128 > 340282366920938463463374607431768211455L: # 2**128 - 1
        raise OverflowError("Number is not a 128-bit unsigned integer: %d" %
                            uint128)
    encoded = range(20)
    for i in reversed(encoded):
        encoded[i] = _charset[uint128 % 85]
        uint128 //= 85
    return ''.join(encoded)


def ipv6_b85decode(encoded, _lookup=RFC1924_CHAR_TO_INT):
    """
    Decodes an RFC1924 Base-85 encoded string to its 128-bit unsigned integral
    representation.

    :param encoded:
        RFC1924 Base85-encoded string.
    :returns:
        A 128-bit unsigned integer.
    """
    if len(encoded) != 20:
        raise ValueError(
            "Encoded IPv6 value must be exactly 20 characters long: got %r" %
            encoded
        )
    uint128 = 0L
    for char in encoded:
        uint128 = uint128 * 85 + _lookup[char]
    return uint128
