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
:module: mom.codec.base62
:synopsis: Base-62 representation for compact human-input & 7-bit ASCII safety.

Where should you use base-62?
-----------------------------
Base-62 representation is 7 bit-ASCII safe, MIME-safe, URL-safe, HTTP
cookie-safe, and almost **human being-safe**. Base-62 representation can:

* be readable and editable by a human being;
* safely and compactly represent numbers;
* contain only alphanumeric characters;
* not contain punctuation characters.

For examples of places where you can use base-62, see the documentation
for :mod:`mom.codec.base58`.

In general, use base-62 in any 7-bit ASCII-safe compact communication where
human beings and communication devices may be significantly involved.

When to prefer base-62 over base-58?
------------------------------------
When you don't care about the visual ambiguity between these characters:

* 0 (ASCII NUMERAL ZERO)
* O (ASCII UPPERCASE ALPHABET O)
* I (ASCII UPPERCASE ALPHABET I)
* l (ASCII LOWERCASE ALPHABET L)

For a practical example, see the documentation for :mod:`mom.codec.base58`.

Functions
---------
.. autofunction:: b62encode
.. autofunction:: b62decode
"""

from __future__ import absolute_import, division

import re
from mom._compat import have_python3, ZERO_BYTE
from mom.builtins import byte, is_bytes, b
from mom.codec._base import base_number_to_bytes, base_decode_to_number
from mom.codec.integer import bytes_to_integer, integer_to_bytes
from mom.functional import leading


WHITESPACE_PATTERN = re.compile(b(r'(\s)*'), re.MULTILINE)

# Follows ASCII order.
ASCII62_CHARSET = ("0123456789"
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "abcdefghijlkmnopqrstuvwxyz").encode("ascii")
# Therefore, b'0' represents b'\0'.
ASCII62_ORDS = dict((x, i) for i, x in enumerate(ASCII62_CHARSET))


# Really, I don't understand why people use the non-ASCII order,
# but if you really like it that much, go ahead. Be my guest. Here
# is what you will need:
#
# Does not follow ASCII order.
ALT62_CHARSET = ("0123456789"
                 "abcdefghijlkmnopqrstuvwxyz"
                 "ABCDEFGHIJKLMNOPQRSTUVWXYZ").encode("ascii")
# Therefore, b'0' represents b'\0'.
ALT62_ORDS = dict((x, i) for i, x in enumerate(ALT62_CHARSET))


if have_python3:
    ASCII62_CHARSET = tuple(byte(x) for x in ASCII62_CHARSET)
    ALT62_CHARSET = tuple(byte(x) for x in ALT62_CHARSET)

# If you're going to make people type stuff longer than this length
# I don't know what to tell you. Beyond this length powers
# are computed, so be careful if you care about computation speed.
# I think this is a VERY generous range. Most of the stuff you decode
# that is smaller than 256 bytes will be very fast.
POW_62 = tuple(62**power for power in range(256))


def b62encode(raw_bytes,
              _charset=ASCII62_CHARSET, _padding=True, _zero_byte=ZERO_BYTE):
    """
    Base62 encodes a sequence of raw bytes. Zero-byte sequences are
    preserved by default.

    :param raw_bytes:
        Raw bytes to encode.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII62_CHARSET``
        that uses natural ASCII order.
    :param _padding:
        (Internal) ``True`` (default) to include prefixed zero-byte sequence
        padding converted to appropriate representation.
    :returns:
        Base-62 encoded bytes.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("data must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    number = bytes_to_integer(raw_bytes)
    encoded = b('')
    while number > 0:
        number, remainder = divmod(number, 62)
        encoded = _charset[remainder] + encoded
    if _padding:
        zero_leading = leading(lambda w: w == _zero_byte[0], raw_bytes)
        encoded = (_charset[0] * zero_leading) + encoded
    return encoded


def b62decode(encoded,
              _charset=ASCII62_CHARSET,
              _lookup=ASCII62_ORDS,
              _powers=POW_62):
    """
    Base-62 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

    :param encoded:
        Base-62 encoded bytes.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII62_CHARSET``
        that uses natural ASCII order.
    :param _lookup:
        (Internal) Ordinal-to-character lookup table for the specified
        character set.
    :param _powers:
        (Internal) Tuple of Pre-computed powers of 62.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("encoded data must be bytes: got %r" %
                        type(encoded).__name__)

    # Ignore whitespace.
    encoded = b('').join(encoded.split())

    # Convert to big integer.
    number = base_decode_to_number(encoded, 62, _lookup, _powers)

    # 0 byte is represented using the first character in the character set.
    zero_base_char = _charset[0]

    # Adds zero prefix padding if required.
    return base_number_to_bytes(number, encoded, zero_base_char)


def _b62decode(encoded,
              _charset=ASCII62_CHARSET,
              _lookup=ASCII62_ORDS,
              _ignore_pattern=WHITESPACE_PATTERN,
              _zero_byte=ZERO_BYTE):
    """
    Base-62 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

    :param encoded:
        Base-62 encoded bytes.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII62_CHARSET``
        that uses natural ASCII order.
    :param _lookup:
        (Internal) Ordinal-to-character lookup table for the specified
        character set.
    :param _ignore_pattern:
        (Internal) Regular expression pattern to ignore bytes within encoded
        byte data.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("encoded data must be bytes: got %r" %
                        type(encoded).__name__)

    # Ignore whitespace.
    if _ignore_pattern:
        encoded = re.sub(_ignore_pattern, b(''), encoded)

    # Convert to big integer.
    number = 0
    for i, x in enumerate(reversed(encoded)):
        number += _lookup[x] * (62**i)

    # Obtain raw bytes.
    if number:
        raw_bytes = integer_to_bytes(number)
    else:
        # We don't want to convert to b'\x00' when we get number == 0.
        # That would add an off-by-one extra zero byte in the result.
        raw_bytes = b('')

    # Add prefixed padding if required.
    # 0 byte is represented using the first character in the character set.
    zero_char = _charset[0]
    # The extra [0] index in zero_byte_char[0] is for Python2.x-Python3.x
    # compatibility. Indexing into Python 3 bytes yields an integer, whereas
    # in Python 2.x it yields a single-byte string.
    zero_leading = leading(lambda w: w == zero_char[0], encoded)
    if zero_leading:
        padding = _zero_byte * zero_leading
        raw_bytes = padding + raw_bytes
    return raw_bytes
