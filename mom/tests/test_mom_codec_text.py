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
from mom.codec import text
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b


class Test_to_utf8_if_unicode(unittest2.TestCase):
  def test_encodes_unicode_strings(self):
    self.assertEqual(text.utf8_encode_if_unicode(constants.UNICODE_STRING), constants.UTF8_BYTES)
    self.assertTrue(builtins.is_bytes(text.utf8_encode_if_unicode(constants.UNICODE_STRING)))

    self.assertEqual(text.utf8_encode_if_unicode(constants.UNICODE_STRING2), constants.UTF8_BYTES2)
    self.assertTrue(builtins.is_bytes(text.utf8_encode_if_unicode(constants.UNICODE_STRING2)))

  def test_does_not_encode_else_to_utf8(self):
    self.assertEqual(text.utf8_encode_if_unicode(constants.UTF8_BYTES), constants.UTF8_BYTES)
    self.assertTrue(builtins.is_bytes(text.utf8_encode_if_unicode(constants.UTF8_BYTES)))

    self.assertEqual(text.utf8_encode_if_unicode(constants.UTF8_BYTES2), constants.UTF8_BYTES2)
    self.assertTrue(builtins.is_bytes(text.utf8_encode_if_unicode(constants.UTF8_BYTES2)))

    self.assertEqual(text.utf8_encode_if_unicode(None), None)
    self.assertEqual(text.utf8_encode_if_unicode(False), False)
    self.assertEqual(text.utf8_encode_if_unicode(5), 5)
    self.assertEqual(text.utf8_encode_if_unicode([]), [])
    self.assertEqual(text.utf8_encode_if_unicode(()), ())
    self.assertEqual(text.utf8_encode_if_unicode({}), {})
    self.assertEqual(text.utf8_encode_if_unicode(object), object)


class Test_to_unicode_if_bytes(unittest2.TestCase):
  def test_encodes_bytes_to_unicode(self):
    self.assertEqual(text.to_unicode_if_bytes(constants.UTF8_BYTES), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.to_unicode_if_bytes(constants.UTF8_BYTES)))

    self.assertEqual(text.to_unicode_if_bytes(constants.UTF8_BYTES2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.to_unicode_if_bytes(constants.UTF8_BYTES2)))

  def test_does_not_encode_else_to_unicode(self):
    self.assertEqual(text.to_unicode_if_bytes(constants.UNICODE_STRING), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.to_unicode_if_bytes(constants.UNICODE_STRING)))

    self.assertEqual(text.to_unicode_if_bytes(constants.UNICODE_STRING2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.to_unicode_if_bytes(constants.UNICODE_STRING2)))

    self.assertEqual(text.to_unicode_if_bytes(None), None)
    self.assertEqual(text.to_unicode_if_bytes(False), False)
    self.assertEqual(text.to_unicode_if_bytes(5), 5)
    self.assertEqual(text.to_unicode_if_bytes([]), [])
    self.assertEqual(text.to_unicode_if_bytes(()), ())
    self.assertEqual(text.to_unicode_if_bytes({}), {})
    self.assertEqual(text.to_unicode_if_bytes(object), object)


class Test_utf8_decode_if_bytes(unittest2.TestCase):
  def test_encodes_bytes_to_unicode(self):
    self.assertEqual(text.utf8_decode_if_bytes(constants.UTF8_BYTES), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.utf8_decode_if_bytes(constants.UTF8_BYTES)))

    self.assertEqual(text.utf8_decode_if_bytes(constants.UTF8_BYTES2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.utf8_decode_if_bytes(constants.UTF8_BYTES2)))

  def test_does_not_encode_else_to_unicode(self):
    self.assertEqual(text.utf8_decode_if_bytes(constants.UNICODE_STRING), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.utf8_decode_if_bytes(constants.UNICODE_STRING)))

    self.assertEqual(text.utf8_decode_if_bytes(constants.UNICODE_STRING2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.utf8_decode_if_bytes(constants.UNICODE_STRING2)))

    self.assertEqual(text.utf8_decode_if_bytes(None), None)
    self.assertEqual(text.utf8_decode_if_bytes(False), False)
    self.assertEqual(text.utf8_decode_if_bytes(5), 5)
    self.assertEqual(text.utf8_decode_if_bytes([]), [])
    self.assertEqual(text.utf8_decode_if_bytes(()), ())
    self.assertEqual(text.utf8_decode_if_bytes({}), {})
    self.assertEqual(text.utf8_decode_if_bytes(object), object)


class Test_bytes_to_unicode(unittest2.TestCase):
  def test_converts_bytes_to_unicode(self):
    self.assertEqual(text.bytes_to_unicode(constants.UTF8_BYTES), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.bytes_to_unicode(constants.UTF8_BYTES)))

    self.assertEqual(text.bytes_to_unicode(constants.UTF8_BYTES2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.bytes_to_unicode(constants.UTF8_BYTES2)))

  def test_does_not_encode_unicode_and_None_to_unicode(self):
    self.assertEqual(text.bytes_to_unicode(constants.UNICODE_STRING), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.bytes_to_unicode(constants.UNICODE_STRING)))

    self.assertEqual(text.bytes_to_unicode(constants.UNICODE_STRING2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.bytes_to_unicode(constants.UNICODE_STRING2)))

    self.assertEqual(text.bytes_to_unicode(None), None)

  def test_raises_TypeError_when_not_string_or_None(self):
    self.assertRaises(TypeError, text.bytes_to_unicode, 5)
    self.assertRaises(TypeError, text.bytes_to_unicode, False)
    self.assertRaises(TypeError, text.bytes_to_unicode, True)
    self.assertRaises(TypeError, text.bytes_to_unicode, [])
    self.assertRaises(TypeError, text.bytes_to_unicode, ())
    self.assertRaises(TypeError, text.bytes_to_unicode, {})
    self.assertRaises(TypeError, text.bytes_to_unicode, object)

  def test_raises_UnicodeDecodeError_when_latin1_bytes(self):
    self.assertRaises(UnicodeDecodeError, text.bytes_to_unicode, constants.LATIN1_BYTES)


