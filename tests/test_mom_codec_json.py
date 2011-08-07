#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.codec.json import encode, decode
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
        # decode accepts both bytes and unicode, but strings it returns
        # are always unicode.
        self.assertEqual(decode(json_foo), ufoo)
        self.assertEqual(decode(json_ufoo), ufoo)

        # Non-ascii bytes are interpreted as utf8
        self.assertEqual(decode(utf8_encode(json_unicode_value)), unicode_value)


class Test_encode(unittest2.TestCase):
    def test_encode(self):
        # json deals with strings, not bytes, but our encoding function should
        # accept bytes as well as long as they are utf8.
        self.assertEqual(decode(encode(unicode_value)), unicode_value)
        self.assertEqual(decode(encode(utf8_encode(unicode_value))),
                         unicode_value)
        self.assertRaises(UnicodeDecodeError, encode, x_byte)

if __name__ == "__main__":
    unittest2.main()
