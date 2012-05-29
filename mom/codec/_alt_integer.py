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


"""Alternative implementations of integer module routines that
were bench-marked to be slower."""


from __future__ import absolute_import

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801


import array
import struct

from mom import _compat
from mom import builtins


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


ZERO_BYTE = _compat.ZERO_BYTE
EMPTY_BYTE = _compat.EMPTY_BYTE


def uint_to_bytes_naive_array_based(uint, chunk_size=0):
  """
  Converts an integer into bytes.

  :param uint:
      Unsigned integer value.
  :param chunk_size:
      Chunk size.
  :returns:
      Bytes.
  """
  if uint < 0:
    raise ValueError("Negative numbers cannot be used: %i" % uint)
  if uint == 0:
    bytes_count = 1
  else:
    bytes_count = builtins.integer_byte_length(uint)
  byte_array = array.array("B", [0] * bytes_count)
  for count in builtins.range(bytes_count - 1, -1, -1):
    byte_array[count] = uint & 0xff
    uint >>= 8
  raw_bytes = byte_array.tostring()

  if chunk_size > 0:
    # Bounds checking. We're not doing this up-front because the
    # most common use case is not specifying a chunk size. In the worst
    # case, the number will already have been converted to bytes above.
    length = len(raw_bytes)
    bytes_needed = bytes_count
    if bytes_needed > chunk_size:
      raise OverflowError("Need %d bytes for number, but chunk size is %d" %
                          (bytes_needed, chunk_size))
    remainder = length % chunk_size
    if remainder:
      raw_bytes = (chunk_size - remainder) * ZERO_BYTE + raw_bytes
  return raw_bytes


def uint_to_bytes_naive(number, block_size=0):
  """
  Naive slow and accurate implementation. Base for all our tests.

  Converts a number to a string of bytes.

  :param number: the number to convert
  :param block_size: the number of bytes to output. If the number encoded to
      bytes is less than this, the block will be zero-padded. When not given,
      the returned block is not padded.

  :raises:
      ``OverflowError`` when block_size is given and the number takes up more
      bytes than fit into the block.
  """
  if number < 0:
    raise ValueError("Negative numbers cannot be used: %d" % number)

  # Do some bounds checking
  needed_bytes = builtins.integer_byte_length(number)
  if block_size > 0:
    if needed_bytes > block_size:
      raise OverflowError("Needed %i bytes for number, but block size "
                          "is %i" % (needed_bytes, block_size))

  # Convert the number to bytes.
  if number == 0:
    raw_bytes = [ZERO_BYTE]
  else:
    raw_bytes = []
    num = number
    while num > 0:
      raw_bytes.insert(0, builtins.byte(num & 0xFF))
      num >>= 8

  # Pad with zeroes to fill the block
  if block_size > 0:
    padding_size = (block_size - needed_bytes)
    if number == 0:
      padding_size -= 1
    padding = ZERO_BYTE * padding_size
  else:
    padding = EMPTY_BYTE
  return padding + EMPTY_BYTE.join(raw_bytes)


# From pycrypto (for verification only).
def uint_to_bytes_pycrypto(uint, blocksize=0):
  """long_to_bytes(n:long, blocksize:int) : string
  Convert a long integer to a byte string.

  If optional blocksize is given and greater than zero, pad the front of the
  byte string with binary zeros so that the length is a multiple of
  blocksize.
  """
  # after much testing, this algorithm was deemed to be the fastest
  raw_bytes = EMPTY_BYTE
  uint = int(uint)
  while uint > 0:
    raw_bytes = struct.pack(">I", uint & 0xffffffff) + raw_bytes
    uint >>= 32
    # strip off leading zeros
  i = 0
  for i in builtins.range(len(raw_bytes)):
    if raw_bytes[i] != ZERO_BYTE[0]:
      break
  else:
    # only happens when n == 0
    raw_bytes = ZERO_BYTE
    i = 0
  raw_bytes = raw_bytes[i:]
  # add back some pad bytes. this could be done more efficiently w.r.t. the
  # de-padding being done above, but sigh...
  if blocksize > 0 and len(raw_bytes) % blocksize:
    raw_bytes = (blocksize - len(raw_bytes) % blocksize) * ZERO_BYTE + raw_bytes
  return raw_bytes


