#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.builtins import is_bytes, is_bytes_or_unicode
from mom.codec.integer import bytes_to_uint
from mom.security.random import \
    generate_random_hex_string, generate_random_uint_between, \
    generate_random_bits, generate_random_uint_atmost, \
    generate_random_uint_exactly, ALPHANUMERIC, \
    ASCII_PRINTABLE, ALPHA, LOWERCASE_ALPHANUMERIC, \
    LOWERCASE_ALPHA, DIGITS, generate_random_password, \
    generate_random_sequence, calculate_entropy, generate_random_string


class Test_generate_random_bits(unittest2.TestCase):
    def test_range(self):
        for i in range(999):
            n_bits = 4
            value = bytes_to_uint(generate_random_bits(n_bits))
            self.assertTrue(value >= 0 and value < (1 << n_bits))

    def test_uniqueness(self):
        # The likelyhood of recurrence should be tiny if a large enough
        # bit size is chosen.
        self.assertNotEqual(generate_random_bits(64), generate_random_bits(64))

    def test_ValueError_when_0_bits(self):
        self.assertRaises(ValueError, generate_random_bits, 0)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_bits, None)
        self.assertRaises(TypeError, generate_random_bits, {})
        self.assertRaises(TypeError, generate_random_bits, object)
        self.assertRaises(TypeError, generate_random_bits, True)
        self.assertRaises(TypeError, generate_random_bits, "")



class Test_generate_random_ulong_exactly(unittest2.TestCase):
    def test_range(self):
        for i in range(128):
            n_bits = i + 1
            for j in range(128):
                x = generate_random_uint_exactly(n_bits)
                # Ensure high bit is set
                #self.assertTrue(x & (2 ** (n_bits - 1)))
                self.assertTrue(x >= (1 << (n_bits - 1)) and
                                x < (1 << n_bits), "huh? x=%d" % x)

    def test_ValueError_when_0_bits(self):
        self.assertRaises(ValueError, generate_random_uint_exactly, 0)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_uint_exactly, None)
        self.assertRaises(TypeError, generate_random_uint_exactly, {})
        self.assertRaises(TypeError, generate_random_uint_exactly, object)
        self.assertRaises(TypeError, generate_random_uint_exactly, True)
        self.assertRaises(TypeError, generate_random_uint_exactly, "")

        
class Test_generate_random_ulong_atmost(unittest2.TestCase):
    def test_range(self):
        for i in range(128):
            n_bits = i + 1
            for j in range(128):
                x = generate_random_uint_atmost(n_bits)
                self.assertTrue(x >= 0 and x < (1 << n_bits),
                                "huh? x=%d" % x)

    def test_ValueError_when_0_bits(self):
        self.assertRaises(ValueError, generate_random_uint_atmost, 0)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_uint_atmost, None)
        self.assertRaises(TypeError, generate_random_uint_atmost, {})
        self.assertRaises(TypeError, generate_random_uint_atmost, object)
        self.assertRaises(TypeError, generate_random_uint_atmost, True)
        self.assertRaises(TypeError, generate_random_uint_atmost, "")


class Test_generate_random_hex_string(unittest2.TestCase):
    def test_length(self):
        default_length = 8
        self.assertEqual(len(generate_random_hex_string()), default_length,
                     "Length does not match "\
                     "default expected length of %d." % default_length)
        self.assertEqual(len(generate_random_hex_string(length=10)), 10,
                     "Length does not match expected length.")


    def test_uniqueness(self):
        # The likelyhood of recurrence should be tiny if a large enough
        # length is chosen.
        self.assertNotEqual(generate_random_hex_string(),
                         generate_random_hex_string(),
                         "Not unique.")

    def test_is_string(self):
        self.assertTrue(is_bytes(generate_random_hex_string()),
                        "Not a bytestring.")

    def test_TypeError_if_invalid_length_type(self):
        self.assertRaises(TypeError, generate_random_hex_string, None)
        self.assertRaises(TypeError, generate_random_hex_string, "")

    def test_raises_ValueError_if_invalid_length(self):
        self.assertRaises(ValueError, generate_random_hex_string, 33)
        self.assertRaises(ValueError, generate_random_hex_string, 0)
        self.assertRaises(ValueError, generate_random_hex_string, -1)
        self.assertRaises(ValueError, generate_random_hex_string, 33)
        self.assertRaises(ValueError, generate_random_hex_string, True)
        self.assertRaises(ValueError, generate_random_hex_string, False)

