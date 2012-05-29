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
import math
import struct

from mom import _alt_builtins
from mom import _compat
from mom import builtins
from mom.security import random
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b
byte = builtins.byte
hex = builtins.hex
bin = builtins.bin

RANDOM_BYTES = random.generate_random_bytes(100)


class Test_byte(unittest2.TestCase):
  def test_byte(self):
    for i in range(256):
      byt = byte(i)
      self.assertTrue(builtins.is_bytes(byt))
      self.assertEqual(ord(byt), i)

  def test_raises_Error_on_overflow(self):
    self.assertRaises(struct.error, byte, 256)
    self.assertRaises(struct.error, byte, -1)


class Test_bytes_leading_and_trailing(unittest2.TestCase):
  def test_leading(self):
    self.assertEqual(builtins.bytes_leading(b("\x00\x00\x00\x00")), 4)
    self.assertEqual(builtins.bytes_leading(b("\x00\x00\x00")), 3)
    self.assertEqual(builtins.bytes_leading(b("\x00\x00\xff")), 2)
    self.assertEqual(builtins.bytes_leading(b("\xff")), 0)
    self.assertEqual(builtins.bytes_leading(b("\x00\xff")), 1)
    self.assertEqual(builtins.bytes_leading(b("\x00")), 1)
    self.assertEqual(builtins.bytes_leading(b("\x00\x00\x00\xff")), 3)
    self.assertEqual(builtins.bytes_leading(b("")), 0)

  def test_trailing(self):
    self.assertEqual(builtins.bytes_trailing(b("\x00\x00\x00\x00")), 4)
    self.assertEqual(builtins.bytes_trailing(b("\x00\x00\x00")), 3)
    self.assertEqual(builtins.bytes_trailing(b("\xff\x00\x00")), 2)
    self.assertEqual(builtins.bytes_trailing(b("\xff")), 0)
    self.assertEqual(builtins.bytes_trailing(b("\x00")), 1)
    self.assertEqual(builtins.bytes_trailing(b("\xff\x00\x00\x00")), 3)
    self.assertEqual(builtins.bytes_trailing(b("")), 0)

  def test_TypeError_when_bad_type(self):
    self.assertRaises(TypeError, builtins.bytes_trailing, constants.UNICODE_STRING)
    self.assertRaises(TypeError, builtins.bytes_trailing, 1)
    self.assertRaises(TypeError, builtins.bytes_trailing, None)
    self.assertRaises(TypeError, builtins.bytes_leading, constants.UNICODE_STRING)
    self.assertRaises(TypeError, builtins.bytes_leading, 1)
    self.assertRaises(TypeError, builtins.bytes_leading, None)


class Test_bin(unittest2.TestCase):
  def test_binary_0_1_and_minus_1(self):
    self.assertEqual(bin(0), "0b0")
    self.assertEqual(bin(1), "0b1")
    self.assertEqual(bin(-1), "-0b1")

  def test_binary_value(self):
    self.assertEqual(bin(12), "0b1100")
    self.assertEqual(bin(2 ** 32), "0b100000000000000000000000000000000")

  def test_binary_negative_value(self):
    self.assertEqual(bin(-1200), "-0b10010110000")

  def test_binary_default_prefix(self):
    self.assertEqual(bin(0), "0b0")
    self.assertEqual(bin(1), "0b1")
    self.assertEqual(bin(12), "0b1100")
    self.assertEqual(bin(2 ** 32), "0b100000000000000000000000000000000")
    self.assertEqual(bin(-1200), "-0b10010110000")

  def test_binary_custom_prefix(self):
    self.assertEqual(bin(0, "B"), "B0")
    self.assertEqual(bin(1, "B"), "B1")
    self.assertEqual(bin(12, "B"), "B1100")
    self.assertEqual(bin(2 ** 32, "B"), "B100000000000000000000000000000000")
    self.assertEqual(bin(-1200, "B"), "-B10010110000")

  def test_binary_no_prefix(self):
    self.assertEqual(bin(0, None), "0")
    self.assertEqual(bin(1, ""), "1")
    self.assertEqual(bin(12, None), "1100")
    self.assertEqual(bin(2 ** 32, None), "100000000000000000000000000000000")
    self.assertEqual(bin(-1200, None), "-10010110000")

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, bin, None, None)
    self.assertRaises(TypeError, bin, "error")
    self.assertRaises(TypeError, bin, 2.0)
    self.assertRaises(TypeError, bin, object)


