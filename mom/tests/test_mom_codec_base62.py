#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2
from mom.builtins import b
from mom.codec import hex_decode, base62_decode, base62_encode
from mom.codec._alt_base import b62decode_naive
from mom.codec.base62 import b62encode, b62decode, ASCII62_BYTES, ALT62_BYTES
from mom.security.random import generate_random_bytes

random_bytes_len_512 = generate_random_bytes(512)

zero_bytes = b('\x00\x00\x00\x00')
one_zero_byte = b('\x00')
raw_data = hex_decode(b('005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64'))
encoded = b('01041W9weGIezvwKmSO0laL8BGx4qp64Q8')
encoded_with_whitespace = b('''
01041W9weGIezvwKmS
O0laL8BGx4qp64Q8
''')

padding_raw = b('''\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
''')

class Test_base62_codec(unittest2.TestCase):
    def test_ensure_charset_length(self):
        self.assertEqual(len(ASCII62_BYTES), 62)
        self.assertEqual(len(ALT62_BYTES), 62)

    def test_codec_identity(self):
        self.assertEqual(
            b62decode(b62encode(random_bytes_len_512)),
            random_bytes_len_512
        )
        self.assertEqual(
            b62decode_naive(b62encode(random_bytes_len_512)),
            random_bytes_len_512
        )
        self.assertEqual(
            base62_decode(base62_encode(random_bytes_len_512)),
            random_bytes_len_512
        )

    def test_encodes_zero_prefixed_padding(self):
        self.assertEqual(b62decode(b62encode(padding_raw)), padding_raw)
        self.assertEqual(b62decode_naive(b62encode(padding_raw)), padding_raw)
        self.assertEqual(base62_decode(base62_encode(padding_raw)), padding_raw)

    def test_zero_bytes(self):
        self.assertEqual(b62encode(zero_bytes), b('0000'))
        self.assertEqual(b62decode(b('0000')), zero_bytes)
        self.assertEqual(b62decode_naive(b('0000')), zero_bytes)
        self.assertEqual(b62encode(one_zero_byte), b('0'))
        self.assertEqual(b62decode(b('0')), one_zero_byte)
        self.assertEqual(b62decode_naive(b('0')), one_zero_byte)

        self.assertEqual(base62_encode(zero_bytes), b('0000'))
        self.assertEqual(base62_decode(b('0000')), zero_bytes)
        self.assertEqual(base62_encode(one_zero_byte), b('0'))
        self.assertEqual(base62_decode(b('0')), one_zero_byte)

    def test_encoding_and_decoding(self):
        self.assertEqual(b62encode(raw_data), encoded)
        self.assertEqual(b62decode(encoded), raw_data)
        self.assertEqual(b62decode(encoded_with_whitespace), raw_data)
        self.assertEqual(b62decode_naive(encoded), raw_data)
        self.assertEqual(b62decode_naive(encoded_with_whitespace), raw_data)

        self.assertEqual(base62_encode(raw_data), encoded)
        self.assertEqual(base62_decode(encoded), raw_data)
        self.assertEqual(base62_decode(encoded_with_whitespace), raw_data)
