#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.codec.json import json_encode, json_decode
from mom.codec.text import utf8_encode
try:
    unicode
    from tests.constants import ufoo, json_ufoo, json_foo, \
        json_unicode_value, unicode_value, x_byte
except NameError:
    from tests.py3kconstants import ufoo, json_ufoo, json_foo, \
        json_unicode_value, unicode_value, x_byte


class Test_decode(unittest2.TestCase):
    def test_decode(self):
        # decode accepts unicode only.
        self.assertEqual(json_decode(json_ufoo), ufoo)

    def test_raises_error_when_invalid_type(self):
        self.assertRaises(TypeError, json_decode, json_foo)


class Test_encode(unittest2.TestCase):
    def test_encode(self):
        # json deals with strings, not bytes.
        self.assertEqual(json_decode(json_encode(unicode_value)), unicode_value)

    def test_raises_error_when_invalid_type(self):
        self.assertRaises(TypeError, json_encode, utf8_encode(unicode_value))
        self.assertRaises(TypeError, json_encode, x_byte)

if __name__ == "__main__":
    unittest2.main()
