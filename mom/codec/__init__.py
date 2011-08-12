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

This module contains codecs for converting between hex, base64, base85,
decimal, and binary representations of bytes.

Understand that bytes are simply base-256 representation.

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
.. autofunction:: base58_encode
.. autofunction:: base58_decode
.. autofunction:: hex_encode
.. autofunction:: hex_decode
.. autofunction:: decimal_encode
.. autofunction:: decimal_decode
.. autofunction:: bin_encode
.. autofunction:: bin_decode

.. automodule:: mom.codec.base58
.. automodule:: mom.codec.base85
.. automodule:: mom.codec.integer
.. automodule:: mom.codec.json
.. automodule:: mom.codec.text

"""

from __future__ import absolute_import

import binascii
from mom._compat import have_python3, ZERO_BYTE
from mom.builtins import is_bytes, b
from mom.functional import leading, chunks
from mom.codec.integer import bytes_to_integer, integer_to_bytes
from mom.codec.base58 import b58decode, b58encode
from mom.codec.base85 import b85encode, b85decode, rfc1924_b85encode, \
    rfc1924_b85decode


__all__ = [
    "base85_encode",
    "base85_decode",
    "base64_encode",
    "base64_decode",
    "base64_urlsafe_encode",
    "base64_urlsafe_decode",
    "base58_encode",
    "base58_decode",
    "hex_encode",
    "hex_decode",
    "decimal_encode",
    "decimal_decode",
    "bin_encode",
    "bin_decode",
]



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


def base58_encode(raw_bytes):
    """
    Encodes raw bytes into base-58 representation. URL-safe and human safe.

    Encode your Unicode strings to a byte encoding before base-58-encoding
    them.

    Convenience wrapper for consistency.

    :param raw_bytes:
        Bytes to encode.
    :returns:
        Base-58 encoded bytes.
    """
    return b58encode(raw_bytes)


def base58_decode(encoded):
    """
    Decodes base-58-encoded bytes into raw bytes.

    Convenience wrapper for consistency.

    :param encoded:
        Base-58 encoded representation.
    :returns:
        Raw bytes.
    """
    return b58decode(encoded)


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

