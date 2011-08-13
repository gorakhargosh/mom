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
:see: http://tools.ietf.org/html/rfc1924
:see: http://www.piclist.com/techref/method/encode.htm

Where should you use base85?
----------------------------
Base85-encoding is used to compactly represent binary data in 7-bit ASCII.
It is, therefore, 7-bit MIME-safe but not safe to use in URLs, SGML, HTTP
cookies, and other similar places. Example scenarios where Base85 encoding
can be put to use are Adobe PDF documents, Adobe PostScript format, binary
diffs (patches), efficiently storing RSA keys, etc.

The ASCII85 character set-based encoding is mostly used by Adobe PDF and
PostScript formats. It may also be used to store RSA keys or binary data
with a lot of zero byte sequences. The RFC1924 character set-based encoding,
however, may be used to compactly represent 128-bit unsigned integers (like
IPv6 addresses) or binary diffs. Encoding based on RFC1924 does not compact
zero byte sequences, so this form of encoding is less space-efficient than
the ASCII85 version which compacts redundant zero byte sequences.

About base85 and this implementation
------------------------------------
Base-85 represents 4 bytes as 5 ASCII characters. This is a 7% improvement
over base-64, which translates to a size increase of ~25% over plain
binary data for base-85 versus that of ~37% for base-64.

However, because the base64 encoding routines in Python are implemented
in C, base-64 may be less expensive to compute. This implementation of
base-85 uses a lot of tricks to reduce computation time and is hence
generally faster than many other implementations. If computation speed
is a concern for you, please contribute a C implementation or wait for one.

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
from array import array
from struct import unpack, pack
from mom import string
from mom.builtins import is_bytes, b, byte_ord, byte
from mom._compat import range, ZERO_BYTE, UINT128_MAX, UINT32_MAX


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


EXCLAMATION_CHUNK = b('!!!!!')
ZERO_GROUP_CHAR = b('z')
WHITESPACE_PATTERN = re.compile(b(r'(\s)*'), re.MULTILINE)

# Use this if you want the base85 codec to encode/decode including
# ASCII85 prefixes/suffixes.
ASCII85_PREFIX = b('<~')
ASCII85_SUFFIX = b('~>')

# ASCII85 characters.
ASCII85_BYTES = array('B', [(num + 33) for num in range(85)])
ASCII85_ORDS = array('B', [255] * 128)
for ordinal, _byte in enumerate(ASCII85_BYTES):
    ASCII85_ORDS[_byte] = ordinal

# http://tools.ietf.org/html/rfc1924
RFC1924_BYTES = array('B', (string.digits +
                string.ascii_uppercase +
                string.ascii_lowercase +
                "!#$%&()*+-;<=>?@^_`{|}~").encode("ascii"))
RFC1924_ORDS = array('B', [255] * 128)
for ordinal, _byte in enumerate(RFC1924_BYTES):
    RFC1924_ORDS[_byte] = ordinal


# Pre-computed powers (array index) of 85 used to unroll encoding loops
# Therefore, 85**i is equivalent to POW_85[i] for index 0 through 19
# (inclusive).
#
#POW_85 = tuple(85**power for power in range(20))
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
    19687440434072265625, #L ->
    1673432436896142578125,
    142241757136172119140625,
    12090549356574630126953125,
    1027696695308843560791015625,
    87354219101251702667236328125,
    7425108623606394726715087890625,
    631134233006543551770782470703125,
    53646409805556201900516510009765625,
    4559944833472277161543903350830078125,
)


def _check_compact_char_occurrence(encoded, zero_char, chunk_size=5):
    """
    Ensures 'z' characters do not occur in the middle of 5-tuple chunks
    when decoding. It will raise a ``ValueError`` if such an occurrence is
    found.

    :param encoded:
        The encoded sequence. (ASCII encoded string).
    :param zero_char:
        The 'z' character (default 'z').
    :param chunk_size:
        5 (default).
    """
    counter = 0
    for i, x in enumerate(encoded):
        if x == zero_char[0]:
            if counter % chunk_size:
                raise ValueError(
                    'zero char `%r` occurs in the middle of a chunk ' \
                    'at index %d' % (zero_char, i)
                )
            else:
                counter = 0
        else:
            counter += 1


