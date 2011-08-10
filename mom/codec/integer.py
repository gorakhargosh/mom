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
:module: mom.codec.integer
:synopsis: Routines for converting between integers and bytes.

Number-bytes conversion
-----------------------
These codecs are "lossy" as they don't preserve prefixed padding zero bytes.
In a more mathematical sense,

    ``g(f(x))`` is **almost** an identity function, but not exactly.

where ``g`` is the decoder and ``f`` is a encoder.

.. autofunction:: bytes_to_integer
.. autofunction:: integer_to_bytes
"""

import binascii
from struct import pack, unpack
from mom.builtins import is_bytes, byte, b, integer_byte_count, is_integer


__all__ = [
    "bytes_to_integer",
    "integer_to_bytes",
]

ZERO_BYTE = byte(0)


def bytes_to_integer(raw_bytes):
    """
    Converts bytes to integer::

        bytes_to_integer(bytes) : integer

    This is (essentially) the inverse of integer_to_bytes().

    Encode your Unicode strings to a byte encoding before converting them.

    .. WARNING: Does not preserve leading zero bytes.

    :param raw_bytes:
        Raw bytes (base-256 representation).
    :returns:
        Integer.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    # binascii.b2a_hex is written in C as is int.
    return int(binascii.b2a_hex(raw_bytes), 16)


def _bytes_to_integer(raw_bytes):
    """
    Converts bytes (base-256 representation) to integer::

        bytes_to_integer(bytes) : integer

    This is (essentially) the inverse of integer_to_bytes().

    Encode your Unicode strings to a byte encoding before converting them.

    .. WARNING: Does not preserve leading zero bytes.

    :param raw_bytes:
        Raw bytes (base-256 representation).
    :returns:
        Integer.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)

    length = len(raw_bytes)
    remainder = length % 4
    if remainder:
        # Ensure we have a length that is a multiple of 4 by prefixing
        # sufficient zero padding.
        padding_size = 4 - remainder
        length += padding_size
        raw_bytes = ZERO_BYTE * padding_size + raw_bytes

    # Now unpack integers and accumulate.
    int_value = 0
    for i in range(0, length, 4):
        chunk = raw_bytes[i:i+4]
        int_value = (int_value << 32) + unpack('>I', chunk)[0]
    return int_value


def _integer_to_bytes(number, chunk_size=0):
    """
    Convert a integer to bytes::

        integer_to_bytes(n:int, blocksize:int) : string

    .. WARNING: Does not preserve leading zeros.

    This is based on the PyCrypto implementation by Barry Warsaw.

    :param number:
        Integer value
    :param chunk_size:
        If optional chunk_size is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        chunk_size. Raises an OverflowError if the chunk_size is not sufficient
        to represent the integer.
    :returns:
        Raw bytes (base-256 representation).
    """
    number = int(number)

    if number < 0:
        raise ValueError('Number must be unsigned integer: %d' % number)

    raw_bytes = b('')
    number = number
    while number > 0:
        raw_bytes = pack('>I', number & 0xffffffff) + raw_bytes
        number >>= 32

    # Strip off leading zeros
    for i in range(len(raw_bytes)):
        if raw_bytes[i] != ZERO_BYTE[0]:
            break
    else:
        # only happens when num == 0
        raw_bytes = ZERO_BYTE
        i = 0
    raw_bytes = raw_bytes[i:]

    # Add back some pad bytes. This could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    length = len(raw_bytes)
    if chunk_size > 0 and length % chunk_size:
        zero_leading = 0
        for zero_leading, x in enumerate(raw_bytes):
            if x != ZERO_BYTE[0]:
                break
        bytes_needed = length - zero_leading
        if bytes_needed > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (bytes_needed, chunk_size)
            )
        raw_bytes = (chunk_size - len(raw_bytes) % chunk_size) * \
                    ZERO_BYTE + raw_bytes
    return raw_bytes


def integer_to_bytes(number, chunk_size=0):
    """
    Convert a integer to bytes (base-256 representation)::

        integer_to_bytes(n:int, chunk_size:int) : string

    .. WARNING:
        Does not preserve leading zeros if you don't specify a chunk size.

    :param number:
        Integer value
    :param chunk_size:
        If optional chunk size is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        ``chunk_size``. Raises an OverflowError if the chunk_size is not
        sufficient to represent the integer.
    :returns:
        Raw bytes (base-256 representation).
    """

    if not is_integer(number):
        raise TypeError("Expected unsigned integer as argument 1, got: %r" %
            type(number).__name__)

    if number < 0:
        raise ValueError('Number must be unsigned integer: %d' % number)

    raw_bytes = b('')
    if not number:
        raw_bytes = ZERO_BYTE

    num = number
    while num > 0:
        raw_bytes = pack('>I', num & 0xffffffff) + raw_bytes
        num >>= 32

    # Count the number of zero prefix bytes.
    zero_leading = 0
    for zero_leading, x in enumerate(raw_bytes):
        if x != ZERO_BYTE[0]:
            break

    if chunk_size > 0:
        # Bounds checking. We're not doing this up-front because the
        # most common use case is not specifying a chunk size. In the worst
        # case, the number will already have been converted to bytes above.
        length = len(raw_bytes)
        bytes_needed = length - zero_leading
        if bytes_needed > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (bytes_needed, chunk_size)
            )
        remainder = length % chunk_size
        if remainder:
            raw_bytes = (chunk_size - remainder) * ZERO_BYTE + raw_bytes
    else:
        raw_bytes = raw_bytes[zero_leading:]
    return raw_bytes
