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

"""
:module: mom.security.hash
:synopsis: Convenient hashing functions.

SHA-1 digests
-------------
.. autofunction:: sha1_base64_digest
.. autofunction:: sha1_digest
.. autofunction:: sha1_hex_digest

MD5 digests
-----------
.. autofunction:: md5_base64_digest
.. autofunction:: md5_digest
.. autofunction:: md5_hex_digest

HMAC-SHA-1 digests
------------------
.. autofunction:: hmac_sha1_base64_digest
.. autofunction:: hmac_sha1_digest

"""

from __future__ import absolute_import

import hashlib
import hmac

from mom import builtins
from mom import codec


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "hmac_sha1_base64",
    "hmac_sha1_digest",
    "md5_base64_digest",
    "md5_digest",
    "md5_hex_digest",
    "sha1_base64_digest",
    "sha1_digest",
    "sha1_hex_digest",
    ]


def sha1_digest(*inputs):
  """
  Calculates a SHA-1 digest of a variable number of inputs.

  :param inputs:
      A variable number of inputs for which the digest will be calculated.
  :returns:
      A byte string containing the SHA-1 message digest.
  """
  hash_func = hashlib.sha1()
  for i in inputs:
    if not builtins.is_bytes(i):
      raise TypeError("input type must be bytes: got %r" % type(i).__name__)
    hash_func.update(i)
  return hash_func.digest()


def sha1_hex_digest(*inputs):
  """
  Calculates hexadecimal representation of the SHA-1 digest of a variable
  number of inputs.

  :param inputs:
      A variable number of inputs for which the digest will be calculated.
  :returns:
      Hexadecimal representation of the SHA-1 digest.
  """
  return codec.hex_encode(sha1_digest(*inputs))


def sha1_base64_digest(*inputs):
  """
  Calculates Base-64-encoded SHA-1 digest of a variable
  number of inputs.

  :param inputs:
      A variable number of inputs for which the digest will be calculated.
  :returns:
      Base-64-encoded SHA-1 digest.
  """
  return codec.base64_encode(sha1_digest(*inputs))


def md5_digest(*inputs):
  """
  Calculates a MD5 digest of a variable number of inputs.

  :param inputs:
      A variable number of inputs for which the digest will be calculated.
  :returns:
      A byte string containing the MD5 message digest.
  """
  hash_func = hashlib.md5()
  for i in inputs:
    if not builtins.is_bytes(i):
      raise TypeError("input type must be bytes: got %r" % type(i).__name__)
    hash_func.update(i)
  return hash_func.digest()


def md5_hex_digest(*inputs):
  """
  Calculates hexadecimal representation of the MD5 digest of a variable
  number of inputs.

  :param inputs:
      A variable number of inputs for which the digest will be calculated.
  :returns:
      Hexadecimal representation of the MD5 digest.
  """
  return codec.hex_encode(md5_digest(*inputs))


def md5_base64_digest(*inputs):
  """
  Calculates Base-64-encoded MD5 digest of a variable
  number of inputs.

  :param inputs:
      A variable number of inputs for which the digest will be calculated.
  :returns:
      Base-64-encoded MD5 digest.
  """
  return codec.base64_encode(md5_digest(*inputs))


def hmac_sha1_digest(key, data):
  """
  Calculates a HMAC SHA-1 digest.

  :param key:
      The key for the digest.
  :param data:
      The raw bytes data for which the digest will be calculated.
  :returns:
      HMAC SHA-1 Digest.
  """
  if not builtins.is_bytes(data):
    raise TypeError("data type must be bytes: got %r" % type(data).__name__)

  return hmac.new(key, data, hashlib.sha1).digest()


def hmac_sha1_base64_digest(key, data):
  """
  Calculates a base64-encoded HMAC SHA-1 signature.

  :param key:
      The key for the signature.
  :param data:
      The data to be signed.
  :returns:
      Base64-encoded HMAC SHA-1 signature.
  """
  return codec.base64_encode(hmac_sha1_digest(key, data))
