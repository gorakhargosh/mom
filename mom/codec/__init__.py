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
:module: mom.codec
:synopsis: Many different types of common encode/decode function.

This module contains codecs for converting between integers and bytes, and
the hex, base64, base85, decimal, and binary representations of bytes.

Bytes base-encoding
-------------------
These codecs preserve bytes "as is" when decoding back to bytes. In a more
mathematical sense,

    ``g(f(x))`` is an **identity function**

where ``g`` is the decoder and ``f`` is the encoder.

Why have we reproduced base64 encoding/decoding functions here when the
standard library has them? Well, those functions behave differently in
Python 2.x and Python 3.x. The Python 3.x equivalents do not accept Unicode
strings as their arguments, whereas the Python 2.x versions would happily
encode your Unicode strings without warning you-you know that you are supposed
to encode them to UTF-8 or another byte encoding before you base64-encode them
right? These wrappers are re-implemented so that you do not make these mistakes.
Use them. They will help prevent unexpected bugs.

.. autofunction:: base85_encode
.. autofunction:: base85_decode
.. autofunction:: base64_encode
.. autofunction:: base64_decode
.. autofunction:: base64_urlsafe_encode
.. autofunction:: base64_urlsafe_decode
.. autofunction:: hex_encode
.. autofunction:: hex_decode
.. autofunction:: decimal_encode
.. autofunction:: decimal_decode
.. autofunction:: bin_encode
.. autofunction:: bin_decode

Number-bytes conversion
-----------------------
These codecs are "lossy" as they don't preserve prefixed padding zero bytes.
In a more mathematical sense,

    ``g(f(x))`` is **almost** an identity function, but not exactly.

where ``g`` is the decoder and ``f`` is a encoder.

.. autofunction:: bytes_to_integer
.. autofunction:: integer_to_bytes
"""

from __future__ import absolute_import

import binascii
from struct import pack, unpack
from mom._compat import have_python3
from mom.builtins import is_bytes, b, byte
from mom.functional import leading, chunks
from mom.codec.base85 import b85encode, b85decode, rfc1924_b85encode, \
    rfc1924_b85decode


__all__ = [
    "base85_encode",
    "base85_decode",
    "base64_encode",
    "base64_decode",
    "base64_urlsafe_encode",
    "base64_urlsafe_decode",
    "hex_encode",
    "hex_decode",
    "decimal_encode",
    "decimal_decode",
    "bin_encode",
    "bin_decode",
    "bytes_to_integer",
    "integer_to_bytes",
]

ZERO_BYTE = byte(0)

# Bytes base-encoding.

_B85_DECODE_MAP = {
    "ASCII85": b85decode,
    "RFC1924": rfc1924_b85decode,
}
_B85_ENCODE_MAP = {
    "ASCII85": b85encode,
    "RFC1924": rfc1924_b85encode,
}

def base85_encode(raw_bytes, charset="ASCII85", _encode_map=_B85_ENCODE_MAP):
    """
    Encodes raw bytes into ASCII85 representation.

    Encode your Unicode strings to a byte encoding before base85-encoding them.

    :param raw_bytes:
        Bytes to encode.
    :param charset:
        "ASCII85" (default) or "RFC1924".
    :returns:
        ASCII85 encoded string.
    """
    try:
        return _encode_map[charset.upper()](raw_bytes)
    except KeyError:
        raise ValueError("Invalid character set specified: %r" % charset)


def base85_decode(encoded, charset="ASCII85", _decode_map=_B85_DECODE_MAP):
    """
    Decodes ASCII85-encoded bytes into raw bytes.

    :param encoded:
        ASCII85 encoded representation.
    :param charset:
        "ASCII85" (default) or "RFC1924".
    :returns:
        Raw bytes.
    """
    try:
        return _decode_map[charset.upper()](encoded)
    except KeyError:
        raise ValueError("Invalid character set specified: %r" % charset)


def base64_urlsafe_encode(raw_bytes):
    """
    Encodes raw bytes into URL-safe base64 bytes.

    Encode your Unicode strings to a byte encoding before base64-encoding them.

    :param raw_bytes:
        Bytes to encode.
    :returns:
        Base64 encoded string without newline characters.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be bytes: got %r" %
                        type(raw_bytes).__name__)
    # This is 3-4x faster than urlsafe_b64decode() -Guido.
    # We're not using the base64.py wrapper around binascii because
    # this module itself is a wrapper. binascii is implemented in C, so
    # we avoid module overhead however small.
    encoded = binascii.b2a_base64(raw_bytes)[:-1]
    return encoded.rstrip(b('=')).replace(b('+'), b('-')).replace(b('/'),b('_'))


