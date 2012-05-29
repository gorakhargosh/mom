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

""":synopsis: More portable JSON encoding and decoding routines.
:module: mom.codec.json

.. autofunction:: json_encode
.. autofunction:: json_decode
"""

from __future__ import absolute_import

from mom import _compat
from mom import builtins
from mom.codec import _json_compat
from mom.codec import text


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


if _compat.HAVE_PYTHON3:
  json_dumps = _json_compat.json_dumps
else:
  json_dumps = lambda o: _json_compat.json_dumps(o).decode("utf-8")


def json_encode(obj):
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
  if builtins.is_bytes(obj):
    raise TypeError("Cannot work with bytes.")
  return json_dumps(text.utf8_decode_recursive(obj)).replace("</", "<\\/")


def json_decode(encoded):
  """
  Decodes a JSON string into its equivalent Python value.

  :param encoded:
      JSON string.
  :returns:
      Decoded Python value.
  """
  if builtins.is_bytes(encoded):
    raise TypeError("Cannot work with bytes.")
  return _json_compat.json_loads(encoded)
