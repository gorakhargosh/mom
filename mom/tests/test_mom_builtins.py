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

from __future__ import absolute_import

import unittest2
import math
import struct
from mom._alt_builtins import integer_byte_length_shift_counting, \
    integer_byte_length_word_aligned, integer_bit_length_shift_counting, \
    integer_bit_length_word_aligned
from mom._compat import get_word_alignment, MACHINE_WORD_SIZE, \
    UINT64_MAX, UINT32_MAX, UINT16_MAX, UINT8_MAX, ZERO_BYTE
from mom.security.random import generate_random_bytes
from mom.builtins import \
    is_unicode, \
    is_bytes, \
    is_bytes_or_unicode, \
    bin, \
    hex, \
    integer_byte_length, \
    integer_bit_length, \
    is_sequence,\
    is_odd, \
    is_even, \
    is_negative, \
    is_positive, byte, bytes_leading, bytes_trailing, b, \
    integer_byte_size, integer_bit_count

try:
    unicode
    from mom.tests.constants import unicode_string, unicode_string2, \
        utf8_bytes, utf8_bytes2, latin1_bytes
except NameError:
    from mom.tests.py3kconstants import unicode_string, unicode_string2, \
        utf8_bytes, utf8_bytes2, latin1_bytes

unicode_string = unicode_string
unicode_string2 = unicode_string2
utf8_bytes = utf8_bytes
utf8_bytes2 = utf8_bytes2
latin1_bytes = latin1_bytes

random_bytes = generate_random_bytes(100)

class Test_byte(unittest2.TestCase):
    def test_byte(self):
        for i in range(256):
            byt = byte(i)
            self.assertTrue(is_bytes(byt))
            self.assertEqual(ord(byt), i)

    def test_raises_Error_on_overflow(self):
        self.assertRaises(struct.error, byte, 256)
        self.assertRaises(struct.error, byte, -1)


class Test_bytes_leading_and_trailing(unittest2.TestCase):
    def test_leading(self):
        self.assertEqual(bytes_leading(b('\x00\x00\x00\x00')), 4)
        self.assertEqual(bytes_leading(b('\x00\x00\x00')), 3)
        self.assertEqual(bytes_leading(b('\x00\x00\xff')), 2)
        self.assertEqual(bytes_leading(b('\xff')), 0)
        self.assertEqual(bytes_leading(b('\x00\xff')), 1)
        self.assertEqual(bytes_leading(b('\x00')), 1)
        self.assertEqual(bytes_leading(b('\x00\x00\x00\xff')), 3)
        self.assertEqual(bytes_leading(b('')), 0)

    def test_trailing(self):
        self.assertEqual(bytes_trailing(b('\x00\x00\x00\x00')), 4)
        self.assertEqual(bytes_trailing(b('\x00\x00\x00')), 3)
        self.assertEqual(bytes_trailing(b('\xff\x00\x00')), 2)
        self.assertEqual(bytes_trailing(b('\xff')), 0)
        self.assertEqual(bytes_trailing(b('\x00')), 1)
        self.assertEqual(bytes_trailing(b('\xff\x00\x00\x00')), 3)
        self.assertEqual(bytes_trailing(b('')), 0)

            
class Test_bin(unittest2.TestCase):
    def test_binary_0_1_and_minus_1(self):
        self.assertEqual(bin(0), '0b0')
        self.assertEqual(bin(1), '0b1')
        self.assertEqual(bin(-1), '-0b1')

    def test_binary_value(self):
        self.assertEqual(bin(12), '0b1100')
        self.assertEqual(bin(2**32), '0b100000000000000000000000000000000')

    def test_binary_negative_value(self):
        self.assertEqual(bin(-1200), '-0b10010110000')

    def test_binary_default_prefix(self):
        self.assertEqual(bin(0), '0b0')
        self.assertEqual(bin(1), '0b1')
        self.assertEqual(bin(12), '0b1100')
        self.assertEqual(bin(2**32), '0b100000000000000000000000000000000')
        self.assertEqual(bin(-1200), '-0b10010110000')

    def test_binary_custom_prefix(self):
        self.assertEqual(bin(0, 'B'), 'B0')
        self.assertEqual(bin(1, 'B'), 'B1')
        self.assertEqual(bin(12, 'B'), 'B1100')
        self.assertEqual(bin(2**32, 'B'), 'B100000000000000000000000000000000')
        self.assertEqual(bin(-1200, 'B'), '-B10010110000')

    def test_binary_no_prefix(self):
        self.assertEqual(bin(0, None), '0')
        self.assertEqual(bin(1, ''), '1')
        self.assertEqual(bin(12, None), '1100')
        self.assertEqual(bin(2**32, None), '100000000000000000000000000000000')
        self.assertEqual(bin(-1200, None), '-10010110000')

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, bin, None, None)
        self.assertRaises(TypeError, bin, "error")
        self.assertRaises(TypeError, bin, 2.0)
        self.assertRaises(TypeError, bin, object)

