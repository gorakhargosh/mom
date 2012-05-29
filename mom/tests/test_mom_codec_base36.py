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
from mom.codec import base36
from mom.codec import integer
from mom.security import random


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b
ZERO_BYTE = _compat.ZERO_BYTE


RANDOM_BYTES = random.generate_random_bytes(384)
ZERO_BYTES_4 = ZERO_BYTE * 4
RAW_DATA = b("""\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
""")


class Test_base36_codec(unittest2.TestCase):
  def test_ensure_charset_length(self):
    self.assertEqual(len(base36.ASCII36_BYTES), 36)

  def test_codec_identity(self):
    self.assertEqual(base36.b36decode(base36.b36encode(RANDOM_BYTES)), RANDOM_BYTES)
    self.assertEqual(codec.base36_decode(codec.base36_encode(RANDOM_BYTES)),
                     RANDOM_BYTES)

  def test_encodes_zero_prefixed_padding(self):
    self.assertEqual(base36.b36decode(base36.b36encode(RAW_DATA)), RAW_DATA)
    self.assertEqual(codec.base36_decode(codec.base36_encode(RAW_DATA)), RAW_DATA)

  def test_zero_bytes(self):
    self.assertEqual(base36.b36encode(ZERO_BYTES_4), b("0000"))
    self.assertEqual(base36.b36decode(b("0000")), ZERO_BYTES_4)
    self.assertEqual(base36.b36encode(ZERO_BYTE), b("0"))
    self.assertEqual(base36.b36decode(b("0")), ZERO_BYTE)

    self.assertEqual(codec.base36_encode(ZERO_BYTES_4), b("0000"))
    self.assertEqual(codec.base36_decode(b("0000")), ZERO_BYTES_4)
    self.assertEqual(codec.base36_encode(ZERO_BYTE), b("0"))
    self.assertEqual(codec.base36_decode(b("0")), ZERO_BYTE)

  def test_hello_world(self):
    hello_world = b("\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64")
    encoded_hello_world = base36.b36encode(hello_world)
    self.assertEqual(base36.b36decode(encoded_hello_world), hello_world)

  def test_decoder_ignores_whitespace(self):
    hello_world_encoded = b(" \nFUV      RSIVVNF\nRBJW\tAJO\x0b")
    self.assertEqual(base36.b36decode(hello_world_encoded), b("hello world"))

  def test_wikipedia_encoding(self):
    encoding_table = [
      (1, b("1")),
      (10, b("A")),
      (100, b("2S")),
      (1000, b("RS")),
      (10000, b("7PS")),
      (100000, b("255S")),
      (1000000, b("LFLS")),
      (1000000000, b("GJDGXS")),
      (1000000000000, b("CRE66I9S")),
    ]
    for number, encoded in encoding_table:
      raw_bytes = integer.uint_to_bytes(number)
      self.assertEqual(base36.b36encode(raw_bytes), encoded)
      self.assertEqual(base36.b36decode(encoded), raw_bytes)

  def test_wikipedia_decoding(self):
    decoding_table = [
      (b("1"), 1),
      (b("10"), 36),
      (b("100"), 1296),
      (b("1000"), 46656),
      (b("10000"), 1679616),
      (b("100000"), 60466176),
      (b("1000000"), 2176782336),
      (b("10000000"), 78364164096),
      (b("100000000"), 2821109907456),
    ]
    for encoded, number in decoding_table:
      raw_bytes = integer.uint_to_bytes(number)
      self.assertEqual(base36.b36encode(raw_bytes), encoded)
      self.assertEqual(base36.b36decode(encoded), raw_bytes)
