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

# Alternative implementations of integer module routines that
# were benchmarked to be slower.

from __future__ import absolute_import

try:
    # Utilize psyco if it is available.
    # This should help speed up 32-bit versions of Python if you have
    # psyco installed.
    import psyco
    psyco.full()
except ImportError:
    pass

from array import array
from struct import pack, pack_into, unpack
from mom._compat import range, ZERO_BYTE, \
    get_word_alignment, EMPTY_BYTE, \
    map, reduce
from mom.builtins import integer_byte_length, byte, is_bytes, byte_ord


def uint_to_bytes_naive_array_based(uint, chunk_size=0):
    """
    Converts an integer into bytes.

    :param uint:
        Unsigned integer value.
    :param chunk_size:
        Chunk size.
    :returns:
        Bytes.
    """
    if uint < 0:
        raise ValueError('Negative numbers cannot be used: %i' % uint)
    if uint == 0:
        bytes_count = 1
    else:
        bytes_count = integer_byte_length(uint)
    byte_array = array('B', [0] * bytes_count)
    for count in range(bytes_count - 1, -1, -1):
        byte_array[count] = uint & 0xff
        uint >>= 8
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
            raw_bytes = (chunk_size - remainder) * ZERO_BYTE + raw_bytes
    return raw_bytes


def uint_to_bytes_naive(number, block_size=0):
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
        padding = EMPTY_BYTE
    return padding + EMPTY_BYTE.join(raw_bytes)


# From pycrypto (for verification only).
def uint_to_bytes_pycrypto(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = EMPTY_BYTE
    n = int(n)
    while n > 0:
        s = pack('>I', n & 0xffffffff) + s
        n >>= 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != ZERO_BYTE[0]:
            break
    else:
        # only happens when n == 0
        s = ZERO_BYTE
        i = 0
    s = s[i:]
    # add back some pad bytes. this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * ZERO_BYTE + s
    return s


def uint_to_bytes_array_based(number, chunk_size=0):
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

    raw_bytes = EMPTY_BYTE
    if not number:
        raw_bytes = ZERO_BYTE

    # Align packing to machine word size.
    num = number
    word_bits, word_bytes, max_uint, pack_type = get_word_alignment(num)
    pack_format = ">" + pack_type

    temp_buffer = array("B", [0] * word_bytes)
    a = array("B", raw_bytes)
    while num > 0:
        pack_into(pack_format, temp_buffer, 0, num & max_uint)
        a = temp_buffer + a
        num >>= word_bits

    # Count the number of zero prefix bytes.
    zero_leading = 0
    length = len(a)
    for zero_leading in range(length):
        if a[zero_leading]:
            break
    raw_bytes = a[zero_leading:].tostring()

    if chunk_size > 0:
        # Bounds checking. We're not doing this up-front because the
        # most common use case is not specifying a chunk size. In the worst
        # case, the number will already have been converted to bytes above.
        length = len(raw_bytes)
        if length > chunk_size:
            raise OverflowError(
                "Need %d bytes for number, but chunk size is %d" %
                (length, chunk_size)
            )
        remainder = length % chunk_size
        if remainder:
            raw_bytes = (chunk_size - remainder) * ZERO_BYTE + raw_bytes
    return raw_bytes


def bytes_to_uint_naive(raw_bytes, _zero_byte=ZERO_BYTE):
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


#def uint_to_bytes(number, chunk_size=0):
#    """
#    Convert an unsigned integer to bytes (base-256 representation)::
#    Does not preserve leading zeros if you don't specify a chunk size.
#
#    :param number:
#        Integer value
#    :param chunk_size:
#        If optional chunk size is given and greater than zero, pad the front of
#        the byte string with binary zeros so that the length is a multiple of
#        ``chunk_size``.
#    :returns:
#        Raw bytes (base-256 representation).
#    :raises:
#        ``OverflowError`` when block_size is given and the number takes up more
#        bytes than fit into the block.
#    """
#    # Machine word-aligned implementation and unsurprisingly the fastest of
#    # all these implementations.
#    if number < 0:
#        raise ValueError('Number must be unsigned integer: %d' % number)
#
#    raw_bytes = EMPTY_BYTE
#    # Align packing to machine word size.
#    num = number
#    word_bits, word_bytes, max_uint, pack_type = get_word_alignment(num)
#    pack_format = ">" + pack_type
#    while num > 0:
#        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
#        num >>= word_bits
#    # Get the index of the first non-zero byte.
#    first_non_zero = bytes_leading(raw_bytes)
#
#    if number == 0:
#        raw_bytes = ZERO_BYTE
#
#    if chunk_size > 0:
#        # Bounds checking. We're not doing this up-front because the
#        # most common use case is not specifying a chunk size. In the worst
#        # case, the number will already have been converted to bytes above.
#        length = len(raw_bytes) - first_non_zero
#        if length > chunk_size:
#            raise OverflowError(
#                "Need %d bytes for number, but chunk size is %d" %
#                (length, chunk_size)
#            )
#        remainder = length % chunk_size
#        if remainder:
#            padding_size = (chunk_size - remainder)
#            if first_non_zero > 0:
#                raw_bytes = raw_bytes[first_non_zero-padding_size:]
#            else:
#                raw_bytes = (padding_size * ZERO_BYTE) + raw_bytes
#    else:
#        raw_bytes = raw_bytes[first_non_zero:]
#    return raw_bytes
#


def uint_to_bytes_simple(num):
    assert num >= 0
    rv = []
    while num:
        rv.append(byte(num & 0xff))
        num >>= 8
    return EMPTY_BYTE.join(reversed(rv))


def bytes_to_uint_simple(bytes):
    return reduce(lambda a, b: a << 8 | b, map(byte_ord, bytes), 0)