class Test_hex(unittest2.TestCase):
  def test_hex_0_1_and_minus_1(self):
    self.assertEqual(hex(0), "0x0")
    self.assertEqual(hex(1), "0x1")
    self.assertEqual(hex(-1), "-0x1")

  def test_hex_value(self):
    self.assertEqual(hex(12), "0xc")
    self.assertEqual(hex(2 ** 32), "0x100000000")

  def test_hex_negative_value(self):
    self.assertEqual(hex(-1200), "-0x4b0")

  def test_hex_default_prefix(self):
    self.assertEqual(hex(0), "0x0")
    self.assertEqual(hex(1), "0x1")
    self.assertEqual(hex(12), "0xc")
    self.assertEqual(hex(2 ** 32), "0x100000000")

  def test_hex_custom_prefix(self):
    self.assertEqual(hex(0, "X"), "X0")
    self.assertEqual(hex(1, "X"), "X1")
    self.assertEqual(hex(12, "X"), "Xc")
    self.assertEqual(hex(2 ** 32, "X"), "X100000000")

  def test_hex_lower_case(self):
    self.assertEqual(hex(12), "0xc")

  def test_hex_no_prefix(self):
    self.assertEqual(hex(0, None), "0")
    self.assertEqual(hex(1, ""), "1")
    self.assertEqual(hex(12, None), "c")
    self.assertEqual(hex(2 ** 32, None), "100000000")

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, hex, None, None)
    self.assertRaises(TypeError, hex, "error")
    self.assertRaises(TypeError, hex, 2.0)
    self.assertRaises(TypeError, hex, object)


class Test_integer_byte_length(unittest2.TestCase):
  def test_byte_length_zero_if_zero(self):
    self.assertEqual(builtins.integer_byte_length(0), 0)
    self.assertEqual(_alt_builtins.integer_byte_length_shift_counting(0), 0)
    self.assertEqual(_alt_builtins.integer_byte_length_word_aligned(0), 0)

  def test_byte_length_correctness(self):
    numbers = [-12, 12, 1200, 120091, 123456789]
    for num in numbers:
      if num < 0:
        bit_length = len(bin(num, None)) - 1
      else:
        bit_length = len(bin(num, None))
      count = int(math.ceil(bit_length / 8.0))
      self.assertEqual(builtins.integer_byte_length(num), count,
                       "Boom. for number %d, expected %d" % (num, count))
      self.assertEqual(_alt_builtins.integer_byte_length_shift_counting(num), count)
      self.assertEqual(_alt_builtins.integer_byte_length_word_aligned(num), count)

    self.assertEqual(builtins.integer_byte_length(1 << 1023), 128)
    self.assertEqual(builtins.integer_byte_length((1 << 1024) - 1), 128)
    self.assertEqual(builtins.integer_byte_length(1 << 1024), 129)

    self.assertEqual(_alt_builtins.integer_byte_length_shift_counting(1 << 1023), 128)
    self.assertEqual(_alt_builtins.integer_byte_length_shift_counting((1 << 1024) - 1), 128)
    self.assertEqual(_alt_builtins.integer_byte_length_shift_counting(1 << 1024), 129)

    self.assertEqual(_alt_builtins.integer_byte_length_shift_counting(1 << 1023), 128)
    self.assertEqual(_alt_builtins.integer_byte_length_shift_counting((1 << 1024) - 1), 128)
    self.assertEqual(_alt_builtins.integer_byte_length_word_aligned(1 << 1024), 129)


  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, builtins.integer_byte_length, None)
    self.assertRaises(TypeError, builtins.integer_byte_length, object)

    self.assertRaises(TypeError, _alt_builtins.integer_byte_length_shift_counting, None)
    self.assertRaises(TypeError, _alt_builtins.integer_byte_length_shift_counting, object)
    self.assertRaises(TypeError, _alt_builtins.integer_byte_length_word_aligned, object)