class Test_hex(unittest2.TestCase):
    def test_hex_0_1_and_minus_1(self):
        self.assertEqual(hex(0), '0x0')
        self.assertEqual(hex(1), '0x1')
        self.assertEqual(hex(-1), '-0x1')

    def test_hex_value(self):
        self.assertEqual(hex(12), '0xc')
        self.assertEqual(hex(2**32), '0x100000000')

    def test_hex_negative_value(self):
        self.assertEqual(hex(-1200), '-0x4b0')

    def test_hex_default_prefix(self):
        self.assertEqual(hex(0), '0x0')
        self.assertEqual(hex(1), '0x1')
        self.assertEqual(hex(12), '0xc')
        self.assertEqual(hex(2**32), '0x100000000')

    def test_hex_custom_prefix(self):
        self.assertEqual(hex(0, 'X'), 'X0')
        self.assertEqual(hex(1, 'X'), 'X1')
        self.assertEqual(hex(12, 'X'), 'Xc')
        self.assertEqual(hex(2**32, 'X'), 'X100000000')

    def test_hex_lower_case(self):
        self.assertEqual(hex(12), '0xc')

    def test_hex_no_prefix(self):
        self.assertEqual(hex(0, None), '0')
        self.assertEqual(hex(1, ''), '1')
        self.assertEqual(hex(12, None), 'c')
        self.assertEqual(hex(2**32, None), '100000000')

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, hex, None, None)
        self.assertRaises(TypeError, hex, "error")
        self.assertRaises(TypeError, hex, 2.0)
        self.assertRaises(TypeError, hex, object)


class Test_integer_byte_length(unittest2.TestCase):
    def test_byte_length_zero_if_zero(self):
        self.assertEqual(integer_byte_length(0), 0)
        self.assertEqual(integer_byte_length_shift_counting(0), 0)
        self.assertEqual(integer_byte_length_word_aligned(0), 0)

    def test_byte_length_correctness(self):
        numbers = [-12, 12, 1200, 120091, 123456789]
        for num in numbers:
            if num < 0:
                bit_length = len(bin(num, None)) - 1
            else:
                bit_length = len(bin(num, None))
            count = int(math.ceil(bit_length / 8.0))
            self.assertEqual(integer_byte_length(num), count,
                             "Boom. for number %d, expected %d" % (num, count))
            self.assertEqual(integer_byte_length_shift_counting(num), count)
            self.assertEqual(integer_byte_length_word_aligned(num), count)

        self.assertEqual(integer_byte_length(1 << 1023), 128)
        self.assertEqual(integer_byte_length((1 << 1024) - 1), 128)
        self.assertEqual(integer_byte_length(1 << 1024), 129)

        self.assertEqual(integer_byte_length_shift_counting(1 << 1023), 128)
        self.assertEqual(integer_byte_length_shift_counting((1 << 1024) - 1), 128)
        self.assertEqual(integer_byte_length_shift_counting(1 << 1024), 129)

        self.assertEqual(integer_byte_length_shift_counting(1 << 1023), 128)
        self.assertEqual(integer_byte_length_shift_counting((1 << 1024) - 1), 128)
        self.assertEqual(integer_byte_length_word_aligned(1 << 1024), 129)


    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, integer_byte_length, None)
        self.assertRaises(TypeError, integer_byte_length, object)

        self.assertRaises(TypeError, integer_byte_length_shift_counting, None)
        self.assertRaises(TypeError, integer_byte_length_shift_counting, object)
        self.assertRaises(TypeError, integer_byte_length_word_aligned, object)


