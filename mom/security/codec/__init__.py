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
:module: mom.security.codec
:synopsis: Codecs to encode and decode keys and certificates in various formats.

PEM key decoders
----------------
.. autofunction:: public_key_pem_decode
.. autofunction:: private_key_pem_decode

"""

from __future__ import absolute_import

from mom.security.codec import pem
from mom.security.codec.pem import rsa
from mom.security.codec.pem import x509


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


def public_key_pem_decode(pem_key):
  """
  Decodes a PEM-encoded public key/X.509 certificate string into
  internal representation.

  :param pem_key:
      The PEM-encoded key. Must be one of:
      1. RSA public key.
      2. X.509 certificate.
  :returns:
      A dictionary of key information.
  """
  pem_key = pem_key.strip()
  if pem_key.startswith(pem.CERT_PEM_HEADER):
    key = x509.X509Certificate(pem_key).public_key
  elif pem_key.startswith(pem.PUBLIC_KEY_PEM_HEADER):
    key = rsa.RSAPublicKey(pem_key).public_key
  else:
    raise NotImplementedError("Only PEM X.509 certificates & public "
                              "RSA keys can be read.")
  return key


def private_key_pem_decode(pem_key):
  """
  Decodes a PEM-encoded private key string into internal representation.

  :param pem_key:
      The PEM-encoded RSA private key.
  :returns:
      A dictionary of key information.
  """
  pem_key = pem_key.strip()
  if (pem_key.startswith(pem.PRIVATE_KEY_PEM_HEADER) or
      pem_key.startswith(pem.RSA_PRIVATE_KEY_PEM_HEADER)):
    key = rsa.RSAPrivateKey(pem_key).private_key
  else:
    raise NotImplementedError("Only PEM private RSA keys can be read.")
  return key
