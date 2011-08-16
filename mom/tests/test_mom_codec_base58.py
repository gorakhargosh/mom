#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from mom.builtins import b
from mom.codec import hex_decode, base58_decode, base58_encode
from mom.codec._alt_base import b58decode_naive, b58encode_naive
from mom.codec.base58 import b58encode, b58decode, ALT58_BYTES, ASCII58_BYTES
from mom.codec.integer import uint_to_bytes, bytes_to_uint
from mom.security.random import generate_random_bytes

random_bytes = generate_random_bytes(384)

zero_bytes = b('\x00\x00\x00\x00')
one_zero_byte = b('\x00')
raw_data = hex_decode(b('005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64'))
encoded = b('19TbMSWwHvnxAKy12iNm3KdbGfzfaMFViT')
encoded_with_whitespace = b('''
19TbMSWwHvnxAKy12iN
m3KdbGfzfaMFViT
''')

padding_raw = b('''\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
''')

class Test_base58_codec(unittest2.TestCase):
    def test_ensure_charset_length(self):
        self.assertEqual(len(ASCII58_BYTES), 58)
        self.assertEqual(len(ALT58_BYTES), 58)

    def test_codec_identity(self):
        self.assertEqual(b58decode(b58encode(random_bytes)), random_bytes)
        self.assertEqual(b58decode_naive(b58encode(random_bytes)), random_bytes)
        self.assertEqual(base58_decode(base58_encode(random_bytes)),
                         random_bytes)

    def test_encodes_zero_prefixed_padding(self):
        self.assertEqual(b58decode(b58encode(padding_raw)), padding_raw)
        self.assertEqual(b58decode_naive(b58encode(padding_raw)), padding_raw)
        self.assertEqual(base58_decode(base58_encode(padding_raw)), padding_raw)

    def test_zero_bytes(self):
        self.assertEqual(b58encode(zero_bytes), b('1111'))
        self.assertEqual(b58decode(b('1111')), zero_bytes)
        self.assertEqual(b58decode_naive(b('1111')), zero_bytes)
        self.assertEqual(b58encode(one_zero_byte), b('1'))
        self.assertEqual(b58decode(b('1')), one_zero_byte)
        self.assertEqual(b58decode_naive(b('1')), one_zero_byte)

        self.assertEqual(base58_encode(zero_bytes), b('1111'))
        self.assertEqual(base58_decode(b('1111')), zero_bytes)
        self.assertEqual(base58_encode(one_zero_byte), b('1'))
        self.assertEqual(base58_decode(b('1')), one_zero_byte)

    def test_encoding_and_decoding(self):
        hello_world = b('\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64')

        self.assertEqual(b58encode(hello_world), b58encode_naive(hello_world))
        self.assertEqual(b58decode(b58encode(hello_world)), hello_world)

        self.assertEqual(bytes_to_uint(b58decode(b("16Ho7Hs"))), 3471844090)
        self.assertEqual(b58encode(uint_to_bytes(3471844090, 5)), b("16Ho7Hs"))

        self.assertEqual(b58encode(raw_data), encoded)
        self.assertEqual(b58decode(encoded), raw_data)
        self.assertEqual(b58decode(encoded_with_whitespace), raw_data)
        self.assertEqual(b58decode_naive(encoded), raw_data)
        self.assertEqual(b58decode_naive(encoded_with_whitespace), raw_data)

        self.assertEqual(base58_encode(raw_data), encoded)
        self.assertEqual(base58_decode(encoded), raw_data)
        self.assertEqual(base58_decode(encoded_with_whitespace), raw_data)
