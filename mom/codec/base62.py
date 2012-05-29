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

""":synopsis: Base-62 7-bit ASCII-safe representation for compact human-input.
:module: mom.codec.base62

Where should you use base-62?
-----------------------------
Base-62 representation is 7 bit-ASCII safe, MIME-safe, URL-safe, HTTP
cookie-safe, and almost **human being-safe**. Base-62 representation can:

* be readable and editable by a human being;
* safely and compactly represent numbers;
* contain only alphanumeric characters;
* not contain punctuation characters.

For examples of places where you can use base-62, see the documentation
for :mod:`mom.codec.base58`.

In general, use base-62 in any 7-bit ASCII-safe compact communication where
human beings and communication devices may be significantly involved.

When to prefer base-62 over base-58?
------------------------------------
When you don't care about the visual ambiguity between these characters:

* 0 (ASCII NUMERAL ZERO)
* O (ASCII UPPERCASE ALPHABET O)
* I (ASCII UPPERCASE ALPHABET I)
* l (ASCII LOWERCASE ALPHABET L)

A practical example (versioned static asset URLs):
--------------------------------------------------
In order to reduce the number of HTTP requests for static assets sent to a
Web server, developers often include a hash of the asset being served into
the URL and set the expiration time of the asset to a very long period (say,
365 days).

This enables an almost perfect form of client-side asset caching while still
serving fresh content when it changes. To minimize the size overhead
introduced into the URL by such hashed-identifiers, the identifiers
themselves can be shortened using base-58 or base-62 encoding. For example::

    $ sha1sum file.js
    a497f210fc9c5d02fc7dc7bd211cb0c74da0ae16

The asset URL for this file can be::

    http://s.example.com/js/a497f210fc9c5d02fc7dc7bd211cb0c74da0ae16/file.js

where ``example.com`` is a canonical domain used only for informational
purposes. However, the hashed-identifier in the URL is long but can be
reduced using base-62 to::

    # Base-58
    http://s.example.com/js/3HzsRcRETLZ3qFgDzG1QE7CJJNeh/file.js

    # Base-62
    http://s.example.com/js/NU3qW1G4teZJynubDFZnbzeOUFS/file.js

The first 12 characters of a SHA-1 hash are sufficiently strong for serving
static assets while minimizing collision overhead in the context of a
small-to-medium-sized Website and considering these are URLs for static served
assets that can change over periods of time. You may want to consider
using the full hash for large-scale Websites. Therefore, we can shorten the
original asset URL to::

    http://s.example.com/js/a497f210fc9c/file.js

which can then be reduced utilizing base-58 or base-62 encoding to::

    # Base-58
    http://s.example.com/js/2QxqmqiFm/file.js

    # Base-62
    http://s.example.com/js/pO7arZWO/file.js

These are a much shorter URLs than the original. Notice that we have not
renamed the file ``file.js`` to ``2QxqmqiFm.js`` or ``pO7arZWO.js``
because that would cause an unnecessary explosion of files on the server
as new files would be generated every time the source files change.
Instead, we have chosen to make use of Web server URL-rewriting rules
to strip the hashed identifier and serve the file fresh as it is on the
server file system. These are therefore **non-versioned assets**--only
the URLs that point at them are versioned. That is if you took a diff
between the files that these URLs point at::

    http://s.example.com/js/pO7arZWO/file.js
    http://s.example.com/js/2qiFqxEm/file.js

you would *not* see a difference. Only the URLs differ to trick the browser
into caching as well as it can.

The hashed-identifier is not part of the query string for this asset URL
because certain proxies do not cache files served from URLs that include
query strings. That is, we are **not** doing this::

    # Base-58 -- Don't do this. Not all proxies will cache it.
    http://s.example.com/js/file.js?v=2QxqmqiFm

    # Base-62 -- Don't do this. Not all proxies will cache it.
    http://s.example.com/js/file.js?v=pO7arZWO

If you wish to support **versioned assets**, however, you may need to
rename files to include their hashed identifiers and avoid URL-rewriting
instead. For example::

    # Base-58
    http://s.example.com/js/file-2QxqmqiFm.js

    # Base-62
    http://s.example.com/js/file-pO7arZWO.js

.. NOTE::
    Do note that the base-58 encoded version of the SHA-1 hash (40 characters
    in hexadecimal representation) may have a length of either 27 or 28.
    Similarly, for the SHA-1 hash (40 characters in hex), the base62-encoded
    version may have a length of either 26 or 27.

    Therefore, please ensure that your rewriting rules take variable length
    into account.

The following benefits are therefore achieved:

* Client-side caching is fully utilized
* The number of HTTP requests sent to Web servers by clients is reduced.
* When assets change, so do their SHA-1 hashed identifiers, and hence their
  asset URLs.
* Shorter URLs also implies that fewer bytes are transferred in HTTP responses.
* Bandwidth consumption is reduced by a noticeably large factor.
* Multiple versions of assets (if required).

Essentially, URLs shortened using base-58 or base-62 encoding can result
in a faster Web-browsing experience for end-users.

Functions
---------
.. autofunction:: b62encode
.. autofunction:: b62decode
"""

