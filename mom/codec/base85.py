#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2008 Nick Galbreath
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
:module: mom.codec.base85
:synopsis: Adobe-modified Base85 encoding and decoding functions.
:see: http://en.wikipedia.org/wiki/Ascii85

Functions
---------
.. autofunction:: b85encode
.. autofunction:: b85decode
"""

from __future__ import absolute_import, division

from struct import unpack, pack
from mom._compat import range


__all__ = [
    "b85encode",
    "b85decode",
]


CHAR_TO_INT = [
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256,   0, 256,   1,
    2,   3, 256,   4,   5,   6,   7,   8, 256,   9,  10,  11,
    12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22, 256,
    23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,
    35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,
    47,  48,  49,  50,  51,  52,  53,  54, 256,  55,  56,  57,
    58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
    70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,
    82,  83,  84, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256,
    256, 256, 256, 256]


INT_TO_CHAR = [
    '!',  '#',  '$',  '%', '\'',  '(',  ')',  '*',  '+',  '-',
    '.',  '/',  '0',  '1',  '2',  '3',  '4',  '5',  '6',  '7',
    '8',  '9',  ':',  '<',  '=',  '>',  '?',  '@',  'A',  'B',
    'C',  'D',  'E',  'F',  'G',  'H',  'I',  'J',  'K',  'L',
    'M',  'N',  'O',  'P',  'Q',  'R',  'S',  'T',  'U',  'V',
    'W',  'X',  'Y',  'Z',  '[',  ']',  '^',  '_',  '`',  'a',
    'b',  'c',  'd',  'e',  'f',  'g',  'h',  'i',  'j',  'k',
    'l',  'm',  'n',  'o',  'p',  'q',  'r',  's',  't',  'u',
    'v',  'w',  'x',  'y',  'z'
    ]


INT_TO_ASCII85 = "0123456789" \
                 "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                 "abcdefghijklmnopqrstuvwxyz" \
                 "!#$%&()*+-;<=>?@^_`{|}~"


def encode(raw_bytes):
    length = len(raw_bytes)

    # We need chunks of 32-bit (4 bytes chunk size) unsigned integers,
    # which means the length of the byte sequence must be divisible by 4.
    # Ensures length by appending additional padding zero bytes if required.
    # ceil_div(length, 4).
    num_uint32, remainder = divmod(length, 4)
    if remainder:
        padding_size = 4 - remainder
        raw_bytes += '\x00' * padding_size
        length = length + padding_size
        num_uint32 += 1
    else:
        padding_size = 0

    ascii_chars = []
    # Ascii85 uses a big-endian convention.
    # See: http://en.wikipedia.org/wiki/Ascii85
    for x in unpack('>' + 'L' * num_uint32, raw_bytes):
#        remainders = range(5)
#        for i in reversed(remainders):
#            remainders[i] = INT_TO_ASCII85[uint32_value % 85]
#            uint32_value //= 85
#        ascii_chars.extend(remainders)
        # Above loop unrolled:
        ascii_chars.extend((INT_TO_CHAR[x // 52200625],      # 85**4 = 52200625
                            INT_TO_CHAR[(x // 614125) % 85], # 85**3 = 614125
                            INT_TO_CHAR[(x // 7225) % 85],   # 85**2 = 7225
                            INT_TO_CHAR[(x // 85) % 85],     # 85**1 = 85
                            INT_TO_CHAR[x % 85]))            # 85**0 = 1
    return ''.join(ascii_chars)


# covert 4 characters into 5
def b85encode(raw_bytes):
    """
    Encode raw bytes using Base85.

    :param raw_bytes:
        The raw bytes to encode.
    :returns:
        The base85-encoded bytes are returned.
    """
    parts = []
    num_chunks = len(raw_bytes) // 4
    format = '!' + str(num_chunks) + 'I'
    for x in unpack(format, raw_bytes):
        # Network order (big endian), 32-bit unsigned integer
        # note: x86 is little endian
#        parts.extend((INT_TO_CHAR[x // 52200625],
#                      INT_TO_CHAR[(x // 614125) % 85],
#                      INT_TO_CHAR[(x // 7225) % 85],
#                      INT_TO_CHAR[(x // 85) % 85],
#                      INT_TO_CHAR[x % 85]))
        parts.append(INT_TO_CHAR[x // 52200625])
        parts.append(INT_TO_CHAR[(x // 614125) % 85])
        parts.append(INT_TO_CHAR[(x // 7225) % 85])
        parts.append(INT_TO_CHAR[(x // 85) % 85])
        parts.append(INT_TO_CHAR[x % 85])
    return ''.join(parts)


# MAY be 10-20% faster, when running on pysco
#   certainly 2x SLOWER when running normally.
#
# also does not use the 'struct' module which may be desirable
# to some
def _b85encode(raw_bytes):
    """
    Encode raw bytes using Base85.

    :param raw_bytes:
        The raw bytes to encode.
    :returns:
        The base85-encoded bytes are returned.
    """
    parts = []
    for i in range(0, len(raw_bytes), 4):
        chunk = raw_bytes[i:i+4]
        x = ord(chunk[3]) + 256*(
                ord(chunk[2]) + 256*(
                    ord(chunk[1]) + 256*ord(chunk[0])
                )
            )

        # network order (big endian), 32-bit unsigned integer
        # note: x86 is little endian
        parts.append(INT_TO_CHAR[x // 52200625])
        parts.append(INT_TO_CHAR[(x // 614125) % 85])
        parts.append(INT_TO_CHAR[(x // 7225) % 85])
        parts.append(INT_TO_CHAR[(x // 85) % 85])
        parts.append(INT_TO_CHAR[x % 85])
    return ''.join(parts)


# convert 5 characters to 4
def b85decode(encoded):
    """
    Decodes base85-encoded bytes to raw bytes.

    :param encoded:
        Encoded bytes.
    :returns:
        The base85-decoded bytes are returned.
    """
    parts = []
    for i in range(0, len(encoded), 5):
        bsum = 0
        for j in range(0,5):
            val = CHAR_TO_INT[ord(encoded[i+j])]
            bsum = 85*bsum + val
        tmp = pack('!I', bsum)
        parts.append(tmp)
        #parts += tmp
        #parts += unpack('cccc', tmp)
    return ''.join(parts)


# convert 5 characters to 4
def _b85decode(encoded):
    """
    Decodes base85-encoded bytes to raw bytes.

    :param encoded:
        Encoded bytes.
    :returns:
        The base85-decoded bytes are returned.
    """
    parts = []
    for i in range(0, len(encoded), 5):
        bsum = 0
        for j in range(0,5):
            val = CHAR_TO_INT[ord(encoded[i+j])]
            bsum = 85*bsum + val
        parts.append(chr((bsum >> 24) & 0xff))
        parts.append(chr((bsum >> 16) & 0xff))
        parts.append(chr((bsum >> 8) & 0xff))
        parts.append(chr(bsum & 0xff))
    return ''.join(parts)
