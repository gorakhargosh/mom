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
.. autofunction:: byte

Size counting
-------------
.. autofunction:: integer_bit_length
.. autofunction:: integer_byte_length

Type detection predicates
-------------------------
.. autofunction:: is_bytes
.. autofunction:: is_bytes_or_unicode
.. autofunction:: is_integer
.. autofunction:: is_sequence
.. autofunction:: is_unicode

Number predicates
-----------------
People screw these up too. Useful in functional programming.

.. autofunction:: is_even
.. autofunction:: is_negative
.. autofunction:: is_odd
.. autofunction:: is_positive

"""

from __future__ import absolute_import

try:
    # Use Psyco (if available) because it cuts execution time into almost half
    # on 32-bit architecture.
    import psyco
    psyco.full()
except ImportError:
    pass

from struct import pack

from mom._compat import \
    byte_literal, bytes_type, unicode_type, basestring_type, range, reduce, \
    next, integer_types, get_machine_alignment, byte_ord, ZERO_BYTE


__all__ = [
    "byte",
    "bytes",
    "bin",
    "hex",
    "integer_byte_length",
    "integer_bit_length",
    "is_sequence",
    "is_unicode",
    "is_bytes",
    "is_bytes_or_unicode",
    "is_integer",
    "is_even",
    "is_negative",
    "is_odd",
    "is_positive",
]

# Integral range
range = range

reduce = reduce
next = next


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



def byte(num):
    """
    Converts a number between 0 and 255 (both inclusive) to a base-256 (byte)
    representation.

    Use it as a replacement for ``chr`` where you are expecting a byte
    because this will work on all versions of Python.

    Raises :class:``struct.error`` on overflow.

    :param num:
        An unsigned integer between 0 and 255 (both inclusive).
    :returns:
        A single byte.
    """
    return pack("B", num)


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
        bit_string = str(num & 1) + bit_string
        num >>= 1
    bit_string = str(num) + bit_string
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
    Converts a integer value to its hexadecimal representation.

    :param num:
        Integer value.
    :param prefix:
        The prefix to use for the hexadecimal string. Default "0x" to mimic
        ``hex()``.
    :returns:
        Hexadecimal string.
    """
#    if num is None:
#        raise TypeError("'%r' object cannot be interpreted as an index" \
#                        % type(num).__name__)
    prefix = prefix or ""
    if num < 0:
        num = -num
        prefix = "-" + prefix

    # Make sure this is an int and not float.
    num & 1

    hex_num = "%x" % num
    return prefix + hex_num.lower()


def is_sequence(obj):
    """
    Determines whether the given value is a sequence.

    Sets, lists, tuples, bytes, dicts, and strings are treated as sequence.

    :param obj:
        The value to test.
    :returns:
        ``True`` if value is a sequence; ``False`` otherwise.
    """
    try:
        list(obj)
        return True
    except TypeError: #, exception:
        #assert "is not iterable" in bytes(exception)
        return False


def is_unicode(obj):
    """
    Determines whether the given value is a Unicode string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if value is a Unicode string; ``False`` otherwise.
    """
    return isinstance(obj, unicode_type)


def is_bytes(obj):
    """
    Determines whether the given value is a bytes instance.

    :param obj:
        The value to test.
    :returns:
        ``True`` if value is a bytes instance; ``False`` otherwise.
    """
    return isinstance(obj, bytes_type)


