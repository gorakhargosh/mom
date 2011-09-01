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

from mom._compat import HAVE_PYTHON3

if HAVE_PYTHON3:
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
