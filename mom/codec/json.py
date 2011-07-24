#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Facebook.
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: mom.codec.json
:synopsis: More portable JSON encoding and decoding routines.

.. autofunction:: encode
.. autofunction:: decode
"""

from __future__ import absolute_import
from mom.codec.text import utf8_decode_recursive
from mom.codec._json_compat import json_dumps, json_loads


def encode(obj):
    """
    Encodes a Python value into its equivalent JSON string.

    JSON permits but does not require forward slashes to be escaped.
    This is useful when json data is emitted in a <script> tag
    in HTML, as it prevents </script> tags from prematurely terminating
    the javscript. Some json libraries do this escaping by default,
    although python's standard library does not, so we do it here.

    :see: http://stackoverflow.com/questions/1580647/json-why-are-forward-slashes-escaped
    :param obj:
        Python value.
    :returns:
        JSON string.
    """
    return json_dumps(utf8_decode_recursive(obj)).replace("</", "<\\/")


def decode(encoded):
    """
    Decodes a JSON string into its equivalent Python value.

    :param encoded:
        JSON string.
    :returns:
        Decoded Python value.
    """
    return json_loads(encoded)

