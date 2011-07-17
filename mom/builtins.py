#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.builtins
:synopsis: Deals with a lot of cross-version issues.


``bytes``, ``str``, ``unicode``, and ``basestring`` mean different
things to Python 2.5, 2.6, and 3.x.

These are the original meanings of the types.

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

This module introduces the 'bytes' type for Python 2.5 and adds a
few utility functions that will continue to keep working as they should
even when Python versions change.

Rules to follow:
* Use ``bytes`` where you want byte strings (binary data).
* Use ``unicode`` where you want Unicode strings (unencoded text).

The meanings of these types have been changed to suit Python 3.

Encodings
---------
.. autofunction:: bin
.. autofunction:: hex

Size counting
-------------
.. autofunction:: long_bit_length
.. autofunction:: long_byte_count

Type detection
--------------
.. autofunction:: is_bytes
.. autofunction:: is_bytes_or_unicode
.. autofunction:: is_integer
.. autofunction:: is_sequence
.. autofunction:: is_unicode

Unicode string encoding
-----------------------
.. autofunction:: bytes_to_unicode
.. autofunction:: bytes_to_unicode_recursive
.. autofunction:: to_unicode_if_bytes
.. autofunction:: to_utf8_if_unicode
.. autofunction:: unicode_to_utf8
.. autofunction:: unicode_to_utf8_recursive
"""

from __future__ import absolute_import

__license__ = """\
The Apache Licence, Version 2.0

Copyright (C) 2005 Trevor Perrin <trevp@trevp.net>
Copyright (C) 2009 Facebook.
Copyright (C) 2010 Google Inc.
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
    "Trevor Perrin",
    "Yesudeep Mangalapilly",
])

__all__ = [
    "bytes",
    "bin",
    "hex",
    "long_byte_count",
    "long_bit_length",
    "is_sequence",
    "is_unicode",
    "is_bytes",
    "is_bytes_or_unicode",
    "is_integer",
    "unicode_to_utf8",
    "bytes_to_unicode",
    "to_utf8_if_unicode",
    "to_unicode_if_bytes",
    "bytes_to_unicode_recursive",
]

from mom._builtins import \
    byte_literal, bytes_type, unicode_type, basestring_type

try:
    # Check whether we have reduce as a built-in.
    __reduce_test__ = reduce((lambda num1, num2: num1 + num2), [1, 2, 3, 4])
except NameError:
    # Python 3k
    from functools import reduce
reduce = reduce


# Types and their meanings:
#
# * ``bytes`` = bytes (binary data or a sequence of bytes).
# * ``unicode`` = Unicode string or text (for backward compatibility,
#    2to3 converts these).

bytes = bytes_type

# We don't really need to define this type.
# 2to3 will automatically convert it to Python 3-``str`` anyway.
# unicode = unicode_type

# Don't do this. This will break the 2to3 tool.
# Avoid using str. Use ``bytes`` or ``unicode``. ``bytes`` will
# prevail the transition and ``unicode`` can be translated automatically
# by the 2to3 tool. ``str`` is a mind-mess.
# str = unicode_type

# Fake byte literal support.
b = byte_literal


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
    if num is None:
        raise TypeError("'%r' object cannot be interpreted as an index" \
                        % type(num).__name__)
    prefix = prefix or ""
    if num < 0:
        num = -num
        prefix = "-" + prefix
    bit_string = ''
    while num > 1:
        bit_string = bytes(num & 1) + bit_string
        num >>= 1
    bit_string = bytes(num) + bit_string
    return prefix + bit_string


#def _bin_lookup(num, prefix="0b"):
#    """
#    Converts a long value to its binary representation based on a lookup table.
#
#    Alternative implementation of :func:``bin``.
#
#    :param num:
#        Long value.
#    :param prefix:
#        The prefix to use for the bitstring. Default "0b" to mimic Python
#        builtin ``bin()``.
#    :returns:
#        Bit string.
#    """
#    prefix = prefix or ""
#    bit_string = ''
#    lookup = {'0':'000', '1':'001', '2':'010', '3':'011',
#              '4':'100', '5':'101', '6':'110', '7':'111'}
#    for c in oct(num)[1:]:
#        bit_string += lookup[c]
#    return prefix + bit_string
#
#
#def _bin_recursive(num, prefix="0b"):
#    """
#    Converts a long value to its binary representation recursively.
#
#    Alternative implementation of :func:``bin``.
#
#    :param num:
#        Long value.
#    :param prefix:
#        The prefix to use for the bitstring. Default "0b" to mimic Python
#        builtin ``bin()``.
#    :returns:
#        Bit string.
#    """
#    prefix = prefix or ""
#    if num <= 1:
#        bitstring = bytes(num)
#    else:
#        bitstring = _bin_recursive(num >> 1) + bytes(num & 1)
#    return prefix + bitstring


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
    if num is None:
        raise TypeError("'%r' object cannot be interpreted as an index" \
                        % type(num).__name__)
    prefix = prefix or ""
    if num < 0:
        num = -num
        prefix = "-" + prefix

    # To ensure TypeError is raised when non integer is passed.
    x = num & 1

    hex_num = "%x" % num
    return prefix + hex_num.lower()


