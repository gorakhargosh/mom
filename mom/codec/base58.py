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
:module: mom.codec.base58
:synopsis: Base-58 representation for unambiguous display & compact human-input.

Where should you use base-58?
-----------------------------
Base-85 representation is 7 bit-ASCII safe, MIME-safe, URL-safe, HTTP
cookie-safe, and **human being-safe**. Base-58 representation can:

* be readable and editable by a human being;
* safely and compactly represent numbers;
* contain only alphanumeric characters (omitting a few with visually-
  ambiguously glyphs--namely, "0OIl");
* not contain punctuation characters.

Example scenarios where base-58 encoding may be used:

* Visually-legible account numbers
* Shortened URL paths
* OAuth verification codes
* Unambiguously printable and displayable key codes (for example,
  net-banking PINs, verification codes sent via SMS, etc.)
* Bitcoin decentralized crypto-currency addresses
* CAPTCHAs
* Revision control changset identifiers

In general, use base-58 in any 7-bit ASCII-safe compact communication where
both human beings, paper, and communication devices may be significantly
involved.

The default base-58 character set is ``[0-9A-Za-z]`` (base-62) with some
characters omitted to make them visually-legible and unambiguously printable.
The characters omitted are:

* 0 (ASCII NUMERAL ZERO)
* O (UPPERCASE ASCII ALPHABET O)
* I (UPPERCASE ASCII ALPHABET I)
* l (LOWERCASE ASCII ALPHABET L)

A practical example (shortened static asset URLs):
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
reduced to::

    http://s.example.com/js/3HzsRcRETLZ3qFgDzG1QE7CJJNeh/file.js

The first 12 characters of a SHA-1 hash are sufficiently strong for serving
static assets while minimizing collision overhead in the context of a
small-to-medium size Website and considering these are URLs for static served
assets that can change over periods of time. You may want to consider
using the full hash for large-scale Websites. Therefore, we can shorten the
original asset URL to::

    http://s.example.com/js/a497f210fc9c/file.js

which can then be reduced utilizing base-58 or base-62 encoding to::

    http://s.example.com/js/2QxqmqiFm/file.js

This is a much shorter URL than the original. Notice that we have not
renamed the file ``filename.js`` to ``2QxqmqiFm.js`` because that would
cause an unnecessary explosion of files on the server as new files would
be generated every time the source files changed. Instead, we have
chosen to make use of Web server URL-rewriting rules to strip the hashed
identifier and serve the file fresh as it is on the server file system. The
hashed-identifier is not part of the query string for this asset URL because
certain proxies do not cache files served from URLs that include query
strings. If you wish to support versioned assets, however, then you
may need to rename files to their hashed identifiers instead.

The following benefits are therefore achieved::

* Client-side caching is fully utilized
* The number of HTTP requests sent to Web servers by clients is reduced.
* When assets change, so do their SHA-1 hashed identifiers, and hence their
  asset URLs.
* Shorter URLs also implies that fewer bytes are transferred in HTTP responses.
* Bandwidth consumption is reduced by a noticeably large factor.

Essentially, URLs shortened using base-85 encoding can result in a faster
Web-browsing experience for end-users.

Functions
---------
.. autofunction:: b58encode
.. autofunction:: b58decode
"""


from __future__ import absolute_import, division

import re
from mom._compat import have_python3
from mom.builtins import byte, is_bytes, b
from mom.codec import bytes_to_integer
from mom.functional import leading


ZERO_BYTE = byte(0)
WHITESPACE_PATTERN = re.compile(b(r'(\s)*'), re.MULTILINE)

# Follows ASCII order.
ASCII58_CHARSET = ("123456789"
                  "ABCDEFGHJKLMNPQRSTUVWXYZ"
                  "abcdefghijkmnopqrstuvwxyz").encode("ascii")
# Therefore, b'1' represents b'\0'.
ASCII58_ORDS = dict((x, i) for i, x in enumerate(ASCII58_CHARSET))

# Does not follow ASCII order.
FLICKR58_CHARSET = ("123456789"
                  "abcdefghijkmnopqrstuvwxyz"
                  "ABCDEFGHJKLMNPQRSTUVWXYZ").encode("ascii")
# Therefore, b'1' represents b'\0'.
FLICKR58_ORDS = dict((x, i) for i, x in enumerate(FLICKR58_CHARSET))

if have_python3:
    ASCII58_CHARSET = tuple(byte(x) for x in ASCII58_CHARSET)
    FLICKR58_CHARSET = tuple(byte(x) for x in FLICKR58_CHARSET)


def b58encode(raw_bytes, _charset=ASCII58_CHARSET, _padding=True):
    """
    Base58 encodes a sequence of raw bytes. Zero-byte sequences are
    preserved by default.

    :param raw_bytes:
        Raw bytes to encode.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII58_CHARSET``
        that uses natural ASCII order.
    :param _padding:
        (Internal) ``True`` (default) to include prefixed zero-byte sequence
        padding converted to appropriate representation.
    :returns:
        Base-58 encoded bytes.
    """
    if not is_bytes(raw_bytes):
        raise TypeError("data must be raw bytes: got %r" %
                        type(raw_bytes).__name__)
    number = bytes_to_integer(raw_bytes)
    encoded = b('')
    while number > 0:
        number, remainder = divmod(number, 58)
        encoded = _charset[remainder] + encoded
    if _padding:
        zero_leading = leading(lambda w: w == ZERO_BYTE[0], raw_bytes)
        encoded = (_charset[0] * zero_leading) + encoded
    return encoded


def b58decode(encoded,
              _charset=ASCII58_CHARSET,
              _lookup=ASCII58_ORDS,
              _ignore_pattern=WHITESPACE_PATTERN):
    """
    Base-58 decodes a sequence of bytes into raw bytes. Whitespace is ignored.
    
    :param encoded:
        Base-58 encoded bytes.
    :param _charset:
        (Internal) The character set to use. Defaults to ``ASCII58_CHARSET``
        that uses natural ASCII order.
    :param _lookup:
        (Internal) Ordinal-to-character lookup table for the specified
        character set.
    :param _ignore_pattern:
        (Internal) Regular expression pattern to ignore bytes within encoded
        byte data.
    :returns:
        Raw bytes.
    """
    if not is_bytes(encoded):
        raise TypeError("encoded data must be bytes: got %r" %
                        type(encoded).__name__)

    # Ignore whitespace.
    if _ignore_pattern:
        encoded = re.sub(_ignore_pattern, b(''), encoded)

    pass
