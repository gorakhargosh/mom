#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc.
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

from __future__ import absolute_import

import unittest2
from mom.builtins import b
from mom.codec import hex_decode, base62_decode, base62_encode
from mom.codec._alt_base import b62decode_naive, b62encode_naive
from mom.codec.base62 import b62encode, b62decode, ASCII62_BYTES, ALT62_BYTES
from mom.security.random import generate_random_bytes
from mom.tests.constants import UNICODE_STRING

RANDOM_BYTES_LEN_512 = generate_random_bytes(512)

ZERO_BYTES = b('\x00\x00\x00\x00')
ONE_ZERO_BYTE = b('\x00')
RAW_DATA = hex_decode(b('005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64'))
ENCODED = b('01041W9weGIezvwKmSO0laL8BGx4qp64Q8')
ENCODED_WITH_WHITESPACE = b('''
01041W9weGIezvwKmS
O0laL8BGx4qp64Q8
''')

PADDING_RAW = b('''\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
''')

class Test_base62_codec(unittest2.TestCase):
  def test_ensure_charset_length(self):
    self.assertEqual(len(ASCII62_BYTES), 62)
    self.assertEqual(len(ALT62_BYTES), 62)

  def test_codec_identity(self):
    self.assertEqual(
      b62decode(b62encode(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      b62decode_naive(b62encode(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      b62decode(b62encode_naive(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      b62decode_naive(b62encode_naive(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      base62_decode(base62_encode(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )

  def test_encodes_zero_prefixed_padding(self):
    self.assertEqual(b62decode(b62encode(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(b62decode_naive(b62encode(PADDING_RAW)), PADDING_RAW)

    self.assertEqual(b62decode(b62encode_naive(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(b62decode_naive(b62encode_naive(PADDING_RAW)), PADDING_RAW)

    self.assertEqual(base62_decode(base62_encode(PADDING_RAW)), PADDING_RAW)

  def test_zero_bytes(self):
    self.assertEqual(b62encode(ZERO_BYTES), b('0000'))
    self.assertEqual(b62encode_naive(ZERO_BYTES), b('0000'))
    self.assertEqual(b62decode(b('0000')), ZERO_BYTES)
    self.assertEqual(b62decode_naive(b('0000')), ZERO_BYTES)
    self.assertEqual(b62encode(ONE_ZERO_BYTE), b('0'))
    self.assertEqual(b62encode_naive(ONE_ZERO_BYTE), b('0'))
    self.assertEqual(b62decode(b('0')), ONE_ZERO_BYTE)
    self.assertEqual(b62decode_naive(b('0')), ONE_ZERO_BYTE)

    self.assertEqual(base62_encode(ZERO_BYTES), b('0000'))
    self.assertEqual(base62_decode(b('0000')), ZERO_BYTES)
    self.assertEqual(base62_encode(ONE_ZERO_BYTE), b('0'))
    self.assertEqual(base62_decode(b('0')), ONE_ZERO_BYTE)

  def test_encoding_and_decoding(self):
    self.assertEqual(b62encode(RAW_DATA), ENCODED)
    self.assertEqual(b62encode_naive(RAW_DATA), ENCODED)
    self.assertEqual(b62decode(ENCODED), RAW_DATA)
    self.assertEqual(b62decode(ENCODED_WITH_WHITESPACE), RAW_DATA)
    self.assertEqual(b62decode_naive(ENCODED), RAW_DATA)
    self.assertEqual(b62decode_naive(ENCODED_WITH_WHITESPACE), RAW_DATA)

    self.assertEqual(base62_encode(RAW_DATA), ENCODED)
    self.assertEqual(base62_decode(ENCODED), RAW_DATA)
    self.assertEqual(base62_decode(ENCODED_WITH_WHITESPACE), RAW_DATA)

  def test_TypeError_when_bad_type(self):
    self.assertRaises(TypeError, b62encode, UNICODE_STRING)
    self.assertRaises(TypeError, b62encode_naive, UNICODE_STRING)
    self.assertRaises(TypeError, b62decode, UNICODE_STRING)
    self.assertRaises(TypeError, b62decode_naive, UNICODE_STRING)

