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
:module: mom.security.rsa.pycrypto
:synopsis: PyCrypto RSA implementation wrapper.

.. autoclass:: PrivateKey
.. autoclass:: PublicKey
"""

from __future__ import absolute_import

from Crypto import PublicKey
from mom.security.rsa import keys


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


class PrivateKey(keys.PrivateKey):
  """
  Represents a RSA private key.

  :param encoded_key:
      The encoded key string.
  :param encoding:
      The encoding method of the key. Default PEM.
  """

  def __init__(self, key_info, encoded_key, encoding):
    super(PrivateKey, self).__init__(key_info, encoded_key, encoding)
    key_info_args = (
        self.key_info["modulus"],
        self.key_info["publicExponent"],
        self.key_info["privateExponent"],
        self.key_info["prime1"],
        self.key_info["prime2"],
        #self.key_info["exponent1"],
        #self.key_info["exponent2"],
        #self.key_info["coefficient"],
        )
    self._key = PublicKey.RSA.construct(key_info_args)

  def _sign(self, digest):
    """
    Sign the digest.
    """
    return self.key.sign(digest, "")[0]

  def _verify(self, digest, signature):
    """
    Verify signature against digest signed by public key.
    """
    #public_key = self.key.publickey()
    #return public_key.verify(digest, (signature,))
    return self.key.verify(digest, (signature,))

  @property
  def key(self):
    return self._key

  @property
  def size(self):
    return self.key.n


class PublicKey(keys.PublicKey):
  """
  Represents a RSA public key.

  :param encoded_key:
      The encoded key string.
  :param encoding:
      The encoding method of the key. Default PEM.
  """

  def __init__(self, key_info, encoded_key, encoding):
    super(PublicKey, self).__init__(key_info, encoded_key, encoding)
    key_info_args = (
        self.key_info["modulus"],
        self.key_info["exponent"],
        )
    self._key = PublicKey.RSA.construct(key_info_args)

  def _sign(self, digest):
    """
    Sign the digest.
    """
    return self.key.sign(digest, "")[0]

  def _verify(self, digest, signature):
    """
    Verify signature against digest signed by public key.
    """
    return self.key.verify(digest, (signature,))

  @property
  def key(self):
    return self._key

  @property
  def size(self):
    return self.key.n
