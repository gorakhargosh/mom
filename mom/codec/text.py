#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Facebook.
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

""":synopsis: Common functions for text encodings.
:module: mom.codec.text

Text encoding
-------------

::

    "There is no such thing as plain text."
                              - Plain Text.


UTF-8 is one of the many ways in which Unicode strings can be represented as
a *sequence of bytes*, and because UTF-8 is more portable between diverse
systems, you must ensure to convert your Unicode strings to UTF-8 encoded
bytes before they leave your system and ensure to decode UTF-8 encoded bytes
back into Unicode strings before you start working with them in your
code--that is, if you know those bytes are UTF-8 encoded.


Terminology
~~~~~~~~~~~
* The process of **encoding** is that of converting a Unicode string into a
  sequence of bytes. The **method** using which this conversion is done is
  *also* called an **encoding**::

        Unicode string   -> Encoded bytes
        ---------------------------------
        "深入 Python"     -> b"\\xe6\\xb7\\xb1\\xe5\\x85\\xa5 Python"

  The **encoding** (method) used to *encode* in this example is UTF-8.

* The process of **decoding** is that of converting a sequence of bytes into a
  Unicode string::

        Encoded bytes                      -> Unicode string
        ----------------------------------------------------
        b"\\xe6\\xb7\\xb1\\xe5\\x85\\xa5 Python" -> "深入 Python"

  The **encoding** (method) used to *decode* in this example is UTF-8.

A very crude explanation of when to use what
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Essentially, inside your own system, work with::

    "深入 Python"

and not::

    b"\\xe6\\xb7\\xb1\\xe5\\x85\\xa5 Python"

but when sending things out to other systems that may not see `"深入 Python"`
the way Python does, you encode it into UTF-8 bytes::

    b"\\xe6\\xb7\\xb1\\xe5\\x85\\xa5 Python"

**and tell** those systems that you're using UTF-8 to encode your Unicode
strings so that those systems can decode the bytes you sent appropriately.

When receiving text from other systems, ask for their encodings.
Decode the text using the appropriate encoding method as soon as you receive
it and then operate on the resulting Unicode text.


Read these before you begin to use these functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. http://www.joelonsoftware.com/articles/Unicode.html
2. http://diveintopython3.org/strings.html
3. http://docs.python.org/howto/unicode.html
4. http://docs.python.org/library/codecs.html


.. autofunction:: utf8_encode
.. autofunction:: utf8_decode
.. autofunction:: utf8_encode_if_unicode
.. autofunction:: utf8_decode_if_bytes
.. autofunction:: utf8_encode_recursive
.. autofunction:: utf8_decode_recursive
.. autofunction:: bytes_to_unicode
.. autofunction:: bytes_to_unicode_recursive
.. autofunction:: to_unicode_if_bytes
.. autofunction:: ascii_encode
.. autofunction:: latin1_encode
"""

from __future__ import absolute_import

from mom import builtins


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "ascii_encode",
    "bytes_to_unicode",
    "bytes_to_unicode_recursive",
    "latin1_encode",
    "to_unicode_if_bytes",
    "utf8_decode",
    "utf8_decode_if_bytes",
    "utf8_decode_recursive",
    "utf8_encode",
    "utf8_encode_if_unicode",
    "utf8_encode_recursive",
    ]


def utf8_encode(unicode_text):
  """
  UTF-8 encodes a Unicode string into bytes; bytes and None are left alone.

  Work with Unicode strings in your code and encode your Unicode strings into
  UTF-8 before they leave your system.

  :param unicode_text:
      If already a byte string or None, it is returned unchanged.
      Otherwise it must be a Unicode string and is encoded as UTF-8 bytes.
  :returns:
      UTF-8 encoded bytes.
  """
  if unicode_text is None or builtins.is_bytes(unicode_text):
    return unicode_text
  if not builtins.is_unicode(unicode_text):
    raise TypeError("unsupported argument type: %r" %
                    type(unicode_text).__name__)
  return unicode_text.encode("utf-8")


def utf8_decode(utf8_encoded_bytes):
  """
  Decodes bytes into a Unicode string using the UTF-8 encoding.

  Decode your UTF-8 encoded bytes into Unicode strings as soon as
  they arrive into your system. Work with Unicode strings in your code.

  :param utf8_encoded_bytes:
      UTF-8 encoded bytes.
  :returns:
      Unicode string.
  """
  return bytes_to_unicode(utf8_encoded_bytes)


def utf8_encode_if_unicode(obj):
  """
  UTF-8 encodes the object only if it is a Unicode string.

  :param obj:
      The value that will be UTF-8 encoded if it is a Unicode string.
  :returns:
      UTF-8 encoded bytes if the argument is a Unicode string; otherwise
      the value is returned unchanged.
  """
  return utf8_encode(obj) if builtins.is_unicode(obj) else obj


def utf8_decode_if_bytes(obj):
  """
  Decodes UTF-8 encoded bytes into a Unicode string.

  :param obj:
      Python object. If this is a bytes instance, it will be decoded
      into a Unicode string; otherwise, it will be left alone.
  :returns:
      Unicode string if the argument is a bytes instance;
      the unchanged object otherwise.
  """
  return to_unicode_if_bytes(obj)


def to_unicode_if_bytes(obj, encoding="utf-8"):
  """
  Decodes encoded bytes into a Unicode string.

  :param obj:
      The value that will be converted to a Unicode string.
  :param encoding:
      The encoding used to decode bytes. Defaults to UTF-8.
  :returns:
      Unicode string if the argument is a byte string. Otherwise the value
      is returned unchanged.
  """
  return bytes_to_unicode(obj, encoding) if builtins.is_bytes(obj) else obj


def bytes_to_unicode(raw_bytes, encoding="utf-8"):
  """
  Converts bytes to a Unicode string decoding it according to the encoding
  specified.

  :param raw_bytes:
      If already a Unicode string or None, it is returned unchanged.
      Otherwise it must be a byte string.
  :param encoding:
      The encoding used to decode bytes. Defaults to UTF-8
  """
  if raw_bytes is None or builtins.is_unicode(raw_bytes):
    return raw_bytes
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("unsupported argument type: %r" % type(raw_bytes).__name__)
  return raw_bytes.decode(encoding)


def utf8_encode_recursive(obj):
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
    return dict((utf8_encode_recursive(k),
                 utf8_encode_recursive(v)) for (k, v) in obj.items())
  elif isinstance(obj, list):
    return list(utf8_encode_recursive(i) for i in obj)
  elif isinstance(obj, tuple):
    return tuple(utf8_encode_recursive(i) for i in obj)
  elif builtins.is_unicode(obj):
    return utf8_encode(obj)
  else:
    return obj


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
  elif builtins.is_bytes(obj):
    return bytes_to_unicode(obj, encoding=encoding)
  else:
    return obj


def utf8_decode_recursive(obj):
  """
  Walks a simple data structure, converting bytes to Unicode strings.

  Supports lists, tuples, and dictionaries.

  :param obj:
      The Python data structure to walk recursively looking for
      byte strings.
  :returns:
      obj with all the byte strings converted to Unicode strings.
  """
  return bytes_to_unicode_recursive(obj)


def ascii_encode(obj):
  """
  Encodes a string using ASCII encoding.

  :param obj:
      String to encode.
  :returns:
      ASCII-encoded bytes.
  """
  return obj.encode("ascii")


def latin1_encode(obj):
  """
  Encodes a string using LATIN-1 encoding.

  :param obj:
      String to encode.
  :returns:
      LATIN-1 encoded bytes.
  """
  return obj.encode("latin1")
