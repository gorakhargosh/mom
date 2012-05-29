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


""":synopsis: Many different types of common encode/decode function.
:module: mom.codec

This module contains codecs for converting between hex, base64, base85,
base58, base62, base36, decimal, and binary representations of bytes.

Understand that bytes are simply base-256 representation. A PNG file::

    \\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00
    \\x05\\x00\\x00\\x00\\x05\\x08\\x06\\x00\\x00\\x00\\x8do&
    \\xe5\\x00\\x00\\x00\\x1cIDAT\\x08\\xd7c\\xf8\\xff\\xff?
    \\xc3\\x7f\\x06 \\x05\\xc3 \\x12\\x84\\xd01\\xf1\\x82X\\xcd
    \\x04\\x00\\x0e\\xf55\\xcb\\xd1\\x8e\\x0e\\x1f\\x00\\x00\\x00
    \\x00IEND\\xaeB`\\x82

That is what an example PNG file looks like as a stream of bytes (base-256)
in Python (with line-breaks added for visual-clarity).

If we wanted to send this PNG within an email message, which is restricted to
ASCII characters, we cannot simply add these bytes in and hope they go
through unchanged. The receiver at the other end expects to get a copy
of exactly the same bytes that you send. Because we are limited to using
ASCII characters, we need to "encode" this binary data into a subset of
ASCII characters before transmitting, and the receiver needs to "decode"
those ASCII characters back into binary data before attempting to display it.

.. pull-quote::

    **Base-encoding raw bytes into ASCII characters is used to safely
    transmit binary data through any medium that does not inherently support
    non-ASCII data.**

Therefore, we need to convert the above PNG binary data into something
that looks like (again, line-breaks have been added for visual clarity only)::

    iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI
    12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJg
    gg==

The base-encoding method that we can use is limited by these criteria:

1. The number of ASCII characters, a subset of ASCII, that we can use
   to represent binary data (case-sensitivity, ambiguity, base, deviation
   from standard characters, etc.)
2. Whether human beings are involved in the transmission of data. Ergo,
   visual clarity, legibility, readability, human-inputability, and even
   *double-click-to-select-ability*! *(Hint: try double-clicking the encoded
   data above to see whether it selects all of it--it won't).* This is a
   corollary for point 1.
3. Whether we want the process to be more time-efficient or space-efficient.
   That is, whether we can process binary data in chunks or whether we need
   to convert it into an arbitrarily large integer before encoding,
   respectively.



Terminology
-----------

Answer this question:

.. pull-quote::

    How many **times** should I multiply 2 by itself to obtain 8?

You say:

.. pull-quote::

    That's a dumb question. 3 times!

Well, congratulations! You have just re-discovered **logarithms**.
In a system of equations, we may have unknowns. Given an
equation with 3 parts, 2 of which are known, we often need to find the 3rd.
Logarithms are used when you know the base (radix) and the number, but not the
exponent.

    **Logarithms help you find exponents.**

Take for example::

    2**0 = 1
    2**1 = 2
    2**2 = 4
    2**3 = 8
    2**4 = 16
    2**5 = 32
    2**6 = 64

Alternatively, logarithms can be thought of as answering the question:

.. pull-quote::

    **Raising 2 to which exponent gets me 64?**

This is the same as doing::

    import math
    math.log(64, 2)    # 6.0; number 64, base 2.
    6.0

read as "logarithm to the base 2 of 64" which gives 6. That is, if
we raise 2 to the power 6, we get 64.

The concept of **roots** or radicals is also related. Roots help you find the
base (radix) given the exponent and the number. So::

    root(8, 3)   # 2.0; cube root. exponent 3, number 8.

.. pull-quote::

        **Roots help you find the base.**

Hopefully, that brings you up to speed and enables you to clearly **see the
relationship between powers, logarithms, and roots**.

We will often refer to the term **byte** and mean it to be
an octet (8) of bits. **The number of bits in a byte is dependent on the
processor architecture.** Therefore, we *can* have a 9-bit byte or even
a 36-bit byte.

.. pull-quote::

    **For our purposes, however, a byte means a chunk of 8 bits--that is,
    an octet.**

By the term "**encoding**," throughout this discussion, we mean **a way of
representing a sequence of bytes in terms of a subset of US-ASCII characters,
each of which uses 7 bits**. This ensures that in communication and messaging
that involves the transmission of binary data, at a small increase in encoded
size, we can *safely* transmit this data encoded as ASCII_ text. We could be
pedantic and use the phrase "ASCII-subset-based encoding" everywhere, but we'll
simply refer to it as "encoding" instead.

.. _ASCII: http://en.wikipedia.org/wiki/ASCII


How it applies to encodings
---------------------------
Byte, or base-256, representation allows each byte to be represented
using one of 256 values (0-255 inclusive). Modern processors can process
data in chunks of 32 bits (4 bytes), 64 bits (8 bytes), and so on. Notice
that these are powers of 2 given that our processors are binary machines.

We could feed a 64-bit processor with 8 bits of data at a time, but
that would guarantee that the codec will be only 1/8th as time-efficient as it
can be. That is, if you feed the same 64-bit processor with 64 bits of data
at a time instead, the encoding process will be 8 times as fast. Whoa!

Therefore, in order to ensure that our codecs are fast, we need to feed
our processors data in chunks to be more time-efficient. The two types of
encoding we discuss here are:

1. big-integer-based polynomial-time base-conversions
2. chunked linear-time base-conversions.

.. pull-quote::

    **These two types of encoding are not always compatible with each other.**

Big-integer based encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~
This method of encoding is generally costlier because the raw bytes
(base-256 representation) are first converted into a big integer, which
is then subsequently repeatedly divided to obtain an encoded sequence
of bytes. Bases 58, 60, and 62 are not powers of 2, and therefore cannot
be reliably or efficiently encoded in chunks of powers of 2 (used by
microprocessors) so as to produce the same encoded representations as
their big integer encoded representations. Therefore,
using these encodings for a large amount of binary data is not advised.
The base-58 and base-62 modules in this library are meant to be used with
small amounts of binary data.

Chunked encoding
~~~~~~~~~~~~~~~~
Base encoding a chunk of 4 bytes at a time (32 bits at a time) means
we would need a way to represent each of the 256**4 (4294967296) values with
our encoding::

    256**4 # 4294967296
    2**32  # 4294967296

Given an encoding alphabet of 85 ASCII characters, for example, we need
to find an exponent (logarithm) that allows us to represent each one of these
4294967296 values::

    85**4 # 52200625
    85**5 # 4437053125

    >>> 85**5 >= 2**32
    True

Done using logarithms::

    import math
    math.log(2**32, 85)   # 4.9926740807111996

Therefore, we would need 5 characters from this encoding alphabet to represent
4 bytes. Since 85 is not a power of 2, there is going to be a little wastage
of space and the codec will need to deal with padding and de-padding bytes
to ensure the resulting size to be a multiple of the chunk size, but the
byte sequence will be more compact than its base-16 (hexadecimal)
representation, for example::

    import math
    math.log(2**32, 16)   # 8.0

As you can see, if we used hexadecimal representation instead, each 4-byte
chunk would be represented using 8 characters from the encoding alphabet.
This is clearly less space-efficient than using 5 characters per 4 bytes of
binary data.

Base-64 as another example
--------------------------
Base-64 allows us to represent 256**4 (4294967296) values using 64
ASCII characters.


Bytes base-encoding
-------------------
These codecs preserve bytes "as is" when decoding back to bytes. In a more
mathematical sense,

    ``g(f(x))`` is an **identity function**

where ``g`` is the decoder and ``f`` is the encoder.

Why have we reproduced base64 encoding/decoding functions here when the
standard library has them? Well, those functions behave differently in
Python 2.x and Python 3.x. The Python 3.x equivalents do not accept Unicode
strings as their arguments, whereas the Python 2.x versions would happily
encode your Unicode strings without warning you-you know that you are supposed
to encode them to UTF-8 or another byte encoding before you base64-encode them
right? These wrappers are re-implemented so that you do not make these mistakes.
Use them. They will help prevent unexpected bugs.

.. autofunction:: base85_encode
.. autofunction:: base85_decode
.. autofunction:: base64_encode
.. autofunction:: base64_decode
.. autofunction:: base64_urlsafe_encode
.. autofunction:: base64_urlsafe_decode
.. autofunction:: base62_encode
.. autofunction:: base62_decode
.. autofunction:: base58_encode
.. autofunction:: base58_decode
.. autofunction:: base36_encode
.. autofunction:: base36_decode
.. autofunction:: hex_encode
.. autofunction:: hex_decode
.. autofunction:: decimal_encode
.. autofunction:: decimal_decode
.. autofunction:: bin_encode
.. autofunction:: bin_decode

.. automodule:: mom.codec.base85
.. automodule:: mom.codec.base62
.. automodule:: mom.codec.base58
.. automodule:: mom.codec.integer
.. automodule:: mom.codec.json
.. automodule:: mom.codec.text
.. automodule:: mom.codec._base

"""

