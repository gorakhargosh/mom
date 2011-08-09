#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from mom.builtins import b
from mom.codec import hex_decode
from mom.codec.base58 import b58encode, b58decode
from mom.security.random import generate_random_bytes

random_bytes_len_4093 = generate_random_bytes(4093)

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
    def test_codec_identity(self):
        self.assertEqual(
            b58decode(b58encode(random_bytes_len_4093)),
            random_bytes_len_4093
        )

    def test_padding(self):
        self.assertEqual(b58decode(b58encode(padding_raw)), padding_raw)

    def test_zero_bytes(self):
        self.assertEqual(b58encode(zero_bytes), b('1111'))
        self.assertEqual(b58decode(b('1111')), zero_bytes)
        self.assertEqual(b58encode(one_zero_byte), b('1'))
        self.assertEqual(b58decode(b('1')), one_zero_byte)

    def test_encoding_and_decoding(self):
        self.assertEqual(b58encode(raw_data), encoded)
        self.assertEqual(b58decode(encoded), raw_data)
        self.assertEqual(b58decode(encoded_with_whitespace), raw_data)
