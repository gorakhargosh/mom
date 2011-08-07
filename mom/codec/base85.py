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
#
# WARNING:
# --------
# Before you begin fiddling with the source code, know that this is not
# how clean and legible Python software is written. This code employs a few
# common tricks to reduce computation time. Ensure that you understand them
# before working with this code.

"""
:module: mom.codec.base85
:synopsis: ASCII-85 and RFC1924 Base85 encoding and decoding functions.
:see: http://en.wikipedia.org/wiki/Ascii85

Functions
---------
.. autofunction:: b85encode
.. autofunction:: b85decode
.. autofunction:: rfc1924_b85encode
.. autofunction:: rfc1924_b85decode
.. autofunction:: ipv6_b85encode
.. autofunction:: ipv6_b85decode
"""

from __future__ import absolute_import, division

import re
from struct import unpack, pack
from mom.builtins import is_bytes
from mom._compat import range


__all__ = [
    "b85encode",
    "b85decode",
    "rfc1924_b85encode",
    "rfc1924_b85decode",
    "ASCII85_PREFIX",
    "ASCII85_SUFFIX",
    "ipv6_b85encode",
    "ipv6_b85decode",
]


def _ascii85_chr(num):
    """
    Converts an ordinal into its ASCII85 character.

    :param num:
        Ordinal value.
    :returns:
        base85 character.
    """
    return chr(num + 33)


def _ascii85_ord(char):
    """
    Converts an ASCII85 character into its ordinal.

    :param char:
        Base85 character
    :returns:
        Ordinal value.
    """
    return ord(char) - 33

# Use this if you want the base85 codec to encode/decode including
# ASCII85 prefixes/suffixes.
ASCII85_PREFIX = '<~'
ASCII85_SUFFIX = '~>'

WHITESPACE_PATTERN = re.compile(r'(\s)*', re.MULTILINE)

# ASCII85 characters.
ASCII85_CHARS = "".join(map(_ascii85_chr, range(85)))
ASCII85_ORDS = dict((x, _ascii85_ord(x)) for x in ASCII85_CHARS)

# http://tools.ietf.org/html/rfc1924
RFC1924_CHARS = "0123456789" \
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                "abcdefghijklmnopqrstuvwxyz" \
                "!#$%&()*+-;<=>?@^_`{|}~"
RFC1924_ORDS = dict((x, i) for i, x in enumerate(RFC1924_CHARS))


# Pre-computed powers (array index) of 85 used to unroll encoding loops
# Therefore, 85**i is equivalent to POW_85[i] for index 0 through 19
# (inclusive).
#
# Calculated using:
# POW_85 = tuple([85**x for x in range(20)]).
POW_85 = (
    1,
    85,
    7225,
    614125,
    52200625,
    4437053125,
    377149515625,
    32057708828125,
    2724905250390625,
    231616946283203125,
    19687440434072265625L,
    1673432436896142578125L,
    142241757136172119140625L,
    12090549356574630126953125L,
    1027696695308843560791015625L,
    87354219101251702667236328125L,
    7425108623606394726715087890625L,
    631134233006543551770782470703125L,
    53646409805556201900516510009765625L,
    4559944833472277161543903350830078125L
)

def check_compact_char_occurrence(sequence, zero_char='z', chunk_size=5):
    """
    Ensures 'z' characters do not occur in the middle of 5-tuple chunks
    when decoding. It will raise a ``ValueError`` if such an occurrence is
    found.

    :param sequence:
        The encoded sequence.
    :param zero_char:
        The 'z' character (default 'z').
    :param chunk_size:
        5 (default).
    """
    counter = 0
    for i, x in enumerate(sequence):
        if x == zero_char:
            if counter % chunk_size:
                raise ValueError(
                    'zero char `%r` occurs in the middle of a chunk ' \
                    'at index %d' % (zero_char, i)
                )
            else:
                counter = 0
        else:
            counter += 1

            
