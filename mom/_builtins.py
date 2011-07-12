#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Core builtins.
#
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
:module: mom._builtins
:synopsis: Deals with a lot of cross-version issues.

Should not be used in public code. Use the wrappers in mom.
"""

from __future__ import absolute_import

try:
    # Python 2.6 or higher.
    bytes_type = bytes
except NameError:
    # Python 2.5
    bytes_type = str

try:
    # Not Python3
    unicode_type = unicode
    basestring_type = basestring
except NameError:
    # Python3.
    unicode_type = str
    basestring_type = (str, bytes)