from __future__ import absolute_import

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

import binascii

from mom import _compat
from mom import builtins
from mom import functional
from mom.codec import base36
from mom.codec import base58
from mom.codec import base62
from mom.codec import base85
from mom.codec import integer


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "B85_ASCII",
    "B85_RFC1924",
    "base36_decode",
    "base36_encode",
    "base58_decode",
    "base58_encode",
    "base62_decode",
    "base62_encode",
    "base64_decode",
    "base64_encode",
    "base64_urlsafe_decode",
    "base64_urlsafe_encode",
    "base85_decode",
    "base85_encode",
    "bin_decode",
    "bin_encode",
    "decimal_decode",
    "decimal_encode",
    "hex_decode",
    "hex_encode",
    ]


b = builtins.b

ZERO_BYTE = _compat.ZERO_BYTE
EMPTY_BYTE = _compat.EMPTY_BYTE
UNDERSCORE_BYTE = _compat.UNDERSCORE_BYTE
FORWARD_SLASH_BYTE = _compat.FORWARD_SLASH_BYTE
HYPHEN_BYTE = _compat.HYPHEN_BYTE
PLUS_BYTE = _compat.PLUS_BYTE
EQUAL_BYTE = _compat.EQUAL_BYTE
DIGIT_ZERO_BYTE = _compat.DIGIT_ZERO_BYTE