def is_bytes_or_unicode(obj):
    """
    Determines whether the given value is an instance of a string irrespective
    of whether it is a byte string or a Unicode string.

    :param obj:
        The value to test.
    :returns:
        ``True`` if value is any type of string; ``False`` otherwise.
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
    return isinstance(obj, integer_types) and not isinstance(obj, bool)


def integer_byte_length(num):
    """
    Number of bytes needed to represent a integer.

    :param num:
        Integer value. If num is 0, returns 0.
    :returns:
        The number of bytes in the integer.
    """
    if num == 0:
        return 0
    bits = integer_bit_length(num)
    quanta, remainder = divmod(bits, 8)
    if remainder:
        quanta += 1
    return quanta


def _integer_byte_length(num):
    """
    Number of bytes needed to represent a integer.

    :param num:
        Integer value. If num is 0, returns 0.
    :returns:
        The number of bytes in the integer.
    """
    if num == 0:
        return 0
    bits = _integer_bit_length(num)
    quanta, remainder = divmod(bits, 8)
    if remainder:
        quanta += 1
    return quanta
    # The following does floating point division.
    #return int(math.ceil(bits / 8.0))


def _integer_raw_bytes_without_leading(num,
                      _zero_byte=ZERO_BYTE,
                      _get_machine_alignment=get_machine_alignment):
    if num == 0:
        return b('')
    if num < 0:
        num = -num
    raw_bytes = b('')
    word_bits, num_bytes, max_uint, pack_type = _get_machine_alignment(num)
    pack_format = ">" + pack_type
    while num > 0:
        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
        num >>= word_bits

    # Count the number of zero prefix bytes.
    zero_leading = 0
    for zero_leading, x in enumerate(raw_bytes):
        if x != _zero_byte[0]:
            break

    # Bytes remaining without zero padding is the number of bytes required
    # to represent this integer.
    return raw_bytes[zero_leading:]


def _integer_byte_length_1(num):
    """
    Number of bytes needed to represent a integer.

    :param num:
        Integer value. If num is 0, returns 0. If num is negative,
        its absolute value will be considered.
    :returns:
        The number of bytes in the integer.
    """
    return len(_integer_raw_bytes_without_leading(num))


def _integer_bit_length(num):
    """
    Number of bits needed to represent a integer excluding any prefix
    0 bits.

    :param num:
        Integer value. If num is 0, returns 0. Only the absolute value of the
        number is considered. Therefore, signed integers will be abs(num)
        before the number's bit length is determined.
    :returns:
        Returns the number of bits in the integer.
    """
    bits = 0
    if num < 0:
        num = -num
    if num == 0:
        return 0
    while num >> bits:
        bits += 1
    return bits


def _integer_bit_length_1(num):
    """
    Number of bits needed to represent a integer excluding any prefix
    0 bits.

    :param num:
        Integer value. If num is 0, returns 0. Only the absolute value of the
        number is considered. Therefore, signed integers will be abs(num)
        before the number's bit length is determined.
    :returns:
        Returns the number of bits in the integer.
    """
    if num == 0:
        return 0
    if num < 0:
        num = -num
    if num > 0x80:
        raw_bytes = _integer_raw_bytes_without_leading(num)
        first_byte = byte_ord(raw_bytes[0])
        bits = 0
        while first_byte >> bits:
            bits += 1
        return ((len(raw_bytes)-1) * 8) + bits
    else:
        bits = 0
        while num >> bits:
            bits += 1
        return bits


def integer_bit_length(num):
    """
    Number of bits needed to represent a integer excluding any prefix
    0 bits.

    :param num:
        Integer value. If num is 0, returns 0. Only the absolute value of the
        number is considered. Therefore, signed integers will be abs(num)
        before the number's bit length is determined.
    :returns:
        Returns the number of bits in the integer.
    """
    # import math
    #if num is None:
    #    raise TypeError("'%r' object cannot be interpreted as an index" \
    #                    % type(num).__name__)
    if num == 0:
        return 0
    if num < 0:
        num = -num

    # Make sure this is an int and not float.
    num & 1
    
    hex_num = "%x" % num #hex(num, None)
    return ((len(hex_num) - 1) * 4) + {
        '0':0, '1':1, '2':2, '3':2,
        '4':3, '5':3, '6':3, '7':3,
        '8':4, '9':4, 'a':4, 'b':4,
        'c':4, 'd':4, 'e':4, 'f':4,
     }[hex_num[0]]
    #return int(math.floor(math.log(n, 2))+1)


def is_even(num):
    """
    Determines whether a number is even.

    :param num:
        Integer
    :returns:
        ``True`` if even; ``False`` otherwise.
    """
    return not (num & 1)


def is_odd(num):
    """
    Determines whether a number is odd.

    :param num:
        Integer
    :returns:
        ``True`` if odd; ``False`` otherwise.
    """
    return bool(num & 1)


def is_positive(num):
    """
    Determines whether a number is positive.

    :param num:
        Number
    :returns:
        ``True`` if positive; ``False`` otherwise.
    """
    if not isinstance(num, integer_types + (bool, float)):
        raise TypeError("unsupported operand type: %r", type(num).__name__)
    return num > 0


def is_negative(num):
    """
    Determines whether a number is negative.

    :param num:
        Number
    :returns:
        ``True`` if positive; ``False`` otherwise.
    """
    if not isinstance(num, integer_types + (bool, float)):
        raise TypeError("unsupported operand type: %r", type(num).__name__)
    return num < 0