def b85encode(raw_bytes,
              prefix=None,
              suffix=None,
              _padding=False,
              _base85_chars=ASCII85_CHARS,
              _compact_zero=True,
              _compact_char='z',
              _pow_85=POW_85):
    """
    ASCII-85 encodes a sequence of raw bytes.

    The character set in use is::

        ASCII 33 ("!") to ASCII 117 ("u")

    If the number of raw bytes is not divisible by 4, the byte sequence
    is padded with up to 3 null bytes before encoding. After encoding,
    as many bytes as were added as padding are removed from the end of the
    encoded sequence if ``padding`` is ``False`` (default).

    Encodes a zero-group (\x00\x00\x00\x00) as 'z' instead of '!!!!!'.

    The resulting encoded ASCII string is *not URL-safe* nor is it
    safe to include within SGML/XML/HTML documents. You will need to escape
    special characters if you decide to include such an encoded string
    within these documents.

    :param raw_bytes:
        Raw bytes.
    :param prefix:
        The prefix used by the encoded text. None by default.
    :param suffix:
        The suffix used by the encoded text. None by default.
    :param _padding:
        (Internal) ``True`` if padding should be included; ``False`` (default)
        otherwise. You should not need to use this--the default value is
        usually the expected value. If you find a need to use this more
        often than not, *tell us* so that we can make this argument public.
    :param _base85_chars:
        (Internal) Character set to use.
    :param _compact_zero:
        (Internal) Encodes a zero-group (\x00\x00\x00\x00) as 'z' instead of
        '!!!!!' if this is ``True`` (default).
    :param _compact_char:
        (Internal) Character used to represent compact groups ('z' default)
    :param _pow_85:
        (Internal) Powers of 85 lookup table.
    :returns:
        ASCII-85 encoded bytes.
    """
    prefix = prefix or ''
    suffix = suffix or ''

    if not is_bytes(raw_bytes):
        raise TypeError("argument must be raw bytes: got %r" %
                        type(raw_bytes).__name__)

    # We need chunks of 32-bit (4 bytes chunk size) unsigned integers,
    # which means the length of the byte sequence must be divisible by 4.
    # Ensures length by appending additional padding zero bytes if required.
    # ceil_div(length, 4).
    num_uint32, remainder = divmod(len(raw_bytes), 4)
    if remainder:
        # TODO: Write a test for this.
        # If we have a remainder, upto 3 padding bytes are added,
        # which means in the encoded output sans-padding, the final 5-tuple
        # chunk will have at least 2 characters.
        padding_size = 4 - remainder
        raw_bytes += '\x00' * padding_size
        num_uint32 += 1
    else:
        padding_size = 0

    ascii_chars = []
    # Ascii85 uses a big-endian convention.
    # See: http://en.wikipedia.org/wiki/Ascii85
    for x in unpack('>' + 'L' * num_uint32, raw_bytes):
