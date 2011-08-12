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
from struct import pack, unpack, pack_into
from array import array

from mom._compat import get_machine_alignment, range, ZERO_BYTE
from mom.builtins import is_bytes, byte, b, integer_byte_length


__all__ = [
    "bytes_to_integer",
    "integer_to_bytes",
]



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


def _bytes_to_integer(raw_bytes, _zero_byte=ZERO_BYTE):
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
        raw_bytes = _zero_byte * padding_size + raw_bytes

    # Now unpack integers and accumulate.
    int_value = 0
    for i in range(0, length, 4):
        chunk = raw_bytes[i:i+4]
        int_value = (int_value << 32) + unpack('>I', chunk)[0]
    return int_value


def _integer_to_bytes_array_based(number, chunk_size=0):
    """
    Converts an integer into a byte array.

    [Simplest possible implementation]
    
    :param number:
        Long value
    :returns:
        Long.
    """
# Even without this check a type error will be raised. Reduces overhead.
#    if not is_integer(number):
#        raise TypeError("Expected unsigned integer as argument 1, got: %r" %
#            type(number).__name__)

    if number < 0:
        raise ValueError('Negative numbers cannot be used: %i' % number)

    if number == 0:
        bytes_count = 1
    else:
        bytes_count = integer_byte_length(number)
    byte_array = array('B', [0] * bytes_count)
    for count in range(bytes_count - 1, -1, -1):
        byte_array[count] = number & 0xff
        number >>= 8
    raw_bytes =  byte_array.tostring()

    if chunk_size > 0:
        # Bounds checking. We're not doing this up-front because the
        # most common use case is not specifying a chunk size. In the worst
        # case, the number will already have been converted to bytes above.
        length = len(raw_bytes)
        bytes_needed = bytes_count
        if bytes_needed > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (bytes_needed, chunk_size)
            )
        remainder = length % chunk_size
        if remainder:
            raw_bytes = (chunk_size - remainder) * b('\x00') + raw_bytes
    return raw_bytes


def _integer_to_bytes_python_rsa(number, block_size=0):
    """
    Naive slow and accurate implementation. Base for all our tests.

    Converts a number to a string of bytes.

    :param number: the number to convert
    :param block_size: the number of bytes to output. If the number encoded to
        bytes is less than this, the block will be zero-padded. When not given,
        the returned block is not padded.

    :raises:
        ``OverflowError`` when block_size is given and the number takes up more
        bytes than fit into the block.
    """

# Even without this check a type error will be raised. Reduces overhead.
#    if not is_integer(number):
#        raise TypeError("Expected unsigned integer as argument 1, got: %r" %
#            type(number).__name__)

    if number < 0:
        raise ValueError('Negative numbers cannot be used: %d' % number)

    # Do some bounds checking
    needed_bytes = integer_byte_length(number)
    if block_size > 0:
        if needed_bytes > block_size:
            raise OverflowError('Needed %i bytes for number, but block size '
                'is %i' % (needed_bytes, block_size))

    # Convert the number to bytes.
    if number == 0:
        raw_bytes = [ZERO_BYTE]
    else:
        raw_bytes = []
        num = number
        while num > 0:
            raw_bytes.insert(0, byte(num & 0xFF))
            num >>= 8

    # Pad with zeroes to fill the block
    if block_size > 0:
        padding_size = (block_size - needed_bytes)
        if number == 0:
            padding_size -= 1
        padding =  ZERO_BYTE * padding_size
    else:
        padding = b('')
    return padding + b('').join(raw_bytes)


def integer_to_bytes(number, chunk_size=0,
                     _zero_byte=ZERO_BYTE,
                     _get_machine_alignment=get_machine_alignment):
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
    :raises:
        ``OverflowError`` when block_size is given and the number takes up more
        bytes than fit into the block.
    """
    # Machine word-aligned implementation.
    # ~19x faster than naive implementation on 32-bit processors.
    # ~33x faster than naive implementation on 64-bit processors.
    # ~50x faster on 64-bit pypy 1.5
    
# Even without this check a type error will be raised. Reduces overhead.
#    if not is_integer(number):
#        raise TypeError("Expected unsigned integer as argument 1, got: %r" %
#            type(number).__name__)

    if number < 0:
        raise ValueError('Number must be unsigned integer: %d' % number)

#    count = 0
    raw_bytes = b('')
    if not number:
        # Count the zero byte as well.
#        count = 1
        raw_bytes = _zero_byte

    # Align packing to machine word size.
    num = number
    word_bits, word_bytes, max_uint, pack_type = _get_machine_alignment(num)
    pack_format = ">" + pack_type
    while num > 0:
        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
#        count += 1
        num >>= word_bits

    # Count the number of zero prefix bytes.
    zero_leading = 0
    for zero_leading, x in enumerate(raw_bytes):
        if x != _zero_byte[0]:
            break

    if chunk_size > 0:
        # Bounds checking. We're not doing this up-front because the
        # most common use case is not specifying a chunk size. In the worst
        # case, the number will already have been converted to bytes above.
        #length = count * word_bytes
        length = len(raw_bytes)
        #assert l == length
        bytes_needed = length - zero_leading
        if bytes_needed > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (bytes_needed, chunk_size)
            )
        remainder = length % chunk_size
        if remainder:
            raw_bytes = (chunk_size - remainder) * _zero_byte + raw_bytes
    else:
        raw_bytes = raw_bytes[zero_leading:]
    return raw_bytes


def integer_to_bytes_a(number, chunk_size=0,
                       _zero_byte=ZERO_BYTE,
                       _get_machine_alignment=get_machine_alignment):
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
    :raises:
        ``OverflowError`` when block_size is given and the number takes up more
        bytes than fit into the block.
    """
    # Machine word aligned byte array based implementation.

    if number < 0:
        raise ValueError('Number must be unsigned integer: %d' % number)

#    count = 0
    raw_bytes = b('')
    if not number:
#        # Count the zero byte as well.
#        count = 1
        raw_bytes = ZERO_BYTE

    # Align packing to machine word size.
    num = number
    word_bits, word_bytes, max_uint, pack_type = _get_machine_alignment(num)
    pack_format = ">" + pack_type

    temp_buffer = array("B", [0] * word_bytes)
    #a = array("B", [0] * count)
    a = array("B", raw_bytes)
    while num > 0:
        pack_into(pack_format, temp_buffer, 0, num & max_uint)
        a = temp_buffer + a
        #count += 1
        num >>= word_bits

    # Count the number of zero prefix bytes.
    zero_leading = 0
    length = len(a)
    for zero_leading in range(length):
        if a[zero_leading]:
            break

    raw_bytes = a.tostring()
    if chunk_size > 0:
        # Bounds checking. We're not doing this up-front because the
        # most common use case is not specifying a chunk size. In the worst
        # case, the number will already have been converted to bytes above.
        #length = count * word_bytes
        #assert l == length
        bytes_needed = length - zero_leading
        if bytes_needed > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (bytes_needed, chunk_size)
            )
        remainder = length % chunk_size
        if remainder:
            raw_bytes = (chunk_size - remainder) * _zero_byte + raw_bytes
    else:
        raw_bytes = raw_bytes[zero_leading:]
    return raw_bytes
