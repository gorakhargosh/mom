#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest2
from mom.builtins import b
from mom.codec._alt_integer import uint_to_bytes_naive
from mom.codec.integer import uint_to_bytes
from mom.prime_sieve import sieve

# Long value from Python-RSA.
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
        for prime in sieve:
            self.assertEqual(uint_to_bytes(prime),
                             uint_to_bytes_naive(prime),
                             "Boom %d" % prime)

    def test_zero(self):
        self.assertEqual(uint_to_bytes(0), b('\x00'))
        self.assertEqual(uint_to_bytes(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes(0, 0, 1), b('\x00'))
        self.assertEqual(uint_to_bytes(0, 0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes(0, 0, 7), b('\x00') * 7)

    def test_ValueError_when_not_unsigned_integer(self):
        self.assertRaises(ValueError, uint_to_bytes, -1)

    def test_TypeError_when_not_integer(self):
        self.assertRaises(TypeError, uint_to_bytes, 2.4)
        self.assertRaises(TypeError, uint_to_bytes, "")
        self.assertRaises(TypeError, uint_to_bytes, b(''))
        self.assertRaises(TypeError, uint_to_bytes, object)
        self.assertRaises(TypeError, uint_to_bytes, dict())
        self.assertRaises(TypeError, uint_to_bytes, set([]))
        self.assertRaises(TypeError, uint_to_bytes, [])
        self.assertRaises(TypeError, uint_to_bytes, ())
