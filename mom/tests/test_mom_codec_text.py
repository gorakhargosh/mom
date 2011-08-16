#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.builtins import is_bytes, is_unicode, b
from mom.codec.text import utf8_encode_if_unicode, \
    to_unicode_if_bytes, bytes_to_unicode, utf8_encode, \
    utf8_encode_recursive, bytes_to_unicode_recursive, \
    utf8_decode, utf8_decode_if_bytes
from mom.tests.constants import *

class Test_to_utf8_if_unicode(unittest2.TestCase):
    def test_encodes_unicode_strings(self):
        self.assertEqual(utf8_encode_if_unicode(unicode_string), utf8_bytes)
        self.assertTrue(is_bytes(utf8_encode_if_unicode(unicode_string)))

        self.assertEqual(utf8_encode_if_unicode(unicode_string2), utf8_bytes2)
        self.assertTrue(is_bytes(utf8_encode_if_unicode(unicode_string2)))


    def test_does_not_encode_else_to_utf8(self):
        self.assertEqual(utf8_encode_if_unicode(utf8_bytes), utf8_bytes)
        self.assertTrue(is_bytes(utf8_encode_if_unicode(utf8_bytes)))

        self.assertEqual(utf8_encode_if_unicode(utf8_bytes2), utf8_bytes2)
        self.assertTrue(is_bytes(utf8_encode_if_unicode(utf8_bytes2)))

        self.assertEqual(utf8_encode_if_unicode(None), None)
        self.assertEqual(utf8_encode_if_unicode(False), False)
        self.assertEqual(utf8_encode_if_unicode(5), 5)
        self.assertEqual(utf8_encode_if_unicode([]), [])
        self.assertEqual(utf8_encode_if_unicode(()), ())
        self.assertEqual(utf8_encode_if_unicode({}), {})
        self.assertEqual(utf8_encode_if_unicode(object), object)


class Test_to_unicode_if_bytes(unittest2.TestCase):
    def test_encodes_bytes_to_unicode(self):
        self.assertEqual(to_unicode_if_bytes(utf8_bytes), unicode_string)
        self.assertTrue(is_unicode(to_unicode_if_bytes(utf8_bytes)))

        self.assertEqual(to_unicode_if_bytes(utf8_bytes2), unicode_string2)
        self.assertTrue(is_unicode(to_unicode_if_bytes(utf8_bytes2)))

    def test_does_not_encode_else_to_unicode(self):
        self.assertEqual(to_unicode_if_bytes(unicode_string), unicode_string)
        self.assertTrue(is_unicode(to_unicode_if_bytes(unicode_string)))

        self.assertEqual(to_unicode_if_bytes(unicode_string2), unicode_string2)
        self.assertTrue(is_unicode(to_unicode_if_bytes(unicode_string2)))

        self.assertEqual(to_unicode_if_bytes(None), None)
        self.assertEqual(to_unicode_if_bytes(False), False)
        self.assertEqual(to_unicode_if_bytes(5), 5)
        self.assertEqual(to_unicode_if_bytes([]), [])
        self.assertEqual(to_unicode_if_bytes(()), ())
        self.assertEqual(to_unicode_if_bytes({}), {})
        self.assertEqual(to_unicode_if_bytes(object), object)

class Test_utf8_decode_if_bytes(unittest2.TestCase):
    def test_encodes_bytes_to_unicode(self):
        self.assertEqual(utf8_decode_if_bytes(utf8_bytes), unicode_string)
        self.assertTrue(is_unicode(utf8_decode_if_bytes(utf8_bytes)))

        self.assertEqual(utf8_decode_if_bytes(utf8_bytes2), unicode_string2)
        self.assertTrue(is_unicode(utf8_decode_if_bytes(utf8_bytes2)))

    def test_does_not_encode_else_to_unicode(self):
        self.assertEqual(utf8_decode_if_bytes(unicode_string), unicode_string)
        self.assertTrue(is_unicode(utf8_decode_if_bytes(unicode_string)))

        self.assertEqual(utf8_decode_if_bytes(unicode_string2), unicode_string2)
        self.assertTrue(is_unicode(utf8_decode_if_bytes(unicode_string2)))

        self.assertEqual(utf8_decode_if_bytes(None), None)
        self.assertEqual(utf8_decode_if_bytes(False), False)
        self.assertEqual(utf8_decode_if_bytes(5), 5)
        self.assertEqual(utf8_decode_if_bytes([]), [])
        self.assertEqual(utf8_decode_if_bytes(()), ())
        self.assertEqual(utf8_decode_if_bytes({}), {})
        self.assertEqual(utf8_decode_if_bytes(object), object)

