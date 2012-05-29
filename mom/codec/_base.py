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

""":synopsis: Routines used by ASCII-based base converters.
:module: mom.codec._base

.. autofunction:: base_encode
.. autofunction:: base_decode
.. autofunction:: base_to_uint
.. autofunction:: uint_to_base256
"""

from __future__ import absolute_import

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

from mom import _compat
from mom import builtins
from mom.codec import integer


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


ZERO_BYTE = _compat.ZERO_BYTE
EMPTY_BYTE = _compat.EMPTY_BYTE


def base_encode(raw_bytes, base, base_bytes, base_zero, padding=True):
  """
  Encodes raw bytes given a base.

  :param raw_bytes:
      Raw bytes to encode.
  :param base:
      Unsigned integer base.
  :param base_bytes:
      The ASCII bytes used in the encoded string. "Character set" or "alphabet".
  :param base_zero:

  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("data must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  number = integer.bytes_to_uint(raw_bytes)
  encoded = EMPTY_BYTE
  while number > 0:
    number, remainder = divmod(number, base)
    encoded = base_bytes[remainder] + encoded
  if padding:
    zero_leading = builtins.bytes_leading(raw_bytes)
    encoded = encoded.rjust(len(encoded) + zero_leading, base_zero)
  return encoded


def base_decode(encoded, base, base_ords, base_zero, powers):
  """Decode from base to base 256."""
  if not builtins.is_bytes(encoded):
    raise TypeError("encoded data must be bytes: got %r" %
                    type(encoded).__name__)
    # Ignore whitespace.
  encoded = EMPTY_BYTE.join(encoded.split())
  # Convert to big integer.
  number = base_to_uint(encoded, base, base_ords, powers)
  return uint_to_base256(number, encoded, base_zero)


def base_to_uint(encoded,
                 base,
                 ord_lookup_table,
                 powers):
  """
  Decodes bytes from the given base into a big integer.

  :param encoded:
      Encoded bytes.
  :param base:
      The base to use.
  :param ord_lookup_table:
      The ordinal lookup table to use.
  :param powers:
      Pre-computed tuple of powers of length ``powers_length``.
  """
  # Convert to big integer.
  #    number = 0
  #    for i, x in enumerate(reversed(encoded)):
  #        number += _lookup[x] * (base**i)
  # Above loop divided into precomputed powers section and computed.
  number = 0
  length = len(encoded)
  powers_length = len(powers)
  for i, char in enumerate(encoded[length:-powers_length - 1:-1]):
    number += ord_lookup_table[char] * powers[i]
  for i in range(powers_length, length):
    char = encoded[length - i - 1]
    number += ord_lookup_table[char] * (base ** i)
  return number


def uint_to_base256(number, encoded, base_zero):
  """Convert uint to base 256."""
  if number == 0:
    raw_bytes = EMPTY_BYTE
  else:
    raw_bytes = integer.uint_to_bytes(number)
  zero_leading = builtins.bytes_leading(encoded, base_zero)
  if zero_leading:
    raw_bytes = raw_bytes.rjust(len(raw_bytes) + zero_leading, ZERO_BYTE)
  return raw_bytes
