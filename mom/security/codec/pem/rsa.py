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
:module: mom.security.codec.pem.rsa
:synopsis: RSA keys certificates parsing.

.. autoclass:: RSAPublicKey
.. autoclass:: RSAPrivateKey
"""

from __future__ import absolute_import

from mom import builtins
from pyasn1 import type
from pyasn1.codec.der import decoder
from pyasn1.codec.der import encoder

from mom.security.codec import pem
from mom.security.codec.asn1 import rsadsa
from mom.security.codec.asn1.x509 import SubjectPublicKeyInfo
from mom.security.codec.pem.x509 import X509Certificate


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


class RSAPrivateKey(object):
  """
  ASN.1 Syntax::

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

      Version ::= INTEGER
  """
  # http://tools.ietf.org/html/rfc3279 - Section 2.3.1
  _RSA_OID = type.univ.ObjectIdentifier("1.2.840.113549.1.1.1")

  def __init__(self, key):
    self._key = key
    self._key_asn1, self._private_key_asn1 = self.decode_from_pem_key(key)

  def encode(self):
    return self.encode_to_pem_private_key(self._key_asn1)

  @property
  def private_key(self):
    asn = self._private_key_asn1
    return dict(
        version=int(asn.getComponentByName("version")),
        modulus=int(asn.getComponentByName("modulus")),
        publicExponent=int(asn.getComponentByName("publicExponent")),
        privateExponent=int(asn.getComponentByName("privateExponent")),
        prime1=int(asn.getComponentByName("prime1")),
        prime2=int(asn.getComponentByName("prime2")),
        exponent1=int(asn.getComponentByName("exponent1")),
        exponent2=int(asn.getComponentByName("exponent2")),
        coefficient=int(asn.getComponentByName("coefficient")),
        )

  @classmethod
  def decode_from_pem_key(cls, key):
    keyType = rsadsa.RSAPrivateKey()
    try:
      der = pem.pem_to_der_private_rsa_key(key)
    except Exception:
      der = pem.pem_to_der_private_key(key)

    cover_asn1 = decoder.decode(der)[0]
    if len(cover_asn1) < 1:
      raise ValueError("No RSA private key found after ASN.1 decoding.")

    algorithm = cover_asn1[1][0]
    if algorithm != cls._RSA_OID:
      raise ValueError("Only RSA encryption is supported: got algorithm `%r`" %
                       algorithm)
    key_der = builtins.bytes(cover_asn1[2])
    key_asn1 = decoder.decode(key_der, asn1Spec=keyType)[0]
    return cover_asn1, key_asn1

  @classmethod
  def encode_to_pem_private_key(cls, key_asn1):
    return pem.der_to_pem_private_rsa_key(encoder.encode(key_asn1))


TEST_RSA_PRIVATE_KEYS = (
    """
