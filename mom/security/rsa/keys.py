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
:module: mom.security.rsa.keys
:synopsis: Implements abstract classes for keys.
"""

from __future__ import absolute_import

from mom import _compat
from mom import builtins
from mom.codec import integer


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b

ZERO_BYTE = _compat.ZERO_BYTE

SHA1_DIGESTINFO = b("""\
\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14""")
SHA1_DIGESTINFO_LEN = len(SHA1_DIGESTINFO)
ZERO_ONE_BYTES = b("\x00\x01")
FF_BYTE = b("\xff")


def pkcs1_v1_5_encode(key_size, data):
  """
  Encodes a key using PKCS1's emsa-pkcs1-v1_5 encoding.

  :author:
      Rick Copeland <rcopeland@geek.net>

  :param key_size:
      RSA key size.
  :param data:
      Data
  :returns:
      A blob of data as large as the key's N, using PKCS1's
      "emsa-pkcs1-v1_5" encoding.
  """
  size = len(integer.uint_to_bytes(key_size))
  filler = FF_BYTE * (size - SHA1_DIGESTINFO_LEN - len(data) - 3)
  return ZERO_ONE_BYTES + filler + ZERO_BYTE + SHA1_DIGESTINFO + data


class Key(object):
  """
  Abstract class representing an encryption key.
  """

  def __init__(self,
               key_info,
               encoded_key,
               encoding,
               *unused_args,
               **unused_kwargs):
    self._key_info = key_info
    self._encoded_key = encoded_key
    self._encoding = encoding

  @property
  def encoded_key(self):
    """
    Returns the original encoded key string.
    """
    return self._encoded_key

  @property
  def encoding(self):
    """
    Returns the original encoding method name of the key.
    """
    return self._encoding

  @property
  def key(self):
    """
    Returns the internal key.
    """
    return NotImplemented

  @property
  def size(self):
    """
    Returns the size of the key (n).
    """
    return NotImplemented

  @property
  def key_info(self):
    """
    Returns the key information parsed from the provided encoded key.
    """
    return self._key_info

  def sign(self, digest):
    """
    Signs a digest with the key.

    :param digest:
        The SHA-1 digest of the data.
    :returns:
        Signature byte string.
    """
    return integer.uint_to_bytes(self._sign(digest))

  def verify(self, digest, signature_bytes):
    """
    Verifies a signature against that computed by signing the provided
    data.

    :param digest:
        The SHA-1 digest of the data.
    :param signature_bytes:
        The signature raw byte string.
    :returns:
        ``True`` if the signature matches; ``False`` otherwise.
    """
    return self._verify(digest, integer.bytes_to_uint(signature_bytes))

  def pkcs1_v1_5_sign(self, digest):
    """
    Signs a base string using your RSA private key.

    :param digest:
        Data digest byte string.
    :returns:
        Signature.
    """
    digest = pkcs1_v1_5_encode(self.size, digest)
    return self.sign(digest)

  def pkcs1_v1_5_verify(self, digest, signature_bytes):
    """
    Verifies the signature against a given base string using your
    public key.

    :param digest:
        The data digest to be signed.
    :param signature_bytes:
        Signature to be verified.
    :returns:
        ``True`` if signature matches; ``False`` if verification fails.
    """
    digest = pkcs1_v1_5_encode(self.size, digest)
    return self.verify(digest, signature_bytes)

  def _sign(self, digest):
    """Sign."""
    raise NotImplementedError("Override this method.")

  def _verify(self, digest, signature):
    """Verify"""
    raise NotImplementedError("Override this method.")


class PrivateKey(Key):
  """
  Abstract private key class.

      RSAPrivateKey ::= SEQUENCE {
        version Version,
        modulus INTEGER, -- n
        publicExponent INTEGER, -- e
        privateExponent INTEGER, -- d
        prime1 INTEGER, -- p
        prime2 INTEGER, -- q
        exponent1 INTEGER, -- d mod (p-1)
        exponent2 INTEGER, -- d mod (q-1)
        coefficient INTEGER -- (inverse of q) mod p }
  """
  pass


class PublicKey(Key):
  """
  Abstract public key class.
  """
  pass
