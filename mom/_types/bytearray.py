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

""":synopsis: Byte arrays.
:module: mom._types.bytearray

Creation and manipulation
-------------------------
.. autofunction:: bytearray_concat
.. autofunction:: bytearray_create
.. autofunction:: bytearray_create_zeros

Type conversion
---------------
.. autofunction:: bytearray_to_bytes
.. autofunction:: bytearray_to_long
.. autofunction:: bytes_to_bytearray
.. autofunction:: long_to_bytearray

OpenSSL MPI Bignum conversion
-----------------------------
.. autofunction:: long_to_mpi
.. autofunction:: mpi_to_long
"""

from __future__ import absolute_import

from array import array
from mom import builtins


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


def bytearray_create(sequence):
  """
  Creates a byte array from a given sequence.

  :param sequence:
      The sequence from which a byte array will be created.
  :returns:
      A byte array.
  """
  return array("B", sequence)


def bytearray_create_zeros(count):
  """
  Creates a zero-filled byte array of with ``count`` bytes.

  :param count:
      The number of zero bytes.
  :returns:
      Zero-filled byte array.
  """
  return array("B", [0] * count)


def bytearray_concat(byte_array1, byte_array2):
  """
  Concatenates two byte arrays.

  :param byte_array1:
      Byte array 1
  :param byte_array2:
      Byte array 2
  :returns:
      Concatenated byte array.
  """
  return byte_array1 + byte_array2


def bytearray_to_bytes(byte_array):
  """
  Converts a byte array into a string.

  :param byte_array:
      The byte array.
  :returns:
      String.
  """
  return byte_array.tostring()


def bytes_to_bytearray(byte_string):
  """
  Converts a string into a byte array.

  :param byte_string:
      String value.
  :returns:
      Byte array.
  """
  byte_array = bytearray_create_zeros(0)
  byte_array.fromstring(byte_string)
  return byte_array


# TODO: Keep these functions around.
def bytearray_to_long(byte_array):
  """
  Converts a byte array to long.

  :param byte_array:
      The byte array.
  :returns:
      Long.
  """
  total = 0
  multiplier = 1
  for count in range(len(byte_array) - 1, -1, -1):
    byte_val = byte_array[count]
    total += multiplier * byte_val
    multiplier *= 256
  return total


def long_to_bytearray(num):
  """
  Converts a long into a byte array.

  :param num:
      Long value
  :returns:
      Long.
  """
  bytes_count = builtins.integer_byte_length(num)
  byte_array = bytearray_create_zeros(bytes_count)
  for count in range(bytes_count - 1, -1, -1):
    byte_array[count] = int(num % 256)
    num >>= 8
  return byte_array


def mpi_to_long(mpi_byte_string):
  """
  Converts an OpenSSL-format MPI Bignum byte string into a long.

  :param mpi_byte_string:
      OpenSSL-format MPI Bignum byte string.
  :returns:
      Long value.
  """
  #    from mom._types.bytearray import \
  #        bytes_to_bytearray, bytearray_to_long

  # Make sure this is a positive number
  assert (ord(mpi_byte_string[4]) & 0x80) == 0

  byte_array = bytes_to_bytearray(mpi_byte_string[4:])
  return bytearray_to_long(byte_array)


def long_to_mpi(num):
  """
  Converts a long value into an OpenSSL-format MPI Bignum byte string.

  :param num:
      Long value.
  :returns:
      OpenSSL-format MPI Bignum byte string.
  """
  #    from mom._types.bytearray import \
  #        long_to_bytearray, bytearray_concat, \
  #        bytearray_to_bytes, bytearray_create_zeros

  byte_array = long_to_bytearray(num)
  ext = 0
  # If the high-order bit is going to be set,
  # add an extra byte of zeros
  if not (builtins.integer_bit_length(num) & 0x7):
    ext = 1
  length = builtins.integer_byte_length(num) + ext
  byte_array = bytearray_concat(bytearray_create_zeros(4 + ext), byte_array)
  byte_array[0] = (length >> 24) & 0xFF
  byte_array[1] = (length >> 16) & 0xFF
  byte_array[2] = (length >> 8) & 0xFF
  byte_array[3] = length & 0xFF
  return bytearray_to_bytes(byte_array)