class Test_integer_byte_size(unittest2.TestCase):
  def test_1_if_zero(self):
    self.assertEqual(builtins.integer_byte_size(0), 1)

  def test_values(self):
    self.assertEqual(builtins.integer_byte_size(255), 1)
    self.assertEqual(builtins.integer_byte_size(256), 2)
    self.assertEqual(builtins.integer_byte_size(0xffff), 2)
    self.assertEqual(builtins.integer_byte_size(0xffffff), 3)
    self.assertEqual(builtins.integer_byte_size(0xffffffff), 4)
    self.assertEqual(builtins.integer_byte_size(0xffffffffff), 5)
    self.assertEqual(builtins.integer_byte_size(0xffffffffffff), 6)
    self.assertEqual(builtins.integer_byte_size(0xffffffffffffff), 7)
    self.assertEqual(builtins.integer_byte_size(0xffffffffffffffff), 8)

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, builtins.integer_byte_size, None)
    self.assertRaises(TypeError, builtins.integer_byte_size, object)

  def test_byte_size_correctness(self):
    numbers = [-12, 12, 1200, 120091, 123456789]
    for num in numbers:
      if num < 0:
        bit_length = len(bin(num, None)) - 1
      else:
        bit_length = len(bin(num, None))
      count = int(math.ceil(bit_length / 8.0))
      self.assertEqual(builtins.integer_byte_size(num), count,
                       "Boom. for number %d, expected %d" % (num, count))

    self.assertEqual(builtins.integer_byte_size(1 << 1023), 128)
    self.assertEqual(builtins.integer_byte_size((1 << 1024) - 1), 128)
    self.assertEqual(builtins.integer_byte_size(1 << 1024), 129)


class Test_integer_bit_count(unittest2.TestCase):
  def test_bit_count(self):
    self.assertEqual(builtins.integer_bit_count(0), 0)
    self.assertEqual(builtins.integer_bit_count(1), 1)
    self.assertEqual(builtins.integer_bit_count(255), 8)
    self.assertEqual(builtins.integer_bit_count(2), 1)
    self.assertEqual(builtins.integer_bit_count(3), 2)
    self.assertEqual(builtins.integer_bit_count(5), 2)
    self.assertEqual(builtins.integer_bit_count(1 << 128), 1)
    self.assertEqual(builtins.integer_bit_count((1 << 129) - 1), 129)
    self.assertEqual(builtins.integer_bit_count(1 << 1024), 1)
    self.assertEqual(builtins.integer_bit_count((1 << 1024) - 1), 1024)

  def test_negative_checks_against_abs(self):
    self.assertEqual(builtins.integer_bit_count(-1), 1)
    self.assertEqual(builtins.integer_bit_count(-255), 8)

  def test_TypeError_when_bad_type(self):
    self.assertRaises(TypeError, builtins.integer_bit_count, "")
    self.assertRaises(TypeError, builtins.integer_bit_count, {})
    self.assertRaises(TypeError, builtins.integer_bit_count, object)
    self.assertRaises(TypeError, builtins.integer_bit_count, [])