class Test_integer_byte_size(unittest2.TestCase):
    def test_1_if_zero(self):
        self.assertEqual(integer_byte_size(0), 1)

    def test_values(self):
        self.assertEqual(integer_byte_size(255), 1)
        self.assertEqual(integer_byte_size(256), 2)
        self.assertEqual(integer_byte_size(0xffff), 2)
        self.assertEqual(integer_byte_size(0xffffff), 3)
        self.assertEqual(integer_byte_size(0xffffffff), 4)
        self.assertEqual(integer_byte_size(0xffffffffff), 5)
        self.assertEqual(integer_byte_size(0xffffffffffff), 6)
        self.assertEqual(integer_byte_size(0xffffffffffffff), 7)
        self.assertEqual(integer_byte_size(0xffffffffffffffff), 8)

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, integer_byte_size, None)
        self.assertRaises(TypeError, integer_byte_size, object)

    def test_byte_size_correctness(self):
        numbers = [-12, 12, 1200, 120091, 123456789]
        for num in numbers:
            if num < 0:
                bit_length = len(bin(num, None)) - 1
            else:
                bit_length = len(bin(num, None))
            count = int(math.ceil(bit_length / 8.0))
            self.assertEqual(integer_byte_size(num), count,
                             "Boom. for number %d, expected %d" % (num, count))

        self.assertEqual(integer_byte_size(1 << 1023), 128)
        self.assertEqual(integer_byte_size((1 << 1024) - 1), 128)
        self.assertEqual(integer_byte_size(1 << 1024), 129)

class Test_integer_bit_count(unittest2.TestCase):
    def test_bit_count(self):
        self.assertEqual(integer_bit_count(0), 0)
        self.assertEqual(integer_bit_count(1), 1)
        self.assertEqual(integer_bit_count(255), 8)
        self.assertEqual(integer_bit_count(2), 1)
        self.assertEqual(integer_bit_count(3), 2)
        self.assertEqual(integer_bit_count(5), 2)
        self.assertEqual(integer_bit_count(1 << 128), 1)
        self.assertEqual(integer_bit_count((1 << 129) - 1), 129)
        self.assertEqual(integer_bit_count(1 << 1024), 1)
        self.assertEqual(integer_bit_count((1 << 1024) - 1), 1024)

    def test_negative_checks_against_abs(self):
        self.assertEqual(integer_bit_count(-1), 1)
        self.assertEqual(integer_bit_count(-255), 8)

    def test_TypeError_when_bad_type(self):
        self.assertRaises(TypeError, integer_bit_count, "")
        self.assertRaises(TypeError, integer_bit_count, {})
        self.assertRaises(TypeError, integer_bit_count, object)
        self.assertRaises(TypeError, integer_bit_count, [])


class Test_integer_bit_length(unittest2.TestCase):
    def test_bit_length_0_if_zero(self):
        self.assertEqual(integer_bit_length(0), 0)
        self.assertEqual(integer_bit_length_shift_counting(0), 0)
        self.assertEqual(integer_bit_length_word_aligned(0), 0)

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
            self.assertEqual(integer_bit_length(num), length)
            self.assertEqual(integer_bit_length_shift_counting(num), length)
            self.assertEqual(integer_bit_length_word_aligned(num), length)

        self.assertEqual(integer_bit_length(1023), 10)
        self.assertEqual(integer_bit_length(1024), 11)
        self.assertEqual(integer_bit_length(1025), 11)
        self.assertEqual(integer_bit_length(1 << 1024), 1025)
        self.assertEqual(integer_bit_length((1 << 1024) + 1), 1025)
        self.assertEqual(integer_bit_length((1 << 1024) - 1), 1024)
        self.assertEqual(integer_bit_length((1<<32)-1), 32)
        self.assertEqual(integer_bit_length((1<<64)-1), 64)

        self.assertEqual(integer_bit_length_shift_counting(1023), 10)
        self.assertEqual(integer_bit_length_shift_counting(1024), 11)
        self.assertEqual(integer_bit_length_shift_counting(1025), 11)
        self.assertEqual(integer_bit_length_shift_counting(1 << 1024), 1025)
        self.assertEqual(integer_bit_length_shift_counting((1 << 1024) + 1), 1025)
        self.assertEqual(integer_bit_length_shift_counting((1 << 1024) - 1), 1024)
        self.assertEqual(integer_bit_length_shift_counting((1<<32)-1), 32)
        self.assertEqual(integer_bit_length_shift_counting((1<<64)-1), 64)

        self.assertEqual(integer_bit_length_word_aligned(1023), 10)
        self.assertEqual(integer_bit_length_word_aligned(1024), 11)
        self.assertEqual(integer_bit_length_word_aligned(1025), 11)
        self.assertEqual(integer_bit_length_word_aligned(1 << 1024), 1025)
        self.assertEqual(integer_bit_length_word_aligned((1 << 1024) + 1), 1025)
        self.assertEqual(integer_bit_length_word_aligned((1 << 1024) - 1), 1024)
        self.assertEqual(integer_bit_length_word_aligned((1<<32)-1), 32)
        self.assertEqual(integer_bit_length_word_aligned((1<<64)-1), 64)

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, integer_bit_length, None)
        self.assertRaises(TypeError, integer_bit_length, object)

        self.assertRaises(TypeError, integer_bit_length_shift_counting, None)
        self.assertRaises(TypeError, integer_bit_length_shift_counting, object)

        self.assertRaises(TypeError, integer_bit_length_word_aligned, None)
        self.assertRaises(TypeError, integer_bit_length_word_aligned, object)


