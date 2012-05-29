#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google Inc. All Rights Reserved.
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

""":synopsis: Base-58 repr for unambiguous display & compact human-input.
:module: mom.codec.base58


Where should you use base-58?
-----------------------------
Base-58 representation is 7 bit-ASCII safe, MIME-safe, URL-safe, HTTP
cookie-safe, and **human being-safe**. Base-58 representation can:

* be readable and editable by a human being;
* safely and compactly represent numbers;
* contain only alphanumeric characters (omitting a few with visually-
  ambiguously glyphs--namely, "0OIl");
* not contain punctuation characters.

Example scenarios where base-58 encoding may be used:

* Visually-legible account numbers
* Shortened URL paths
* OAuth verification codes
* Unambiguously printable and displayable key codes (for example,
  net-banking PINs, verification codes sent via SMS, etc.)
* Bitcoin decentralized crypto-currency addresses
* CAPTCHAs
* Revision control changeset identifiers
* Encoding email addresses compactly into JavaScript that decodes by itself
  to display on Web pages in order to reduce spam by stopping email harvesters
  from scraping email addresses from Web pages.

In general, use base-58 in any 7-bit ASCII-safe compact communication where
human beings, paper, and communication devices may be significantly
involved.

The default base-58 character set is ``[0-9A-Za-z]`` (base-62) with some
characters omitted to make them visually-legible and unambiguously printable.
The characters omitted are:

* 0 (ASCII NUMERAL ZERO)
* O (ASCII UPPERCASE ALPHABET O)
* I (ASCII UPPERCASE ALPHABET I)
* l (ASCII LOWERCASE ALPHABET L)

For a practical example, see the documentation for :mod:`mom.codec.base62`.

Functions
---------
.. autofunction:: b58encode
.. autofunction:: b58decode
"""

from __future__ import absolute_import
from __future__ import division

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

from mom import _compat
from mom import builtins
from mom.codec import _base


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


# Follows ASCII order.
ASCII58_BYTES = ("123456789"
                 "ABCDEFGHJKLMNPQRSTUVWXYZ"
                 "abcdefghijkmnopqrstuvwxyz").encode("ascii")
# Therefore, b"1" represents b"\0".
ASCII58_ORDS = dict((x, i) for i, x in enumerate(ASCII58_BYTES))


# Really, I don't understand why people use the non-ASCII order,
# but if you really like it that much, go ahead. Be my guest. Here
# is what you will need:
#
# Does not follow ASCII order.
ALT58_BYTES = ("123456789"
               "abcdefghijkmnopqrstuvwxyz"
               "ABCDEFGHJKLMNPQRSTUVWXYZ").encode("ascii")
# Therefore, b"1" represents b"\0".
ALT58_ORDS = dict((x, i) for i, x in enumerate(ALT58_BYTES))

if _compat.HAVE_PYTHON3:
  ASCII58_BYTES = tuple(builtins.byte(x) for x in ASCII58_BYTES)
  ALT58_BYTES = tuple(builtins.byte(x) for x in ALT58_BYTES)

# If you're going to make people type stuff longer than this length
# I don't know what to tell you. Beyond this length powers
# are computed, so be careful if you care about computation speed.
# I think this is a VERY generous range. Decoding bytes fewer than 512
# will use this pre-computed lookup table, and hence, be faster.
POW_58 = tuple(58 ** power for power in builtins.range(512))


def b58encode(raw_bytes,
              base_bytes=ASCII58_BYTES, _padding=True):
  """
  Base58 encodes a sequence of raw bytes. Zero-byte sequences are
  preserved by default.

  :param raw_bytes:
      Raw bytes to encode.
  :param base_bytes:
      The character set to use. Defaults to ``ASCII58_BYTES``
      that uses natural ASCII order.
  :param _padding:
      (Internal) ``True`` (default) to include prefixed zero-byte sequence
      padding converted to appropriate representation.
  :returns:
      Base-58 encoded bytes.
  """
  return _base.base_encode(raw_bytes, 58, base_bytes, base_bytes[0], _padding)


def b58decode(encoded,
              base_bytes=ASCII58_BYTES,
              base_ords=ASCII58_ORDS):
  """
  Base-58 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

  :param encoded:
      Base-58 encoded bytes.
  :param base_bytes:
      (Internal) The character set to use. Defaults to ``ASCII58_BYTES``
      that uses natural ASCII order.
  :param base_ords:
      (Internal) Ordinal-to-character lookup table for the specified
      character set.
  :returns:
      Raw bytes.
  """
  # Zero byte is represented using the first character in the character set.
  # Adds zero byte prefix padding if required.
  return _base.base_decode(encoded, 58, base_ords, base_bytes[0], POW_58)