# Bytes base-encoding.

B85_ASCII = "ASCII85"
B85_RFC1924 = "RFC1924"

B85_DECODE_MAP = {
    B85_ASCII: base85.b85decode,
    B85_RFC1924: base85.rfc1924_b85decode,
    }
B85_ENCODE_MAP = {
    B85_ASCII: base85.b85encode,
    B85_RFC1924: base85.rfc1924_b85encode,
    }


def base85_encode(raw_bytes, charset=B85_ASCII):
  """
  Encodes raw bytes into ASCII85 representation.

  Encode your Unicode strings to a byte encoding before base85-encoding them.

  :param raw_bytes:
      Bytes to encode.
  :param charset:
      "ASCII85" (default) or "RFC1924".
  :returns:
      ASCII85 encoded string.
  """
  try:
    return B85_ENCODE_MAP[charset.upper()](raw_bytes)
  except KeyError:
    raise ValueError("Invalid character set specified: %r" % charset)


def base85_decode(encoded, charset=B85_ASCII):
  """
  Decodes ASCII85-encoded bytes into raw bytes.

  :param encoded:
      ASCII85 encoded representation.
  :param charset:
      "ASCII85" (default) or "RFC1924".
  :returns:
      Raw bytes.
  """
  try:
    return B85_DECODE_MAP[charset.upper()](encoded)
  except KeyError:
    raise ValueError("Invalid character set specified: %r" % charset)


