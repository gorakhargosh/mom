#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 Trevor Perrin <trevp@trevp.net>
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: mom._types.bytearray
:synopsis: Byte arrays.

Creation and manipulation
-------------------------
.. autofunction:: bytearray_create
.. autofunction:: bytearray_create_zeros
.. autofunction:: bytearray_concat

Type conversion
---------------
.. autofunction:: bytearray_to_bytes
.. autofunction:: bytes_to_bytearray
.. autofunction:: bytearray_to_long
.. autofunction:: long_to_bytearray
"""

from __future__ import absolute_import

from array import array
from mom.builtins import long_byte_count


def bytearray_create(sequence):
    """
    Creates a byte array from a given sequence.

    :param sequence:
        The sequence from which a byte array will be created.
    :returns:
        A byte array.
    """
    return array('B', sequence)


def bytearray_create_zeros(count):
    """
    Creates a zero-filled byte array of with ``count`` bytes.

    :param count:
        The number of zero bytes.
    :returns:
        Zero-filled byte array.
    """
    return array('B', [0] * count)


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


def bytearray_to_long(byte_array):
    """
    Converts a byte array to long.

    :param byte_array:
        The byte array.
    :returns:
        Long.
    """
    total = 0L
    multiplier = 1L
    for count in range(len(byte_array)-1, -1, -1):
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
    bytes_count = long_byte_count(num)
    byte_array = bytearray_create_zeros(bytes_count)
    for count in range(bytes_count - 1, -1, -1):
        byte_array[count] = int(num % 256)
        num >>= 8
    return byte_array