class Test_generate_random_ulong_between(unittest2.TestCase):
    def test_range(self):
        low, high = 1, 10
        for x in range(1000):
            value = generate_random_uint_between(low, high)
            self.assertTrue(value >= low and value < high)

    def test_ValueError_when_low_greater_than_high(self):
        low, high = 4, 3
        self.assertRaises(ValueError, generate_random_uint_between, low, high)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_uint_between, None, None)
        self.assertRaises(TypeError, generate_random_uint_between, {}, {})
        self.assertRaises(TypeError, generate_random_uint_between, object, object)
        self.assertRaises(TypeError, generate_random_uint_between, True, True)
        self.assertRaises(TypeError, generate_random_uint_between, "", "")


class Test_generate_random_string(unittest2.TestCase):
    def test_random_string_length(self):
        for i in range(10):
            self.assertEqual(len(generate_random_string(64)),
                             len(generate_random_string(64)))
            self.assertEqual(len(generate_random_string(64)), 64)

    def test_is_string(self):
        self.assertTrue(is_bytes_or_unicode(generate_random_string(64)))

    def test_uniqueness(self):
        # For a decent enough entropy.
        for i in range(10):
            self.assertNotEqual(generate_random_string(64),
                                generate_random_string(64))

class Test_generate_random_password(unittest2.TestCase):
    def test_random_password_length(self):
        symbol_sets = [
            DIGITS,
            LOWERCASE_ALPHA,
            LOWERCASE_ALPHANUMERIC,
            ALPHA,
            ALPHANUMERIC,
            ASCII_PRINTABLE,
        ]
        lengths_64 = [
            20,
            14,
            13,
            12,
            11,
            10
        ]
        lengths_1024 = [
            309,
            218,
            199,
            180,
            172,
            157,
        ]
        for length, symbols in zip(lengths_64, symbol_sets):
            for i in range(10):
                self.assertEqual(len(generate_random_password(64, symbols)),
                                 length)
        for length, symbols in zip(lengths_1024, symbol_sets):
            for i in range(10):
                self.assertEqual(len(generate_random_password(1024, symbols)),
                                 length)

    def test_uniqueness(self):
        # For a decent enough entropy.
        for i in range(10):
            self.assertNotEqual(generate_random_password(64),
                                generate_random_password(64))


class Test_generate_random_sequence(unittest2.TestCase):
    def test_raises_TypeError_when_length_is_not_integer(self):
        self.assertRaises(TypeError, generate_random_sequence, None, ALPHA)

    def test_raises_TypeError_when_pool_is_None(self):
        self.assertRaises(TypeError, generate_random_sequence, 6, None)

    def test_raises_ValueError_when_length_is_not_positive(self):
        self.assertRaises(ValueError, generate_random_sequence, 0, ALPHA)
        self.assertRaises(ValueError, generate_random_sequence, -1, ALPHA)

class Test_calculate_entropy(unittest2.TestCase):
    def test_entropy(self):
        symbol_sets = [
            DIGITS,
            LOWERCASE_ALPHA,
            LOWERCASE_ALPHANUMERIC,
            ALPHA,
            ALPHANUMERIC,
            ASCII_PRINTABLE,
        ]
        lengths_64 = [
            20,
            14,
            13,
            12,
            11,
            10
        ]
        lengths_1024 = [
            309,
            218,
            199,
            180,
            172,
            157,
        ]
        lengths_128 = [
            39,
            28,
            25,
            23,
            22,
            20,
        ]


        for length, symbols in zip(lengths_64, symbol_sets):
            for i in range(10):
                self.assertTrue(calculate_entropy(length, symbols) >= 64)
        for length, symbols in zip(lengths_1024, symbol_sets):
            for i in range(10):
                self.assertTrue(calculate_entropy(length, symbols) >= 1024)
        for length, symbols in zip(lengths_128, symbol_sets):
            for i in range(10):
                self.assertTrue(calculate_entropy(length, symbols) >= 128)