def is_sequence(obj):
    """
    Determines whether the given value is a sequence.

    Sets, lists, tuples, bytes, dicts, and strings are treated as sequence.

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
    return isinstance(obj, unicode_type)


def is_bytes(obj):
    """
    Determines whether the given value is a byte string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if ``value`` is a byte string; ``False`` otherwise.
    """
    return isinstance(obj, bytes_type)


def is_bytes_or_unicode(obj):
    """
    Determines whether the given value is an instance of a string irrespective
    of whether it is a byte string or a Unicode string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if ``value`` is a string; ``False`` otherwise.
    """
    return isinstance(obj, basestring_type)


def is_integer(obj):
    """
    Determines whether the object value is actually an integer and not a bool.

    :param obj:
        The value to test.
    :returns:
        ``True`` if yes; ``False`` otherwise.
    """
    return isinstance(obj, (int, long)) and not isinstance(obj, bool)


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


def bytes_to_unicode_recursive(obj, encoding="utf-8"):
    """
    Walks a simple data structure, converting byte strings to unicode.

    Supports lists, tuples, and dictionaries.

    :param obj:
        The Python data structure to walk recursively looking for
        byte strings.
    :param encoding:
        The encoding to use when decoding the byte string into Unicode.
        Default UTF-8.
    :returns:
        obj with all the byte strings converted to Unicode strings.
    """
    if isinstance(obj, dict):
        return dict((bytes_to_unicode_recursive(k),
                     bytes_to_unicode_recursive(v)) for (k, v) in obj.items())
    elif isinstance(obj, list):
        return list(bytes_to_unicode_recursive(i) for i in obj)
    elif isinstance(obj, tuple):
        return tuple(bytes_to_unicode_recursive(i) for i in obj)
    elif is_bytes(obj):
        return bytes_to_unicode(obj, encoding=encoding)
    else:
        return obj


def unicode_to_utf8_recursive(obj):
    """
    Walks a simple data structure, converting Unicode strings to UTF-8 encoded
    byte strings.

    Supports lists, tuples, and dictionaries.

    :param obj:
        The Python data structure to walk recursively looking for
        Unicode strings.
    :returns:
        obj with all the Unicode strings converted to byte strings.
    """
    if isinstance(obj, dict):
        return dict((unicode_to_utf8_recursive(k),
                     unicode_to_utf8_recursive(v)) for (k, v) in obj.items())
    elif isinstance(obj, list):
        return list(unicode_to_utf8_recursive(i) for i in obj)
    elif isinstance(obj, tuple):
        return tuple(unicode_to_utf8_recursive(i) for i in obj)
    elif is_unicode(obj):
        return unicode_to_utf8(obj)
    else:
        return obj


def long_byte_count(num):
    """
    Number of bytes needed to represent a long integer.

    :param num:
        Long value. If num is 0, then :func:`long_byte_count` returns 0.
    :returns:
        The number of bytes in the long integer.
    """
    import math

    if num == 0:
        return 0
    bits = long_bit_length(num)
    return int(math.ceil(bits / 8.0))


#if getattr(long, 'bit_length'):
#    # Use the python 2.7+ or 3.1+ built-in if available.
#    def long_bit_length(num):
#        return num.bit_length()
#else:
def long_bit_length(num):
    """
    Number of bits needed to represent a long integer excluding any prefix
    0 bits.

    :param num:
        Long value. If num is 0, then :func:`long_bit_length` returns 0.
    :returns:
        Returns the number of bits in the long integer.
    """
    bits = 0
    if num < 0:
        num = -num
    while num >> bits:
        bits += 1
    return bits


def _long_bit_length(num):
    """
    Number of bits needed to represent a long integer excluding any prefix
    0 bits.

    :param num:
        Long value. If num is 0, then :func:`long_bit_length` returns 0.
    :returns:
        Returns the number of bits in the long integer.
    """
    # import math
    if num is None:
        raise TypeError("'%r' object cannot be interpreted as an index" \
                        % type(num).__name__)
    if num == 0:
        return 0
    if num < 0:
        num = -num
    hex_num = hex(num, None)
    return ((len(hex_num) - 1) * 4) + {
        '0':0, '1':1, '2':2, '3':2,
        '4':3, '5':3, '6':3, '7':3,
        '8':4, '9':4, 'a':4, 'b':4,
        'c':4, 'd':4, 'e':4, 'f':4,
     }[hex_num[0]]
    #return int(math.floor(math.log(n, 2))+1)
