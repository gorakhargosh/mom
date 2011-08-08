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
diffs (patches), efficiently storing RSA PEM keys, etc.

The ASCII85 character set-based encoding is mostly used by Adobe PDF and
PostScript formats. It may also be used to store PEM keys or binary data
with a lot of zero byte sequences. The RFC1924 character set-based encoding,
however, may be used to compactly represent 128-bit unsigned numbers (like
IPv6 addresses) or binary diffs. Encoding based on RFC1924 does not compact
zero byte sequences, so this form of encoding is less efficient than the
ASCII85 version where a lot of redundant zero byte sequences are expected.


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
from mom import string
from struct import unpack, pack
from mom.builtins import is_bytes, b, byte
from mom._compat import range, have_python3


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


UINT128_MAX = (1 << 128) - 1    # 340282366920938463463374607431768211455L
UINT32_MAX = 0xffffffff # (1 << 32) - 1      # 4294967295
ZERO_BYTE = byte(0)
EXCLAMATION_CHUNK = b('!!!!!')
ZERO_GROUP_CHAR = b('z')
WHITESPACE_PATTERN = re.compile(b(r'(\s)*'), re.MULTILINE)

# Use this if you want the base85 codec to encode/decode including
# ASCII85 prefixes/suffixes.
ASCII85_PREFIX = b('<~')
ASCII85_SUFFIX = b('~>')

# ASCII85 characters.
ASCII85_CHARSET = b('').join(byte(num + 33) for num in range(85))

# http://tools.ietf.org/html/rfc1924
RFC1924_CHARSET = (string.digits +
                string.ascii_uppercase +
                string.ascii_lowercase +
                "!#$%&()*+-;<=>?@^_`{|}~").encode("ascii")
RFC1924_ORDS = dict((x, i) for i, x in enumerate(RFC1924_CHARSET))

if have_python3:
    # Python 3 bytes when indexed yield integers, not single-character
    # byte strings.
    ASCII85_ORDS = dict((x, x - 33) for x in ASCII85_CHARSET)
    ASCII85_CHARSET = tuple(byte(x) for x in ASCII85_CHARSET)
    RFC1924_CHARSET = tuple(byte(x) for x in RFC1924_CHARSET)
