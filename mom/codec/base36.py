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
:module: mom.codec.base36
:synopsis: Base-36 codec.

.. autofunction:: b36encode
.. autofunction:: b36decode

"""

from __future__ import absolute_import

from mom import string
from mom._compat import HAVE_PYTHON3, EMPTY_BYTE
from mom.builtins import byte
from mom.codec._base import base_encode, uint_to_base256

# Follows ASCII order.
ASCII36_BYTES = (string.digits +
                string.ascii_uppercase).encode("ascii")
# Therefore, b'1' represents b'\0'.
if HAVE_PYTHON3:
    ASCII36_BYTES = tuple(byte(x) for x in ASCII36_BYTES)


def b36encode(raw_bytes, base_bytes=ASCII36_BYTES, _padding=True):
    """
    Base-36 encodes a sequence of raw bytes. Zero-byte sequences are
    preserved by default.

    :param raw_bytes:
        Raw bytes to encode.
    :param base_bytes:
        The character set to use. Defaults to ``ASCII36_BYTES``
        that uses natural ASCII order.
    :param _padding:
        (Internal) ``True`` (default) to include prefixed zero-byte sequence
        padding converted to appropriate representation.
    :returns:
        Uppercase (default) base-36 encoded bytes.
    """
    return base_encode(raw_bytes, 36, base_bytes, base_bytes[0], _padding)


def b36decode(encoded, base_bytes=ASCII36_BYTES):
    """
    Base-36 decodes a sequence of bytes into raw bytes.

    Leading, trailing, and internal whitespace is ignored. The case
    of the encoded byte string is also ignored. For example, you may pass
    in ``AbCd`` instead of ``ABCD``.

    :param encoded:
        Case-insensitive base-36 encoded bytes.
    :param base_bytes:
        (Internal) The character set to use. Defaults to ``ASCII36_BYTES``
        that uses natural ASCII order.
    :returns:
        Raw bytes.
    """
    # Ignore whitespace.
    encoded = EMPTY_BYTE.join(encoded.split())
    return uint_to_base256(int(encoded, 36), encoded, base_bytes[0])
