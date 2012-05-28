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
from mom.tests import constants
from mom.security import random

from mom import codec
from mom.tests import test_mom_codec_base85


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b

BASE85_RAW = test_mom_codec_base85.RAW
BASE85_ENCODED = test_mom_codec_base85.ENCODED

# Generates a 1024-bit strength random byte string.
RANDOM_BYTES_1024 = random.generate_random_bytes(1024 >> 3)
# Generates a 2048-bit strength random byte string.
RANDOM_BYTES_2048 = random.generate_random_bytes(2048 >> 3)
# Generates a 4093 byte length random byte string.
RANDOM_BYTES_4093 = random.generate_random_bytes(4093)

ZERO_BYTES = b("\x00\x00\x00\x00")
ONE_ZERO_BYTE = b("\x00")

RANDOM_LONG_VALUE = random.generate_random_uint_between(0, 99999999999999999)
ZERO_LONG = 0
NEGATIVE_LONG_VALUE = -1

LONG_VALUE = 71671831749689734735896910666236152091910950933161125188784836897624039426313152092699961904060141667369
EXPECTED_BLOCKSIZE_BYTES = b("""\
\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)""")
LONG_VALUE_BLOCKSIZE = 45
EXPECTED_BYTES = b("""\
\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)""")


# Base64 encoding this sequence of bytes using the standard Base-64 alphabet
# produces a "/", "+", and "=" in the encoded sequence.
URL_SAFETY_TEST_BYTES = b("""\
G\x81Y\x9aK\x9d\xf2\xe9\x81\x06\xc6\xbe6\xa5\x0e\xc0k\x91I\x05\xde\xd8\
\xdc\xd6\xa7\xf2\x9f\t\x8c\xa1\xa6\xf3\x19\xc7\x0b\xfd=z\x02Z\xbeR\xc0\
\xc6~`\xddfzA""")
URL_SAFETY_TEST_STANDARD_ENCODED =\
b("R4FZmkud8umBBsa+NqUOwGuRSQXe2NzWp/KfCYyhpvMZxwv9PXoCWr5SwMZ+YN1mekE=")
URL_SAFETY_TEST_SAFE_ENCODED =\
b("R4FZmkud8umBBsa-NqUOwGuRSQXe2NzWp_KfCYyhpvMZxwv9PXoCWr5SwMZ-YN1mekE")


class Test_base85_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(codec.base85_decode(codec.base85_encode(BASE85_RAW)), BASE85_RAW)

  def test_encoding_and_decoding(self):
    self.assertEqual(codec.base85_encode(BASE85_RAW), BASE85_ENCODED)
    self.assertEqual(codec.base85_decode(BASE85_ENCODED), BASE85_RAW)

  def test_raises_KeyError_when_invalid_charset(self):
    self.assertRaises(ValueError,
                      codec.base85_encode, BASE85_RAW, "BADCHARSET")
    self.assertRaises(ValueError,
                      codec.base85_decode, BASE85_ENCODED, "BADCHARSET")


class Test_base58_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(codec.base58_decode(codec.base58_encode(RANDOM_BYTES_1024)),
                     RANDOM_BYTES_1024)
    self.assertEqual(codec.base58_decode(codec.base58_encode(RANDOM_BYTES_4093)),
                     RANDOM_BYTES_4093)

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, codec.base58_encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.base58_encode, None)
    self.assertRaises(TypeError, codec.base58_decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.base58_decode, None)


class Test_base64_codec(unittest2.TestCase):
  def test_encodes_without_trailing_newline(self):
    self.assertFalse(codec.base64_encode(ZERO_BYTES).endswith(b("\n")))
    self.assertFalse(codec.base64_encode(RANDOM_BYTES_1024).endswith(b("\n")))
    self.assertFalse(codec.base64_encode(RANDOM_BYTES_2048).endswith(b("\n")))
    self.assertFalse(codec.base64_encode(RANDOM_BYTES_4093).endswith(
      b("\n")))

  def test_codec_identity(self):
    # Not zero-destructive.
    self.assertEqual(codec.base64_decode(codec.base64_encode(ZERO_BYTES)), ZERO_BYTES)
    self.assertEqual(codec.base64_decode(codec.base64_encode(RANDOM_BYTES_1024)),
                     RANDOM_BYTES_1024)
    self.assertEqual(codec.base64_decode(codec.base64_encode(RANDOM_BYTES_2048)),
                     RANDOM_BYTES_2048)
    self.assertEqual(codec.base64_decode(codec.base64_encode(RANDOM_BYTES_4093)),
                     RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, codec.base64_encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.base64_encode, None)

    self.assertRaises(TypeError, codec.base64_decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.base64_decode, None)