#        chars = list(range(5))
#        for i in reversed(chars):
#            chars[i] = _base85_chars[x % 85]
#            x //= 85
#        ascii_chars.extend(chars)
        # Above loop unrolled:
        ascii_chars.extend((
            _base85_chars[x // _pow_85[4]], # Don't need %85. Already <85.
            _base85_chars[(x // _pow_85[3]) % 85],
            _base85_chars[(x // _pow_85[2]) % 85],
            _base85_chars[(x // 85) % 85],     # 85**1 = 85
            _base85_chars[x % 85],             # 85**0 = 1
        ))
    if padding_size and not _padding:
        # Only as much padding added before encoding is removed after encoding.
        ascii_chars = ascii_chars[:-padding_size]
    encoded = ''.join(ascii_chars)
    encoded = encoded.replace('!!!!!', _compact_char) \
              if _compact_zero else encoded
    return prefix + encoded + suffix


def b85decode(encoded,
              prefix=None,
              suffix=None,
              _base85_ords=ASCII85_ORDS,
              _base85_chars=ASCII85_CHARS,
              _ignore_pattern=WHITESPACE_PATTERN,
              _uncompact_zero=True,
              _compact_char='z'):
    """
    Decodes a base85 encoded string into raw bytes.

    :param encoded:
        Encoded ASCII string.
    :param prefix:
        The prefix used by the encoded text. None by default.
    :param suffix:
        The suffix used by the encoded text. None by default.
    :param _ignore_pattern:
        (Internal) By default all whitespace is ignored. This must be an
        ``re.compile()`` instance. You should not need to use this.
    :param _base85_ords:
        (Internal) A function to convert a base85 character to its ordinal
        value. You should not need to use this.
    :param _uncompact_zero:
        (Internal) Treats 'z' (a zero-group (\x00\x00\x00\x00)) as a '!!!!!'
        if ``True`` (default).
    :param _compact_char:
        (Internal) Character used to represent compact groups ('z' default)
    :returns:
        Base85-decoded raw bytes.
    """
    prefix = prefix or ""
    suffix = suffix or ""

    # Must be US-ASCII, not Unicode.
    encoded = encoded.encode("latin1")

    # ASCII-85 ignores whitespace.
    if _ignore_pattern:
        encoded = re.sub(_ignore_pattern, '', encoded)

    # Strip the prefix and suffix.
    if prefix and encoded.startswith(prefix):
        encoded = encoded[len(prefix):]
    if suffix and encoded.endswith(suffix):
        encoded = encoded[:-len(suffix)]

    # Replace all the 'z' occurrences with '!!!!!'
    if _uncompact_zero:
        check_compact_char_occurrence(encoded, _compact_char, 5)
        encoded = encoded.replace(_compact_char, '!!!!!')

    # We want 5-tuple chunks, so pad with as many base85_ord == 84 characters
    # as required to satisfy the length.
    length = len(encoded)
    num_uint32s, remainder = divmod(length, 5)
    if remainder:
        padding_character = _base85_chars[84]   # 'u' for ASCII85.
        padding_size = 5 - remainder
        encoded += padding_character * padding_size
        num_uint32s += 1
        length += padding_size
    else:
        padding_size = 0

    uint32s = []
    #for chunk in chunks(encoded, 5):
    for i in range(0, length, 5):
        a, b, c, d, e = chunk = encoded[i:i+5]
#        uint32_value = 0
#        try:
#            for char in chunk:
#                uint32_value = uint32_value * 85 + _base85_ords[char]
#        except KeyError:
#            raise OverflowError("Cannot decode chunk `%r`" % chunk)
#        Above loop unrolled:
        try:
            uint32_value = ((((_base85_ords[a] *
                            85 + _base85_ords[b]) *
                            85 + _base85_ords[c]) *
                            85 + _base85_ords[d]) *
                            85 + _base85_ords[e])
        except KeyError:
            raise OverflowError("Cannot decode chunk `%r`" % chunk)

        # Groups of characters that decode to a value greater than 2**32 − 1
        # (encoded as "s8W-!") will cause a decoding error.
        if uint32_value > 4294967295: # 2**32 - 1
            raise OverflowError("Cannot decode chunk `%r`" % chunk)

        uint32s.append(uint32_value)

    raw_bytes = pack(">" + "L" * num_uint32s, *uint32s)
    if padding_size:
        # Only as much padding added before decoding is removed after decoding.
        raw_bytes = raw_bytes[:-padding_size]
    return raw_bytes


def rfc1924_b85encode(raw_bytes,
                      _padding=False):
    """
    Base85 encodes using the RFC1924 character set.

    The character set is::

        0–9, A–Z, a–z, and then !#$%&()*+-;<=>?@^_`{|}~

    These characters are specifically not included::

        "',./:[]\

    This is the encoding used by Mercurial, for example. They chose the IPv6
    character set and encode using the Adobe encoding method.
    This implementation also does not compact zero-byte sequences.

    :see: http://tools.ietf.org/html/rfc1924
    :param raw_bytes:
        Raw bytes.
    :param _padding:
        (Internal) Whether padding should be included in the encoded output.
        (Default ``False``, which is usually what you want.)
    :returns:
        RFC1924 base85 encoded string.
    """
    return b85encode(raw_bytes,
                     _padding=_padding,
                     _base85_chars=RFC1924_CHARS,
                     _compact_zero=False)


def rfc1924_b85decode(encoded):
    """
    Base85 decodes using the RFC1924 character set.

    This is the encoding used by Mercurial, for example. They chose the IPv6
    character set and encode using the Adobe encoding method.
    This implementation also does not uncompact zero-byte sequences.

    :see: http://tools.ietf.org/html/rfc1924
    :param encoded:
        RFC1924 Base85 encoded string.
    :returns:
        Decoded bytes.
    """
    return b85decode(encoded,
                     _base85_ords=RFC1924_ORDS,
                     _base85_chars=RFC1924_CHARS,
                     _uncompact_zero=False)



def ipv6_b85encode(uint128,
                   _base85_chars=RFC1924_CHARS,
                   _pow_85=POW_85):
    """
    Encodes a 128-bit unsigned integer using the RFC 1924 base-85 encoding.
    Used to encode IPv6 addresses or 128-bit chunks.

    :param uint128:
        A 128-bit unsigned integer to be encoded.
    :param _base85_chars:
        (Internal) Base85 encoding charset lookup table.
    :param _pow_85:
        (Internal) Powers of 85 lookup table.
    :returns:
        RFC1924 Base85-encoded string.
    """
    if uint128 < 0:
        raise ValueError("Number is not a 128-bit unsigned integer: got %d" %
                         uint128)
    if uint128 > 340282366920938463463374607431768211455L: # 2**128 - 1
        raise OverflowError("Number is not a 128-bit unsigned integer: %d" %
                            uint128)
#    encoded = list(range(20))
#    for i in reversed(encoded):
#        encoded[i] = _base85_chars[uint128 % 85]
#        uint128 //= 85
    # Above loop unrolled:
    encoded = (
        _base85_chars[(uint128 // _pow_85[19])], # Don't need %85. Already < 85
        _base85_chars[(uint128 // _pow_85[18]) % 85],
        _base85_chars[(uint128 // _pow_85[17]) % 85],
        _base85_chars[(uint128 // _pow_85[16]) % 85],
        _base85_chars[(uint128 // _pow_85[15]) % 85],
        _base85_chars[(uint128 // _pow_85[14]) % 85],
        _base85_chars[(uint128 // _pow_85[13]) % 85],
        _base85_chars[(uint128 // _pow_85[12]) % 85],
        _base85_chars[(uint128 // _pow_85[11]) % 85],
        _base85_chars[(uint128 // _pow_85[10]) % 85],
        _base85_chars[(uint128 // _pow_85[9]) % 85],
        _base85_chars[(uint128 // _pow_85[8]) % 85],
        _base85_chars[(uint128 // _pow_85[7]) % 85],
        _base85_chars[(uint128 // _pow_85[6]) % 85],
        _base85_chars[(uint128 // _pow_85[5]) % 85],
        _base85_chars[(uint128 // _pow_85[4]) % 85],
        _base85_chars[(uint128 // _pow_85[3]) % 85],
        _base85_chars[(uint128 // _pow_85[2]) % 85],
        _base85_chars[(uint128 // 85) % 85],   #85**1 == 85
        _base85_chars[uint128 % 85],           #85**0 == 1
    )
    return ''.join(encoded)


def ipv6_b85decode(encoded,
                   _base85_ords=RFC1924_ORDS):
    """
    Decodes an RFC1924 Base-85 encoded string to its 128-bit unsigned integral
    representation. Used to base85-decode IPv6 addresses or 128-bit chunks.

    :param encoded:
        RFC1924 Base85-encoded string.
    :param _base85_ords:
        (Internal) Look up table.
    :param _whitespace:
        (Internal) Whitespace characters.
    :returns:
        A 128-bit unsigned integer.
    """
    encoded = encoded.encode("latin1")
    if len(encoded) != 20:
        raise ValueError(
            "Encoded IPv6 value must be exactly 20 characters long: got %r" %
            encoded
        )
    #uint128 = 0L
    #for char in encoded:
    #    uint128 = uint128 * 85 + _base85_ords[char]
    # Above loop unrolled to process 4 5-tuple chunks instead:
    #a, b, c, d, e = encoded[0:5]
    # a = encoded[0]..e = encoded[4]
    uint128 = ((((_base85_ords[encoded[0]] *
                85 + _base85_ords[encoded[1]]) *
                85 + _base85_ords[encoded[2]]) *
                85 + _base85_ords[encoded[3]]) *
                85 + _base85_ords[encoded[4]])
    #a, b, c, d, e = encoded[5:10]
    # a = encoded[5]..e = encoded[9]
    uint128 = (((((uint128 * 85 + _base85_ords[encoded[5]]) *
                85 + _base85_ords[encoded[6]]) *
                85 + _base85_ords[encoded[7]]) *
                85 + _base85_ords[encoded[8]]) *
                85 + _base85_ords[encoded[9]])
    #a, b, c, d, e = encoded[10:15]
    # a = encoded[10]..e = encoded[14]
    uint128 = (((((uint128 * 85 + _base85_ords[encoded[10]]) *
                85 + _base85_ords[encoded[11]]) *
                85 + _base85_ords[encoded[12]]) *
                85 + _base85_ords[encoded[13]]) *
                85 + _base85_ords[encoded[14]])
    #a, b, c, d, e = encoded[15:20]
    # a = encoded[15]..e = encoded[19]
    uint128 = (((((uint128 * 85 + _base85_ords[encoded[15]]) *
                85 + _base85_ords[encoded[16]]) *
                85 + _base85_ords[encoded[17]]) *
                85 + _base85_ords[encoded[18]]) *
                85 + _base85_ords[encoded[19]])
    return uint128
