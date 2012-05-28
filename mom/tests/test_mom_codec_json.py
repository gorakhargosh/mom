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

from __future__ import absolute_import

import unittest2

from mom.codec import json
from mom.codec import text
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


class Test_decode(unittest2.TestCase):
  def test_decode(self):
    # decode accepts unicode only.
    self.assertEqual(json.json_decode(constants.JSON_UFOO), constants.UFOO)

  def test_raises_error_when_invalid_type(self):
    self.assertRaises(TypeError, json.json_decode, constants.JSON_FOO)


class Test_encode(unittest2.TestCase):
  def test_encode(self):
    # json deals with strings, not bytes.
    self.assertEqual(json.json_decode(json.json_encode(constants.UNICODE_VALUE)), constants.UNICODE_VALUE)

  def test_raises_error_when_invalid_type(self):
    self.assertRaises(TypeError, json.json_encode, text.utf8_encode(constants.UNICODE_VALUE))
    self.assertRaises(TypeError, json.json_encode, constants.X_BYTE)

if __name__ == "__main__":
  unittest2.main()
