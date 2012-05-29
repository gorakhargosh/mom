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

""":synopsis: Library compatibility.
:module: mom.codec._json_compat
"""

from __future__ import absolute_import

from mom.codec import text


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
except (AssertionError, ImportError):
  try:
    # Try to use the simplejson library.
    import simplejson as json

    def json_loads(value):
      """Wrapper to decode JSON."""
      return json.loads(text.utf8_decode(value))

    def json_dumps(value):
      """Wrapper to encode JSON."""
      return json.dumps(value)
  except ImportError:
    try:
      # For Google App Engine.
      from django.utils import simplejson as json

      def json_loads(value):
        """Wrapper to decode JSON."""
        return json.loads(text.utf8_decode(value))

      def json_dumps(value):
        """Wrapper to encode JSON."""
        return json.dumps(value)
    except ImportError:

      def json_loads(unused_value):
        """Wrapper to decode JSON."""
        raise NotImplementedError("A JSON parser is required, e.g., "
                                  "simplejson at "
                                  "http://pypi.python.org/pypi/simplejson/")

      json_dumps = json_loads


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"
