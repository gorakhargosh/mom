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
from mom.builtins import bytes_to_unicode_recursive, bytes_to_unicode

try:
    # Built-in JSON library.
    import json
    assert hasattr(json, "loads") and hasattr(json, "dumps")

    def json_loads(value):
        """Wrapper to decode JSON."""
        return json.loads(value)
    def json_dumps(value):
        """Wrapper to encode JSON."""
        return json.dumps(value)
except Exception:
    try:
        # Try to use the simplejson library.
        import simplejson as json
        def json_loads(value):
            """Wrapper to decode JSON."""
            return json.loads(bytes_to_unicode(value))
        def json_dumps(value):
            """Wrapper to encode JSON."""
            return json.dumps(value)
    except ImportError:
        try:
            # For Google App Engine.
            from django.utils import simplejson as json
            def json_loads(value):
                """Wrapper to decode JSON."""
                return json.loads(bytes_to_unicode(value))
            def json_dumps(value):
                """Wrapper to encode JSON."""
                return json.dumps(value)
        except ImportError:
            def json_loads(s):
                """Wrapper to decode JSON."""
                raise NotImplementedError(
                    "A JSON parser is required, e.g., simplejson at "
                    "http://pypi.python.org/pypi/simplejson/")
            json_dumps = json_loads


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
    return json_dumps(bytes_to_unicode_recursive(obj)).replace("</", "<\\/")


def decode(encoded):
    """
    Decodes a JSON string into its equivalent Python value.

    :param encoded:
        JSON string.
    :returns:
        Decoded Python value.
    """
    return json_loads(encoded)