def base64_urlsafe_decode(encoded):
    """
    Decodes URL-safe base64-encoded bytes into raw bytes.

    :param encoded:
        Base-64 encoded representation.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("argument must be bytes: got %r" %
                        type(encoded).__name__)
    remainder = len(encoded) % 4
    if remainder:
        encoded += b('=') * (4 - remainder)
    # This is 3-4x faster than urlsafe_b64decode() -Guido.
    # We're not using the base64.py wrapper around binascii because
    # this module itself is a wrapper. binascii is implemented in C, so
    # we avoid module overhead however small.
    encoded = encoded.replace(b('-'), b('+')).replace(b('_'),b('/'))
    return binascii.a2b_base64(encoded)


def base64_encode(raw_bytes):
    """
    Encodes raw bytes into base64 representation without appending a trailing
    newline character. Not URL-safe.

    Encode your Unicode strings to a byte encoding before base64-encoding them.

    :param raw_bytes:
        Bytes to encode.
    :returns:
        Base64 encoded bytes without newline characters.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be bytes: got %r" %
                        type(raw_bytes).__name__)
    return binascii.b2a_base64(raw_bytes)[:-1]


def base64_decode(encoded):
    """
    Decodes base64-encoded bytes into raw bytes. Not URL-safe.

    :param encoded:
        Base-64 encoded representation.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("argument must be bytes: got %r" %
                        type(encoded).__name__)
    return binascii.a2b_base64(encoded)


def hex_encode(raw_bytes):
    """
    Encodes raw bytes into hexadecimal representation.

    Encode your Unicode strings to a byte encoding before hex-encoding them.

    :param raw_bytes:
        Bytes.
    :returns:
        Hex-encoded representation.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    return binascii.b2a_hex(raw_bytes)


def hex_decode(encoded):
    """
    Decodes hexadecimal-encoded bytes into raw bytes.

    :param encoded:
        Hex representation.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("argument must be bytes: got %r" %
                        type(encoded).__name__)
    return binascii.a2b_hex(encoded)


def decimal_encode(raw_bytes):
    """
    Encodes raw bytes into decimal representation. Leading zero bytes are
    preserved.

    Encode your Unicode strings to a byte encoding before decimal-encoding them.

    :param raw_bytes:
        Bytes.
    :returns:
        Decimal-encoded representation.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    padding = b("0") * leading((lambda w: w == ZERO_BYTE[0]), raw_bytes)
    int_val = bytes_to_integer(raw_bytes)
    return padding + str(int_val).encode("ascii") if int_val else padding


def decimal_decode(encoded):
    """
    Decodes decimal-encoded bytes to raw bytes. Leading zeros are converted to
    leading zero bytes.

    :param encoded:
        Decimal-encoded representation.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("argument must be bytes: got %r" %
                        type(encoded).__name__)
    padding = ZERO_BYTE * leading((lambda x: x == b("0")[0]), encoded)
    int_val = int(encoded)
    return padding + integer_to_bytes(int_val) if int_val else padding


_HEX_TO_BIN_LOOKUP = {
    b('0'): b('0000'),
    b('1'): b('0001'),
    b('2'): b('0010'),
    b('3'): b('0011'),
    b('4'): b('0100'),
    b('5'): b('0101'),
    b('6'): b('0110'),
    b('7'): b('0111'),
    b('8'): b('1000'),
    b('9'): b('1001'),
    b('a'): b('1010'), b('A'): b('1010'),
    b('b'): b('1011'), b('B'): b('1011'),
    b('c'): b('1100'), b('C'): b('1100'),
    b('d'): b('1101'), b('D'): b('1101'),
    b('e'): b('1110'), b('E'): b('1110'),
    b('f'): b('1111'), b('F'): b('1111'),
}
if have_python3:
    # Indexing into Python 3 bytes yields ords, not single-byte strings.
    _HEX_TO_BIN_LOOKUP = \
        dict((k[0], v) for k, v in _HEX_TO_BIN_LOOKUP.items())
_BIN_TO_HEX_LOOKUP = {
    b('0000'): b('0'),
    b('0001'): b('1'),
    b('0010'): b('2'),
    b('0011'): b('3'),
    b('0100'): b('4'),
    b('0101'): b('5'),
    b('0110'): b('6'),
    b('0111'): b('7'),
    b('1000'): b('8'),
    b('1001'): b('9'),
    b('1010'): b('a'),
    b('1011'): b('b'),
    b('1100'): b('c'),
    b('1101'): b('d'),
    b('1110'): b('e'),
    b('1111'): b('f'),
}
def bin_encode(raw_bytes):
    """
    Encodes raw bytes into binary representation.

    Encode your Unicode strings to a byte encoding before binary-encoding them.

    :param raw_bytes:
        Raw bytes.
    :returns:
        Binary representation.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    return b('').join(_HEX_TO_BIN_LOOKUP[hex_char]
                   for hex_char in hex_encode(raw_bytes))

    # Prefixed zero-bytes destructive. '\x00\x00' treated as '\x00'
    #return bin(bytes_to_integer(byte_string))[2:]


