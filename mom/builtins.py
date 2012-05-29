#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google Inc. All Rights Reserved.
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


""":synopsis: Deals with a lot of cross-version issues.
:module: mom.builtins

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

This module introduces the "bytes" type for Python 2.5 and adds a
few utility functions that will continue to keep working as they should
even when Python versions change.

Rules to follow:
* Use ``bytes`` where you want byte strings (binary data).

The meanings of these types have been changed to suit Python 3.

Encodings
---------
.. autofunction:: bin
.. autofunction:: hex
.. autofunction:: byte
.. autofunction:: byte_ord


Bits and bytes size counting
----------------------------
.. autofunction:: bytes_leading
.. autofunction:: bytes_trailing
.. autofunction:: integer_bit_length
.. autofunction:: integer_bit_size
.. autofunction:: integer_byte_length
.. autofunction:: integer_byte_size

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

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

import struct
from mom import _compat


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "byte",
    "byte_ord",
    "bytes",
    "bytes_leading",
    "bytes_trailing",
    "bin",
    "hex",
    "integer_byte_length",
    "integer_byte_size",
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
range = _compat.range
map = _compat.map
reduce = _compat.reduce
next = _compat.next

# Types and their meanings:
#
# * ``bytes`` = bytes (binary data or a sequence of bytes).
# * ``unicode`` = Unicode string or text (for backward compatibility,
#    2to3 converts these).
bytes = _compat.BYTES_TYPE

# Fake byte literal support.
b = _compat.byte_literal

byte_ord = _compat.byte_ord


dict_each = _compat.dict_each


def byte(number):
  """
  Converts a number between 0 and 255 (both inclusive) to a base-256 (byte)
  representation.

  Use it as a replacement for ``chr`` where you are expecting a byte
  because this will work on all versions of Python.

  Raises :class:``struct.error`` on overflow.

  :param number:
      An unsigned integer between 0 and 255 (both inclusive).
  :returns:
      A single byte.
  """
  return struct.pack("B", number)


def bytes_leading(raw_bytes, needle=_compat.ZERO_BYTE):
  """
  Finds the number of prefixed byte occurrences in the haystack.

  Useful when you want to deal with padding.

  :param raw_bytes:
      Raw bytes.
  :param needle:
      The byte to count. Default \000.
  :returns:
      The number of leading needle bytes.
  """
  if not is_bytes(raw_bytes):
    raise TypeError("argument must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  leading = 0
  # Indexing keeps compatibility between Python 2.x and Python 3.x
  needle_byte = needle[0]
  for raw_byte in raw_bytes:
    if raw_byte == needle_byte:
      leading += 1
    else:
      break
  return leading


def bytes_trailing(raw_bytes, needle=_compat.ZERO_BYTE):
  """
  Finds the number of suffixed byte occurrences in the haystack.

  Useful when you want to deal with padding.

  :param raw_bytes:
      Raw bytes.
  :param needle:
      The byte to count. Default \000.
  :returns:
      The number of trailing needle bytes.
  """
  if not is_bytes(raw_bytes):
    raise TypeError("argument must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  trailing = 0
  # Indexing keeps compatibility between Python 2.x and Python 3.x
  needle_byte = needle[0]
  for raw_byte in reversed(raw_bytes):
    if raw_byte == needle_byte:
      trailing += 1
    else:
      break
  return trailing


def bin(number, prefix="0b"):
  """
  Converts a long value to its binary representation.

  :param number:
      Long value.
  :param prefix:
      The prefix to use for the bitstring. Default "0b" to mimic Python
      builtin ``bin()``.
  :returns:
      Bit string.
  """
  if number is None:
    raise TypeError("'%r' object cannot be interpreted as an index" %
                    type(number).__name__)
  prefix = prefix or ""
  if number < 0:
    number = -number
    prefix = "-" + prefix
  bit_string = ""
  while number > 1:
    bit_string = str(number & 1) + bit_string
    number >>= 1
  bit_string = str(number) + bit_string
  return prefix + bit_string


def hex(number, prefix="0x"):
  """
  Converts a integer value to its hexadecimal representation.

  :param number:
      Integer value.
  :param prefix:
      The prefix to use for the hexadecimal string. Default "0x" to mimic
      ``hex()``.
  :returns:
      Hexadecimal string.
  """
  prefix = prefix or ""
  if number < 0:
    number = -number
    prefix = "-" + prefix

  # Make sure this is an int and not float.
  _ = number & 1

  hex_num = "%x" % number
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
  except TypeError:  #, exception:
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
  return isinstance(obj, _compat.UNICODE_TYPE)


def is_bytes(obj):
  """
  Determines whether the given value is a bytes instance.

  :param obj:
      The value to test.
  :returns:
      ``True`` if value is a bytes instance; ``False`` otherwise.
  """
  return isinstance(obj, _compat.BYTES_TYPE)


def is_bytes_or_unicode(obj):
  """
  Determines whether the given value is an instance of a string irrespective
  of whether it is a byte string or a Unicode string.

  :param obj:
      The value to test.
  :returns:
      ``True`` if value is any type of string; ``False`` otherwise.
  """
  return isinstance(obj, _compat.BASESTRING_TYPE)


def is_integer(obj):
  """
  Determines whether the object value is actually an integer and not a bool.

  :param obj:
      The value to test.
  :returns:
      ``True`` if yes; ``False`` otherwise.
  """
  return isinstance(obj, _compat.INTEGER_TYPES) and not isinstance(obj, bool)


def integer_byte_length(number):
  """
  Number of bytes needed to represent a integer excluding any prefix 0 bytes.

  :param number:
      Integer value. If num is 0, returns 0.
  :returns:
      The number of bytes in the integer.
  """
  quanta, remainder = divmod(integer_bit_length(number), 8)
  if remainder:
    quanta += 1
  return quanta


def integer_byte_size(number):
  """
  Size in bytes of an integer.

  :param number:
      Integer value. If num is 0, returns 1.
  :returns:
      Size in bytes of an integer.
  """
  quanta, remainder = divmod(integer_bit_length(number), 8)
  if remainder or number == 0:
    quanta += 1
  return quanta


def integer_bit_length(number):
  """
  Number of bits needed to represent a integer excluding any prefix
  0 bits.

  :param number:
      Integer value. If num is 0, returns 0. Only the absolute value of the
      number is considered. Therefore, signed integers will be abs(num)
      before the number's bit length is determined.
  :returns:
      Returns the number of bits in the integer.
  """
  # Public domain. Taken from tlslite. This is the fastest implementation
  # I have found.

  # Do not change this to `not num` otherwise a TypeError will not
  # be raised when `None` is passed in as a value.
  if number == 0:
    return 0
  if number < 0:
    number = -number
    # Make sure this is an int and not float.
  _ = number & 1
  hex_num = "%x" % number
  return ((len(hex_num) - 1) * 4) + {
      "0": 0, "1": 1, "2": 2, "3": 2,
      "4": 3, "5": 3, "6": 3, "7": 3,
      "8": 4, "9": 4, "a": 4, "b": 4,
      "c": 4, "d": 4, "e": 4, "f": 4,
      }[hex_num[0]]
  #return int(math.floor(math.log(n, 2))+1)


def integer_bit_size(number):
  """
  Number of bits needed to represent a integer excluding any prefix
  0 bits.

  :param number:
      Integer value. If num is 0, returns 1. Only the absolute value of the
      number is considered. Therefore, signed integers will be abs(num)
      before the number's bit length is determined.
  :returns:
      Returns the number of bits in the integer.
  """
  if number == 0:
    return 1
  return integer_bit_length(number)


def integer_bit_count(number):
  """
  Returns the number of set (1) bits in an unsigned integer.

  :param number:
      An integer. If this is a negative integer, its absolute
      value will be considered.
  :returns:
      The number of set bits in an unsigned integer.
  """
  # Licensed under the PSF License.
  # Taken from http://wiki.python.org/moin/BitManipulation
  number = abs(number)
  count = 0
  while number:
    number &= number - 1
    count += 1
  return count


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
  if not isinstance(num, _compat.INTEGER_TYPES + (bool, float)):
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
  if not isinstance(num, _compat.INTEGER_TYPES + (bool, float)):
    raise TypeError("unsupported operand type: %r", type(num).__name__)
  return num < 0
