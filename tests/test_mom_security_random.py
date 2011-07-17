#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.codec import bytes_to_long
from mom.security.random import \
    generate_random_hex_string, generate_random_ulong_between, \
    generate_random_bits


class Test_generate_random_bits(unittest2.TestCase):
    def test_range(self):
        for i in range(9999):
            n_bits = 4
            value = bytes_to_long(generate_random_bits(n_bits))
            self.assertTrue(value >= 0 and value < (2L ** n_bits))

    def test_uniqueness(self):
        self.assertNotEqual(generate_random_bits(64), generate_random_bits(64))

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



class Test_generate_random_ulong_between(unittest2.TestCase):
    def test_range(self):
        low, high = 1, 10
        for x in range(1000):
            value = generate_random_ulong_between(low, high)
            self.assertTrue(value >= low and value < high)


    def test_raises_ValueError_when_low_greater_than_high(self):
        low, high = 4, 3
        self.assertRaises(ValueError, generate_random_ulong_between, low, high)