-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALRiMLAh9iimur8V
A7qVvdqxevEuUkW4K+2KdMXmnQbG9Aa7k7eBjK1S+0LYmVjPKlJGNXHDGuy5Fw/d
7rjVJ0BLB+ubPK8iA/Tw3hLQgXMRRGRXXCn8ikfuQfjUS1uZSatdLB81mydBETlJ
hI6GH4twrbDJCR2Bwy/XWXgqgGRzAgMBAAECgYBYWVtleUzavkbrPjy0T5FMou8H
X9u2AC2ry8vD/l7cqedtwMPp9k7TubgNFo+NGvKsl2ynyprOZR1xjQ7WgrgVB+mm
uScOM/5HVceFuGRDhYTCObE+y1kxRloNYXnx3ei1zbeYLPCHdhxRYW7T0qcynNmw
rn05/KO2RLjgQNalsQJBANeA3Q4Nugqy4QBUCEC09SqylT2K9FrrItqL2QKc9v0Z
zO2uwllCbg0dwpVuYPYXYvikNHHg+aCWF+VXsb9rpPsCQQDWR9TT4ORdzoj+Nccn
qkMsDmzt0EfNaAOwHOmVJ2RVBspPcxt5iN4HI7HNeG6U5YsFBb+/GZbgfBT3kpNG
WPTpAkBI+gFhjfJvRw38n3g/+UeAkwMI2TJQS4n8+hid0uus3/zOjDySH3XHCUno
cn1xOJAyZODBo47E+67R4jV1/gzbAkEAklJaspRPXP877NssM5nAZMU0/O/NGCZ+
3jPgDUno6WbJn5cqm8MqWhW1xGkImgRk+fkDBquiq4gPiT898jusgQJAd5Zrr6Q8
AO/0isr/3aa6O6NLQxISLKcPDk2NOccAfS/xOtfOz4sJYM3+Bs4Io9+dZGSDCA54
Lw03eHTNQghS0A==
-----END PRIVATE KEY-----""",
    )


TEST_PRIVATE_KEYS = (0,)


class RSAPublicKey(object):
  """
  ASN.1 Syntax::

      SubjectPublicKeyInfo  ::=  SEQUENCE  {
          algorithm            AlgorithmIdentifier,
          subjectPublicKey     BIT STRING  }
  """
  # http://tools.ietf.org/html/rfc3279 - Section 2.3.1
  _RSA_OID = type.univ.ObjectIdentifier("1.2.840.113549.1.1.1")

  def __init__(self, key):
    self._key = key
    self._key_asn1 = self.decode_from_pem_key(key)

  def encode(self):
    return self.encode_to_pem_key(self._key_asn1)

  @property
  def public_key(self):
    algorithm = self._key_asn1.getComponentByName("algorithm")[0]
    if algorithm != self._RSA_OID:
      raise NotImplementedError("Only RSA encryption is supported: "
                                "got algorithm `%r`" % algorithm)
    modulus, exponent = self.parse_public_rsa_key_bits(
        self._key_asn1.getComponentByName("subjectPublicKey"))
    return dict(
        modulus=modulus,
        exponent=exponent,
        )

  @classmethod
  def parse_public_rsa_key_bits(cls, public_key_bitstring):
    """
    Extracts the RSA modulus and exponent from a RSA public key bit string.

    :param public_key_bitstring:
        ASN.1 public key bit string.
    :returns:
        Tuple of (modulus, exponent)
    """
    return X509Certificate.parse_public_rsa_key_bits(public_key_bitstring)

  @classmethod
  def decode_from_pem_key(cls, key):
    keyType = SubjectPublicKeyInfo()
    der = pem.pem_to_der_public_key(key)
    key_asn1 = decoder.decode(der, asn1Spec=keyType)[0]
    if len(key_asn1) < 1:
      raise ValueError("No RSA public key found after ASN.1 decoding.")
    return key_asn1

  @classmethod
  def encode_to_pem_key(cls, key_asn1):
    return pem.der_to_pem_public_key(encoder.encode(key_asn1))


TEST_PUBLIC_PEM_KEYS = (
    """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC0YjCwIfYoprq/FQO6lb3asXrx
LlJFuCvtinTF5p0GxvQGu5O3gYytUvtC2JlYzypSRjVxwxrsuRcP3e641SdASwfr
mzyvIgP08N4S0IFzEURkV1wp/IpH7kH41EtbmUmrXSwfNZsnQRE5SYSOhh+LcK2w
yQkdgcMv11l4KoBkcwIDAQAB
-----END PUBLIC KEY-----
""",
    )

# pylint: disable-msg=C0301
TEST_PUBLIC_KEYS = (
    (
        126669640320683290646795148731116725859129871317489646670977486626744987251277308188134951784112892388851824395559423655294483477900467304936849324412630428474313221323982004833431306952809970692055204065814102382627007630050419900189287007179961309761697749877767089292033899335453619375029318017462636143731,
        65537),
    )
# pylint: enable-msg=C0301
