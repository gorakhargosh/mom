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

.. autofunction:: base64_decode
.. autofunction:: base64_encode

.. autofunction:: base64_to_bytearray
.. autofunction:: bytearray_to_base64

.. autofunction:: bytes_to_hex
.. autofunction:: hex_to_bytes

.. autofunction:: bytes_to_base64
.. autofunction:: base64_to_bytes

.. autofunction:: bytes_to_decimal
.. autofunction:: decimal_to_bytes

.. autofunction:: bytes_to_long
.. autofunction:: long_to_bytes

.. autofunction:: bytes_to_bin
.. autofunction:: bin_to_bytes

.. autofunction:: base64_to_long
.. autofunction:: long_to_base64

.. autofunction:: bin_to_long
.. autofunction:: long_to_bin

.. autofunction:: hex_to_long
.. autofunction:: long_to_hex

.. autofunction:: mpi_to_long
.. autofunction:: long_to_mpi
"""

import struct
import binascii
from mom.builtins import bytes, hex, bin, byte_count, bit_count
from mom._types.bytearray import \
    bytearray_concat, \
    bytearray_create_zeros, \
    bytes_to_bytearray, \
    bytearray_to_bytes, \
    long_to_bytearray, \
    bytearray_to_long

try:
    # Check whether we have reduce as a built-in.
    __reduce_test__ = reduce((lambda num1, num2: num1 + num2), [1, 2, 3, 4])
except NameError:
    # Python 3k
    from functools import reduce


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


def bytes_to_hex(byte_string):
    """
    Converts a byte string to its hex representation.

    :param byte_string:
        Byte string.
    :returns:
        Hex-encoded byte string.
    """
    return binascii.b2a_hex(byte_string)


def hex_to_bytes(encoded):
    """
    Converts a hex byte string to its byte representation.

    :param encoded:
        Hex string.
    :returns:
        Byte string.
    """
    return binascii.a2b_hex(encoded)


def bytes_to_base64(byte_string):
    """
    Converts a byte string to its Base64 representation.
    (Mostly for consistency.)

    :param byte_string:
        Byte string.
    :returns:
        Base64-encoded byte string.
    """
    return base64_encode(byte_string)


def base64_to_bytes(encoded):
    """
    Decodes a base-64 encoded string into a byte string.

    :param encoded:
        Base-64 encoded byte string.
    :returns:
        byte string.
    """
    return base64_decode(encoded)


def bytes_to_decimal(byte_string):
    """
    Converts a byte string to its decimal representation.

    :param byte_string:
        Byte string.
    :returns:
        Decimal-encoded byte string.
    """
    #return bytes(int(bytes_to_hex(byte_string), 16))
    return bytes(bytes_to_long(byte_string))


def decimal_to_bytes(encoded):
    """
    Converts a decimal encoded string to its byte representation.

    :param encoded:
        Decimal encoded string.
    :returns:
        Byte string.
    """
    return long_to_bytes(long(encoded))


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
    return bytes_to_bytearray(base64_decode(encoded))


def bytearray_to_base64(byte_array):
    """
    Base-64 encodes a byte array.

    :param byte_array:
        The byte array.
    :returns:
        Base-64 encoded byte array without newlines.
    """
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
    return reduce((lambda first, second: (first << 1) + second), binary)


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


def bytes_to_bin(byte_string):
    """
    Converts a byte string to binary representation.

    :param byte_string:
        Byte string.
    :returns:
        Binary representation of the byte string.
    """
    return long_to_bin(bytes_to_long(byte_string))


def bin_to_bytes(binary):
    """
    Converts a binary representation to bytes.

    :param binary:
        Binary representation.
    :returns:
        Byte string.
    """
    return long_to_bytes(bin_to_long(binary))


def mpi_to_long(mpi_byte_string):
    """
    Converts an OpenSSL-format MPI Bignum byte string into a long.

    :param mpi_byte_string:
        OpenSSL-format MPI Bignum byte string.
    :returns:
        Long value.
    """
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
    byte_array = long_to_bytearray(num)
    ext = 0
    #If the high-order bit is going to be set,
    #add an extra byte of zeros
    if not (bit_count(num) & 0x7):
        ext = 1
    length = byte_count(num) + ext
    byte_array = bytearray_concat(bytearray_create_zeros(4+ext), byte_array)
    byte_array[0] = (length >> 24) & 0xFF
    byte_array[1] = (length >> 16) & 0xFF
    byte_array[2] = (length >> 8) & 0xFF
    byte_array[3] = length & 0xFF
    return bytearray_to_bytes(byte_array)
