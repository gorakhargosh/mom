#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc.
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

from mom.builtins import b

unicode_string = '\u00ae'
unicode_string2 = '深入 Python'
foo = b('foo')
ufoo = 'foo'
json_foo = b('"foo"')
json_ufoo = '"foo"'
json_unicode_value = '"\u00e9"'
unicode_value = '\u00e9'
x_byte = b("\xe9")
utf8_bytes = b('\xc2\xae')
utf8_bytes2 = b('\xe6\xb7\xb1\xe5\x85\xa5 Python')
latin1_bytes = b("\xe9")
