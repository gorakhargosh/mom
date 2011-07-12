#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 Trevor Perrin <trevp@trevp.net>
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
:module: mom.codec
:synopsis: Many different types of common encode/decode functions.

Hexadecimal, base-64, binary, and decimal are byte string encodings.
``bytearray`` is an array of bytes. This module contains codecs for
converting between long, hex, base64, decimal, binary, mpi, and bytearray.

Bytes base-encoding
-------------------
.. autofunction:: base64_decode
.. autofunction:: base64_encode
.. autofunction:: bin_encode
.. autofunction:: bin_decode
.. autofunction:: hex_encode
.. autofunction:: hex_decode
.. autofunction:: decimal_encode
.. autofunction:: decimal_decode

Bytearray encoding
------------------
.. autofunction:: base64_to_bytearray
.. autofunction:: bytearray_to_base64

Numerical base-encoding
-----------------------
.. autofunction:: bytes_to_long
.. autofunction:: long_to_bytes

.. autofunction:: base64_to_long
.. autofunction:: long_to_base64

.. autofunction:: bin_to_long
.. autofunction:: long_to_bin

.. autofunction:: hex_to_long
.. autofunction:: long_to_hex

.. autofunction:: mpi_to_long
.. autofunction:: long_to_mpi
"""

import binascii

try:
    # Check whether we have reduce as a built-in.
    __reduce_test__ = reduce((lambda num1, num2: num1 + num2), [1, 2, 3, 4])
except NameError:
    # Python 3k
    from functools import reduce

from mom.builtins import bytes, hex, bin, long_byte_count, long_bit_length
from mom.itertools import group


# Bytes base-encoding.

def base64_decode(encoded):
    """
    Decodes a base-64 encoded string into a byte string.

    :param encoded:
        Base-64 encoded byte string.
    :returns:
        byte string.
    """
    return binascii.a2b_base64(encoded)


def base64_encode(byte_string):
    """
    Encodes a byte string using Base 64 and removes the last new line character.

    :param byte_string:
        The byte string to encode.
    :returns:
        Base64 encoded string without newline characters.
    """
    return binascii.b2a_base64(byte_string)[:-1]


def hex_encode(byte_string):
    """
    Converts a byte string to its hex representation.

    :param byte_string:
        Byte string.
    :returns:
        Hex-encoded byte string.
    """
    return binascii.b2a_hex(byte_string)


def hex_decode(encoded):
    """
    Converts a hex byte string to its byte representation.

    :param encoded:
        Hex string.
    :returns:
        Byte string.
    """
    return binascii.a2b_hex(encoded)


def decimal_encode(byte_string):
    """
    Converts a byte string to its decimal representation.

    :param byte_string:
        Byte string.
    :returns:
        Decimal-encoded byte string.
    """
    return bytes(int(hex_encode(byte_string), 16))
    #return bytes(bytes_to_long(byte_string))


def decimal_decode(encoded):
    """
    Converts a decimal encoded string to its byte representation.

    :param encoded:
        Decimal encoded string.
    :returns:
        Byte string.
    """
    return long_to_bytes(long(encoded))


_HEX_TO_BIN_LOOKUP = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010', 'A': '1010',
    'b': '1011', 'B': '1011',
    'c': '1100', 'C': '1100',
    'd': '1101', 'D': '1101',
    'e': '1110', 'E': '1110',
    'f': '1111', 'F': '1111',
}
_BIN_TO_HEX_LOOKUP = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': 'a',
    '1011': 'b',
    '1100': 'c',
    '1101': 'd',
    '1110': 'e',
    '1111': 'f',
}

def bin_encode(byte_string):
    """
    Converts a byte string to binary representation.

    :param byte_string:
        Byte string.
    :returns:
        Binary representation of the byte string.
    """
    return ''.join(_HEX_TO_BIN_LOOKUP[hex_char] for hex_char in hex_encode(byte_string))

    # Zero-bytes destructive. '\x00\x00' treated as '\x00'
    #return long_to_bin(bytes_to_long(byte_string))


def bin_decode(binary_string):
    """
    Converts a binary representation to bytes.

    :param binary_string:
        Binary representation.
    :returns:
        Byte string.
    """
    return hex_decode(''.join(_BIN_TO_HEX_LOOKUP[byt]
                              for byt in group(binary_string, 4)))

    # Zero-bytes destructive. '\x00\x00' treated as '\x00'
    #return long_to_bytes(bin_to_long(binary))


# Long base-encodings
def long_to_base64(num):
    """
    Base-64 encodes a long.

    :param num:
        A long integer.
    :returns:
        Base-64 encoded byte string.
    """
    byte_string = long_to_bytes(num)
    return base64_encode(byte_string)


def base64_to_long(encoded):
    """
    Base-64 decodes a string into a long.

    :param encoded:
        The encoded byte string.
    :returns:
        Long value.
    """
    byte_string = base64_decode(encoded)
    return bytes_to_long(byte_string)


def base64_to_bytearray(encoded):
    """
    Converts a base-64 encoded value into a byte array.

    :param encoded:
        The base-64 encoded value.
    :returns:
        Byte array.
    """
    from mom._types.bytearray import bytes_to_bytearray

    return bytes_to_bytearray(base64_decode(encoded))


def bytearray_to_base64(byte_array):
    """
    Base-64 encodes a byte array.

    :param byte_array:
        The byte array.
    :returns:
        Base-64 encoded byte array without newlines.
    """
    from mom._types.bytearray import bytearray_to_bytes

    return base64_encode(bytearray_to_bytes(byte_array))


def long_to_hex(num):
    """
    Converts a long value to its hexadecimal representation without prefix.

    :param num:
        Long value.
    :returns:
        Hexadecimal string.
    """
    return hex(num, None)


def hex_to_long(encoded):
    """Convert a hex string to an integer.

    The hex string can be any length. It can start with an 0x, or not.
    Unrecognized characters will raise a ValueError.

    This function released into the public domain by it's author, Lion
    Kimbro.

    :param encoded:
        Hexadecimal string.
    :returns:
        Long value.
    """
    num = 0  # Resulting integer
    encoded = encoded.lower()  # Hex string
    if encoded[:2] == "0x":
        encoded = encoded[2:]
    for character in encoded:  # Hex character
        num *= 16
        if "0" <= character <= "9":
            num += ord(character) - ord("0")
        elif "a" <= character <= "f":
            num += ord(character) - ord("a") + 10
        else:
            raise ValueError(character)
    return num


def long_to_bin(num):
    """
    Converts a long value to its binary representation without prefix.

    :param num:
        Long value.
    :returns:
        Bit string.
    """
    return bin(num, None)


def bin_to_long(binary):
    """
    Converts a bit sequence to a long value.

    :param binary:
        Bit sequence.
    :returns:
        Long value.
    """
    return reduce((lambda first, second: (int(first) << 1) + int(second)), binary)


# Taken from PyCrypto "as is".
# Improved conversion functions contributed by Barry Warsaw, after
# careful benchmarking

def long_to_bytes(num, blocksize=0):
    """
    Convert a long integer to a byte string::

        long_to_bytes(n:long, blocksize:int) : string

    :param num:
        Long value
    :param blocksize:
        If optional blocksize is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        blocksize.
    :returns:
        Byte string.
    """
    import struct

    # after much testing, this algorithm was deemed to be the fastest
    s = ''
    num = long(num)
    pack = struct.pack
    while num > 0:
        s = pack('>I', num & 0xffffffffL) + s
        num >>= 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\000':
            break
    else:
        # only happens when n == 0
        s = '\000'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\000' + s
    return s


def bytes_to_long(byte_string):
    """
    Convert a byte string to a long integer::

        bytes_to_long(bytestring) : long

    This is (essentially) the inverse of long_to_bytes().

    :param byte_string:
        A byte string.
    :returns:
        Long.
    """
    import struct

    acc = 0L
    unpack = struct.unpack
    length = len(byte_string)
    if length % 4:
        extra = (4 - length % 4)
        byte_string = '\000' * extra + byte_string
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', byte_string[i:i+4])[0]
    return acc


def mpi_to_long(mpi_byte_string):
    """
    Converts an OpenSSL-format MPI Bignum byte string into a long.

    :param mpi_byte_string:
        OpenSSL-format MPI Bignum byte string.
    :returns:
        Long value.
    """
    from mom._types.bytearray import \
        bytes_to_bytearray, bytearray_to_long

    #Make sure this is a positive number
    assert (ord(mpi_byte_string[4]) & 0x80) == 0

    byte_array = bytes_to_bytearray(mpi_byte_string[4:])
    return bytearray_to_long(byte_array)


def long_to_mpi(num):
    """
    Converts a long value into an OpenSSL-format MPI Bignum byte string.

    :param num:
        Long value.
    :returns:
        OpenSSL-format MPI Bignum byte string.
    """
    from mom._types.bytearray import \
        long_to_bytearray, bytearray_concat, \
        bytearray_to_bytes, bytearray_create_zeros

    byte_array = long_to_bytearray(num)
    ext = 0
    #If the high-order bit is going to be set,
    #add an extra byte of zeros
    if not (long_bit_length(num) & 0x7):
        ext = 1
    length = long_byte_count(num) + ext
    byte_array = bytearray_concat(bytearray_create_zeros(4+ext), byte_array)
    byte_array[0] = (length >> 24) & 0xFF
    byte_array[1] = (length >> 16) & 0xFF
    byte_array[2] = (length >> 8) & 0xFF
    byte_array[3] = length & 0xFF
    return bytearray_to_bytes(byte_array)
