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
:module: mom.codec.base58
:synopsis: Base-58 representation for unambiguous display & compact human-input.


Where should you use base-58?
-----------------------------
Base-58 representation is 7 bit-ASCII safe, MIME-safe, URL-safe, HTTP
cookie-safe, and **human being-safe**. Base-58 representation can:

* be readable and editable by a human being;
* safely and compactly represent numbers;
* contain only alphanumeric characters (omitting a few with visually-
  ambiguously glyphs--namely, "0OIl");
* not contain punctuation characters.

Example scenarios where base-58 encoding may be used:

* Visually-legible account numbers
* Shortened URL paths
* OAuth verification codes
* Unambiguously printable and displayable key codes (for example,
  net-banking PINs, verification codes sent via SMS, etc.)
* Bitcoin decentralized crypto-currency addresses
* CAPTCHAs
* Revision control changeset identifiers
* Encoding email addresses compactly into JavaScript that decodes by itself
  to display on Web pages in order to reduce spam by stopping email harvesters
  from scraping email addresses from Web pages.

In general, use base-58 in any 7-bit ASCII-safe compact communication where
human beings, paper, and communication devices may be significantly
involved.

The default base-58 character set is ``[0-9A-Za-z]`` (base-62) with some
characters omitted to make them visually-legible and unambiguously printable.
The characters omitted are:

* 0 (ASCII NUMERAL ZERO)
* O (ASCII UPPERCASE ALPHABET O)
* I (ASCII UPPERCASE ALPHABET I)
* l (ASCII LOWERCASE ALPHABET L)

For a practical example, see the documentation for :mod:`mom.codec.base62`.

Functions
---------
.. autofunction:: b58encode
.. autofunction:: b58decode
"""


from __future__ import absolute_import, division

from mom._compat import have_python3, ZERO_BYTE, range
from mom.builtins import byte, is_bytes, b
from mom.codec._base import base_decode_to_number, base_number_to_bytes
from mom.codec.integer import bytes_to_integer, integer_to_bytes
from mom.functional import leading


# Follows ASCII order.
ASCII58_CHARSET = ("123456789"
                  "ABCDEFGHJKLMNPQRSTUVWXYZ"
                  "abcdefghijkmnopqrstuvwxyz").encode("ascii")
# Therefore, b'1' represents b'\0'.
ASCII58_ORDS = dict((x, i) for i, x in enumerate(ASCII58_CHARSET))


# Really, I don't understand why people use the non-ASCII order,
# but if you really like it that much, go ahead. Be my guest. Here
# is what you will need:
#
# Does not follow ASCII order.
ALT58_CHARSET = ("123456789"
                 "abcdefghijkmnopqrstuvwxyz"
                 "ABCDEFGHJKLMNPQRSTUVWXYZ").encode("ascii")
# Therefore, b'1' represents b'\0'.
ALT58_ORDS = dict((x, i) for i, x in enumerate(ALT58_CHARSET))

if have_python3:
    ASCII58_CHARSET = tuple(byte(x) for x in ASCII58_CHARSET)
    ALT58_CHARSET = tuple(byte(x) for x in ALT58_CHARSET)

# If you're going to make people type stuff longer than this length
# I don't know what to tell you. Beyond this length powers
# are computed, so be careful if you care about computation speed.
# I think this is a VERY generous range. Most of the stuff you decode
# that is smaller than 256 bytes will be very fast.
POW_58 = tuple(58**power for power in range(256))


def b58encode(raw_bytes,
              _charset=ASCII58_CHARSET, _padding=True, _zero_byte=ZERO_BYTE):
    """
    Base58 encodes a sequence of raw bytes. Zero-byte sequences are
    preserved by default.

    :param raw_bytes:
        Raw bytes to encode.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII58_CHARSET``
        that uses natural ASCII order.
    :param _padding:
        (Internal) ``True`` (default) to include prefixed zero-byte sequence
        padding converted to appropriate representation.
    :returns:
        Base-58 encoded bytes.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("data must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    number = bytes_to_integer(raw_bytes)
    encoded = b('')
    while number > 0:
        number, remainder = divmod(number, 58)
        encoded = _charset[remainder] + encoded
    if _padding:
        zero_leading = leading(lambda w: w == _zero_byte[0], raw_bytes)
        encoded = (_charset[0] * zero_leading) + encoded
    return encoded


def b58decode(encoded,
              _charset=ASCII58_CHARSET,
              _lookup=ASCII58_ORDS,
              _powers=POW_58):
    """
    Base-58 decodes a sequence of bytes into raw bytes. Whitespace is ignored.
    
    :param encoded:
        Base-58 encoded bytes.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII58_CHARSET``
        that uses natural ASCII order.
    :param _lookup:
        (Internal) Ordinal-to-character lookup table for the specified
        character set.
    :param _powers:
        (Internal) Tuple of Pre-computed powers of 58.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("encoded data must be bytes: got %r" %
                        type(encoded).__name__)

    # Ignore whitespace.
    encoded = b('').join(encoded.split())

    # Convert to big integer.
    number = base_decode_to_number(encoded, 58, _lookup, _powers)
    
    # 0 byte is represented using the first character in the character set.
    zero_base_char = _charset[0]

    # Adds zero prefix padding if required.
    return base_number_to_bytes(number, encoded, zero_base_char)


def _b58decode(encoded,
              _charset=ASCII58_CHARSET,
              _lookup=ASCII58_ORDS,
              _zero_byte=ZERO_BYTE):
    """
    Simple implementation for benchmarking.

    Base-58 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

    :param encoded:
        Base-58 encoded bytes.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII58_CHARSET``
        that uses natural ASCII order.
    :param _lookup:
        (Internal) Ordinal-to-character lookup table for the specified
        character set.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("encoded data must be bytes: got %r" %
                        type(encoded).__name__)

    import re
    WHITESPACE_PATTERN = re.compile(b(r'(\s)*'), re.MULTILINE)

    # Ignore whitespace.
    encoded = re.sub(WHITESPACE_PATTERN, b(''), encoded)

    # Convert to big integer.
    number = 0
    for i, x in enumerate(reversed(encoded)):
        number += _lookup[x] * (58**i)

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
