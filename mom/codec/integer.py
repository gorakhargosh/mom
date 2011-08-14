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

.. autofunction:: bytes_to_uint
.. autofunction:: uint_to_bytes
"""

# This module contains only the implementations that were bench-marked
# to be the fastest. See _alt_integer.py for alternative but slower
# implementations.

from __future__ import absolute_import, division

try:
    # Utilize psyco if it is available.
    # This should help speed up 32-bit versions of Python if you have
    # psyco installed.
    import psyco
    psyco.full()
except ImportError:
    pass

import binascii
from struct import pack

from mom._compat import get_word_alignment, ZERO_BYTE
from mom.builtins import is_bytes, b, bytes_leading


__all__ = [
    "bytes_to_uint",
    "uint_to_bytes",
]


def bytes_to_uint(raw_bytes):
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


def unsigned_integer_to_bytes(number):
    if number < 0:
        raise ValueError("Number must be an unsigned integer: %d" % number)

    # Ensure the number is an integer.
    number & 1

    raw_bytes = b('')

    # Pack the integer one machine word at a time into bytes.
    num = number
    word_bits, _, max_uint, pack_type = get_word_alignment(num)
    pack_format = ">%s" % pack_type
    while num > 0:
        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
        num >>= word_bits

    # Obtain the index of the first non-zero byte.
    zero_leading = bytes_leading(raw_bytes)

    if number == 0:
        raw_bytes = ZERO_BYTE

    # De-padding.
    raw_bytes = raw_bytes[zero_leading:]
    return raw_bytes


def uint_to_bytes(number, chunk_size=0):
    """
    Convert an unsigned integer to bytes (base-256 representation)::
    Does not preserve leading zeros if you don't specify a chunk size.

    :param number:
        Integer value
    :param chunk_size:
        If optional chunk size is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        ``chunk_size``.
    :returns:
        Raw bytes (base-256 representation).
    :raises:
        ``OverflowError`` when block_size is given and the number takes up more
        bytes than fit into the block.
    """
    # Machine word-aligned implementation and unsurprisingly the fastest of
    # all these implementations.
    if number < 0:
        raise ValueError('Number must be unsigned integer: %d' % number)

    raw_bytes = b('')
    # Align packing to machine word size.
    num = number
    word_bits, word_bytes, max_uint, pack_type = get_word_alignment(num)
    pack_format = ">" + pack_type
    while num > 0:
        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
        num >>= word_bits
    # Get the index of the first non-zero byte.
    first_non_zero = bytes_leading(raw_bytes)

    if number == 0:
        raw_bytes = ZERO_BYTE

    if chunk_size > 0:
        # Bounds checking. We're not doing this up-front because the
        # most common use case is not specifying a chunk size. In the worst
        # case, the number will already have been converted to bytes above.
        length = len(raw_bytes) - first_non_zero
        if length > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (length, chunk_size)
            )
        remainder = length % chunk_size
        if remainder:
            padding_size = (chunk_size - remainder)
            if first_non_zero > 0:
                raw_bytes = raw_bytes[first_non_zero-padding_size:]
            else:
                raw_bytes = (padding_size * ZERO_BYTE) + raw_bytes
    else:
        raw_bytes = raw_bytes[first_non_zero:]
    return raw_bytes


def _uint_to_bytes_pycrypto(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = b('')
    n = int(n)
    while n > 0:
        s = pack('>I', n & 0xffffffff) + s
        n >>= 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != b('\000')[0]:
            break
    else:
        # only happens when n == 0
        s = b('\000')
        i = 0
    s = s[i:]
    # add back some pad bytes. this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * b('\000') + s
    return s