def base64_urlsafe_encode(raw_bytes):
  """
  Encodes raw bytes into URL-safe base64 bytes.

  Encode your Unicode strings to a byte encoding before base64-encoding them.

  :param raw_bytes:
      Bytes to encode.
  :returns:
      Base64 encoded string without newline characters.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("argument must be bytes: got %r" %
                    type(raw_bytes).__name__)
    # This is 3-4x faster than urlsafe_b64decode() -Guido.
  # We're not using the base64.py wrapper around binascii because
  # this module itself is a wrapper. binascii is implemented in C, so
  # we avoid module overhead however small.
  encoded = binascii.b2a_base64(raw_bytes)[:-1]
  return (encoded
          .rstrip(EQUAL_BYTE)
          .replace(PLUS_BYTE, HYPHEN_BYTE)
          .replace(FORWARD_SLASH_BYTE, UNDERSCORE_BYTE))


def base64_urlsafe_decode(encoded):
  """
  Decodes URL-safe base64-encoded bytes into raw bytes.

  :param encoded:
      Base-64 encoded representation.
  :returns:
      Raw bytes.
  """
  if not builtins.is_bytes(encoded):
    raise TypeError("argument must be bytes: got %r" %
                    type(encoded).__name__)
  remainder = len(encoded) % 4
  if remainder:
    encoded += EQUAL_BYTE * (4 - remainder)
    # This is 3-4x faster than urlsafe_b64decode() -Guido.
  # We're not using the base64.py wrapper around binascii because
  # this module itself is a wrapper. binascii is implemented in C, so
  # we avoid module overhead however small.
  encoded = (encoded
             .replace(HYPHEN_BYTE, PLUS_BYTE)
             .replace(UNDERSCORE_BYTE, FORWARD_SLASH_BYTE))
  return binascii.a2b_base64(encoded)


def base64_encode(raw_bytes):
  """
  Encodes raw bytes into base64 representation without appending a trailing
  newline character. Not URL-safe.

  Encode your Unicode strings to a byte encoding before base64-encoding them.

  :param raw_bytes:
      Bytes to encode.
  :returns:
      Base64 encoded bytes without newline characters.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("argument must be bytes: got %r" %
                    type(raw_bytes).__name__)
  return binascii.b2a_base64(raw_bytes)[:-1]


def base64_decode(encoded):
  """
  Decodes base64-encoded bytes into raw bytes. Not URL-safe.

  :param encoded:
      Base-64 encoded representation.
  :returns:
      Raw bytes.
  """
  if not builtins.is_bytes(encoded):
    raise TypeError("argument must be bytes: got %r" %
                    type(encoded).__name__)
  return binascii.a2b_base64(encoded)


def base62_encode(raw_bytes):
  """
  Encodes raw bytes into base-62 representation. URL-safe and human safe.

  Encode your Unicode strings to a byte encoding before base-62-encoding
  them.

  Convenience wrapper for consistency.

  :param raw_bytes:
      Bytes to encode.
  :returns:
      Base-62 encoded bytes.
  """
  return base62.b62encode(raw_bytes)


def base62_decode(encoded):
  """
  Decodes base-62-encoded bytes into raw bytes.

  Convenience wrapper for consistency.

  :param encoded:
      Base-62 encoded bytes.
  :returns:
      Raw bytes.
  """
  return base62.b62decode(encoded)


def base58_encode(raw_bytes):
  """
  Encodes raw bytes into base-58 representation. URL-safe and human safe.

  Encode your Unicode strings to a byte encoding before base-58-encoding
  them.

  Convenience wrapper for consistency.

  :param raw_bytes:
      Bytes to encode.
  :returns:
      Base-58 encoded bytes.
  """
  return base58.b58encode(raw_bytes)


def base58_decode(encoded):
  """
  Decodes base-58-encoded bytes into raw bytes.

  Convenience wrapper for consistency.

  :param encoded:
      Base-58 encoded bytes.
  :returns:
      Raw bytes.
  """
  return base58.b58decode(encoded)


def base36_encode(raw_bytes):
  """
  Encodes raw bytes into base-36 representation.

  Encode your Unicode strings to a byte encoding before base-58-encoding
  them.

  Convenience wrapper for consistency.

  :param raw_bytes:
      Bytes to encode.
  :returns:
      Base-36 encoded bytes.
  """
  return base36.b36encode(raw_bytes)


def base36_decode(encoded):
  """
  Decodes base-36-encoded bytes into raw bytes.

  Convenience wrapper for consistency.

  :param encoded:
      Base-36 encoded bytes.
  :returns:
      Raw bytes.
  """
  return base36.b36decode(encoded)