class Test_integer_bit_length(unittest2.TestCase):
  def test_bit_length_0_if_zero(self):
    self.assertEqual(builtins.integer_bit_length(0), 0)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting(0), 0)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned(0), 0)

  def test_bit_length_correct(self):
    numbers = [
      -12,
      12,
      1200,
      120091,
      123456789,
      ]
    for num in numbers:
      if num < 0:
        length = len(bin(num, None)) - 1
      else:
        length = len(bin(num, None))
      self.assertEqual(builtins.integer_bit_length(num), length)
      self.assertEqual(_alt_builtins.integer_bit_length_shift_counting(num), length)
      self.assertEqual(_alt_builtins.integer_bit_length_word_aligned(num), length)

    self.assertEqual(builtins.integer_bit_length(1023), 10)
    self.assertEqual(builtins.integer_bit_length(1024), 11)
    self.assertEqual(builtins.integer_bit_length(1025), 11)
    self.assertEqual(builtins.integer_bit_length(1 << 1024), 1025)
    self.assertEqual(builtins.integer_bit_length((1 << 1024) + 1), 1025)
    self.assertEqual(builtins.integer_bit_length((1 << 1024) - 1), 1024)
    self.assertEqual(builtins.integer_bit_length((1 << 32) - 1), 32)
    self.assertEqual(builtins.integer_bit_length((1 << 64) - 1), 64)

    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting(1023), 10)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting(1024), 11)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting(1025), 11)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting(1 << 1024), 1025)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting((1 << 1024) + 1), 1025)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting((1 << 1024) - 1), 1024)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting((1 << 32) - 1), 32)
    self.assertEqual(_alt_builtins.integer_bit_length_shift_counting((1 << 64) - 1), 64)

    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned(1023), 10)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned(1024), 11)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned(1025), 11)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned(1 << 1024), 1025)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned((1 << 1024) + 1), 1025)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned((1 << 1024) - 1), 1024)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned((1 << 32) - 1), 32)
    self.assertEqual(_alt_builtins.integer_bit_length_word_aligned((1 << 64) - 1), 64)

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, builtins.integer_bit_length, None)
    self.assertRaises(TypeError, builtins.integer_bit_length, object)

    self.assertRaises(TypeError, _alt_builtins.integer_bit_length_shift_counting, None)
    self.assertRaises(TypeError, _alt_builtins.integer_bit_length_shift_counting, object)

    self.assertRaises(TypeError, _alt_builtins.integer_bit_length_word_aligned, None)
    self.assertRaises(TypeError, _alt_builtins.integer_bit_length_word_aligned, object)


class Test_integer_bit_size(unittest2.TestCase):
  def test_bit_size_0_if_zero(self):
    self.assertEqual(builtins.integer_bit_size(0), 1)

  def test_bit_size_correct(self):
    numbers = [
      -12,
      12,
      1200,
      120091,
      123456789,
      ]
    for num in numbers:
      if num < 0:
        size = len(bin(num, None)) - 1
      else:
        size = len(bin(num, None))
      self.assertEqual(builtins.integer_bit_size(num), size)

    self.assertEqual(builtins.integer_bit_size(1023), 10)
    self.assertEqual(builtins.integer_bit_size(1024), 11)
    self.assertEqual(builtins.integer_bit_size(1025), 11)
    self.assertEqual(builtins.integer_bit_size(1 << 1024), 1025)
    self.assertEqual(builtins.integer_bit_size((1 << 1024) + 1), 1025)
    self.assertEqual(builtins.integer_bit_size((1 << 1024) - 1), 1024)
    self.assertEqual(builtins.integer_bit_size((1 << 32) - 1), 32)
    self.assertEqual(builtins.integer_bit_size((1 << 64) - 1), 64)

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, builtins.integer_bit_size, None)
    self.assertRaises(TypeError, builtins.integer_bit_size, object)


class Test_is_bytes(unittest2.TestCase):
  def test_accepts_bytes(self):
    # Must accept any type of bytes.
    self.assertTrue(builtins.is_bytes(RANDOM_BYTES))
    self.assertTrue(builtins.is_bytes(constants.UTF8_BYTES))
    self.assertTrue(builtins.is_bytes(constants.UTF8_BYTES2))
    self.assertTrue(builtins.is_bytes(constants.LATIN1_BYTES))

  def test_rejects_non_bytes(self):
    self.assertFalse(builtins.is_bytes(constants.UNICODE_STRING))
    self.assertFalse(builtins.is_bytes(constants.UNICODE_STRING2))
    self.assertFalse(builtins.is_bytes(False))
    self.assertFalse(builtins.is_bytes(5))
    self.assertFalse(builtins.is_bytes(None))
    self.assertFalse(builtins.is_bytes([]))
    self.assertFalse(builtins.is_bytes(()))
    self.assertFalse(builtins.is_bytes([]))
    self.assertFalse(builtins.is_bytes(object))


