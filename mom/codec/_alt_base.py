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

"""Alternative base conversion implementations, but slower."""

from __future__ import absolute_import

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

import array
import re

from mom import _compat
from mom import builtins
from mom import functional
from mom.codec import base58
from mom.codec import base62
from mom.codec import base85
from mom.codec import integer


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b

ZERO_BYTE = _compat.ZERO_BYTE
UINT128_MAX = _compat.UINT128_MAX
EMPTY_BYTE = _compat.EMPTY_BYTE

WHITESPACE_PATTERN = re.compile(b(r"(\s)*"), re.MULTILINE)


def b58encode_naive(raw_bytes,
                    base_bytes=base58.ASCII58_BYTES,
                    _padding=True,
                    _zero_byte=ZERO_BYTE):
  """
  Base58 encodes a sequence of raw bytes. Zero-byte sequences are
  preserved by default.

  :param raw_bytes:
      Raw bytes to encode.
  :param base_bytes:
      The character set to use. Defaults to ``base58.ASCII58_BYTES``
      that uses natural ASCII order.
  :param _padding:
      (Internal) ``True`` (default) to include prefixed zero-byte sequence
      padding converted to appropriate representation.
  :returns:
      Base-58 encoded bytes.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("data must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  number = integer.bytes_to_uint(raw_bytes)
  encoded = EMPTY_BYTE
  while number > 0:
    encoded = base_bytes[number % 58] + encoded
    number //= 58

  # The following makes more divmod calls but is 2x faster.
  #        number, remainder = divmod(number, 58)
  #        encoded = _charset[remainder] + encoded
  if _padding:
    zero_leading = functional.leading(lambda w: w == _zero_byte[0], raw_bytes)
    encoded = (base_bytes[0] * zero_leading) + encoded
  return encoded


def b62encode_naive(raw_bytes,
                    base_bytes=base62.ASCII62_BYTES,
                    _padding=True,
                    _zero_byte=ZERO_BYTE):
  """
  Base62 encodes a sequence of raw bytes. Zero-byte sequences are
  preserved by default.

  :param raw_bytes:
      Raw bytes to encode.
  :param base_bytes:
      The character set to use. Defaults to ``ASCII62_CHARSET``
      that uses natural ASCII order.
  :param _padding:
      (Internal) ``True`` (default) to include prefixed zero-byte sequence
      padding converted to appropriate representation.
  :returns:
      Base-62 encoded bytes.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("data must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  number = integer.bytes_to_uint(raw_bytes)
  encoded = EMPTY_BYTE
  while number > 0:
    encoded = base_bytes[number % 62] + encoded
    number //= 62
  # The following makes more divmod calls but is 2x faster.
  #        number, remainder = divmod(number, 62)
  #        encoded = _charset[remainder] + encoded
  if _padding:
    zero_leading = functional.leading(lambda w: w == _zero_byte[0], raw_bytes)
    encoded = (base_bytes[0] * zero_leading) + encoded
  return encoded


def b62decode_naive(encoded,
                    _charset=base62.ASCII62_BYTES,
                    _lookup=base62.ASCII62_ORDS):
  """
  Base-62 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

  :param encoded:
      Base-62 encoded bytes.
  :param _charset:
      (Internal) The character set to use. Defaults to ``ASCII62_CHARSET``
      that uses natural ASCII order.
  :param _lookup:
      (Internal) Ordinal-to-character lookup table for the specified
      character set.
  :returns:
      Raw bytes.
  """
  if not builtins.is_bytes(encoded):
    raise TypeError("encoded data must be bytes: got %r" %
                    type(encoded).__name__)

  # Ignore whitespace.
  encoded = re.sub(WHITESPACE_PATTERN, EMPTY_BYTE, encoded)

  # Convert to big integer.
  number = 0
  for i, char in enumerate(reversed(encoded)):
    number += _lookup[char] * (62 ** i)

  # Obtain raw bytes.
  if number:
    raw_bytes = integer.uint_to_bytes(number)
  else:
    # We don't want to convert to b"\x00" when we get number == 0.
    # That would add an off-by-one extra zero byte in the result.
    raw_bytes = EMPTY_BYTE

  # Add prefixed padding if required.
  # 0 byte is represented using the first character in the character set.
  zero_char = _charset[0]
  # The extra [0] index in zero_byte_char[0] is for Python2.x-Python3.x
  # compatibility. Indexing into Python 3 bytes yields an integer, whereas
  # in Python 2.x it yields a single-byte string.
  zero_leading = functional.leading(lambda w: w == zero_char[0], encoded)
  if zero_leading:
    padding = ZERO_BYTE * zero_leading
    raw_bytes = padding + raw_bytes
  return raw_bytes


def b58decode_naive(encoded,
                    _charset=base58.ASCII58_BYTES,
                    _lookup=base58.ASCII58_ORDS):
  """
  Simple implementation for benchmarking.

  Base-58 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

  :param encoded:
      Base-58 encoded bytes.
  :param _charset:
      (Internal) The character set to use. Defaults to ``base58.ASCII58_BYTES``
      that uses natural ASCII order.
  :param _lookup:
      (Internal) Ordinal-to-character lookup table for the specified
      character set.
  :returns:
      Raw bytes.
  """
  if not builtins.is_bytes(encoded):
    raise TypeError("encoded data must be bytes: got %r" %
                    type(encoded).__name__)

  # Ignore whitespace.
  encoded = re.sub(WHITESPACE_PATTERN, EMPTY_BYTE, encoded)

  # Convert to big integer.
  number = 0
  for i, char in enumerate(reversed(encoded)):
    number += _lookup[char] * (58 ** i)

  # Obtain raw bytes.
  if number:
    raw_bytes = integer.uint_to_bytes(number)
  else:
    # We don't want to convert to b"\x00" when we get number == 0.
    # That would add an off-by-one extra zero byte in the result.
    raw_bytes = EMPTY_BYTE

  # Add prefixed padding if required.
  # 0 byte is represented using the first character in the character set.
  zero_char = _charset[0]
  # The extra [0] index in zero_byte_char[0] is for Python2.x-Python3.x
  # compatibility. Indexing into Python 3 bytes yields an integer, whereas
  # in Python 2.x it yields a single-byte string.
  zero_leading = functional.leading(lambda w: w == zero_char[0], encoded)
  if zero_leading:
    padding = ZERO_BYTE * zero_leading
    raw_bytes = padding + raw_bytes
  return raw_bytes


def ipv6_b85decode_naive(encoded,
                         _base85_ords=base85.RFC1924_ORDS):
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
  if not builtins.is_bytes(encoded):
    raise TypeError("Encoded sequence must be bytes: got %r" %
                    type(encoded).__name__)
    # Ignore whitespace.
  encoded = EMPTY_BYTE.join(encoded.split())
  if len(encoded) != 20:
    raise ValueError("Not 20 encoded bytes: %r" % encoded)
  uint128 = 0
  try:
    for char in encoded:
      uint128 = uint128 * 85 + _base85_ords[char]
  except KeyError:
    raise OverflowError("Cannot decode `%r -- may contain stray "
                        "ASCII bytes" % encoded)
  if uint128 > UINT128_MAX:
    raise OverflowError("Cannot decode `%r` -- may contain stray "
                        "ASCII bytes" % encoded)
  return uint128


def ipv6_b85encode_naive(uint128,
                         _base85_bytes=base85.RFC1924_BYTES):
  """
  Encodes a 128-bit unsigned integer using the RFC 1924 base-85 encoding.
  Used to encode IPv6 addresses or 128-bit chunks.

  :param uint128:
      A 128-bit unsigned integer to be encoded.
  :param _base85_bytes:
      (Internal) Base85 encoding charset lookup table.
  :returns:
      RFC1924 Base85-encoded string.
  """
  if uint128 < 0:
    raise ValueError("Number is not a 128-bit unsigned integer: got %d" %
                     uint128)
  if uint128 > UINT128_MAX:
    raise OverflowError("Number is not a 128-bit unsigned integer: %d" %
                        uint128)
    #encoded = list(range(20))
  encoded = array.array("B", list(range(20)))
  for i in reversed(encoded):
    uint128, remainder = divmod(uint128, 85)
    encoded[i] = _base85_bytes[remainder]
  return encoded.tostring()
