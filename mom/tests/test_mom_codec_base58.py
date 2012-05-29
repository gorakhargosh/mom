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

from mom import _compat
from mom import builtins
from mom import codec
from mom.codec import _alt_base
from mom.codec import base58
from mom.codec import integer
from mom.security import random
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b
ZERO_BYTE = _compat.ZERO_BYTE


RANDOM_BYTES = random.generate_random_bytes(384)

ZERO_BYTES_4 = ZERO_BYTE * 4
#raw_data = hex_decode(b("005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64"))
RAW_DATA = b("\x00\\\xc8\x7fJ?\xdf\xe3\xa24kiS&|\xa8g(&0\xd3\xf9\xb7\x8ed")
ENCODED = b("19TbMSWwHvnxAKy12iNm3KdbGfzfaMFViT")
ENCODED_WITH_WHITESPACE = b("""
19TbMSWwHvnxAKy12iN
m3KdbGfzfaMFViT
""")

PADDING_RAW = b("""\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
""")

class Test_base58_codec(unittest2.TestCase):
  def test_ensure_charset_length(self):
    self.assertEqual(len(base58.ASCII58_BYTES), 58)
    self.assertEqual(len(base58.ALT58_BYTES), 58)

  def test_codec_identity(self):
    self.assertEqual(base58.b58decode(base58.b58encode(RANDOM_BYTES)), RANDOM_BYTES)
    self.assertEqual(_alt_base.b58decode_naive(base58.b58encode(RANDOM_BYTES)), RANDOM_BYTES)
    self.assertEqual(codec.base58_decode(codec.base58_encode(RANDOM_BYTES)),
                     RANDOM_BYTES)

  def test_encodes_zero_prefixed_padding(self):
    self.assertEqual(base58.b58decode(base58.b58encode(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(_alt_base.b58decode_naive(base58.b58encode(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(codec.base58_decode(codec.base58_encode(PADDING_RAW)), PADDING_RAW)

  def test_zero_bytes(self):
    self.assertEqual(base58.b58encode(ZERO_BYTES_4), b("1111"))
    self.assertEqual(base58.b58decode(b("1111")), ZERO_BYTES_4)
    self.assertEqual(base58.b58encode(ZERO_BYTE), b("1"))
    self.assertEqual(base58.b58decode(b("1")), ZERO_BYTE)

    self.assertEqual(_alt_base.b58encode_naive(ZERO_BYTES_4), b("1111"))
    self.assertEqual(_alt_base.b58decode_naive(b("1111")), ZERO_BYTES_4)
    self.assertEqual(_alt_base.b58encode_naive(ZERO_BYTE), b("1"))
    self.assertEqual(_alt_base.b58decode_naive(b("1")), ZERO_BYTE)

    self.assertEqual(codec.base58_encode(ZERO_BYTES_4), b("1111"))
    self.assertEqual(codec.base58_decode(b("1111")), ZERO_BYTES_4)
    self.assertEqual(codec.base58_encode(ZERO_BYTE), b("1"))
    self.assertEqual(codec.base58_decode(b("1")), ZERO_BYTE)

  # The bitcoin implementation is a broken one. Do not use.
  #    def test_bitcoin_implementation(self):
  #        hello_world = b("\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64")
  #        encoded_hello_world = base58.b58encode(hello_world)
  #
  #        self.assertEqual(bitcointools_base58.b58encode_bitcoin(raw_data), encoded)
  #        self.assertEqual(bitcointools_base58.b58decode_bitcoin(encoded), raw_data)
  #        self.assertEqual(encoded_hello_world, bitcointools_base58.b58encode_bitcoin(hello_world))
  #        self.assertEqual(bitcointools_base58.b58decode_bitcoin(encoded_hello_world), hello_world)
  #
  #    def test_bitcoin_zero_encode(self):
  #        self.assertEqual(bitcointools_base58.b58encode_bitcoin(zero_bytes_4), b("1111"))
  #        self.assertEqual(bitcointools_base58.b58encode_bitcoin(ZERO_BYTE), b("1"))
  #
  #    def test_bitcoin_zero_decode(self):
  #        self.assertEqual(bitcointools_base58.b58decode_bitcoin(b("1111")), zero_bytes_4)
  #        self.assertEqual(bitcointools_base58.b58decode_bitcoin(b("1")), ZERO_BYTE)

  def test_encoding_and_decoding(self):
    hello_world = b("\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64")
    encoded_hello_world = base58.b58encode(hello_world)

    self.assertEqual(encoded_hello_world, _alt_base.b58encode_naive(hello_world))
    self.assertEqual(base58.b58decode(encoded_hello_world), hello_world)

    self.assertEqual(integer.bytes_to_uint(base58.b58decode(b("16Ho7Hs"))), 3471844090)
    self.assertEqual(base58.b58encode(integer.uint_to_bytes(3471844090, 5)), b("16Ho7Hs"))

    self.assertEqual(base58.b58encode(RAW_DATA), ENCODED)
    self.assertEqual(base58.b58decode(ENCODED), RAW_DATA)
    self.assertEqual(base58.b58decode(ENCODED_WITH_WHITESPACE), RAW_DATA)
    self.assertEqual(_alt_base.b58decode_naive(ENCODED), RAW_DATA)
    self.assertEqual(_alt_base.b58decode_naive(ENCODED_WITH_WHITESPACE), RAW_DATA)

    self.assertEqual(codec.base58_encode(RAW_DATA), ENCODED)
    self.assertEqual(codec.base58_decode(ENCODED), RAW_DATA)
    self.assertEqual(codec.base58_decode(ENCODED_WITH_WHITESPACE), RAW_DATA)

  def test_TypeError_when_bad_type(self):
    self.assertRaises(TypeError, base58.b58encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, _alt_base.b58encode_naive, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base58.b58decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, _alt_base.b58decode_naive, constants.UNICODE_STRING)