class Test_is_bytes(unittest2.TestCase):
    def test_accepts_bytes(self):
        # Must accept any type of bytes.
        self.assertTrue(is_bytes(random_bytes))
        self.assertTrue(is_bytes(utf8_bytes))
        self.assertTrue(is_bytes(utf8_bytes2))
        self.assertTrue(is_bytes(latin1_bytes))

    def test_rejects_non_bytes(self):
        self.assertFalse(is_bytes(unicode_string))
        self.assertFalse(is_bytes(unicode_string2))
        self.assertFalse(is_bytes(False))
        self.assertFalse(is_bytes(5))
        self.assertFalse(is_bytes(None))
        self.assertFalse(is_bytes([]))
        self.assertFalse(is_bytes(()))
        self.assertFalse(is_bytes([]))
        self.assertFalse(is_bytes(object))


class Test_is_unicode(unittest2.TestCase):

    def test_accepts_unicode(self):
        self.assertTrue(is_unicode(unicode_string))
        self.assertTrue(is_unicode(unicode_string2))

    def test_rejects_non_unicode(self):
        self.assertFalse(is_unicode(random_bytes))
        self.assertFalse(is_unicode(utf8_bytes))
        self.assertFalse(is_unicode(utf8_bytes2))
        self.assertFalse(is_unicode(False))
        self.assertFalse(is_unicode(5))
        self.assertFalse(is_unicode(None))
        self.assertFalse(is_unicode([]))
        self.assertFalse(is_unicode(()))
        self.assertFalse(is_unicode({}))
        self.assertFalse(is_unicode(object))


class Test_is_bytes_or_unicode(unittest2.TestCase):
    def test_accepts_any_string(self):
        self.assertTrue(is_bytes_or_unicode(random_bytes))
        self.assertTrue(is_bytes_or_unicode(utf8_bytes))
        self.assertTrue(is_bytes_or_unicode(utf8_bytes2))
        self.assertTrue(is_bytes_or_unicode(unicode_string))
        self.assertTrue(is_bytes_or_unicode(unicode_string2))

    def test_rejects_non_string(self):
        self.assertFalse(is_bytes_or_unicode(False))
        self.assertFalse(is_bytes_or_unicode(5))
        self.assertFalse(is_bytes_or_unicode(None))
        self.assertFalse(is_bytes_or_unicode([]))
        self.assertFalse(is_bytes_or_unicode(()))
        self.assertFalse(is_bytes_or_unicode({}))
        self.assertFalse(is_bytes_or_unicode(object))


class Test_is_sequence(unittest2.TestCase):
    def test_detects_sequences(self):
        self.assertTrue(is_sequence([1,]))
        self.assertTrue(is_sequence((1,)))
        self.assertTrue(is_sequence(""))
        self.assertTrue(is_sequence({}))
        self.assertTrue(is_sequence(dict()))
        self.assertTrue(is_sequence(set([1, 2])))
        self.assertTrue(is_sequence(frozenset([1, 2])))

    def test_rejects_non_sequences(self):
        self.assertFalse(is_sequence(False))
        self.assertFalse(is_sequence(True))
        self.assertFalse(is_sequence(None))
        self.assertFalse(is_sequence(5))
        self.assertFalse(is_sequence(Test_is_sequence))

