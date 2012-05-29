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

""":synopsis: Makes working with Data URI-schemes easier.
:module: mom.net.data
:see: http://en.wikipedia.org/wiki/Data_URI_scheme
:see: https://tools.ietf.org/html/rfc2397

.. autofunction:: data_uri_encode
.. autofunction:: data_uri_parse
"""

from __future__ import absolute_import

try:
  # Python 3.
  from urllib.parse import quote_from_bytes as quote
  from urllib.parse import unquote_to_bytes as unquote
except ImportError:
  # Python 2.5+
  from urllib import quote
  from urllib import unquote

from mom import _compat
from mom import builtins
from mom import codec
from mom import mimeparse


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "data_uri_encode",
    "data_uri_parse",
    ]

b = builtins.b

EMPTY_BYTE = _compat.EMPTY_BYTE


def data_uri_encode(raw_bytes,
                    mime_type=b("text/plain"),
                    charset=b("US-ASCII"),
                    encoder="base64"):
  """
  Encodes raw bytes into a data URI scheme string.

  :param raw_bytes:
      Raw bytes
  :param mime_type:
      The mime type, e.g. b"text/css" or b"image/png". Default b"text/plain".
  :param charset:
      b"utf-8" if you want the data URI to contain a b"charset=utf-8"
      component. Default b"US-ASCII". This does not mean however, that your
      raw_bytes will be encoded by this function. You must ensure that
      if you specify, b"utf-8" (or anything else) as the encoding, you
      have encoded your raw data appropriately.
  :param encoder:
      "base64" or None.
  :returns:
      Data URI.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("only raw bytes can be encoded: got %r" %
                    type(raw_bytes).__name__)
  if encoder == "base64":
    encode = codec.base64_encode
    encoding = b(";base64,")
  else:
    # We want ASCII bytes.
    encode = lambda data: quote(data).encode("ascii")
    encoding = b(",")
  mime_type = mime_type or EMPTY_BYTE

  charset = b(";charset=") + charset if charset else EMPTY_BYTE
  encoded = encode(raw_bytes)
  return EMPTY_BYTE.join((b("data:"), mime_type, charset, encoding, encoded))


def data_uri_parse(data_uri):
  """
  Parses a data URI into raw bytes and metadata.

  :param data_uri:
      The data url string.
      If a mime-type definition is missing in the metadata,
      "text/plain;charset=US-ASCII" will be used as default mime-type.
  :returns:
      A 2-tuple::
          (bytes, mime_type)

      See :func:`mom.http.mimeparse.mimeparse.parse_mime_type` for what ``mime_type``
      looks like.
  """
  if not builtins.is_bytes(data_uri):
    raise TypeError("data URIs must be ASCII-encoded bytes: got %r" %
                    type(data_uri).__name__)
  metadata, encoded = data_uri.rsplit(b(","), 1)
  _, metadata = metadata.split(b("data:"), 1)
  parts = metadata.rsplit(b(";"), 1)
  if parts[-1] == b("base64"):
    decode = codec.base64_decode
    parts = parts[:-1]
  else:
    decode = unquote
  if not parts or not parts[0]:
    parts = [b("text/plain;charset=US-ASCII")]
  mime_type = mimeparse.parse_mime_type(parts[0])
  raw_bytes = decode(encoded)
  return raw_bytes, mime_type