def hex_encode(raw_bytes):
  """
  Encodes raw bytes into hexadecimal representation.

  Encode your Unicode strings to a byte encoding before hex-encoding them.

  :param raw_bytes:
      Bytes.
  :returns:
      Hex-encoded representation.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("argument must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  return binascii.b2a_hex(raw_bytes)


def hex_decode(encoded):
  """
  Decodes hexadecimal-encoded bytes into raw bytes.

  :param encoded:
      Hex representation.
  :returns:
      Raw bytes.
  """
  if not builtins.is_bytes(encoded):
    raise TypeError("argument must be bytes: got %r" %
                    type(encoded).__name__)
  return binascii.a2b_hex(encoded)


def decimal_encode(raw_bytes):
  """
  Encodes raw bytes into decimal representation. Leading zero bytes are
  preserved.

  Encode your Unicode strings to a byte encoding before decimal-encoding them.

  :param raw_bytes:
      Bytes.
  :returns:
      Decimal-encoded representation.
  """
  padding = DIGIT_ZERO_BYTE * builtins.bytes_leading(raw_bytes)
  int_val = integer.bytes_to_uint(raw_bytes)
  if int_val:
    encoded = padding + str(int_val).encode("ascii")
  else:
    encoded = padding
  return encoded


def decimal_decode(encoded):
  """
  Decodes decimal-encoded bytes to raw bytes. Leading zeros are converted to
  leading zero bytes.

  :param encoded:
      Decimal-encoded representation.
  :returns:
      Raw bytes.
  """
  padding = ZERO_BYTE * builtins.bytes_leading(encoded, DIGIT_ZERO_BYTE)
  int_val = int(encoded)
  if int_val:
    decoded = padding + integer.uint_to_bytes(int_val)
  else:
    decoded = padding
  return decoded


_BIN_TO_HEX_LOOKUP = {
    b("0000"): b("0"),
    b("0001"): b("1"),
    b("0010"): b("2"),
    b("0011"): b("3"),
    b("0100"): b("4"),
    b("0101"): b("5"),
    b("0110"): b("6"),
    b("0111"): b("7"),
    b("1000"): b("8"),
    b("1001"): b("9"),
    b("1010"): b("a"),
    b("1011"): b("b"),
    b("1100"): b("c"),
    b("1101"): b("d"),
    b("1110"): b("e"),
    b("1111"): b("f"),
    }

_HEX_TO_BIN_LOOKUP = {
    b("0"): b("0000"),
    b("1"): b("0001"),
    b("2"): b("0010"),
    b("3"): b("0011"),
    b("4"): b("0100"),
    b("5"): b("0101"),
    b("6"): b("0110"),
    b("7"): b("0111"),
    b("8"): b("1000"),
    b("9"): b("1001"),
    b("a"): b("1010"), b("A"): b("1010"),
    b("b"): b("1011"), b("B"): b("1011"),
    b("c"): b("1100"), b("C"): b("1100"),
    b("d"): b("1101"), b("D"): b("1101"),
    b("e"): b("1110"), b("E"): b("1110"),
    b("f"): b("1111"), b("F"): b("1111"),
    }
if _compat.HAVE_PYTHON3:  # pragma: no cover
  # Indexing into Python 3 bytes yields ords, not single-byte strings.
  _HEX_TO_BIN_LOOKUP = dict((k[0], v) for k, v in _HEX_TO_BIN_LOOKUP.items())


def bin_encode(raw_bytes):
  """
  Encodes raw bytes into binary representation.

  Encode your Unicode strings to a byte encoding before binary-encoding them.

  :param raw_bytes:
      Raw bytes.
  :returns:
      Binary representation.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("argument must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
  return EMPTY_BYTE.join(_HEX_TO_BIN_LOOKUP[hex_char]
                         for hex_char in binascii.b2a_hex(raw_bytes))


def bin_decode(encoded):
  """
  Decodes binary-encoded bytes into raw bytes.

  :param encoded:
      Binary representation.
  :returns:
      Raw bytes.
  """
  if not builtins.is_bytes(encoded):
    raise TypeError("argument must be bytes: got %r" %
                    type(encoded).__name__)
  return binascii.a2b_hex(EMPTY_BYTE.join(_BIN_TO_HEX_LOOKUP[nibble]
                                          for nibble
                                          in functional.chunks(encoded, 4)))
