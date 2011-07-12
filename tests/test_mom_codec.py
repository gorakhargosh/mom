#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.codec import base64_encode, base64_decode
from mom.security.random import generate_random_bytes

# Generates a 1024-bit strength random byte string.
random_bytes_1024 = generate_random_bytes(1024 >> 3)
# Generates a 2048-bit strength random byte string.
random_bytes_2048 = generate_random_bytes(2048 >> 3)
# Generates a 4096-bit strength random byte string.
random_bytes_4096 = generate_random_bytes(4096 >> 3)

class Test_base64_codec(unittest2.TestCase):
    def test_encodes_without_trailing_newline(self):
        self.assertFalse(base64_encode(random_bytes_1024).endswith("\n"))
        self.assertFalse(base64_encode(random_bytes_2048).endswith("\n"))
        self.assertFalse(base64_encode(random_bytes_4096).endswith("\n"))

    def test_encode_decode_identity(self):
        self.assertEqual(base64_decode(base64_encode(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(base64_decode(base64_encode(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(base64_decode(base64_encode(random_bytes_4096)), random_bytes_4096)

