#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.builtins import b
from mom.security.random import generate_random_bytes
from mom.codec import \
    base64_encode, \
    base64_decode, \
    hex_to_bytes, \
    bytes_to_hex, \
    bytes_to_base64, \
    base64_to_bytes,\
    decimal_to_bytes, \
    bytes_to_decimal, bytes_to_bin, bin_to_bytes, bytes_to_long, long_to_bytes


# Generates a 1024-bit strength random byte string.
random_bytes_1024 = generate_random_bytes(1024 >> 3)
# Generates a 2048-bit strength random byte string.
random_bytes_2048 = generate_random_bytes(2048 >> 3)
# Generates a 4093 byte length random byte string.
random_bytes_len_4093 = generate_random_bytes(4093)

zero_bytes = b('\x00\x00\x00\x00')
one_zero_byte = b('\x00')

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

class Test_bytes_base64_codec(unittest2.TestCase):
    def test_encodes_without_trailing_newline(self):
        self.assertFalse(bytes_to_base64(zero_bytes).endswith("\n"))
        self.assertFalse(bytes_to_base64(random_bytes_1024).endswith("\n"))
        self.assertFalse(bytes_to_base64(random_bytes_2048).endswith("\n"))
        self.assertFalse(bytes_to_base64(random_bytes_len_4093).endswith("\n"))

    def test_codec_identity(self):
        # Not zero-destructive
        self.assertEqual(base64_to_bytes(bytes_to_base64(zero_bytes)), zero_bytes)
        self.assertEqual(base64_to_bytes(bytes_to_base64(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(base64_to_bytes(bytes_to_base64(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(base64_to_bytes(bytes_to_base64(random_bytes_len_4093)), random_bytes_len_4093)


class Test_bytes_hex_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # Not zero-destructive
        self.assertEqual(hex_to_bytes(bytes_to_hex(zero_bytes)), zero_bytes)
        self.assertEqual(hex_to_bytes(bytes_to_hex(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(hex_to_bytes(bytes_to_hex(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(hex_to_bytes(bytes_to_hex(random_bytes_len_4093)), random_bytes_len_4093)

class Test_bytes_decimal_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # TODO: DESTRUCTIVE behavior for zero bytes (not acceptable).
        self.assertEqual(decimal_to_bytes(bytes_to_decimal(zero_bytes)), zero_bytes)
        self.assertEqual(decimal_to_bytes(bytes_to_decimal(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(decimal_to_bytes(bytes_to_decimal(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(decimal_to_bytes(bytes_to_decimal(random_bytes_len_4093)), random_bytes_len_4093)

class Test_bytes_bin_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # TODO: DESTRUCTIVE behavior for zero bytes (not acceptable).
        self.assertEqual(bin_to_bytes(bytes_to_bin(zero_bytes)), zero_bytes)
        self.assertEqual(bin_to_bytes(bytes_to_bin(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(bin_to_bytes(bytes_to_bin(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(bin_to_bytes(bytes_to_bin(random_bytes_len_4093)), random_bytes_len_4093)

class Test_bytes_long_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # TODO: DESTRUCTIVE behavior for zero bytes (is acceptable here).
        self.assertEqual(long_to_bytes(bytes_to_long(zero_bytes)), one_zero_byte)
        self.assertEqual(long_to_bytes(bytes_to_long(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(long_to_bytes(bytes_to_long(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(long_to_bytes(bytes_to_long(random_bytes_len_4093)), random_bytes_len_4093)