from __future__ import absolute_import
from __future__ import division

# pylint: disable-msg=R0801
try:  # pragma: no cover
  import psyco

  psyco.full()
except ImportError:  # pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

from mom import _compat
from mom import builtins
from mom import string
from mom.codec import _base


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


# Follows ASCII order.
ASCII62_BYTES = (string.DIGITS +
                 string.ASCII_UPPERCASE +
                 string.ASCII_LOWERCASE).encode("ascii")
# Therefore, b"0" represents b"\0".
ASCII62_ORDS = dict((x, i) for i, x in enumerate(ASCII62_BYTES))


# Really, I don't understand why people use the non-ASCII order,
# but if you really like it that much, go ahead. Be my guest. Here
# is what you will need:
#
# Does not follow ASCII order.
ALT62_BYTES = (string.DIGITS +
               string.ASCII_LOWERCASE +
               string.ASCII_UPPERCASE).encode("ascii")
# Therefore, b"0" represents b"\0".
ALT62_ORDS = dict((x, i) for i, x in enumerate(ALT62_BYTES))

if _compat.HAVE_PYTHON3:
  ASCII62_BYTES = tuple(builtins.byte(x) for x in ASCII62_BYTES)
  ALT62_BYTES = tuple(builtins.byte(x) for x in ALT62_BYTES)

# If you're going to make people type stuff longer than this length
# I don't know what to tell you. Beyond this length powers
# are computed, so be careful if you care about computation speed.
# I think this is a VERY generous range. Decoding bytes fewer than 512
# will use this pre-computed lookup table, and hence, be faster.
POW_62 = tuple(62 ** power for power in range(512))


def b62encode(raw_bytes,
              base_bytes=ASCII62_BYTES,
              _padding=True):
  """
  Base62 encodes a sequence of raw bytes. Zero-byte sequences are
  preserved by default.

  :param raw_bytes:
      Raw bytes to encode.
  :param base_bytes:
      (Internal) The character set to use. Defaults to ``ASCII62_BYTES``
      that uses natural ASCII order.
  :param _padding:
      (Internal) ``True`` (default) to include prefixed zero-byte sequence
      padding converted to appropriate representation.
  :returns:
      Base-62 encoded bytes.
  """
  return _base.base_encode(raw_bytes, 62, base_bytes, base_bytes[0], _padding)


def b62decode(encoded,
              base_bytes=ASCII62_BYTES,
              base_ords=ASCII62_ORDS):
  """
  Base-62 decodes a sequence of bytes into raw bytes. Whitespace is ignored.

  :param encoded:
      Base-62 encoded bytes.
  :param base_bytes:
      (Internal) The character set to use. Defaults to ``ASCII62_BYTES``
      that uses natural ASCII order.
  :param base_ords:
      (Internal) Ordinal-to-character lookup table for the specified
      character set.
  :returns:
      Raw bytes.
  """
  # Zero byte is represented using the first character in the character set.
  # Adds zero byte prefix padding if required.
  return _base.base_decode(encoded, 62, base_ords, base_bytes[0], POW_62)
