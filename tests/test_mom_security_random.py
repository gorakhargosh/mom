#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from mom.security.random import \
    generate_random_uint_string, \
    generate_random_hex_string, generate_random_long_in_range


class Test_generate_random_uint_string(unittest2.TestCase):
    def test_uniqueness(self):
        self.assertNotEqual(generate_random_uint_string(), generate_random_uint_string())

    def test_hex_length(self):
        for i in range(1, 1000):
            self.assertEqual(len(generate_random_uint_string(64, 16)), 16)

    def test_unsigned_integer(self):
        self.assertTrue(int(generate_random_uint_string(64, 2), 2) >= 0)
        self.assertTrue(int(generate_random_uint_string(64, 10)) >= 0)
        self.assertTrue(int(generate_random_uint_string(64, 16), 16) >= 0)

    def test_raises_ValueError_when_invalid_bit_strength(self):
        self.assertRaises(ValueError, generate_random_uint_string, 63)
        self.assertRaises(ValueError, generate_random_uint_string, 0)

    def test_raises_ValueError_when_invalid_base(self):
        self.assertRaises(ValueError, generate_random_uint_string, 64, 0)
        self.assertRaises(ValueError, generate_random_uint_string, 64, None)

    def test_result_is_string(self):
        self.assertTrue(isinstance(generate_random_uint_string(64, 10), bytes))
        self.assertTrue(isinstance(generate_random_uint_string(64, 16), bytes))


class Test_generate_random_hex_string(unittest2.TestCase):
    def test_length(self):
        default_length = 8
        self.assertEqual(len(generate_random_hex_string()), default_length,
                     "Verification code length does not match "\
                     "default expected length of %d." % default_length)
        self.assertEqual(len(generate_random_hex_string(length=10)), 10,
                     "Verification code length does not match expected length.")

        self.assertRaises(ValueError, generate_random_hex_string, 33)
        self.assertRaises(ValueError, generate_random_hex_string, 0)
        self.assertRaises(ValueError, generate_random_hex_string, -1)
        self.assertRaises(ValueError, generate_random_hex_string, 33)
        self.assertRaises(TypeError, generate_random_hex_string, None)
        self.assertRaises(TypeError, generate_random_hex_string, "")

    def test_uniqueness(self):
        self.assertNotEqual(generate_random_hex_string(),
                         generate_random_hex_string(),
                         "Verification code is not unique.")

    def test_is_string(self):
        self.assertTrue(isinstance(generate_random_hex_string(), bytes),
                    "Verification code is not a bytestring.")

class Test_generate_random_long_in_range(unittest2.TestCase):
    def test_range(self):
        low, high = 1, 10
        for x in range(1000):
            value = generate_random_long_in_range(low, high)
            self.assertTrue(value >= low and value < high)


    def test_raises_ValueError_when_low_greater_than_high(self):
        low, high = 4, 3
        self.assertRaises(ValueError, generate_random_long_in_range, low, high)