class Test_utf8_decode(unittest2.TestCase):
  def test_converts_utf8_decode(self):
    self.assertEqual(text.utf8_decode(constants.UTF8_BYTES), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.utf8_decode(constants.UTF8_BYTES)))

    self.assertEqual(text.utf8_decode(constants.UTF8_BYTES2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.utf8_decode(constants.UTF8_BYTES2)))

  def test_does_not_encode_unicode_and_None_to_unicode(self):
    self.assertEqual(text.utf8_decode(constants.UNICODE_STRING), constants.UNICODE_STRING)
    self.assertTrue(builtins.is_unicode(text.utf8_decode(constants.UNICODE_STRING)))

    self.assertEqual(text.utf8_decode(constants.UNICODE_STRING2), constants.UNICODE_STRING2)
    self.assertTrue(builtins.is_unicode(text.utf8_decode(constants.UNICODE_STRING2)))

    self.assertEqual(text.utf8_decode(None), None)

  def test_raises_TypeError_when_not_string_or_None(self):
    self.assertRaises(TypeError, text.utf8_decode, 5)
    self.assertRaises(TypeError, text.utf8_decode, False)
    self.assertRaises(TypeError, text.utf8_decode, True)
    self.assertRaises(TypeError, text.utf8_decode, [])
    self.assertRaises(TypeError, text.utf8_decode, ())
    self.assertRaises(TypeError, text.utf8_decode, {})
    self.assertRaises(TypeError, text.utf8_decode, object)

  def test_raises_UnicodeDecodeError_when_latin1_bytes(self):
    self.assertRaises(UnicodeDecodeError, text.utf8_decode, constants.LATIN1_BYTES)


class Test_unicode_to_utf8(unittest2.TestCase):
  def test_encodes_only_unicode_to_utf8(self):
    self.assertEqual(text.utf8_encode(constants.UNICODE_STRING), constants.UTF8_BYTES)
    self.assertTrue(builtins.is_bytes(text.utf8_encode(constants.UNICODE_STRING)))

    self.assertEqual(text.utf8_encode(constants.UNICODE_STRING2), constants.UTF8_BYTES2)
    self.assertTrue(builtins.is_bytes(text.utf8_encode(constants.UNICODE_STRING2)))

  def test_does_not_encode_bytes_or_None_to_utf8(self):
    self.assertEqual(text.utf8_encode(None), None)
    self.assertEqual(text.utf8_encode(constants.UTF8_BYTES), constants.UTF8_BYTES)
    self.assertTrue(builtins.is_bytes(text.utf8_encode(constants.UTF8_BYTES)))

    self.assertEqual(text.utf8_encode(constants.LATIN1_BYTES), constants.LATIN1_BYTES)
    self.assertTrue(builtins.is_bytes(text.utf8_encode(constants.LATIN1_BYTES)))

    self.assertEqual(text.utf8_encode(constants.UTF8_BYTES2), constants.UTF8_BYTES2)
    self.assertTrue(builtins.is_bytes(text.utf8_encode(constants.UTF8_BYTES2)))

  def test_raises_TypeError_when_not_string_or_None(self):
    self.assertRaises(TypeError, text.utf8_encode, 5)
    self.assertRaises(TypeError, text.utf8_encode, False)
    self.assertRaises(TypeError, text.utf8_encode, True)
    self.assertRaises(TypeError, text.utf8_encode, [])
    self.assertRaises(TypeError, text.utf8_encode, ())
    self.assertRaises(TypeError, text.utf8_encode, {})
    self.assertRaises(TypeError, text.utf8_encode, object)


class Test_bytes_to_unicode_recursive(unittest2.TestCase):
  def test_converts_all_bytes_to_unicode_recursively(self):
    p = {
      "l": [constants.UTF8_BYTES2, constants.UTF8_BYTES],
      "t": (constants.UTF8_BYTES2, constants.UTF8_BYTES),
      "d": dict(another=[constants.UTF8_BYTES, constants.UTF8_BYTES2]),
      "b": constants.UTF8_BYTES,
      "n": None,
      }
    e = {
      "l": [constants.UNICODE_STRING2, constants.UNICODE_STRING],
      "t": (constants.UNICODE_STRING2, constants.UNICODE_STRING),
      "d": dict(another=[constants.UNICODE_STRING, constants.UNICODE_STRING2]),
      "b": constants.UNICODE_STRING,
      "n": None,
      }
    self.assertDictEqual(text.bytes_to_unicode_recursive(p), e)


class Test_unicode_to_utf8_recursive(unittest2.TestCase):
  def test_converts_all_unicode_to_utf8_bytes_recursively(self):
    e = {
      b("l"): [constants.UTF8_BYTES2, constants.UTF8_BYTES],
      b("t"): (constants.UTF8_BYTES2, constants.UTF8_BYTES),
      b("d"): {b("another"): [constants.UTF8_BYTES, constants.UTF8_BYTES2]},
      b("b"): constants.UTF8_BYTES,
      b("n"): None,
      }
    p = {
      "l": [constants.UNICODE_STRING2, constants.UNICODE_STRING],
      "t": (constants.UNICODE_STRING2, constants.UNICODE_STRING),
      "d": dict(another=[constants.UNICODE_STRING, constants.UNICODE_STRING2]),
      "b": constants.UNICODE_STRING,
      "n": None,
      }
    self.assertDictEqual(text.utf8_encode_recursive(p), e)