class Test_is_unicode(unittest2.TestCase):
  def test_accepts_unicode(self):
    self.assertTrue(builtins.is_unicode(constants.UNICODE_STRING))
    self.assertTrue(builtins.is_unicode(constants.UNICODE_STRING2))

  def test_rejects_non_unicode(self):
    self.assertFalse(builtins.is_unicode(RANDOM_BYTES))
    self.assertFalse(builtins.is_unicode(constants.UTF8_BYTES))
    self.assertFalse(builtins.is_unicode(constants.UTF8_BYTES2))
    self.assertFalse(builtins.is_unicode(False))
    self.assertFalse(builtins.is_unicode(5))
    self.assertFalse(builtins.is_unicode(None))
    self.assertFalse(builtins.is_unicode([]))
    self.assertFalse(builtins.is_unicode(()))
    self.assertFalse(builtins.is_unicode({}))
    self.assertFalse(builtins.is_unicode(object))


class Test_is_bytes_or_unicode(unittest2.TestCase):
  def test_accepts_any_string(self):
    self.assertTrue(builtins.is_bytes_or_unicode(RANDOM_BYTES))
    self.assertTrue(builtins.is_bytes_or_unicode(constants.UTF8_BYTES))
    self.assertTrue(builtins.is_bytes_or_unicode(constants.UTF8_BYTES2))
    self.assertTrue(builtins.is_bytes_or_unicode(constants.UNICODE_STRING))
    self.assertTrue(builtins.is_bytes_or_unicode(constants.UNICODE_STRING2))

  def test_rejects_non_string(self):
    self.assertFalse(builtins.is_bytes_or_unicode(False))
    self.assertFalse(builtins.is_bytes_or_unicode(5))
    self.assertFalse(builtins.is_bytes_or_unicode(None))
    self.assertFalse(builtins.is_bytes_or_unicode([]))
    self.assertFalse(builtins.is_bytes_or_unicode(()))
    self.assertFalse(builtins.is_bytes_or_unicode({}))
    self.assertFalse(builtins.is_bytes_or_unicode(object))


class Test_is_sequence(unittest2.TestCase):
  def test_detects_sequences(self):
    self.assertTrue(builtins.is_sequence([1, ]))
    self.assertTrue(builtins.is_sequence((1,)))
    self.assertTrue(builtins.is_sequence(""))
    self.assertTrue(builtins.is_sequence({}))
    self.assertTrue(builtins.is_sequence(dict()))
    self.assertTrue(builtins.is_sequence(set([1, 2])))
    self.assertTrue(builtins.is_sequence(frozenset([1, 2])))

  def test_rejects_non_sequences(self):
    self.assertFalse(builtins.is_sequence(False))
    self.assertFalse(builtins.is_sequence(True))
    self.assertFalse(builtins.is_sequence(None))
    self.assertFalse(builtins.is_sequence(5))
    self.assertFalse(builtins.is_sequence(Test_is_sequence))


class Test_is_even(unittest2.TestCase):
  def test_parity(self):
    self.assertTrue(builtins.is_even(2))
    self.assertFalse(builtins.is_even(1))
    self.assertTrue(builtins.is_even(-2))
    self.assertFalse(builtins.is_even(-1))

    self.assertTrue(builtins.is_even(0))

  def test_boolean(self):
    # Python 2.x legacy. Ew.
    self.assertFalse(builtins.is_even(True))
    self.assertTrue(builtins.is_even(False))

  def test_TypeError_when_invalid_type(self):
    self.assertRaises(TypeError, builtins.is_even, 2.0)
    self.assertRaises(TypeError, builtins.is_even, None)
    self.assertRaises(TypeError, builtins.is_even, object)


