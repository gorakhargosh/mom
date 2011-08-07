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
:module: mom.net.http.datauri
:synopsis: Makes working with Data-URI schemes easier.
:see: http://en.wikipedia.org/wiki/Data_URI_scheme

.. autofunction:: datauri_encode
.. autofunction:: datauri_decode
"""

from __future__ import absolute_import

try:
    # Python 3.
    from urllib.parse import quote_plus, unquote_plus
except ImportError:
    # Python 2.5+
    from urllib import quote_plus, unquote_plus

from mom.net.http.mimeparse import parse_mime_type
from mom.codec import base64_encode, base64_decode


__all__ = [
    "datauri_encode",
    "datauri_decode",
]


def datauri_encode(raw_bytes,
                   mime_type='text/plain',
                   charset='US-ASCII',
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
    if encoder == "base64":
        encode = base64_encode
        codec = ";base64,"
    else:
        encode = quote_plus
        codec = ","
    mime_type = mime_type or ""

    charset = ";charset=" + charset if charset else ""
    data = encode(raw_bytes)
    return ''.join(("data:", mime_type, charset, codec, data))


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
    metadata, data = data_uri.rsplit(",", 1)
    _, metadata = metadata.split("data:", 1)
    parts = metadata.rsplit(";", 1)
    if parts[-1] == "base64":
        decode = base64_decode
        parts = parts[:-1]
    else:
        decode = unquote_plus
    raw_bytes = decode(data)
    if not parts or not parts[0]:
        parts = ["text/plain;charset=US-ASCII"]
    mime_type = parse_mime_type(parts[0])
    return raw_bytes, mime_type
