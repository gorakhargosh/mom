#!/usr/bin/env python
# -*- coding: utf8 -*-
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
:module: mom.net.datauri
:synopsis: Makes working with Data-URI schemes easier.
:see: http://en.wikipedia.org/wiki/Data_URI_scheme

.. autofunction:: datauri_encode
.. autofunction:: datauri_decode
"""

from __future__ import absolute_import
from mom.builtins import is_bytes, b

try:
    # Python 3.
    from urllib.parse import quote_from_bytes as quote, \
        unquote_to_bytes as unquote
    from functools import partial
except ImportError:
    # Python 2.5+
    from urllib import quote, unquote

from mom.net.http.mimeparse import parse_mime_type
from mom.codec import base64_encode, base64_decode


__all__ = [
    "datauri_encode",
    "datauri_decode",
]


def datauri_encode(raw_bytes,
                   mime_type=b('text/plain'),
                   charset=b('US-ASCII'),
                   encoder="base64"):
    """
    Encodes raw bytes into a data-uri scheme string.

    :param raw_bytes:
        Raw bytes
    :param mime_type:
        The mime type, e.g. "text/css" or "image/png". Default "text/plain".
    :param charset:
        "utf-8" if you want the data-uri to contain a "charset=utf-8"
        component. Default 'US-ASCII'
    :param encoder:
        "base64" or None.
    :returns:
        Data URI.
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
        encode = quote
        codec = b(",")
    mime_type = mime_type or b("")

    charset = b(";charset=") + charset if charset else b("")
    encoded = encode(raw_bytes)
    return b('').join((b("data:"), mime_type, charset, codec, encoded))


def datauri_decode(data_uri):
    """
    Decodes a data-uri into raw bytes and metadata.

    :param data_uri:
        The data-uri string.
        If a mime-type definition is missing in the metadata,
        "text/plain;charset=US-ASCII" will be used as default mime-type.
    :returns:
        A 2-tuple::
            (bytes, mime_type)

        See :func:`mom.http.mimeparse.parse_mime_type` for what ``mime_type``
        looks like.
    """
    metadata, encoded = data_uri.rsplit(b(","), 1)
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
