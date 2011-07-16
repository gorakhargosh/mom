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
:module: mom.security.random
:synopsis: Random number, string, and bytearray generation utilities.

Bits and bytes
---------------------------
.. autofunction:: generate_random_bytes
.. autofunction:: generate_random_bits

Numbers
-------
.. autofunction:: generate_random_ulong
.. autofunction:: generate_random_long_in_range

Strings
-------
.. autofunction:: generate_random_hex_string
"""

from __future__ import absolute_import

import os
from mom.builtins import long_bit_length
from mom.codec import \
    hex_encode, \
    bytes_to_long


try:
    # Operating system unsigned random.
    os.urandom(1)
    def generate_random_bytes(count):
        """
        Generates a random byte string with ``count`` bytes.

        :param count:
            Number of bytes.
        :returns:
            Random byte string.
        """
        return os.urandom(count)
except AttributeError:
    try:
        __urandom_device__ = open("/dev/urandom", "rb")
        def generate_random_bytes(count):
            """
            Generates a random byte string with ``count`` bytes.

            :param count:
                Number of bytes.
            :returns:
                Random byte string.
            """
            return __urandom_device__.read(count)
    except IOError:
        #Else get Win32 CryptoAPI PRNG
        try:
            import win32prng
            def generate_random_bytes(count):
                """
                Generates a random byte string with ``count`` bytes.

                :param count:
                    Number of bytes.
                :returns:
                    Random byte string.
                """
                random_bytes = win32prng.generate_random_bytes(count)
                assert len(random_bytes) == count
                return random_bytes
        except ImportError:
            # What the fuck?!
            def generate_random_bytes(_):
                """
                WTF.

                :returns:
                    WTF.
                """
                raise NotImplementedError("What the fuck?! No PRNG available.")


def generate_random_long_in_range(low, high):
    """
    Generates a random long integer between low and high, not including
    high.

    The smaller the range, the lower the uniqueness.

    :param low:
        Low
    :param high:
        High
    :returns:
        Random long integer value.
    """
    from mom.builtins import long_byte_count, long_bit_length
    from mom._types.bytearray import \
        bytearray_to_long, bytes_to_bytearray

    if low >= high:
        raise ValueError("High must be greater than low.")
    num_bits = long_bit_length(high)
    num_bytes = long_byte_count(high)
    last_bits = num_bits % 8
    while 1:
        byte_array = bytes_to_bytearray(generate_random_bytes(num_bytes))
        if last_bits:
            byte_array[0] = byte_array[0] % (1 << last_bits)
        num = bytearray_to_long(byte_array)
        if num >= low and num < high:
            return num


def generate_random_bits(n_bits, rand_func=generate_random_bytes):
    """
    Generates the specified number of random bits as a byte string.
    For example::

        f(x) -> y such that
        f(16) ->           1111 1111 1111 1111; bytes_to_long(y) => 65535L
        f(17) -> 0000 0001 1111 1111 1111 1111; bytes_to_long(y) => 131071L

    :param n_bits:
        Number of random bits.

        if n is divisible by 8, (n * 8) bytes will be returned.
        if n is not divisible by 8, ((n * 8) + 1) bytes will be returned
        and the prefixed offset-byte will have `(n % 8)` number of random bits,
        (that is, `8 - (n % 8)` high bits will be cleared).

        The range of the numbers is 0 to (2**n)-1 inclusive.
    :param rand_func:
        Random bytes generator function.
    :returns:
        Bytes.
    """
    if not isinstance(n_bits, (int, long)):
        raise TypeError("unsupported operand type: %r" % type(n_bits).__name__)
    q, r = divmod(n_bits, 8)
    random_bytes = rand_func(q)
    if r:
        offset = ord(rand_func(1)) >> (8 - r)
        random_bytes = chr(offset) + random_bytes
    return random_bytes


def generate_random_ulong(n_bits, exact=False, rand_func=generate_random_bytes):
    """
    Generates a random unsigned long with `n_bits` random bits.

    :param n_bits:
        Number of random bits.
    :param exact:
        If exact is ``True``, the generated unsigned long integer
        will be between 2**(n_bits-1) and (2**n_bits)-1 both inclusive.
        If exact is ``False`` (default), the generated unsigned long integer
        will be between 0 and (2**n_bits)-1 both inclusive.
    :param rand_func:
        Random bytes generator function.
    :returns:
        Returns an unsigned long integer with `n_bits` random bits.
    """
    value = bytes_to_long(generate_random_bits(n_bits, rand_func=rand_func))
    assert(value >= 0 and value < (2L ** n_bits))
    if exact:
        # Set the high bit to ensure bit length.
        value |= 2L ** (n_bits - 1)
        assert(long_bit_length(value) >= n_bits)
    return value


def generate_random_hex_string(length=8):
    """
    Generates a random ASCII-encoded hexadecimal string of an even length.

    :param length:
        Length of the string to be returned. Default 32.
        The length MUST be a positive even number.
    :returns:
        A string representation of a randomly-generated hexadecimal string.
    """
    #if length % 2 or length <= 0:
    if length & 1 or length <= 0:
        raise ValueError(
            "This function expects a positive even number "\
            "length: got length `%r`." % length)
    return hex_encode(generate_random_bytes(length/2))

