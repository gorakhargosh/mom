#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright (C) 2012 Google, Inc.
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
:module: mom.net.scheme.data
:synopsis: Makes working with Data URL-schemes easier.
:see: http://en.wikipedia.org/wiki/Data_URI_scheme
:see: https://tools.ietf.org/html/rfc2397

.. autofunction:: data_urlencode
.. autofunction:: data_urlparse
"""

from __future__ import absolute_import
from mom._compat import EMPTY_BYTE

try:
  # Python 3.
  from urllib.parse import quote_from_bytes as quote,\
    unquote_to_bytes as unquote
except ImportError:
  # Python 2.5+
  from urllib import quote, unquote

from mom.builtins import is_bytes, b
from mom.net.mimeparse import parse_mime_type
from mom.codec import base64_encode, base64_decode


__all__ = [
  "data_urlencode",
  "data_urlparse",
  ]


def data_urlencode(raw_bytes,
                   mime_type=b('text/plain'),
                   charset=b('US-ASCII'),
                   encoder="base64"):
  """
  Encodes raw bytes into a data URL scheme string.

  :param raw_bytes:
      Raw bytes
  :param mime_type:
      The mime type, e.g. b"text/css" or b"image/png". Default b"text/plain".
  :param charset:
      b"utf-8" if you want the data URL to contain a b"charset=utf-8"
      component. Default b'US-ASCII'. This does not mean however, that your
      raw_bytes will be encoded by this function. You must ensure that
      if you specify, b"utf-8" (or anything else) as the encoding, you
      have encoded your raw data appropriately.
  :param encoder:
      "base64" or None.
  :returns:
      Data URL.
  """
  if not is_bytes(raw_bytes):
    raise TypeError(
      "only raw bytes can be encoded: got %r" % type(raw_bytes).__name__
    )
  if encoder == "base64":
    encode = base64_encode
    codec = b(";base64,")
  else:
    # We want ASCII bytes.
    encode = lambda data: quote(data).encode('ascii')
    codec = b(",")
  mime_type = mime_type or EMPTY_BYTE

  charset = b(";charset=") + charset if charset else EMPTY_BYTE
  encoded = encode(raw_bytes)
  return EMPTY_BYTE.join((b("data:"), mime_type, charset, codec, encoded))


def data_urlparse(data_url):
  """
  Parses a data URL into raw bytes and metadata.

  :param data_url:
      The data url string.
      If a mime-type definition is missing in the metadata,
      "text/plain;charset=US-ASCII" will be used as default mime-type.
  :returns:
      A 2-tuple::
          (bytes, mime_type)

      See :func:`mom.http.mimeparse.parse_mime_type` for what ``mime_type``
      looks like.
  """
  if not is_bytes(data_url):
    raise TypeError(
      "data URLs must be ASCII-encoded bytes: got %r" %
      type(data_url).__name__
    )
  metadata, encoded = data_url.rsplit(b(","), 1)
  _, metadata = metadata.split(b("data:"), 1)
  parts = metadata.rsplit(b(";"), 1)
  if parts[-1] == b("base64"):
    decode = base64_decode
    parts = parts[:-1]
  else:
    decode = unquote
  if not parts or not parts[0]:
    parts = [b("text/plain;charset=US-ASCII")]
  mime_type = parse_mime_type(parts[0])
  raw_bytes = decode(encoded)
  return raw_bytes, mime_type
