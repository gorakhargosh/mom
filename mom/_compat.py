#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Facebook.
# Copyright (C) 2010 Google Inc.
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

"""
:module: mom._compat
:synopsis: Deals with a lot of cross-version issues.

Should not be used in public code. Use the wrappers in mom.
"""

from __future__ import absolute_import

import os
import sys
from array import array

try:
    INT_MAX = sys.maxsize
except AttributeError:
    INT_MAX = sys.maxint


INT64_MAX = (1 << 63) - 1
INT32_MAX = (1 << 31) - 1
INT16_MAX = (1 << 15) - 1
UINT128_MAX = (1 << 128) - 1    # 340282366920938463463374607431768211455L
UINT64_MAX = 0xffffffffffffffff # ((1 << 64) - 1)
UINT32_MAX = 0xffffffff # ((1 << 32) - 1)
UINT16_MAX = 0xffff # ((1 << 16) - 1)
UINT8_MAX = 0xff


# Determine the word size of the processor.
if INT_MAX == INT64_MAX:
    # 64-bit processor.
    MACHINE_WORD_SIZE = 64
    UINT_MAX = UINT64_MAX
elif INT_MAX == INT32_MAX:
    # 32-bit processor.
    MACHINE_WORD_SIZE = 32
    UINT_MAX = UINT32_MAX
else:
    # Else we just assume 64-bit processor keeping up with modern times.
    MACHINE_WORD_SIZE = 64
    UINT_MAX = UINT64_MAX

try:
    long_type = long
except NameError:
    long_type = int

    
# They fucking removed long too! Should I call them bastards? No? Bastards!
try:
    int_type = long
    integer_types = (int, long)
except NameError:
    int_type = int
    integer_types = (int,)

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
    have_python3 = False
    def byte_ord(c):
        return ord(c)
except NameError:
    # Python3.
    def byte_ord(c):
        return c
    unicode_type = str
    basestring_type = (str, bytes)
    have_python3 = True

# Integral range.
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
if str is unicode_type:
    def byte_literal(s):
        """
        This innocent-looking byte literal faker can be detrimental to
        performance so define these as constants in your code instead.
        Don't call it repeatedly inside tight loops.
        """
        return s.encode('latin1')
else:
    def byte_literal(s):
        """
        This innocent-looking byte literal faker can be detrimental to
        performance so define these as constants in your code instead.
        Don't call it repeatedly inside tight loops.
        """
        return s

# These are used in a large number of places. Do not remove.
# This may not make sense, but remember that our code may be used within
# tight loops, and we do not want user code to slow down because of
# thousands of calls to byte_literal or b. Do it once here.
ZERO_BYTE = byte_literal('\x00')
EMPTY_BYTE = byte_literal('')
EQUAL_BYTE = byte_literal('=')
PLUS_BYTE = byte_literal('+')
HYPHEN_BYTE = byte_literal('-')
FORWARD_SLASH_BYTE = byte_literal('/')
UNDERSCORE_BYTE = byte_literal('_')
DIGIT_ZERO_BYTE = byte_literal('0')


have_little_endian = bool(byte_ord(array("i",[1]).tostring()[0]))

try:
    # Check whether we have reduce as a built-in.
    __reduce_test__ = reduce((lambda num1, num2: num1 + num2), [1, 2, 3, 4])
except NameError:
    # Python 3k
    from functools import reduce
reduce = reduce

try:
    # Python 2.x
    from itertools import imap as map
except ImportError:
    # Python 3.x
    map = map


if getattr(dict, "iteritems", None):
    def dict_each(func, iterable):
        for k, v in iterable.iteritems():
            func(k, v)
else:
    def dict_each(func, iterable):
        for k, v in iterable.items():
            func(k, v)


try:
    next = next
except NameError:
    # Taken from
    # http://stackoverflow.com/questions/1716428/def-next-for-python-pre-2-6-instead-of-object-next-method/1716464#1716464
    class Throw(object):
        pass

    throw = Throw() # easy sentinel hack
    def next(iterator, default=throw):
        """next(iterator[, default])

        Return the next item from the iterator. If default is given
        and the iterator is exhausted, it is returned instead of
        raising StopIteration.
        """
        try:
            iternext = iterator.next.__call__
            # this way an AttributeError while executing next() isn't hidden
            # (2.6 does this too)
        except AttributeError:
            raise TypeError("%s object is not an iterator" \
                            % type(iterator).__name__)
        try:
            return iternext()
        except StopIteration:
            if default is throw:
                raise
            return default

try:
    # Operating system unsigned random.
    os.urandom(1)
    def generate_random_bytes(count):
        """
        Generates a random byte string with ``count`` bytes.

        :param count:
            Number of bytes.
        :returns:
            Random byte string.
        """
        return os.urandom(count)
except AttributeError:
    try:
        __urandom_device__ = open("/dev/urandom", "rb")
        def generate_random_bytes(count):
            """
            Generates a random byte string with ``count`` bytes.

            :param count:
                Number of bytes.
            :returns:
                Random byte string.
            """
            return __urandom_device__.read(count)
    except IOError:
        #Else get Win32 CryptoAPI PRNG
        try:
            import win32prng
            def generate_random_bytes(count):
                """
                Generates a random byte string with ``count`` bytes.

                :param count:
                    Number of bytes.
                :returns:
                    Random byte string.
                """
                random_bytes = win32prng.generate_random_bytes(count)
                assert len(random_bytes) == count
                return random_bytes
        except ImportError:
            # What the fuck?!
            def generate_random_bytes(_):
                """
                WTF.

                :returns:
                    WTF.
                """
                raise NotImplementedError("What the fuck?! No PRNG available.")


def get_word_alignment(num, force_arch=64,
                       _machine_word_size=MACHINE_WORD_SIZE):
    """
    Returns alignment details for the given number based on the platform
    Python is running on.

    :param num:
        Unsigned integral number.
    :param force_arch:
        If you don't want to use 64-bit unsigned chunks, set this to
        anything other than 64. 32-bit chunks will be preferred then.
        Default 64 will be used when on a 64-bit machine.
    :param _machine_word_size:
        (Internal) The machine word size used for alignment.
    :returns:
        4-tuple::

            (word_bits, word_bytes,
             max_uint, packing_format_type)
    """
    if force_arch == 64 and _machine_word_size >= 64 and num > UINT32_MAX:
        # 64-bit unsigned integer.
        return 64, 8, UINT64_MAX, "Q"
    elif num > UINT16_MAX:
        # 32-bit unsigned integer
        return 32, 4, UINT32_MAX, "L"
    elif num > UINT8_MAX:
        # 16-bit unsigned integer.
        return 16, 2, UINT16_MAX, "H"
    else:
        # 8-bit unsigned integer.
        return 8, 1, UINT8_MAX, "B"

    
def get_machine_array_alignment(num):
    if num > UINT16_MAX:
        # 32-bit unsigned integer
        return 32, UINT32_MAX, "L"
    elif num > UINT8_MAX:
        # 16-bit unsigned integer.
        return 16, UINT16_MAX, "H"
    else:
        # 8-bit unsigned integer.
        return 8, UINT8_MAX, "B"