class Test_is_odd(unittest2.TestCase):
  def test_parity(self):
    self.assertTrue(builtins.is_odd(1))
    self.assertFalse(builtins.is_odd(2))
    self.assertTrue(builtins.is_odd(-1))
    self.assertFalse(builtins.is_odd(-2))
    self.assertFalse(builtins.is_odd(0))

  def test_boolean(self):
    # Python 2.x legacy. Ew.
    self.assertFalse(builtins.is_odd(False))
    self.assertTrue(builtins.is_odd(True))

  def test_TypeError_when_invalid_type(self):
    self.assertRaises(TypeError, builtins.is_odd, 2.0)
    self.assertRaises(TypeError, builtins.is_odd, None)
    self.assertRaises(TypeError, builtins.is_odd, object)


class Test_is_positive(unittest2.TestCase):
  def test_positive(self):
    self.assertTrue(builtins.is_positive(4))
    self.assertFalse(builtins.is_positive(-1))
    self.assertFalse(builtins.is_positive(0))

  def test_floats(self):
    self.assertTrue(builtins.is_positive(4.2))
    self.assertFalse(builtins.is_positive(0.0))
    self.assertFalse(builtins.is_positive(-1.4))

  def test_boolean(self):
    self.assertTrue(builtins.is_positive(True))
    self.assertFalse(builtins.is_positive(False))

  def test_wtf(self):
    self.assertRaises(TypeError, builtins.is_positive, None)
    self.assertRaises(TypeError, builtins.is_positive, "")
    self.assertRaises(TypeError, builtins.is_positive, {})
    self.assertRaises(TypeError, builtins.is_positive, object)


class Test_is_negative(unittest2.TestCase):
  def test_negative(self):
    self.assertFalse(builtins.is_negative(4))
    self.assertTrue(builtins.is_negative(-1))
    self.assertFalse(builtins.is_negative(0))

  def test_floats(self):
    self.assertFalse(builtins.is_negative(4.2))
    self.assertFalse(builtins.is_negative(0.0))
    self.assertTrue(builtins.is_negative(-1.4))

  def test_boolean(self):
    self.assertFalse(builtins.is_negative(True))
    self.assertFalse(builtins.is_negative(False))

  def test_wtf(self):
    self.assertRaises(TypeError, builtins.is_negative, None)
    self.assertRaises(TypeError, builtins.is_negative, "")
    self.assertRaises(TypeError, builtins.is_negative, {})
    self.assertRaises(TypeError, builtins.is_negative, object)


class Test_get_machine_alignment(unittest2.TestCase):
  def test_values(self):
    if _compat.MACHINE_WORD_SIZE == 32:
      self.assertEqual(_compat.get_word_alignment(1 << 64), (32, 4, _compat.UINT32_MAX, "L"))
      self.assertEqual(_compat.get_word_alignment(1 << 32), (32, 4, _compat.UINT32_MAX, "L"))
    elif _compat.MACHINE_WORD_SIZE == 64:
      self.assertEqual(_compat.get_word_alignment(1 << 64), (64, 8, _compat.UINT64_MAX, "Q"))
      self.assertEqual(_compat.get_word_alignment(1 << 32), (64, 8, _compat.UINT64_MAX, "Q"))
    else:
      raise NotImplementedError("Do we support other than 32/64-bit?")
      # Anything 32-bit or below:
    values = [
      (1 << 31, (32, 4, _compat.UINT32_MAX, "L")),
      (1 << 16, (32, 4, _compat.UINT32_MAX, "L")),
      (1 << 15, (16, 2, _compat.UINT16_MAX, "H")),
      (1 << 8, (16, 2, _compat.UINT16_MAX, "H")),
      (1 << 7, (8, 1, _compat.UINT8_MAX, "B"))
    ]
    for num, tup in values:
      self.assertEqual(_compat.get_word_alignment(num), tup, "%d, %r" % (num, tup))

if __name__ == "__main__":
  unittest2.main()