def _b85encode_chunks(raw_bytes,
                      base85_bytes,
                      padding=False,
                      pow_85=POW_85,
                      zero_byte=ZERO_BYTE):
    """
    Base85 encodes processing 32-bit chunks at a time.

    :param raw_bytes:
        Raw bytes.
    :param base85_bytes:
        Character set to use.
    :param padding:
        ``True`` if padding should be included; ``False`` (default)
        otherwise. You should not need to use this--the default value is
        usually the expected value. If you find a need to use this more
        often than not, *tell us* so that we can make this argument public.
    :param pow_85:
        Powers of 85 lookup table.
    :param zero_byte:
        Zero byte.
    :returns:
        Base-85 encoded bytes.
    """
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
        raw_bytes += zero_byte * padding_size
        num_uint32 += 1
    else:
        padding_size = 0

    encoded = array('B', [0] * num_uint32 * 5)
    # ASCII85 uses a big-endian convention.
    # See: http://en.wikipedia.org/wiki/Ascii85
    i = 0
    for x in unpack('>' + 'L' * num_uint32, raw_bytes):
#        chars = list(range(5))
#        for i in reversed(chars):
#            x, mod = divmod(x, 85)
#            chars[i] = _base85_chars[mod]
#        ascii_chars.extend(chars)
        # Above loop unrolled:
        encoded[i]   = base85_bytes[x // pow_85[4]] # Don't need %85.is<85
        encoded[i+1] = base85_bytes[(x // pow_85[3]) % 85]
        encoded[i+2] = base85_bytes[(x // pow_85[2]) % 85]
        encoded[i+3] = base85_bytes[(x // 85) % 85]     # 85**1 = 85
        encoded[i+4] = base85_bytes[x % 85]             # 85**0 = 1
        i += 5

    if padding_size and not padding:
        # Only as much padding added before encoding is removed after encoding.
        encoded = encoded[:-padding_size]

    # In Python 3, this method is deprecated, but as long as we are
    # supporting Python 2.5, we need to use this. Python 3.x names it
    # ``tobytes()``.
    return encoded.tostring()


def _b85decode_chunks(encoded, base85_bytes, base85_ords):
    """
    Base-85 decodes.

    :param encoded:
        Encoded ASCII string.
    :param base85_bytes:
        Character set to use.
    :param base85_ords:
        A function to convert a base85 character to its ordinal
        value. You should not need to use this.
    :returns:
        Base-85-decoded raw bytes.
    """
    # We want 5-tuple chunks, so pad with as many base85_ord == 84 characters
    # as required to satisfy the length.
    length = len(encoded)
    num_uint32s, remainder = divmod(length, 5)
    if remainder:
        padding_byte = byte(base85_bytes[84]) # 'u' (ASCII85); '~' (RFC1924)
        padding_size = 5 - remainder
        encoded += padding_byte * padding_size
        num_uint32s += 1
        length += padding_size
    else:
        padding_size = 0

    uint32s = [0] * num_uint32s
    j = 0
    for i in range(0, length, 5):
        chunk = encoded[i:i+5]

#        uint32_value = 0
#        for char in chunk:
#            uint32_value = uint32_value * 85 + _base85_ords[byte_ord(char)]
#        Above loop unrolled:
        uint32_value = ((((base85_ords[byte_ord(chunk[0])] *
                        85 + base85_ords[byte_ord(chunk[1])]) *
                        85 + base85_ords[byte_ord(chunk[2])]) *
                        85 + base85_ords[byte_ord(chunk[3])]) *
                        85 + base85_ords[byte_ord(chunk[4])])
        # Groups of characters that decode to a value greater than 2**32 − 1
        # (encoded as "s8W-!") will cause a decoding error. Bad byte?
        if uint32_value > UINT32_MAX: # 2**32 - 1
            raise OverflowError("Cannot decode chunk `%r`" % chunk)

        uint32s[j] = uint32_value
        j += 1

    raw_bytes = pack(">" + "L" * num_uint32s, *uint32s)
    if padding_size:
        # Only as much padding added before decoding is removed after decoding.
        raw_bytes = raw_bytes[:-padding_size]
    return raw_bytes


def b85encode(raw_bytes,
              prefix=None,
              suffix=None,
              _base85_bytes=ASCII85_BYTES,
              _padding=False,
              _compact_zero=True,
              _compact_char=ZERO_GROUP_CHAR):
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
    :param _base85_bytes:
        (Internal) Character set to use.
    :param _compact_zero:
        (Internal) Encodes a zero-group (\x00\x00\x00\x00) as 'z' instead of
        '!!!!!' if this is ``True`` (default).
    :param _compact_char:
        (Internal) Character used to represent compact groups ('z' default)
    :returns:
        ASCII-85 encoded bytes.
    """
    prefix = prefix or b("")
    suffix = suffix or b("")
    if not (is_bytes(prefix) and is_bytes(suffix)):
        raise TypeError(
            "Prefix/suffix must be bytes: got prefix %r, %r" %
            (type(prefix).__name__, type(suffix).__name__)
        )
    if not is_bytes(_compact_char):
        raise TypeError("compat character must be raw byte: got %r" %
                        type(_compact_char).__name__)
    if not is_bytes(raw_bytes):
        raise TypeError("data must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    
    # Encode into ASCII85 characters.
    encoded = _b85encode_chunks(raw_bytes, _base85_bytes, _padding)
    encoded = encoded.replace(EXCLAMATION_CHUNK, _compact_char) \
              if _compact_zero else encoded
    return prefix + encoded + suffix


def b85decode(encoded,
              prefix=None,
              suffix=None,
              _base85_bytes=ASCII85_BYTES,
              _base85_ords=ASCII85_ORDS,
              _uncompact_zero=True,
              _compact_char=ZERO_GROUP_CHAR):
    """
    Decodes an ASCII85-encoded string into raw bytes.

    :param encoded:
        Encoded ASCII string.
    :param prefix:
        The prefix used by the encoded text. None by default.
    :param suffix:
        The suffix used by the encoded text. None by default.
    :param _base85_bytes:
        (Internal) Character set to use.
    :param _base85_ords:
        (Internal) A function to convert a base85 character to its ordinal
        value. You should not need to use this.
    :param _uncompact_zero:
        (Internal) Treats 'z' (a zero-group (\x00\x00\x00\x00)) as a '!!!!!'
        if ``True`` (default).
    :param _compact_char:
        (Internal) Character used to represent compact groups ('z' default)
    :returns:
        ASCII85-decoded raw bytes.
    """
    prefix = prefix or b("")
    suffix = suffix or b("")

    if not (is_bytes(prefix) and is_bytes(suffix)):
        raise TypeError(
            "Prefix/suffix must be bytes: got prefix %r, %r" %
            (type(prefix).__name__, type(suffix).__name__)
        )
    if not is_bytes(_compact_char):
        raise TypeError("compat character must be raw byte: got %r" %
                        type(_compact_char).__name__)
    if not is_bytes(encoded):
        raise TypeError(
            "Encoded sequence must be bytes: got %r" % type(encoded).__name__
        )

    # ASCII-85 ignores whitespace.
    encoded = b('').join(encoded.split())

    # Strip the prefix and suffix.
    if prefix and encoded.startswith(prefix):
        encoded = encoded[len(prefix):]
    if suffix and encoded.endswith(suffix):
        encoded = encoded[:-len(suffix)]

    # Replace all the 'z' occurrences with '!!!!!'
    if _uncompact_zero:
        _check_compact_char_occurrence(encoded, _compact_char, 5)
        encoded = encoded.replace(_compact_char, EXCLAMATION_CHUNK)

    return _b85decode_chunks(encoded, _base85_bytes, _base85_ords)


def rfc1924_b85encode(raw_bytes,
                      _padding=False):
    """
    Base85 encodes using the RFC1924 character set.

    The character set is::

        0–9, A–Z, a–z, and then !#$%&()*+-;<=>?@^_`{|}~

    These characters are specifically not included::

        "',./:[]\\

    This is the encoding method used by Mercurial (and git?) to generate
    binary diffs, for example. They chose the IPv6 character set and encode
    using the ASCII85 encoding method while not compacting zero-byte sequences.

    :see: http://tools.ietf.org/html/rfc1924
    :param raw_bytes:
        Raw bytes.
    :param _padding:
        (Internal) Whether padding should be included in the encoded output.
        (Default ``False``, which is usually what you want.)
    :returns:
        RFC1924 base85 encoded string.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("data must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    return _b85encode_chunks(raw_bytes, RFC1924_BYTES, _padding)


def rfc1924_b85decode(encoded):
    """
    Base85 decodes using the RFC1924 character set.

    This is the encoding method used by Mercurial (and git) to generate
    binary diffs, for example. They chose the IPv6 character set and encode
    using the ASCII85 encoding method while not compacting zero-byte sequences.

    :see: http://tools.ietf.org/html/rfc1924
    :param encoded:
        RFC1924 Base85 encoded string.
    :returns:
        Decoded bytes.
    """
    if not is_bytes(encoded):
        raise TypeError(
            "Encoded sequence must be bytes: got %r" % type(encoded).__name__
        )
    # Ignore whitespace.
    encoded = b('').join(encoded.split())
    return _b85decode_chunks(encoded, RFC1924_BYTES, RFC1924_ORDS)


def ipv6_b85encode(uint128,
                   _base85_bytes=RFC1924_BYTES,
                   _pow_85=POW_85):
    """
    Encodes a 128-bit unsigned integer using the RFC 1924 base-85 encoding.
    Used to encode IPv6 addresses or 128-bit chunks.

    :param uint128:
        A 128-bit unsigned integer to be encoded.
    :param _base85_bytes:
        (Internal) Base85 encoding charset lookup table.
    :param _pow_85:
        (Internal) Powers of 85 lookup table.
    :returns:
        RFC1924 Base85-encoded string.
    """
    if uint128 < 0:
        raise ValueError("Number is not a 128-bit unsigned integer: got %d" %
                         uint128)
    if uint128 > UINT128_MAX:
        raise OverflowError("Number is not a 128-bit unsigned integer: %d" %
                            uint128)
#    encoded = list(range(20))
#    for i in reversed(encoded):
#        uint128, remainder = divmod(uint128, 85)
#        encoded[i] = _base85_chars[remainder]
    # Above loop unrolled:
    # pack('B' * 20, ...)
    return pack('BBBBBBBBBBBBBBBBBBBB',
        _base85_bytes[(uint128 // _pow_85[19])], # Don't need %85. Already < 85
        _base85_bytes[(uint128 // _pow_85[18]) % 85],
        _base85_bytes[(uint128 // _pow_85[17]) % 85],
        _base85_bytes[(uint128 // _pow_85[16]) % 85],
        _base85_bytes[(uint128 // _pow_85[15]) % 85],
        _base85_bytes[(uint128 // _pow_85[14]) % 85],
        _base85_bytes[(uint128 // _pow_85[13]) % 85],
        _base85_bytes[(uint128 // _pow_85[12]) % 85],
        _base85_bytes[(uint128 // _pow_85[11]) % 85],
        _base85_bytes[(uint128 // _pow_85[10]) % 85],
        _base85_bytes[(uint128 // _pow_85[9]) % 85],
        _base85_bytes[(uint128 // _pow_85[8]) % 85],
        _base85_bytes[(uint128 // _pow_85[7]) % 85],
        _base85_bytes[(uint128 // _pow_85[6]) % 85],
        _base85_bytes[(uint128 // _pow_85[5]) % 85],
        _base85_bytes[(uint128 // _pow_85[4]) % 85],
        _base85_bytes[(uint128 // _pow_85[3]) % 85],
        _base85_bytes[(uint128 // _pow_85[2]) % 85],
        _base85_bytes[(uint128 // 85) % 85],   #85**1 == 85
        _base85_bytes[uint128 % 85],           #85**0 == 1
    )


def ipv6_b85decode(encoded,
                   _base85_ords=RFC1924_ORDS):
    """
    Decodes an RFC1924 Base-85 encoded string to its 128-bit unsigned integral
    representation. Used to base85-decode IPv6 addresses or 128-bit chunks.

    Whitespace is ignored. Raises an ``OverflowError`` if stray characters
    are found.

    :param encoded:
        RFC1924 Base85-encoded string.
    :param _base85_ords:
        (Internal) Look up table.
    :returns:
        A 128-bit unsigned integer.
    """
    if not is_bytes(encoded):
        raise TypeError(
            "Encoded sequence must be bytes: got %r" % type(encoded).__name__
        )

    # Ignore whitespace.
    encoded = b('').join(encoded.split())

    if len(encoded) != 20:
        raise ValueError("Not 20 encoded bytes: %r" % encoded)

    #uint128 = 0
    #for char in encoded:
    #    uint128 = uint128 * 85 + _base85_ords[byte_ord(char)]
    # Above loop unrolled to process 4 5-tuple chunks instead:
    #v, w, x, y, z = encoded[0:5]
    # v = encoded[0]..z = encoded[4]
    uint128 = ((((_base85_ords[byte_ord(encoded[0])] *
                85 + _base85_ords[byte_ord(encoded[1])]) *
                85 + _base85_ords[byte_ord(encoded[2])]) *
                85 + _base85_ords[byte_ord(encoded[3])]) *
                85 + _base85_ords[byte_ord(encoded[4])])
    #v, w, x, y, z = encoded[5:10]
    # v = encoded[5]..z = encoded[9]
    uint128 = (((((uint128 * 85 + _base85_ords[byte_ord(encoded[5])]) *
                85 + _base85_ords[byte_ord(encoded[6])]) *
                85 + _base85_ords[byte_ord(encoded[7])]) *
                85 + _base85_ords[byte_ord(encoded[8])]) *
                85 + _base85_ords[byte_ord(encoded[9])])
    #v, w, x, y, z = encoded[10:15]
    # v = encoded[10]..z = encoded[14]
    uint128 = (((((uint128 * 85 + _base85_ords[byte_ord(encoded[10])]) *
                85 + _base85_ords[byte_ord(encoded[11])]) *
                85 + _base85_ords[byte_ord(encoded[12])]) *
                85 + _base85_ords[byte_ord(encoded[13])]) *
                85 + _base85_ords[byte_ord(encoded[14])])
    #v, w, x, y, z = encoded[15:20]
    # v = encoded[15]..z = encoded[19]
    uint128 = (((((uint128 * 85 + _base85_ords[byte_ord(encoded[15])]) *
                85 + _base85_ords[byte_ord(encoded[16])]) *
                85 + _base85_ords[byte_ord(encoded[17])]) *
                85 + _base85_ords[byte_ord(encoded[18])]) *
                85 + _base85_ords[byte_ord(encoded[19])])
    if uint128 > UINT128_MAX:
        raise OverflowError("Cannot decode `%r` -- may contain stray " \
                            "ASCII bytes (whitespace?)" % encoded)
    return uint128