class Test_is_even(unittest2.TestCase):
    def test_parity(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(1))
        self.assertTrue(is_even(-2))
        self.assertFalse(is_even(-1))

        self.assertTrue(is_even(0))

    def test_boolean(self):
        # Python 2.x legacy. Ew.
        self.assertFalse(is_even(True))
        self.assertTrue(is_even(False))

    def test_TypeError_when_invalid_type(self):
        self.assertRaises(TypeError, is_even, 2.0)
        self.assertRaises(TypeError, is_even, None)
        self.assertRaises(TypeError, is_even, object)


class Test_is_odd(unittest2.TestCase):
    def test_parity(self):
        self.assertTrue(is_odd(1))
        self.assertFalse(is_odd(2))
        self.assertTrue(is_odd(-1))
        self.assertFalse(is_odd(-2))
        self.assertFalse(is_odd(0))

    def test_boolean(self):
        # Python 2.x legacy. Ew.
        self.assertFalse(is_odd(False))
        self.assertTrue(is_odd(True))

    def test_TypeError_when_invalid_type(self):
        self.assertRaises(TypeError, is_odd, 2.0)
        self.assertRaises(TypeError, is_odd, None)
        self.assertRaises(TypeError, is_odd, object)


class Test_is_positive(unittest2.TestCase):
    def test_positive(self):
        self.assertTrue(is_positive(4))
        self.assertFalse(is_positive(-1))
        self.assertFalse(is_positive(0))

    def test_floats(self):
        self.assertTrue(is_positive(4.2))
        self.assertFalse(is_positive(0.0))
        self.assertFalse(is_positive(-1.4))

    def test_boolean(self):
        self.assertTrue(is_positive(True))
        self.assertFalse(is_positive(False))

    def test_wtf(self):
        self.assertRaises(TypeError, is_positive, None)
        self.assertRaises(TypeError, is_positive, "")
        self.assertRaises(TypeError, is_positive, {})
        self.assertRaises(TypeError, is_positive, object)


class Test_is_negative(unittest2.TestCase):
    def test_negative(self):
        self.assertFalse(is_negative(4))
        self.assertTrue(is_negative(-1))
        self.assertFalse(is_negative(0))

    def test_floats(self):
        self.assertFalse(is_negative(4.2))
        self.assertFalse(is_negative(0.0))
        self.assertTrue(is_negative(-1.4))

    def test_boolean(self):
        self.assertFalse(is_negative(True))
        self.assertFalse(is_negative(False))

    def test_wtf(self):
        self.assertRaises(TypeError, is_negative, None)
        self.assertRaises(TypeError, is_negative, "")
        self.assertRaises(TypeError, is_negative, {})
        self.assertRaises(TypeError, is_negative, object)


class Test_get_machine_alignment(unittest2.TestCase):
    def test_values(self):
        if MACHINE_WORD_SIZE == 32:
            self.assertEqual(get_word_alignment(1 << 64), (32, 4, UINT32_MAX, 'L'))
            self.assertEqual(get_word_alignment(1 << 32), (32, 4, UINT32_MAX, 'L'))
        elif MACHINE_WORD_SIZE == 64:
            self.assertEqual(get_word_alignment(1 << 64), (64, 8, UINT64_MAX, 'Q'))
            self.assertEqual(get_word_alignment(1 << 32), (64, 8, UINT64_MAX, 'Q'))
        else:
            raise NotImplementedError("Do we support other than 32/64-bit?")
        # Anything 32-bit or below:
        values = [
            (1 << 31, (32, 4, UINT32_MAX, 'L')),
            (1 << 16, (32, 4, UINT32_MAX, 'L')),
            (1 << 15, (16, 2, UINT16_MAX, 'H')),
            (1 << 8, (16, 2, UINT16_MAX, 'H')),
            (1 << 7, (8, 1, UINT8_MAX, 'B'))
        ]
        for num, tup  in values:
            self.assertEqual(get_word_alignment(num), tup, "%d, %r" % (num, tup))

if __name__ == "__main__":
    unittest2.main()

