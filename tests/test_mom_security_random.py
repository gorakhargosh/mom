#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.builtins import is_bytes
from mom.codec import bytes_to_long
from mom.security.random import \
    generate_random_hex_string, generate_random_ulong_between, \
    generate_random_bits, generate_random_ulong_atmost, generate_random_ulong_exactly


class Test_generate_random_bits(unittest2.TestCase):
    def test_range(self):
        for i in range(999):
            n_bits = 4
            value = bytes_to_long(generate_random_bits(n_bits))
            self.assertTrue(value >= 0 and value < (2L ** n_bits))

    def test_uniqueness(self):
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
                x = generate_random_ulong_exactly(n_bits)
                # Ensure high bit is set
                #self.assertTrue(x & (2L ** (n_bits - 1)))
                self.assertTrue(x >= (2L ** (n_bits - 1)) and
                                x < (2L ** n_bits), "huh? x=%d" % x)

    def test_ValueError_when_0_bits(self):
        self.assertRaises(ValueError, generate_random_ulong_exactly, 0)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_ulong_exactly, None)
        self.assertRaises(TypeError, generate_random_ulong_exactly, {})
        self.assertRaises(TypeError, generate_random_ulong_exactly, object)
        self.assertRaises(TypeError, generate_random_ulong_exactly, True)
        self.assertRaises(TypeError, generate_random_ulong_exactly, "")

class Test_generate_random_ulong_atmost(unittest2.TestCase):
    def test_range(self):
        for i in range(128):
            n_bits = i + 1
            for j in range(128):
                x = generate_random_ulong_atmost(n_bits)
                self.assertTrue(x >= 0 and x < (2L ** n_bits),
                                "huh? x=%d" % x)

    def test_ValueError_when_0_bits(self):
        self.assertRaises(ValueError, generate_random_ulong_atmost, 0)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_ulong_atmost, None)
        self.assertRaises(TypeError, generate_random_ulong_atmost, {})
        self.assertRaises(TypeError, generate_random_ulong_atmost, object)
        self.assertRaises(TypeError, generate_random_ulong_atmost, True)
        self.assertRaises(TypeError, generate_random_ulong_atmost, "")


class Test_generate_random_hex_string(unittest2.TestCase):
    def test_length(self):
        default_length = 8
        self.assertEqual(len(generate_random_hex_string()), default_length,
                     "Length does not match "\
                     "default expected length of %d." % default_length)
        self.assertEqual(len(generate_random_hex_string(length=10)), 10,
                     "Length does not match expected length.")


    def test_uniqueness(self):
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
            value = generate_random_ulong_between(low, high)
            self.assertTrue(value >= low and value < high)

    def test_ValueError_when_low_greater_than_high(self):
        low, high = 4, 3
        self.assertRaises(ValueError, generate_random_ulong_between, low, high)

    def test_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, generate_random_ulong_between, None, None)
        self.assertRaises(TypeError, generate_random_ulong_between, {}, {})
        self.assertRaises(TypeError, generate_random_ulong_between, object, object)
        self.assertRaises(TypeError, generate_random_ulong_between, True, True)
        self.assertRaises(TypeError, generate_random_ulong_between, "", "")
