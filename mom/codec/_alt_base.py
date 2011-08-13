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


import re
from mom._compat import ZERO_BYTE
from mom.builtins import is_bytes, b
from mom.codec import uint_to_bytes
from mom.codec.base58 import ASCII58_CHARSET, ASCII58_ORDS
from mom.codec.base62 import ASCII62_CHARSET, ASCII62_ORDS
from mom.codec.integer import bytes_to_uint
from mom.functional import leading

WHITESPACE_PATTERN = re.compile(b(r'(\s)*'), re.MULTILINE)


def b58encode_naive(raw_bytes,
                    _charset=ASCII58_CHARSET,
                    _padding=True,
                    _zero_byte=ZERO_BYTE):
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
    number = bytes_to_uint(raw_bytes)
    encoded = b('')
    while number > 0:
        encoded = _charset[number % 58] + encoded
        number //= 58
        # The following makes more divmod calls but is 2x faster.
#        number, remainder = divmod(number, 58)
#        encoded = _charset[remainder] + encoded
    if _padding:
        zero_leading = leading(lambda w: w == _zero_byte[0], raw_bytes)
        encoded = (_charset[0] * zero_leading) + encoded
    return encoded


def b62encode_naive(raw_bytes,
                    _charset=ASCII62_CHARSET,
                    _padding=True,
                    _zero_byte=ZERO_BYTE):
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
    number = bytes_to_uint(raw_bytes)
    encoded = b('')
    while number > 0:
        encoded = _charset[number % 62] + encoded
        number //= 62
        # The following makes more divmod calls but is 2x faster.
#        number, remainder = divmod(number, 62)
#        encoded = _charset[remainder] + encoded
    if _padding:
        zero_leading = leading(lambda w: w == _zero_byte[0], raw_bytes)
        encoded = (_charset[0] * zero_leading) + encoded
    return encoded


def b62decode_naive(encoded,
                    _charset=ASCII62_CHARSET,
                    _lookup=ASCII62_ORDS):
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
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("encoded data must be bytes: got %r" %
                        type(encoded).__name__)

    # Ignore whitespace.
    encoded = re.sub(WHITESPACE_PATTERN, b(''), encoded)

    # Convert to big integer.
    number = 0
    for i, x in enumerate(reversed(encoded)):
        number += _lookup[x] * (62**i)

    # Obtain raw bytes.
    if number:
        raw_bytes = uint_to_bytes(number)
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
        padding = ZERO_BYTE * zero_leading
        raw_bytes = padding + raw_bytes
    return raw_bytes


def b58decode_naive(encoded,
                    _charset=ASCII58_CHARSET,
                    _lookup=ASCII58_ORDS):
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

    # Ignore whitespace.
    encoded = re.sub(WHITESPACE_PATTERN, b(''), encoded)

    # Convert to big integer.
    number = 0
    for i, x in enumerate(reversed(encoded)):
        number += _lookup[x] * (58**i)

    # Obtain raw bytes.
    if number:
        raw_bytes = uint_to_bytes(number)
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
        padding = ZERO_BYTE * zero_leading
        raw_bytes = padding + raw_bytes
    return raw_bytes