def bin_decode(encoded):
    """
    Decodes binary-encoded bytes into raw bytes.

    :param encoded:
        Binary representation.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("argument must be bytes: got %r" %
                        type(encoded).__name__)
    return hex_decode(b('').join(_BIN_TO_HEX_LOOKUP[nibble]
                              for nibble in chunks(encoded, 4)))

    # Prefixed zero-bytes destructive. '\x00\x00\x00' treated as '\x00'
    #return integer_to_bytes(int(encoded, 2))


def bytes_to_integer(raw_bytes):
    """
    Converts bytes to integer::

        bytes_to_integer(bytes) : integer

    This is (essentially) the inverse of integer_to_bytes().

    Encode your Unicode strings to a byte encoding before converting them.

    .. WARNING: Does not preserve leading zero bytes.

    :param raw_bytes:
        Raw bytes.
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
    Converts bytes to integer::

        bytes_to_integer(bytes) : integer

    This is (essentially) the inverse of integer_to_bytes().

    Encode your Unicode strings to a byte encoding before converting them.

    .. WARNING: Does not preserve leading zero bytes.

    :param raw_bytes:
        Raw bytes.
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


def _integer_to_bytes(num, blocksize=0):
    """
    Convert a integer to bytes::

        integer_to_bytes(n:int, blocksize:int) : string

    .. WARNING: Does not preserve leading zeros.

    :param num:
        Integer value
    :param blocksize:
        If optional blocksize is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        blocksize.
    :returns:
        Raw bytes.
    """
    raw_bytes = b('')
    num = int(num)
    while num > 0:
        raw_bytes = pack('>I', num & 0xffffffff) + raw_bytes
        num >>= 32

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
    if blocksize > 0 and len(raw_bytes) % blocksize:
        raw_bytes = (blocksize - len(raw_bytes) % blocksize) * \
                    ZERO_BYTE + raw_bytes
    return raw_bytes


def integer_to_bytes(num, chunk_size=0):
    """
    Convert a integer to bytes::

        integer_to_bytes(n:int, chunk_size:int) : string

    .. WARNING:
        Does not preserve leading zeros if you don't specify a chunk size.

    :param num:
        Integer value
    :param chunk_size:
        If optional chunk size is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        ``chunk_size``.
    :returns:
        Raw bytes.
    """
    num = int(num)
    raw_bytes = b('')
    if not num:
        raw_bytes = ZERO_BYTE
    while num > 0:
        raw_bytes = pack('>I', num & 0xffffffff) + raw_bytes
        num >>= 32

    length = len(raw_bytes)
    if chunk_size > 0:
        remainder = length % chunk_size
        if remainder:
            raw_bytes = (chunk_size - remainder) * ZERO_BYTE + raw_bytes
    else:
        # Count the number of leading zeros.
        leading_zeros = 0
        for leading_zeros in range(length):
            if raw_bytes[leading_zeros] != ZERO_BYTE[0]:
                break
        raw_bytes = raw_bytes[leading_zeros:]
    return raw_bytes
