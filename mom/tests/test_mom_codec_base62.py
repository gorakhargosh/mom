#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google Inc. All Rights Reserved.
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

from mom import builtins
from mom import codec
from mom.codec import _alt_base
from mom.codec import base62
from mom.security import random
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b

RANDOM_BYTES_LEN_512 = random.generate_random_bytes(512)

ZERO_BYTES = b("\x00\x00\x00\x00")
ONE_ZERO_BYTE = b("\x00")
RAW_DATA = codec.hex_decode(b("005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64"))
ENCODED = b("01041W9weGIezvwKmSO0laL8BGx4qp64Q8")
ENCODED_WITH_WHITESPACE = b("""
01041W9weGIezvwKmS
O0laL8BGx4qp64Q8
""")

PADDING_RAW = b("""\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
""")

class Test_base62_codec(unittest2.TestCase):
  def test_ensure_charset_length(self):
    self.assertEqual(len(base62.ASCII62_BYTES), 62)
    self.assertEqual(len(base62.ALT62_BYTES), 62)

  def test_codec_identity(self):
    self.assertEqual(
      base62.b62decode(base62.b62encode(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      _alt_base.b62decode_naive(base62.b62encode(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      base62.b62decode(_alt_base.b62encode_naive(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      _alt_base.b62decode_naive(_alt_base.b62encode_naive(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )
    self.assertEqual(
      codec.base62_decode(codec.base62_encode(RANDOM_BYTES_LEN_512)),
      RANDOM_BYTES_LEN_512
    )

  def test_encodes_zero_prefixed_padding(self):
    self.assertEqual(base62.b62decode(base62.b62encode(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(_alt_base.b62decode_naive(base62.b62encode(PADDING_RAW)), PADDING_RAW)

    self.assertEqual(base62.b62decode(_alt_base.b62encode_naive(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(_alt_base.b62decode_naive(_alt_base.b62encode_naive(PADDING_RAW)), PADDING_RAW)

    self.assertEqual(codec.base62_decode(codec.base62_encode(PADDING_RAW)), PADDING_RAW)

  def test_zero_bytes(self):
    self.assertEqual(base62.b62encode(ZERO_BYTES), b("0000"))
    self.assertEqual(_alt_base.b62encode_naive(ZERO_BYTES), b("0000"))
    self.assertEqual(base62.b62decode(b("0000")), ZERO_BYTES)
    self.assertEqual(_alt_base.b62decode_naive(b("0000")), ZERO_BYTES)
    self.assertEqual(base62.b62encode(ONE_ZERO_BYTE), b("0"))
    self.assertEqual(_alt_base.b62encode_naive(ONE_ZERO_BYTE), b("0"))
    self.assertEqual(base62.b62decode(b("0")), ONE_ZERO_BYTE)
    self.assertEqual(_alt_base.b62decode_naive(b("0")), ONE_ZERO_BYTE)

    self.assertEqual(codec.base62_encode(ZERO_BYTES), b("0000"))
    self.assertEqual(codec.base62_decode(b("0000")), ZERO_BYTES)
    self.assertEqual(codec.base62_encode(ONE_ZERO_BYTE), b("0"))
    self.assertEqual(codec.base62_decode(b("0")), ONE_ZERO_BYTE)

  def test_encoding_and_decoding(self):
    self.assertEqual(base62.b62encode(RAW_DATA), ENCODED)
    self.assertEqual(_alt_base.b62encode_naive(RAW_DATA), ENCODED)
    self.assertEqual(base62.b62decode(ENCODED), RAW_DATA)
    self.assertEqual(base62.b62decode(ENCODED_WITH_WHITESPACE), RAW_DATA)
    self.assertEqual(_alt_base.b62decode_naive(ENCODED), RAW_DATA)
    self.assertEqual(_alt_base.b62decode_naive(ENCODED_WITH_WHITESPACE), RAW_DATA)

    self.assertEqual(codec.base62_encode(RAW_DATA), ENCODED)
    self.assertEqual(codec.base62_decode(ENCODED), RAW_DATA)
    self.assertEqual(codec.base62_decode(ENCODED_WITH_WHITESPACE), RAW_DATA)

  def test_TypeError_when_bad_type(self):
    self.assertRaises(TypeError, base62.b62encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, _alt_base.b62encode_naive, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base62.b62decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, _alt_base.b62decode_naive, constants.UNICODE_STRING)
