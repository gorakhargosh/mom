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

"""
:module: mom.codec._base
:synopsis: Routines used by base converters.

.. autofunction:: base_decode_to_number
.. autofunction:: base_number_to_bytes
"""

try:
    # Use psyco if available.
    import psyco
    psyco.full()
except ImportError:
    pass

from mom._compat import ZERO_BYTE, EMPTY_BYTE
from mom.codec.integer import uint_to_bytes
from mom.builtins import bytes_leading


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
    :param powers_length:
        The length of the powers tuple.
    """
    # Convert to big integer.
#    number = 0
#    for i, x in enumerate(reversed(encoded)):
#        number += _lookup[x] * (base**i)
    # Above loop divided into precomputed powers section and computed.
    number = 0
    length = len(encoded)
    powers_length = len(powers)
    for i, x in enumerate(encoded[length:-powers_length-1:-1]):
        number += ord_lookup_table[x] * powers[i]
    for i in range(powers_length, length):
        x = encoded[length - i - 1]
        number += ord_lookup_table[x] * (base**i)
    return number


def uint_to_base256(number, encoded,
                    base_zero):
    if number == 0:
        raw_bytes = EMPTY_BYTE
    else:
        raw_bytes = uint_to_bytes(number)
    zero_leading = bytes_leading(encoded, base_zero)
    if zero_leading:
        raw_bytes = raw_bytes.rjust(len(raw_bytes) + zero_leading, ZERO_BYTE)
    return raw_bytes
