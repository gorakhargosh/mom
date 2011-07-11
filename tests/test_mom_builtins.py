#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from unittest2 import TestCase as BaseTestCase

from mom.security.random import generate_random_bytes
from mom.builtins import \
    is_unicode, \
    is_bytes, \
    is_bytes_or_unicode, \
    to_utf8_if_unicode, \
    to_unicode_if_bytes, \
    unicode_to_utf8, \
    bytes_to_unicode


random_bytes = generate_random_bytes(100)
utf8_bytes = '\xc2\xae'
unicode_string = u'\u00ae'


class Test_is_bytes(BaseTestCase):
    def test_accepts_bytes(self):
        self.assertTrue(is_bytes(random_bytes))

    def test_rejects_non_bytes(self):
        self.assertFalse(is_bytes(unicode_string))
        self.assertFalse(is_bytes(False))
        self.assertFalse(is_bytes(5))
        self.assertFalse(is_bytes(None))
        self.assertFalse(is_bytes([]))
        self.assertFalse(is_bytes(()))
        self.assertFalse(is_bytes([]))
        self.assertFalse(is_bytes(object))


class Test_is_unicode(BaseTestCase):

    def test_accepts_unicode(self):
        self.assertTrue(is_unicode(unicode_string))

    def test_rejects_non_unicode(self):
        self.assertFalse(is_unicode(random_bytes))
        self.assertFalse(is_unicode(False))
        self.assertFalse(is_unicode(5))
        self.assertFalse(is_unicode(None))
        self.assertFalse(is_unicode([]))
        self.assertFalse(is_unicode(()))
        self.assertFalse(is_unicode({}))
        self.assertFalse(is_unicode(object))


class Test_is_bytes_or_unicode(BaseTestCase):
    def test_accepts_any_string(self):
        self.assertTrue(is_bytes_or_unicode(random_bytes))
        self.assertTrue(is_bytes_or_unicode(unicode_string))

    def test_rejects_non_string(self):
        self.assertFalse(is_bytes_or_unicode(False))
        self.assertFalse(is_bytes_or_unicode(5))
        self.assertFalse(is_bytes_or_unicode(None))
        self.assertFalse(is_bytes_or_unicode([]))
        self.assertFalse(is_bytes_or_unicode(()))
        self.assertFalse(is_bytes_or_unicode({}))
        self.assertFalse(is_bytes_or_unicode(object))


class Test_to_utf8_if_unicode(BaseTestCase):
    def test_encodes_unicode_strings(self):
        self.assertEqual(to_utf8_if_unicode(unicode_string), utf8_bytes)

    def test_does_not_encode_else_to_utf8(self):
        self.assertEqual(to_utf8_if_unicode(utf8_bytes), utf8_bytes)
        self.assertEqual(to_utf8_if_unicode(None), None)
        self.assertEqual(to_utf8_if_unicode(False), False)
        self.assertEqual(to_utf8_if_unicode(5), 5)
        self.assertEqual(to_utf8_if_unicode([]), [])
        self.assertEqual(to_utf8_if_unicode(()), ())
        self.assertEqual(to_utf8_if_unicode({}), {})
        self.assertEqual(to_utf8_if_unicode(object), object)


class Test_to_unicode_if_bytes(BaseTestCase):
    def test_encodes_bytes_to_unicode(self):
        self.assertEqual(to_unicode_if_bytes(utf8_bytes), unicode_string)

    def test_does_not_encode_else_to_unicode(self):
        self.assertEqual(to_unicode_if_bytes(unicode_string), unicode_string)
        self.assertEqual(to_unicode_if_bytes(None), None)
        self.assertEqual(to_unicode_if_bytes(False), False)
        self.assertEqual(to_unicode_if_bytes(5), 5)
        self.assertEqual(to_unicode_if_bytes([]), [])
        self.assertEqual(to_unicode_if_bytes(()), ())
        self.assertEqual(to_unicode_if_bytes({}), {})
        self.assertEqual(to_unicode_if_bytes(object), object)


class Test_to_unicode(BaseTestCase):
    def test_converts_bytes_to_unicode(self):
        self.assertEqual(bytes_to_unicode(utf8_bytes), unicode_string)

    def test_does_not_encode_unicode_and_None_to_unicode(self):
        self.assertEqual(bytes_to_unicode(unicode_string), unicode_string)
        self.assertEqual(bytes_to_unicode(None), None)

    def test_raises_error_when_not_string_or_None(self):
        self.assertRaises(AssertionError, bytes_to_unicode, 5)
        self.assertRaises(AssertionError, bytes_to_unicode, False)
        self.assertRaises(AssertionError, bytes_to_unicode, True)
        self.assertRaises(AssertionError, bytes_to_unicode, [])
        self.assertRaises(AssertionError, bytes_to_unicode, ())
        self.assertRaises(AssertionError, bytes_to_unicode, {})
        self.assertRaises(AssertionError, bytes_to_unicode, object)

class Test_to_utf8(BaseTestCase):
    def test_encodes_only_unicode_to_utf8(self):
        self.assertEqual(unicode_to_utf8(unicode_string), utf8_bytes)

    def test_does_not_encode_bytes_or_None_to_utf8(self):
        self.assertEqual(unicode_to_utf8(None), None)
        self.assertEqual(unicode_to_utf8(utf8_bytes), utf8_bytes)

    def test_raises_error_when_not_string_or_None(self):
        self.assertRaises(AssertionError, unicode_to_utf8, 5)
        self.assertRaises(AssertionError, unicode_to_utf8, False)
        self.assertRaises(AssertionError, unicode_to_utf8, True)
        self.assertRaises(AssertionError, unicode_to_utf8, [])
        self.assertRaises(AssertionError, unicode_to_utf8, ())
        self.assertRaises(AssertionError, unicode_to_utf8, {})
        self.assertRaises(AssertionError, unicode_to_utf8, object)


if __name__ == "__main__":
    unittest2.main()