class Test_bytes_to_unicode(unittest2.TestCase):
    def test_converts_bytes_to_unicode(self):
        self.assertEqual(bytes_to_unicode(utf8_bytes), unicode_string)
        self.assertTrue(is_unicode(bytes_to_unicode(utf8_bytes)))

        self.assertEqual(bytes_to_unicode(utf8_bytes2), unicode_string2)
        self.assertTrue(is_unicode(bytes_to_unicode(utf8_bytes2)))

    def test_does_not_encode_unicode_and_None_to_unicode(self):
        self.assertEqual(bytes_to_unicode(unicode_string), unicode_string)
        self.assertTrue(is_unicode(bytes_to_unicode(unicode_string)))

        self.assertEqual(bytes_to_unicode(unicode_string2), unicode_string2)
        self.assertTrue(is_unicode(bytes_to_unicode(unicode_string2)))

        self.assertEqual(bytes_to_unicode(None), None)

    def test_raises_TypeError_when_not_string_or_None(self):
        self.assertRaises(TypeError, bytes_to_unicode, 5)
        self.assertRaises(TypeError, bytes_to_unicode, False)
        self.assertRaises(TypeError, bytes_to_unicode, True)
        self.assertRaises(TypeError, bytes_to_unicode, [])
        self.assertRaises(TypeError, bytes_to_unicode, ())
        self.assertRaises(TypeError, bytes_to_unicode, {})
        self.assertRaises(TypeError, bytes_to_unicode, object)

    def test_raises_UnicodeDecodeError_when_latin1_bytes(self):
        self.assertRaises(UnicodeDecodeError, bytes_to_unicode, latin1_bytes)


class Test_utf8_decode(unittest2.TestCase):
    def test_converts_utf8_decode(self):
        self.assertEqual(utf8_decode(utf8_bytes), unicode_string)
        self.assertTrue(is_unicode(utf8_decode(utf8_bytes)))

        self.assertEqual(utf8_decode(utf8_bytes2), unicode_string2)
        self.assertTrue(is_unicode(utf8_decode(utf8_bytes2)))

    def test_does_not_encode_unicode_and_None_to_unicode(self):
        self.assertEqual(utf8_decode(unicode_string), unicode_string)
        self.assertTrue(is_unicode(utf8_decode(unicode_string)))

        self.assertEqual(utf8_decode(unicode_string2), unicode_string2)
        self.assertTrue(is_unicode(utf8_decode(unicode_string2)))

        self.assertEqual(utf8_decode(None), None)

    def test_raises_TypeError_when_not_string_or_None(self):
        self.assertRaises(TypeError, utf8_decode, 5)
        self.assertRaises(TypeError, utf8_decode, False)
        self.assertRaises(TypeError, utf8_decode, True)
        self.assertRaises(TypeError, utf8_decode, [])
        self.assertRaises(TypeError, utf8_decode, ())
        self.assertRaises(TypeError, utf8_decode, {})
        self.assertRaises(TypeError, utf8_decode, object)

    def test_raises_UnicodeDecodeError_when_latin1_bytes(self):
        self.assertRaises(UnicodeDecodeError, utf8_decode, latin1_bytes)


class Test_unicode_to_utf8(unittest2.TestCase):
    def test_encodes_only_unicode_to_utf8(self):
        self.assertEqual(utf8_encode(unicode_string), utf8_bytes)
        self.assertTrue(is_bytes(utf8_encode(unicode_string)))

        self.assertEqual(utf8_encode(unicode_string2), utf8_bytes2)
        self.assertTrue(is_bytes(utf8_encode(unicode_string2)))

    def test_does_not_encode_bytes_or_None_to_utf8(self):
        self.assertEqual(utf8_encode(None), None)
        self.assertEqual(utf8_encode(utf8_bytes), utf8_bytes)
        self.assertTrue(is_bytes(utf8_encode(utf8_bytes)))

        self.assertEqual(utf8_encode(latin1_bytes), latin1_bytes)
        self.assertTrue(is_bytes(utf8_encode(latin1_bytes)))

        self.assertEqual(utf8_encode(utf8_bytes2), utf8_bytes2)
        self.assertTrue(is_bytes(utf8_encode(utf8_bytes2)))

    def test_raises_TypeError_when_not_string_or_None(self):
        self.assertRaises(TypeError, utf8_encode, 5)
        self.assertRaises(TypeError, utf8_encode, False)
        self.assertRaises(TypeError, utf8_encode, True)
        self.assertRaises(TypeError, utf8_encode, [])
        self.assertRaises(TypeError, utf8_encode, ())
        self.assertRaises(TypeError, utf8_encode, {})
        self.assertRaises(TypeError, utf8_encode, object)


class Test_bytes_to_unicode_recursive(unittest2.TestCase):
    def test_converts_all_bytes_to_unicode_recursively(self):
        p = {
            "l": [utf8_bytes2, utf8_bytes],
            "t": (utf8_bytes2, utf8_bytes),
            "d": dict(another=[utf8_bytes, utf8_bytes2]),
            "b": utf8_bytes,
            "n": None,
        }
        e = {
            "l": [unicode_string2, unicode_string],
            "t": (unicode_string2, unicode_string),
            "d": dict(another=[unicode_string, unicode_string2]),
            "b": unicode_string,
            "n": None,
        }
        self.assertDictEqual(bytes_to_unicode_recursive(p), e)


class Test_unicode_to_utf8_recursive(unittest2.TestCase):
    def test_converts_all_unicode_to_utf8_bytes_recursively(self):
        e = {
            b("l"): [utf8_bytes2, utf8_bytes],
            b("t"): (utf8_bytes2, utf8_bytes),
            b("d"): {b('another'): [utf8_bytes, utf8_bytes2]},
            b("b"): utf8_bytes,
            b("n"): None,
        }
        p = {
            "l": [unicode_string2, unicode_string],
            "t": (unicode_string2, unicode_string),
            "d": dict(another=[unicode_string, unicode_string2]),
            "b": unicode_string,
            "n": None,
        }
        self.assertDictEqual(utf8_encode_recursive(p), e)