else:
    # Indexing into Python 2 bytes yields single-character byte strings.
    ASCII85_ORDS = dict((x, ord(x) - 33) for x in ASCII85_CHARSET)
    #                 Notice ^. In Python 3, you don't need this.

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

            
def b85encode(raw_bytes,
              prefix=None,
              suffix=None,
              _padding=False,
              _base85_chars=ASCII85_CHARSET,
              _compact_zero=True,
              _compact_char=ZERO_GROUP_CHAR,
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
        raw_bytes += ZERO_BYTE * padding_size
        num_uint32 += 1
    else:
        padding_size = 0

    ascii_chars = [0] * num_uint32 * 5
    # ASCII85 uses a big-endian convention.
    # See: http://en.wikipedia.org/wiki/Ascii85
    i = 0
#    ascii_chars = []
    for x in unpack('>' + 'L' * num_uint32, raw_bytes):
#        chars = list(range(5))
#        for i in reversed(chars):
#            chars[i] = _base85_chars[x % 85]
#            x //= 85
#        ascii_chars.extend(chars)
        # Above loop unrolled:
        ascii_chars[i]   = _base85_chars[x // _pow_85[4]] # Don't need %85. Already <85.
        ascii_chars[i+1] = _base85_chars[(x // _pow_85[3]) % 85]
        ascii_chars[i+2] = _base85_chars[(x // _pow_85[2]) % 85]
        ascii_chars[i+3] = _base85_chars[(x // 85) % 85]     # 85**1 = 85
        ascii_chars[i+4] = _base85_chars[x % 85]             # 85**0 = 1
        i += 5
    if padding_size and not _padding:
        # Only as much padding added before encoding is removed after encoding.
        ascii_chars = ascii_chars[:-padding_size]
    encoded = b('').join(ascii_chars)
    encoded = encoded.replace(EXCLAMATION_CHUNK, _compact_char) \
              if _compact_zero else encoded
    return prefix + encoded + suffix


def b85decode(encoded,
              prefix=None,
              suffix=None,
              _base85_ords=ASCII85_ORDS,
              _base85_chars=ASCII85_CHARSET,
              _ignore_pattern=WHITESPACE_PATTERN,
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
    if _ignore_pattern:
        encoded = re.sub(_ignore_pattern, b(''), encoded)

    # Strip the prefix and suffix.
    if prefix and encoded.startswith(prefix):
        encoded = encoded[len(prefix):]
    if suffix and encoded.endswith(suffix):
        encoded = encoded[:-len(suffix)]

    # Replace all the 'z' occurrences with '!!!!!'
    if _uncompact_zero:
        _check_compact_char_occurrence(encoded, _compact_char, 5)
        encoded = encoded.replace(_compact_char, EXCLAMATION_CHUNK)

    # We want 5-tuple chunks, so pad with as many base85_ord == 84 characters
    # as required to satisfy the length.
    length = len(encoded)
    num_uint32s, remainder = divmod(length, 5)
    if remainder:
        padding_character = _base85_chars[84]   # b'u' for ASCII85.
        padding_size = 5 - remainder
        encoded += padding_character * padding_size
        num_uint32s += 1
        length += padding_size
    else:
        padding_size = 0

    uint32s = [0] * num_uint32s
    j = 0
    for i in range(0, length, 5):
        v, w, x, y, z = chunk = encoded[i:i+5]
#        uint32_value = 0
#        try:
#            for char in chunk:
#                uint32_value = uint32_value * 85 + _base85_ords[char]
#        except KeyError:
#            raise OverflowError("Cannot decode chunk `%r`" % chunk)
#        Above loop unrolled:
        try:
            uint32_value = ((((_base85_ords[v] *
                            85 + _base85_ords[w]) *
                            85 + _base85_ords[x]) *
                            85 + _base85_ords[y]) *
                            85 + _base85_ords[z])
        except KeyError:
            # Showing the chunk provides more context, which makes debugging
            # easier.
            raise KeyError("Invalid Base85 byte in chunk `%r` -- " % chunk)

        # Groups of characters that decode to a value greater than 2**32 − 1
        # (encoded as "s8W-!") will cause a decoding error.
        if uint32_value > UINT32_MAX: # 2**32 - 1
            raise OverflowError("Cannot decode chunk `%r`" % chunk)

        uint32s[j] = uint32_value
        j += 1

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
    return b85encode(raw_bytes,
                     _padding=_padding,
                     _base85_chars=RFC1924_CHARSET,
                     _compact_zero=False)


def rfc1924_b85decode(encoded):
    """
    Base85 decodes using the RFC1924 character set.

    This is the encoding method used by Mercurial (and git?) to generate
    binary diffs, for example. They chose the IPv6 character set and encode
    using the ASCII85 encoding method while not compacting zero-byte sequences.

    :see: http://tools.ietf.org/html/rfc1924
    :param encoded:
        RFC1924 Base85 encoded string.
    :returns:
        Decoded bytes.
    """
    return b85decode(encoded,
                     _base85_ords=RFC1924_ORDS,
                     _base85_chars=RFC1924_CHARSET,
                     _uncompact_zero=False)



def ipv6_b85encode(uint128,
                   _base85_chars=RFC1924_CHARSET,
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
    if uint128 > UINT128_MAX:
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
    return b('').join(encoded)


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
    if not is_bytes(encoded):
        raise TypeError(
            "Encoded sequence must be bytes: got %r" % type(encoded).__name__
        )
    if len(encoded) != 20:
        raise ValueError("Not 20 encoded bytes: %r" % encoded)
    #uint128 = 0L
    #for char in encoded:
    #    uint128 = uint128 * 85 + _base85_ords[char]
    # Above loop unrolled to process 4 5-tuple chunks instead:
    #v, w, x, y, z = encoded[0:5]
    # v = encoded[0]..z = encoded[4]
    uint128 = ((((_base85_ords[encoded[0]] *
                85 + _base85_ords[encoded[1]]) *
                85 + _base85_ords[encoded[2]]) *
                85 + _base85_ords[encoded[3]]) *
                85 + _base85_ords[encoded[4]])
    #v, w, x, y, z = encoded[5:10]
    # v = encoded[5]..z = encoded[9]
    uint128 = (((((uint128 * 85 + _base85_ords[encoded[5]]) *
                85 + _base85_ords[encoded[6]]) *
                85 + _base85_ords[encoded[7]]) *
                85 + _base85_ords[encoded[8]]) *
                85 + _base85_ords[encoded[9]])
    #v, w, x, y, z = encoded[10:15]
    # v = encoded[10]..z = encoded[14]
    uint128 = (((((uint128 * 85 + _base85_ords[encoded[10]]) *
                85 + _base85_ords[encoded[11]]) *
                85 + _base85_ords[encoded[12]]) *
                85 + _base85_ords[encoded[13]]) *
                85 + _base85_ords[encoded[14]])
    #v, w, x, y, z = encoded[15:20]
    # v = encoded[15]..z = encoded[19]
    uint128 = (((((uint128 * 85 + _base85_ords[encoded[15]]) *
                85 + _base85_ords[encoded[16]]) *
                85 + _base85_ords[encoded[17]]) *
                85 + _base85_ords[encoded[18]]) *
                85 + _base85_ords[encoded[19]])
    return uint128
