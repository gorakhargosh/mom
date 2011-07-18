#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom._builtins
:synopsis: Deals with a lot of cross-version issues.

Should not be used in public code. Use the wrappers in mom.
"""

from __future__ import absolute_import

__license__ = """\
The Apache Licence, Version 2.0

Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__ = ", ".join([
    "Yesudeep Mangalapilly",
])


try:
    # Python 2.6 or higher.
    bytes_type = bytes
except NameError:
    # Python 2.5
    bytes_type = str

try:
    # Not Python3
    unicode_type = unicode
    basestring_type = basestring
except NameError:
    # Python3.
    unicode_type = str
    basestring_type = (str, bytes)

try:
    # Python 2.5+
    xrange(0)
    range = xrange
except NameError:
    range = range

# Fake byte literal support:  In python 2.6+, you can say b"foo" to get
# a byte literal (str in 2.x, bytes in 3.x).  There's no way to do this
# in a way that supports 2.5, though, so we need a function wrapper
# to convert our string literals.  b() should only be applied to literal
# latin1 strings.  Once we drop support for 2.5, we can remove this function
# and just use byte literals.
if str is unicode:
    def byte_literal(s):
        return s.encode('latin1')
else:
    def byte_literal(s):
        return s

try:
    # Check whether we have reduce as a built-in.
    __reduce_test__ = reduce((lambda num1, num2: num1 + num2), [1, 2, 3, 4])
except NameError:
    # Python 3k
    from functools import reduce
reduce = reduce



if getattr(dict, "iteritems", None):
    def dict_each(func, iterable):
        for k, v in iterable.iteritems():
            func(k, v)
else:
    def dict_each(func, iterable):
        for k, v in iterable.items():
            func(k, v)
