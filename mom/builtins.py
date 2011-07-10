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
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: mom.builtins
:synopsis: Deals with a lot of cross-version issues.

``bytes``, ``str``, ``unicode``, and ``basestring`` mean different
things to Python 2.5, 2.6, and 3.x.

Use the functions provided instead of the built-in equivalents wherever
possible. Avoid using ``str``—use ``bytes`` or ``unicode`` instead.

Python 2.5
* ``bytes`` is not available.
* ``str`` is a byte string.
* ``unicode`` converts to unicode string.
* ``basestring`` exists.

Python 2.6
* ``bytes`` is available and maps to str
* ``str`` is a byte string.
* ``unicode`` converts to unicode string
* ``basestring`` exists.

Python 3.x
* ``bytes`` is available and does not map to ``str``.
* ``str`` maps to the earlier ``unicode``, but ``unicode`` has been removed.
* ``basestring`` has been removed.
* ``unicode`` has been removed

This module adds portable support for all three versions
of Python. It introduces these portable types that you can use
in your code:

* ``bytes`` where you need byte strings.
* ``unicode`` where you need unicode strings
* a few other utility functions that hide all the
  complications behind type checking therefore cleaning
  up the code base.

Type detection
--------------
.. autofunction:: bytes
.. autofunction:: unicode
.. autofunction:: bin
.. autofunction:: hex
.. autofunction:: str
.. autofunction:: byte_count
.. autofunction:: bit_count
.. autofunction:: is_python3
.. autofunction:: is_sequence
.. autofunction:: is_unicode
.. autofunction:: is_bytes
.. autofunction:: is_bytes_or_unicode
"""

from __future__ import absolute_import

import sys
import math

from mom._builtins import _BytesType, _UnicodeType, _BasestringType


def is_python3():
    """
    Determines whether we're running on Python 3.

    :returns:
        ``True`` if we're using Python 3; ``False`` otherwise.
    """
    return sys.version_info[0] == 3


#def bytes(obj):
#    """
#    Converts an object value to a byte string.
#
#    :param obj:
#        The object.
#    :returns:
#        A byte string representing the object.
#    """
#    return _BytesType(obj)


#def unicode(obj):
#    """
#    Converts a Python object to a unicode string.
#
#    :param obj:
#        The object
#    :returns:
#        Unicode string.
#    """
#    return _UnicodeType(obj)

bytes = _BytesType
unicode = _UnicodeType


def str(_):
    """
    Reminds the developer to use ``bytes()`` or ``unicode()``.
    """
    raise TypeError("Please avoid using ``str()`` in your code. "\
                    "Use ``bytes()`` or ``unicode()`` instead.")


def bin(num, prefix="0b"):
    """
    Converts a long value to its binary representation.

    :param num:
        Long value.
    :param prefix:
        The prefix to use for the bitstring. Default "0b" to mimic Python
        builtin ``bin()``.
    :returns:
        Bit string.
    """
    prefix = prefix or ""
    bit_string = ''
    while num > 1:
        bit_string = bytes(num & 1) + bit_string
        num >>= 1
    bit_string = bytes(num) + bit_string
    return prefix + bit_string


def _bin_lookup(num, prefix="0b"):
    """
    Converts a long value to its binary representation based on a lookup table.

    Alternative implementation of :func:``bin``.

    :param num:
        Long value.
    :param prefix:
        The prefix to use for the bitstring. Default "0b" to mimic Python
        builtin ``bin()``.
    :returns:
        Bit string.
    """
    prefix = prefix or ""
    bit_string = ''
    lookup = {'0':'000','1':'001','2':'010','3':'011',
              '4':'100','5':'101','6':'110','7':'111'}
    for c in oct(num)[1:]:
        bit_string += lookup[c]
    return prefix + bit_string


def _bin_recursive(num, prefix="0b"):
    """
    Converts a long value to its binary representation recursively.

    Alternative implementation of :func:``bin``.

    :param num:
        Long value.
    :param prefix:
        The prefix to use for the bitstring. Default "0b" to mimic Python
        builtin ``bin()``.
    :returns:
        Bit string.
    """
    prefix = prefix or ""
    if num <= 1:
        bitstring = bytes(num)
    else:
        bitstring = _bin_recursive(num >> 1) + bytes(num & 1)
    return prefix + bitstring


