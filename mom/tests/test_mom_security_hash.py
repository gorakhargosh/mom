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

from mom import builtins
from mom import codec
from mom.security import hash
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b

INPUT_MD5_DIGEST = b("\xe8\x0bP\x17\t\x89P\xfcX\xaa\xd8<\x8c\x14\x97\x8e")

INPUT_SHA1_DIGEST = b(
  "\x1f\x8a\xc1\x0f#\xc5\xb5\xbc\x11g\xbd\xa8K\x83>\\\x05zw\xd2")

INPUTS = [b("ab"), b("cd"), b("ef")]

UNICODE_INPUTS = [constants.UNICODE_STRING, constants.UNICODE_STRING2]

# HMAC-SHA1 data.
KEY = b("kd94hf93k423kf44&pfkkdhi9sl3r4s00")

BASE_STRING = b("""GET&\
http%3A%2F%2Fphotos.example.net%2Fphotos&\
file%3Dvacation.jpg%26\
oauth_consumer_key%3Ddpf43f3p2l4k3l03%26\
oauth_nonce%3DchapoH%26\
oauth_signature_method%3DHMAC-SHA1%26\
oauth_timestamp%3D137131202%26\
oauth_token%3Dnnch734d00sl2jdk%26\
size%3Doriginal""")

EXPECTED_HMAC_SHA1_DIGEST = b("""1\xdaPqO"=%#Z\x83\x7fP3,+k.\x8b\xd2""")

EXPECTED_HMAC_SHA1_BASE64_DIGEST = b("MdpQcU8iPSUjWoN/UDMsK2sui9I=")


class Test_sha1_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.sha1_digest(*INPUTS), INPUT_SHA1_DIGEST)

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.sha1_digest, *UNICODE_INPUTS)


class Test_sha1_hex_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.sha1_hex_digest(*INPUTS), codec.hex_encode(INPUT_SHA1_DIGEST))

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.sha1_hex_digest, *UNICODE_INPUTS)


class Test_sha1_base64_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.sha1_base64_digest(*INPUTS),
                     codec.base64_encode(INPUT_SHA1_DIGEST))

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.sha1_base64_digest, *UNICODE_INPUTS)


class Test_md5_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.md5_digest(*INPUTS), INPUT_MD5_DIGEST)

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.md5_digest, *UNICODE_INPUTS)


class Test_md5_hex_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.md5_hex_digest(*INPUTS), codec.hex_encode(INPUT_MD5_DIGEST))


class Test_md5_base64_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.md5_base64_digest(*INPUTS),
                     codec.base64_encode(INPUT_MD5_DIGEST))

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.md5_base64_digest, *UNICODE_INPUTS)


class Test_hmac_sha1_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.hmac_sha1_digest(KEY, BASE_STRING),
                     EXPECTED_HMAC_SHA1_DIGEST)

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.hmac_sha1_digest, *UNICODE_INPUTS)


class Test_hmac_sha1_base64_digest(unittest2.TestCase):
  def test_value(self):
    self.assertEqual(hash.hmac_sha1_base64_digest(KEY, BASE_STRING),
                     EXPECTED_HMAC_SHA1_BASE64_DIGEST)

  def test_raises_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, hash.hmac_sha1_base64_digest, *UNICODE_INPUTS)
