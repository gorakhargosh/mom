#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from mom._compat import have_python3

if have_python3:
    from mom.tests.py3kconstants import \
        unicode_string, unicode_string2, foo, ufoo, \
        json_foo, json_ufoo, json_unicode_value, unicode_value, x_byte, \
        utf8_bytes, utf8_bytes2, latin1_bytes
else:
    from mom.tests.py2kconstants import \
        unicode_string, unicode_string2, foo, ufoo, \
        json_foo, json_ufoo, json_unicode_value, unicode_value, x_byte, \
        utf8_bytes, utf8_bytes2, latin1_bytes

unicode_string = unicode_string
unicode_string2 = unicode_string2
foo = foo
ufoo = ufoo
json_foo = json_foo
json_ufoo = json_ufoo
json_unicode_value = json_unicode_value
unicode_value = unicode_value
x_byte = x_byte
utf8_bytes = utf8_bytes
utf8_bytes2 = utf8_bytes2
latin1_bytes = latin1_bytes
