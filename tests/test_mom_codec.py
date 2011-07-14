#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.builtins import b
from mom.security.random import \
    generate_random_bytes, generate_random_long_in_range
from mom.codec import \
    base64_encode, \
    base64_decode, \
    hex_decode, \
    hex_encode, \
    decimal_decode, \
    decimal_encode, bin_encode, bin_decode, bytes_to_long, long_to_bytes, long_bin_encode, long_bin_decode, long_hex_encode, long_hex_decode, long_base64_encode, long_base64_decode


# Generates a 1024-bit strength random byte string.
random_bytes_1024 = generate_random_bytes(1024 >> 3)
# Generates a 2048-bit strength random byte string.
random_bytes_2048 = generate_random_bytes(2048 >> 3)
# Generates a 4093 byte length random byte string.
random_bytes_len_4093 = generate_random_bytes(4093)

zero_bytes = b('\x00\x00\x00\x00')
one_zero_byte = b('\x00')

random_long_value = generate_random_long_in_range(0, 99999999999999999L)
zero_long = 0L
negative_long_value = -1L

class Test_base64_codec(unittest2.TestCase):
    def test_encodes_without_trailing_newline(self):
        self.assertFalse(base64_encode(zero_bytes).endswith("\n"))
        self.assertFalse(base64_encode(random_bytes_1024).endswith("\n"))
        self.assertFalse(base64_encode(random_bytes_2048).endswith("\n"))
        self.assertFalse(base64_encode(random_bytes_len_4093).endswith("\n"))

    def test_codec_identity(self):
        # Not zero-destructive.
        self.assertEqual(base64_decode(base64_encode(zero_bytes)), zero_bytes)
        self.assertEqual(base64_decode(base64_encode(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(base64_decode(base64_encode(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(base64_decode(base64_encode(random_bytes_len_4093)), random_bytes_len_4093)

class Test_hex_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # Not zero-destructive
        self.assertEqual(hex_decode(hex_encode(zero_bytes)), zero_bytes)
        self.assertEqual(hex_decode(hex_encode(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(hex_decode(hex_encode(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(hex_decode(hex_encode(random_bytes_len_4093)), random_bytes_len_4093)

class Test_decimal_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # TODO: DESTRUCTIVE behavior for zero bytes (not acceptable).
        self.assertEqual(decimal_decode(decimal_encode(zero_bytes)), zero_bytes)
        self.assertEqual(decimal_decode(decimal_encode(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(decimal_decode(decimal_encode(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(decimal_decode(decimal_encode(random_bytes_len_4093)), random_bytes_len_4093)

class Test_bin_codec(unittest2.TestCase):
    def test_codec_identity(self):
        self.assertEqual(bin_decode(bin_encode(zero_bytes)), zero_bytes)
        self.assertEqual(bin_decode(bin_encode(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(bin_decode(bin_encode(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(bin_decode(bin_encode(random_bytes_len_4093)), random_bytes_len_4093)


class Test_bytes_long_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # TODO: DESTRUCTIVE behavior for zero bytes (is acceptable here).
        self.assertEqual(long_to_bytes(bytes_to_long(zero_bytes)), one_zero_byte)
        self.assertEqual(long_to_bytes(bytes_to_long(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(long_to_bytes(bytes_to_long(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(long_to_bytes(bytes_to_long(random_bytes_len_4093)), random_bytes_len_4093)

class Test_long_bin_encode(unittest2.TestCase):
    def test_codec_identify(self):
        self.assertEqual(long_bin_decode(long_bin_encode(random_long_value)), random_long_value)
        self.assertEqual(long_bin_decode(long_bin_encode(zero_long)), zero_long)
        self.assertEqual(long_bin_decode(long_bin_encode(negative_long_value)), negative_long_value)

class Test_long_hex_encode(unittest2.TestCase):
    def test_codec_identify(self):
        self.assertEqual(long_hex_decode(long_hex_encode(random_long_value)), random_long_value)
        self.assertEqual(long_hex_decode(long_hex_encode(zero_long)), zero_long)
        self.assertEqual(long_hex_decode(long_hex_encode(negative_long_value)), negative_long_value)

class Test_long_base64_encode(unittest2.TestCase):
    def test_codec_identify(self):
        self.assertEqual(long_base64_decode(long_base64_encode(random_long_value)), random_long_value)
        self.assertEqual(long_base64_decode(long_base64_encode(zero_long)), zero_long)
        self.assertEqual(long_base64_decode(long_base64_encode(negative_long_value)), negative_long_value)