def uint_to_bytes_array_based(number, chunk_size=0):
  """
  Convert a integer to bytes (base-256 representation)::

      integer_to_bytes(n:int, chunk_size:int) : string

  .. WARNING:
      Does not preserve leading zeros if you don't specify a chunk size.

  :param number:
      Integer value
  :param chunk_size:
      If optional chunk size is given and greater than zero, pad the front of
      the byte string with binary zeros so that the length is a multiple of
      ``chunk_size``. Raises an OverflowError if the chunk_size is not
      sufficient to represent the integer.
  :returns:
      Raw bytes (base-256 representation).
  :raises:
      ``OverflowError`` when block_size is given and the number takes up more
      bytes than fit into the block.
  """
  # Machine word aligned byte array based implementation.
  if number < 0:
    raise ValueError("Number must be unsigned integer: %d" % number)

  raw_bytes = EMPTY_BYTE
  if not number:
    raw_bytes = ZERO_BYTE

  # Align packing to machine word size.
  num = number
  word_bits, word_bytes, max_uint, pack_type = _compat.get_word_alignment(num)
  pack_format = ">" + pack_type

  temp_buffer = array.array("B", [0] * word_bytes)
  byte_array = array.array("B", raw_bytes)
  while num > 0:
    struct.pack_into(pack_format, temp_buffer, 0, num & max_uint)
    byte_array = temp_buffer + byte_array
    num >>= word_bits

  # Count the number of zero prefix bytes.
  zero_leading = 0
  length = len(byte_array)
  for zero_leading in builtins.range(length):
    if byte_array[zero_leading]:
      break
  raw_bytes = byte_array[zero_leading:].tostring()

  if chunk_size > 0:
    # Bounds checking. We're not doing this up-front because the
    # most common use case is not specifying a chunk size. In the worst
    # case, the number will already have been converted to bytes above.
    length = len(raw_bytes)
    if length > chunk_size:
      raise OverflowError("Need %d bytes for number, but chunk size is %d" %
                          (length, chunk_size))
    remainder = length % chunk_size
    if remainder:
      raw_bytes = (chunk_size - remainder) * ZERO_BYTE + raw_bytes
  return raw_bytes


def bytes_to_uint_naive(raw_bytes, _zero_byte=ZERO_BYTE):
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
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("argument must be raw bytes: got %r" %
                    type(raw_bytes).__name__)

  length = len(raw_bytes)
  remainder = length % 4
  if remainder:
    # Ensure we have a length that is a multiple of 4 by prefixing
    # sufficient zero padding.
    padding_size = 4 - remainder
    length += padding_size
    raw_bytes = _zero_byte * padding_size + raw_bytes

  # Now unpack integers and accumulate.
  int_value = 0
  for i in builtins.range(0, length, 4):
    chunk = raw_bytes[i:i + 4]
    int_value = (int_value << 32) + struct.unpack(">I", chunk)[0]
  return int_value


def uint_to_bytes_simple(num):
  """Simple uint to bytes converter."""
  assert num >= 0
  if num == 0:
    return ZERO_BYTE
  byte_array = []
  while num:
    byte_array.append(builtins.byte(num & 0xff))
    num >>= 8
  return EMPTY_BYTE.join(reversed(byte_array))


def bytes_to_uint_simple(raw_bytes):
  """Simple bytes to uint converter."""
  return builtins.reduce(lambda a, b: a << 8 | b,
                         builtins.map(builtins.byte_ord, raw_bytes), 0)
