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

"""Alternative implementations of builtins."""

from __future__ import absolute_import

import struct
from mom import _compat
from mom import builtins


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


ZERO_BYTE = _compat.ZERO_BYTE
EMPTY_BYTE = _compat.EMPTY_BYTE

get_word_alignment = _compat.get_word_alignment


def integer_byte_length_shift_counting(num):
  """
  Number of bytes needed to represent a integer.

  :param num:
      Integer value. If num is 0, returns 0.
  :returns:
      The number of bytes in the integer.
  """
  # Do not change this to `not num` otherwise a TypeError will not
  # be raised when `None` is passed in as a value.
  if num == 0:
    return 0
  bits = integer_bit_length_shift_counting(num)
  quanta, remainder = divmod(bits, 8)
  if remainder:
    quanta += 1
  return quanta
  # The following does floating point division.
  #return int(math.ceil(bits / 8.0))


def integer_bit_length_shift_counting(num):
  """
  Number of bits needed to represent a integer excluding any prefix
  0 bits.

  :param num:
      Integer value. If num is 0, returns 0. Only the absolute value of the
      number is considered. Therefore, signed integers will be abs(num)
      before the number's bit length is determined.
  :returns:
      Returns the number of bits in the integer.
  """
  bits = 0
  if num < 0:
    num = -num
    # Do not change this to `not num` otherwise a TypeError will not
  # be raised when `None` is passed in as a value.
  if num == 0:
    return 0
  while num >> bits:
    bits += 1
  return bits


def _integer_raw_bytes_without_leading(num,
                                       _zero_byte=ZERO_BYTE,
                                       _get_word_alignment=get_word_alignment):
  # Do not change this to `not num` otherwise a TypeError will not
  # be raised when `None` is passed in as a value.
  if num == 0:
    return EMPTY_BYTE
  if num < 0:
    num = -num
  raw_bytes = EMPTY_BYTE
  word_bits, _, max_uint, pack_type = _get_word_alignment(num)
  pack_format = ">" + pack_type
  while num > 0:
    raw_bytes = struct.pack(pack_format, num & max_uint) + raw_bytes
    num >>= word_bits

  # Count the number of zero prefix bytes.
  zero_leading = 0
  for zero_leading, raw_byte in enumerate(raw_bytes):
    if raw_byte != _zero_byte[0]:
      break

  # Bytes remaining without zero padding is the number of bytes required
  # to represent this integer.
  return raw_bytes[zero_leading:]


def integer_byte_length_word_aligned(num):
  """
  Number of bytes needed to represent a integer.

  :param num:
      Integer value. If num is 0, returns 0. If num is negative,
      its absolute value will be considered.
  :returns:
      The number of bytes in the integer.
  """
  return len(_integer_raw_bytes_without_leading(num))


def integer_bit_length_word_aligned(num):
  """
  Number of bits needed to represent a integer excluding any prefix
  0 bits.

  :param num:
      Integer value. If num is 0, returns 0. Only the absolute value of the
      number is considered. Therefore, signed integers will be abs(num)
      before the number's bit length is determined.
  :returns:
      Returns the number of bits in the integer.
  """
  # Do not change this to `not num` otherwise a TypeError will not
  # be raised when `None` is passed in as a value.
  if num == 0:
    return 0
  if num < 0:
    num = -num
  if num > 0x80:
    raw_bytes = _integer_raw_bytes_without_leading(num)
    first_byte = builtins.byte_ord(raw_bytes[0])
    bits = 0
    while first_byte >> bits:
      bits += 1
    return ((len(raw_bytes) - 1) * 8) + bits
  else:
    bits = 0
    while num >> bits:
      bits += 1
    return bits


# def _bin_lookup(num, prefix="0b"):
#   """
#   Converts a long value to its binary representation based on a lookup table.
#
#   Alternative implementation of :func:``bin``.
#
#   :param num:
#       Long value.
#   :param prefix:
#       The prefix to use for the bitstring. Default "0b" to mimic Python
#       builtin ``bin()``.
#   :returns:
#       Bit string.
#   """
#   prefix = prefix or ""
#   bit_string = ""
#   lookup = {"0":"000", "1":"001", "2":"010", "3":"011",
#             "4":"100", "5":"101", "6":"110", "7":"111"}
#   for c in oct(num)[1:]:
#     bit_string += lookup[c]
#   return prefix + bit_string
#
#
# def _bin_recursive(num, prefix="0b"):
#   """
#   Converts a long value to its binary representation recursively.
#
#   Alternative implementation of :func:``bin``.
#
#   :param num:
#       Long value.
#   :param prefix:
#       The prefix to use for the bitstring. Default "0b" to mimic Python
#       builtin ``bin()``.
#   :returns:
#       Bit string.
#   """
#   prefix = prefix or ""
#   if num <= 1:
#     bitstring = bytes(num)
#   else:
#     bitstring = _bin_recursive(num >> 1) + bytes(num & 1)
#   return prefix + bitstring