class Test_base64_urlsafe_codec(unittest2.TestCase):
  def test_encodes_without_trailing_newline(self):
    self.assertFalse(codec.base64_urlsafe_encode(ZERO_BYTES).endswith(b("\n")))
    self.assertFalse(
      codec.base64_urlsafe_encode(RANDOM_BYTES_1024).endswith(b("\n")))

  def test_codec_identity(self):
    # Not zero-destructive.
    self.assertEqual(
      codec.base64_urlsafe_decode(codec.base64_urlsafe_encode(ZERO_BYTES)),
      ZERO_BYTES
    )
    self.assertEqual(
      codec.base64_urlsafe_decode(codec.base64_urlsafe_encode(RANDOM_BYTES_1024)),
      RANDOM_BYTES_1024
    )

  def test_correctness(self):
    self.assertEqual(codec.base64_urlsafe_encode(URL_SAFETY_TEST_BYTES),
                     URL_SAFETY_TEST_SAFE_ENCODED)
    self.assertEqual(codec.base64_encode(URL_SAFETY_TEST_BYTES),
                     URL_SAFETY_TEST_STANDARD_ENCODED)
    self.assertEqual(codec.base64_urlsafe_decode(URL_SAFETY_TEST_SAFE_ENCODED),
                     URL_SAFETY_TEST_BYTES)
    self.assertEqual(codec.base64_decode(URL_SAFETY_TEST_STANDARD_ENCODED),
                     URL_SAFETY_TEST_BYTES)

    # Tests whether this decoder can decode standard encoded base64
    # representation too.
    self.assertEqual(
      codec.base64_urlsafe_decode(URL_SAFETY_TEST_STANDARD_ENCODED),
      URL_SAFETY_TEST_BYTES
    )

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, codec.base64_urlsafe_encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.base64_urlsafe_encode, None)

    self.assertRaises(TypeError, codec.base64_urlsafe_decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.base64_urlsafe_decode, None)


class Test_hex_codec(unittest2.TestCase):
  def test_codec_identity(self):
    # Not zero-destructive
    self.assertEqual(codec.hex_decode(codec.hex_encode(ZERO_BYTES)), ZERO_BYTES)
    self.assertEqual(codec.hex_decode(codec.hex_encode(RANDOM_BYTES_1024)),
                     RANDOM_BYTES_1024)
    self.assertEqual(codec.hex_decode(codec.hex_encode(RANDOM_BYTES_2048)),
                     RANDOM_BYTES_2048)
    self.assertEqual(
      codec.hex_decode(codec.hex_encode(RANDOM_BYTES_4093)),
      RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, codec.hex_encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.hex_encode, None)

    self.assertRaises(TypeError, codec.hex_decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.hex_decode, None)


class Test_decimal_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(
      codec.decimal_decode(codec.decimal_encode(ZERO_BYTES)),
      ZERO_BYTES)
    self.assertEqual(
      codec.decimal_decode(codec.decimal_encode(RANDOM_BYTES_1024)),
      RANDOM_BYTES_1024)
    self.assertEqual(
      codec.decimal_decode(codec.decimal_encode(RANDOM_BYTES_2048)),
      RANDOM_BYTES_2048)
    self.assertEqual(
      codec.decimal_decode(codec.decimal_encode(RANDOM_BYTES_4093)),
      RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, codec.decimal_encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.decimal_encode, None)

    self.assertRaises(TypeError, codec.decimal_decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.decimal_decode, None)


class Test_bin_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(codec.bin_decode(codec.bin_encode(ZERO_BYTES)), ZERO_BYTES)
    self.assertEqual(
      codec.bin_decode(codec.bin_encode(RANDOM_BYTES_1024)), RANDOM_BYTES_1024)
    self.assertEqual(
      codec.bin_decode(codec.bin_encode(RANDOM_BYTES_2048)), RANDOM_BYTES_2048)
    self.assertEqual(
      codec.bin_decode(codec.bin_encode(RANDOM_BYTES_4093)),
      RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, codec.bin_encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.bin_encode, None)

    self.assertRaises(TypeError, codec.bin_decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, codec.bin_decode, None)