def hex(num, prefix="0x"):
    """
    Converts a long value to its hexadecimal representation.

    :param num:
        Long value.
    :param prefix:
        The prefix to use for the hexadecimal string. Default "0x" to mimic
        ``hex()``.
    :returns:
        Hexadecimal string.
    """
    prefix = prefix or ""
    hex_num = "%x" % num
    return prefix + hex_num


def byte_count(num):
    """
    Counts the number of bytes in a long integer.

    :param num:
        Long value.
    :returns:
        The number of bytes in the long integer.
    """
    if not num:
        return 0
    bits = bit_count(num)
    return int(math.ceil(bits / 8.0))


def bit_count(num):
    """
    Counts the number of bits in a long integer.

    :param num:
        Long value.
    :returns:
        Returns the number of bits in the long integer.
    """
    if not num:
        return 0
    hex_num = "%x" % num
    return ((len(hex_num) - 1) * 4) + {
        '0':0, '1':1, '2':2, '3':2,
        '4':3, '5':3, '6':3, '7':3,
        '8':4, '9':4, 'a':4, 'b':4,
        'c':4, 'd':4, 'e':4, 'f':4,
     }[hex_num[0]]
    #return int(math.floor(math.log(n, 2))+1)


def is_sequence(obj):
    """
    Determines whether the given value is a sequence.

    :param obj:
        The value to test.
    :returns:
        ``True`` if the value is a sequence; ``False`` otherwise.
    """
    try:
        list(obj)
        return True
    except TypeError, exception:
        assert "is not iterable" in bytes(exception)
        return False


def is_unicode(obj):
    """
    Determines whether the given value is a Unicode string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if ``value`` is a Unicode string; ``False`` otherwise.
    """
    return isinstance(obj, _UnicodeType)


def is_bytes(obj):
    """
    Determines whether the given value is a byte string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if ``value`` is a byte string; ``False`` otherwise.
    """
    return isinstance(obj, _BytesType)


def is_bytes_or_unicode(obj):
    """
    Determines whether the given value is an instance of a string irrespective
    of whether it is a byte string or a Unicode string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if ``value`` is a string; ``False`` otherwise.
    """
    return isinstance(obj, _BasestringType)


def unicode_to_utf8(obj):
    """
    Converts a string argument to a UTF-8 encoded byte string if it is a
    Unicode string.

    :param obj:
        If already a byte string or None, it is returned unchanged.
        Otherwise it must be a Unicode string and is encoded as UTF-8.
    """
    if obj is None or is_bytes(obj):
        return obj
    assert is_unicode(obj)
    return obj.encode("utf-8")


def bytes_to_unicode(obj, encoding="utf-8"):
    """
    Converts bytes to a Unicode string decoding it according to the encoding
    specified.

    :param obj:
        If already a Unicode string or None, it is returned unchanged.
        Otherwise it must be a byte string.
    :param encoding:
        The encoding used to decode bytes. Defaults to UTF-8
    """
    if obj is None or is_unicode(obj):
        return obj
    assert is_bytes(obj)
    return obj.decode(encoding)


def to_utf8_if_unicode(obj):
    """
    Converts an argument to a UTF-8 encoded byte string if the argument
    is a Unicode string.

    :param obj:
        The value that will be UTF-8 encoded if it is a Unicode string.
    :returns:
        UTF-8 encoded byte string if the argument is a Unicode string; otherwise
        the value is returned unchanged.
    """
    return unicode_to_utf8(obj) if is_unicode(obj) else obj


def to_unicode_if_bytes(obj, encoding="utf-8"):
    """
    Converts an argument to Unicode string if the argument is a byte string
    decoding it as specified by the encoding.

    :param obj:
        The value that will be converted to a Unicode string.
    :param encoding:
        The encoding used to decode bytes. Defaults to UTF-8.
    :returns:
        Unicode string if the argument is a byte string. Otherwise the value
        is returned unchanged.
    """
    return bytes_to_unicode(obj, encoding) if is_bytes(obj) else obj


def to_unicode_recursively(obj):
    """
    Walks a simple data structure, converting byte strings to unicode.

    Supports lists, tuples, and dictionaries.
    """
    if isinstance(obj, dict):
        return dict((to_unicode_recursively(k),
                     to_unicode_recursively(v)) for (k, v) in obj.iteritems())
    elif isinstance(obj, list):
        return list(to_unicode_recursively(i) for i in obj)
    elif isinstance(obj, tuple):
        return tuple(to_unicode_recursively(i) for i in obj)
    elif is_bytes(obj):
        return bytes_to_unicode(obj)
    else:
        return obj
