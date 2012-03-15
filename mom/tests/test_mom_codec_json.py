#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc.
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

from __future__ import absolute_import

import unittest2
from mom.codec.json import json_encode, json_decode
from mom.codec.text import utf8_encode
from mom.tests.constants import *

class Test_decode(unittest2.TestCase):
  def test_decode(self):
    # decode accepts unicode only.
    self.assertEqual(json_decode(json_ufoo), ufoo)

  def test_raises_error_when_invalid_type(self):
    self.assertRaises(TypeError, json_decode, json_foo)


class Test_encode(unittest2.TestCase):
  def test_encode(self):
    # json deals with strings, not bytes.
    self.assertEqual(json_decode(json_encode(unicode_value)), unicode_value)

  def test_raises_error_when_invalid_type(self):
    self.assertRaises(TypeError, json_encode, utf8_encode(unicode_value))
    self.assertRaises(TypeError, json_encode, x_byte)

if __name__ == "__main__":
  unittest2.main()
