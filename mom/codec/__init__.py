#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.codec
:synopsis: Many different types of common encode/decode function.

This module contains codecs for converting between long and bytes, and
the hex, base64, decimal, and binary representations of bytes.

Bytes base-encoding
-------------------
These codecs preserve bytes "as is" when decoding back to bytes. In a more
mathematical sense,

    ``g(f(x))`` is an **identity function**

where ``g`` is the decoder and ``f`` is the encoder.

.. autofunction:: base64_decode
.. autofunction:: base64_encode
.. autofunction:: bin_decode
.. autofunction:: bin_encode
.. autofunction:: decimal_decode
.. autofunction:: decimal_encode
.. autofunction:: hex_decode
.. autofunction:: hex_encode

Number-bytes conversion
-----------------------
These codecs are "lossy" as they don't preserve prefixed padding zero bytes.
In a more mathematical sense,

    ``g(f(x))`` is **almost** an identity function, but not exactly.

where ``g`` is the decoder and ``f`` is a encoder.

.. autofunction:: bytes_to_long
.. autofunction:: long_to_bytes
"""

from __future__ import absolute_import
from mom.functional import leading

__license__ = """\
The Apache Licence, Version 2.0

Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__ = ", ".join([
    "Barry Warsaw",
    "Yesudeep Mangalapilly",
])


import binascii

from mom.builtins import bytes
from mom.functional import ichunks


# Bytes base-encoding.

def base64_encode(raw_bytes):
    """
    Encodes raw bytes into base64 representation without appending a trailing
    newline character.

    :param raw_bytes:
        Bytes to encode.
    :returns:
        Base64 encoded string without newline characters.
    """
    return binascii.b2a_base64(raw_bytes)[:-1]


def base64_decode(encoded):
    """
    Decodes base64-encoded bytes into raw bytes.

    :param encoded:
        Base-64 encoded representation.
    :returns:
        Raw bytes.
    """
    return binascii.a2b_base64(encoded)


def hex_encode(raw_bytes):
    """
    Encodes raw bytes into hexadecimal representation.

    :param raw_bytes:
        Bytes.
    :returns:
        Hex-encoded representation.
    """
    return binascii.b2a_hex(raw_bytes)


def hex_decode(encoded):
    """
    Decodes hexadecimal-encoded bytes into raw bytes.

    :param encoded:
        Hex representation.
    :returns:
        Raw bytes.
    """
    return binascii.a2b_hex(encoded)


def decimal_encode(raw_bytes):
    """
    Encodes raw bytes into decimal representation. Leading zero bytes are
    preserved.

    :param raw_bytes:
        Bytes.
    :returns:
        Decimal-encoded representation.
    """
    padding = "0" * leading((lambda w: w == "\x00"), raw_bytes)
    long_val = bytes_to_long(raw_bytes)
    return padding + bytes(long_val) if long_val else padding


def decimal_decode(encoded):
    """
    Decodes decimal-encoded bytes to raw bytes. Leading zeros are converted to
    leading zero bytes.

    :param encoded:
        Decimal-encoded representation.
    :returns:
        Raw bytes.
    """
    padding = '\x00' * leading((lambda x: x == "0"), encoded)
    long_val = long(encoded)
    return padding + long_to_bytes(long_val) if long_val else padding


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
def bin_encode(raw_bytes):
    """
    Encodes raw bytes into binary representation.

    :param raw_bytes:
        Raw bytes.
    :returns:
        Binary representation.
    """
    return ''.join(_HEX_TO_BIN_LOOKUP[hex_char]
                   for hex_char in hex_encode(raw_bytes))

    # Prefixed zero-bytes destructive. '\x00\x00' treated as '\x00'
    #return bin(bytes_to_long(byte_string))[2:]


def bin_decode(encoded):
    """
    Decodes binary-encoded bytes into raw bytes.

    :param encoded:
        Binary representation.
    :returns:
        Raw bytes.
    """
    return hex_decode(''.join(_BIN_TO_HEX_LOOKUP[nibble]
                              for nibble in map(lambda w: "".join(w),
                                                ichunks(encoded, 4))))

    # Prefixed zero-bytes destructive. '\x00\x00\x00' treated as '\x00'
    #return long_to_bytes(long(encoded, 2))


# Taken from PyCrypto "as is".
# Improved conversion functions contributed by Barry Warsaw, after
# careful benchmarking.
def long_to_bytes(num, blocksize=0):
    """
    Convert a long integer to bytes::

        long_to_bytes(n:long, blocksize:int) : string

    .. WARNING: Does not preserve leading zeros.

    :param num:
        Long value
    :param blocksize:
        If optional blocksize is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        blocksize.
    :returns:
        Raw bytes.
    """
    import struct

    # After much testing, this algorithm was deemed to be the fastest
    s = ''
    num = long(num)
    pack = struct.pack
    while num > 0:
        s = pack('>I', num & 0xffffffffL) + s
        num >>= 32

    # Strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\x00':
            break
    else:
        # only happens when n == 0
        s = '\x00'
        i = 0
    s = s[i:]

    # Add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\x00' + s
    return s


def bytes_to_long(raw_bytes):
    """
    Converts bytes to long integer::

        bytes_to_long(bytes) : long

    This is (essentially) the inverse of long_to_bytes().

    .. WARNING: Does not preserve leading zero bytes.

    :param raw_bytes:
        Raw bytes.
    :returns:
        Long.
    """
    import struct

    acc = 0L
    unpack = struct.unpack
    length = len(raw_bytes)
    if length % 4:
        extra = (4 - length % 4)
        raw_bytes = '\x00' * extra + raw_bytes
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', raw_bytes[i:i+4])[0]
    return acc

