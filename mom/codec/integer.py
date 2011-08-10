#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

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
from mom.builtins import is_bytes, byte, b


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
        Raw bytes (base-256 representation).
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
    Convert a integer to bytes (base-256 representation)::

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
        Raw bytes (base-256 representation).
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
