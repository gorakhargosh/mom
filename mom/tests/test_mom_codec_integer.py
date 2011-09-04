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

import unittest2
from mom.builtins import b
from mom.codec._alt_integer import uint_to_bytes_naive, \
    uint_to_bytes_simple, uint_to_bytes_pycrypto, uint_to_bytes_array_based, \
    uint_to_bytes_naive_array_based, bytes_to_uint_naive, bytes_to_uint_simple
from mom.codec.integer import uint_to_bytes, bytes_to_uint
from mom.prime_sieve import SIEVE

# Long value from Python-RSA.
from mom.tests.constants import unicode_string
from mom.tests.test_mom_codec import long_value_blocksize, \
    expected_blocksize_bytes, zero_bytes, one_zero_byte

long_value = 71671831749689734735896910666236152091910950933161125188784836897624039426313152092699961904060141667369
expected_fill_bytes = b('''\
\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)''')
expected_bytes = b('''\
\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)''')


class Test_unsigned_integer_to_bytes(unittest2.TestCase):
    def test_long_value(self):
        self.assertEqual(uint_to_bytes(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes(long_value, fill_size=45),
                         expected_fill_bytes)

    def test_fill_size(self):
        self.assertEqual(uint_to_bytes(0xc0ff, fill_size=4),
                         b('\x00\x00\xc0\xff'))
        self.assertEqual(uint_to_bytes(0xc0ffee, fill_size=6),
                         b('\x00\x00\x00\xc0\xff\xee'))
        self.assertEqual(uint_to_bytes(123456789, fill_size=6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes(123456789, fill_size=7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

    def test_overflow_allowed(self):
        self.assertEqual(uint_to_bytes(0xc0ff, fill_size=1, overflow=True),
                         b('\xc0\xff'))
        self.assertEqual(uint_to_bytes(123456789, fill_size=3, overflow=True),
                         b('\x07\x5b\xcd\x15'))
        self.assertEqual(uint_to_bytes(0xf00dc0ffee, fill_size=4,
                                       overflow=True),
                         b('\xf0\x0d\xc0\xff\xee'))

    def test_OverflowError_when_fill_size_insufficient(self):
        self.assertRaises(OverflowError, uint_to_bytes, 0xffff,
                          fill_size=1)
        self.assertRaises(OverflowError, uint_to_bytes,
                          123456789, fill_size=3)
        self.assertRaises(OverflowError, uint_to_bytes,
                          0xf00dc0ffee, fill_size=4)

    def test_chunk_size(self):
        self.assertEqual(uint_to_bytes(0xffffeeeeaa, chunk_size=4),
                         b('\x00\x00\x00\xff\xff\xee\xee\xaa'))

    def test_ValueError_when_both_fill_size_and_chunk_size_specified(self):
        self.assertRaises(ValueError, uint_to_bytes, 0xff, 1, 1)

    def test_TypeError_when_fill_size_is_not_an_integer(self):
        self.assertRaises(TypeError, uint_to_bytes, 0xff, '', 0)

    def test_TypeError_when_chunk_size_is_not_an_integer(self):
        self.assertRaises(TypeError, uint_to_bytes, 0xff, 0, '')

    def test_correctness(self):
        self.assertEqual(uint_to_bytes(0xeeeeffff),
                         b('\xee\xee\xff\xff'))
        self.assertEqual(uint_to_bytes(0xeeeeff),
                         b('\xee\xee\xff'))

        self.assertEqual(uint_to_bytes_naive(0xeeeeffff),
                         b('\xee\xee\xff\xff'))
        self.assertEqual(uint_to_bytes_naive(0xeeeeff),
                         b('\xee\xee\xff'))

        self.assertEqual(uint_to_bytes_simple(0xeeeeffff),
                         b('\xee\xee\xff\xff'))
        self.assertEqual(uint_to_bytes_simple(0xeeeeff),
                         b('\xee\xee\xff'))
        
    def test_correctness_against_base_implementation(self):
        # Slow test.
        values = [
            1 << 512,
            1 << 8192,
            1 << 77,
        ]
        for value in values:
            self.assertEqual(uint_to_bytes(value),
                             uint_to_bytes_naive(value),
                             "Boom %d" % value)

    def test_correctness_for_primes(self):
        for prime in SIEVE:
            self.assertEqual(uint_to_bytes(prime),
                             uint_to_bytes_naive(prime),
                             "Boom %d" % prime)

    def test_zero(self):
        self.assertEqual(uint_to_bytes(0), b('\x00'))
        self.assertEqual(uint_to_bytes(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes(0, chunk_size=1), b('\x00'))
        self.assertEqual(uint_to_bytes(0, chunk_size=4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes(0, chunk_size=7), b('\x00') * 7)

        self.assertEqual(uint_to_bytes_naive(0), b('\x00'))
        self.assertEqual(uint_to_bytes_naive(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_naive(0, 7), b('\x00') * 7)
        
        self.assertEqual(uint_to_bytes_simple(0), b('\x00'))


    def test_ValueError_when_not_unsigned_integer(self):
        self.assertRaises(ValueError, uint_to_bytes, -1)
        self.assertRaises(ValueError, uint_to_bytes_naive, -1)
        self.assertRaises(AssertionError, uint_to_bytes_simple, -1)

    def test_TypeError_when_not_integer(self):
        self.assertRaises(TypeError, uint_to_bytes, 2.4)
        self.assertRaises(TypeError, uint_to_bytes, "")
        self.assertRaises(TypeError, uint_to_bytes, b(''))
        self.assertRaises(TypeError, uint_to_bytes, object)
        self.assertRaises(TypeError, uint_to_bytes, dict())
        self.assertRaises(TypeError, uint_to_bytes, set([]))
        self.assertRaises(TypeError, uint_to_bytes, [])
        self.assertRaises(TypeError, uint_to_bytes, ())


class Test_bytes_uint_codec(unittest2.TestCase):
    def test_codec_equivalence(self):
        # Padding bytes are not preserved (it is acceptable here).
        random_bytes = b("\x00\xbcE\x9a\xda]")
        expected_bytes = b("\xbcE\x9a\xda]")
        self.assertEqual(uint_to_bytes(bytes_to_uint(random_bytes)),
                         expected_bytes)
        self.assertEqual(uint_to_bytes(bytes_to_uint_naive(random_bytes)),
                         expected_bytes)
        self.assertEqual(uint_to_bytes(bytes_to_uint_simple(random_bytes)),
                         expected_bytes)

    def test_zero_bytes(self):
        self.assertEqual(uint_to_bytes(bytes_to_uint(zero_bytes)),
                         one_zero_byte)
        self.assertEqual(uint_to_bytes(bytes_to_uint_naive(zero_bytes)),
                         one_zero_byte)
        self.assertEqual(uint_to_bytes(bytes_to_uint_simple(zero_bytes)),
                         one_zero_byte)

    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, bytes_to_uint, unicode_string)
        self.assertRaises(TypeError, bytes_to_uint, None)

        self.assertRaises(TypeError, bytes_to_uint_naive, unicode_string)
        self.assertRaises(TypeError, bytes_to_uint_naive, None)


class Test_uint_to_bytes(unittest2.TestCase):
    def test_accuracy(self):
        self.assertEqual(uint_to_bytes(123456789), b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_pycrypto(123456789),
                         b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_array_based(123456789),
                         b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive(123456789), b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive_array_based(123456789),
                         b('\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_pycrypto(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_array_based(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_naive(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_naive_array_based(long_value),
                         expected_bytes)

    def test_chunk_size(self):
        self.assertEqual(uint_to_bytes(long_value,
                                       long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_pycrypto(long_value,
                                                long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_array_based(long_value,
                                                   long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_naive(long_value,
                                             long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_naive_array_based(long_value,
                                                         long_value_blocksize),
                         expected_blocksize_bytes)


        self.assertEqual(uint_to_bytes(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_pycrypto(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_pycrypto(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_array_based(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_array_based(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_naive(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_naive_array_based(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive_array_based(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

    def test_zero(self):
        self.assertEqual(uint_to_bytes(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_array_based(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_naive(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_naive_array_based(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_pycrypto(0, 4), b('\x00') * 4)

        self.assertEqual(uint_to_bytes(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_naive(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_array_based(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_naive_array_based(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_pycrypto(0, 7), b('\x00') * 7)

        self.assertEqual(uint_to_bytes(0), b('\x00'))
        self.assertEqual(uint_to_bytes_naive(0), b('\x00'))
        self.assertEqual(uint_to_bytes_array_based(0), b('\x00'))
        self.assertEqual(uint_to_bytes_naive_array_based(0), b('\x00'))
        self.assertEqual(uint_to_bytes_pycrypto(0), b('\x00'))

    def test_correctness_against_base_implementation(self):
        # Slow test.
        values = [
            1 << 512,
            1 << 8192,
            1 << 77,
        ]
        for value in values:
            self.assertEqual(uint_to_bytes(value), uint_to_bytes_naive(value),
                             "Boom %d" % value)
            self.assertEqual(uint_to_bytes_array_based(value),
                             uint_to_bytes_naive(value),
                             "Boom %d" % value)
            self.assertEqual(uint_to_bytes(value),
                             uint_to_bytes_naive_array_based(value),
                             "Boom %d" % value)
            self.assertEqual(uint_to_bytes_pycrypto(value),
                             uint_to_bytes_naive(value),
                             "Boom %d" % value)
            self.assertEqual(bytes_to_uint(uint_to_bytes(value)),
                             value,
                             "Boom %d" % value)

    def test_correctness_for_primes(self):
        for prime in SIEVE:
            self.assertEqual(uint_to_bytes(prime), uint_to_bytes_naive(prime),
                             "Boom %d" % prime)
            self.assertEqual(uint_to_bytes_array_based(prime),
                             uint_to_bytes_naive(prime),
                             "Boom %d" % prime)
            self.assertEqual(uint_to_bytes_pycrypto(prime),
                             uint_to_bytes_naive(prime),
                             "Boom %d" % prime)

    def test_raises_OverflowError_when_chunk_size_is_insufficient(self):
        self.assertRaises(OverflowError, uint_to_bytes, 123456789, 3)
        self.assertRaises(OverflowError, uint_to_bytes, 299999999999, 4)

        self.assertRaises(OverflowError,
                          uint_to_bytes_array_based, 123456789, 3)
        self.assertRaises(OverflowError,
                          uint_to_bytes_array_based, 299999999999, 4)

        self.assertRaises(OverflowError, uint_to_bytes_naive, 123456789, 3)
        self.assertRaises(OverflowError, uint_to_bytes_naive, 299999999999, 4)

        self.assertRaises(OverflowError,
                          uint_to_bytes_naive_array_based, 123456789, 3)
        self.assertRaises(OverflowError,
                          uint_to_bytes_naive_array_based, 299999999999, 4)

    def test_raises_ValueError_when_negative_integer(self):
        self.assertRaises(ValueError, uint_to_bytes, -1)
        self.assertRaises(ValueError, uint_to_bytes_array_based, -1)
        self.assertRaises(ValueError, uint_to_bytes_naive, -1)
        self.assertRaises(ValueError, uint_to_bytes_naive_array_based, -1)

    def test_raises_TypeError_when_not_integer(self):
        self.assertRaises(TypeError, uint_to_bytes, None)
        self.assertRaises(TypeError, uint_to_bytes_array_based, None)
        self.assertRaises(TypeError, uint_to_bytes_naive, None)
        self.assertRaises(TypeError, uint_to_bytes_naive_array_based, None)
