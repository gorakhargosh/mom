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
:module: mom.security.codec.asn1.rsadsa
:synopsis: ASN.1/DER decoding and encoding for RSA and DSA private keys.

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

# Read unencrypted PKCS#1/PKIX-compliant, PEM & DER encoded private keys.
# Private keys can be generated with "openssl genrsa|gendsa" commands.

from __future__ import absolute_import

from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import univ


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


MAX = 16


class DSAPrivateKey(univ.Sequence):
  """PKIX compliant DSA private key structure"""
  componentType = namedtype.NamedTypes(
      namedtype.NamedType("version", univ.Integer(
          namedValues=namedval.NamedValues(("v1", 0)))),
      namedtype.NamedType("p", univ.Integer()),
      namedtype.NamedType("q", univ.Integer()),
      namedtype.NamedType("g", univ.Integer()),
      namedtype.NamedType("public", univ.Integer()),
      namedtype.NamedType("private", univ.Integer())
      )


class OtherPrimeInfo(univ.Sequence):
  """Other prime information."""
  componentType = namedtype.NamedTypes(
      namedtype.NamedType("prime", univ.Integer()),
      namedtype.NamedType("exponent", univ.Integer()),
      namedtype.NamedType("coefficient", univ.Integer())
      )


class OtherPrimeInfos(univ.SequenceOf):
  """Other prime information."""
  componentType = OtherPrimeInfo()
  subtypeSpec = (univ.SequenceOf.subtypeSpec +
                 constraint.ValueSizeConstraint(1, MAX))


class RSAPrivateKey(univ.Sequence):
  """PKCS#1 compliant RSA private key structure"""
  componentType = namedtype.NamedTypes(
      namedtype.NamedType("version", univ.Integer(
          namedValues=namedval.NamedValues(("two-prime", 0), ("multi", 1)))),
      namedtype.NamedType("modulus", univ.Integer()),
      namedtype.NamedType("publicExponent", univ.Integer()),
      namedtype.NamedType("privateExponent", univ.Integer()),
      namedtype.NamedType("prime1", univ.Integer()),
      namedtype.NamedType("prime2", univ.Integer()),
      namedtype.NamedType("exponent1", univ.Integer()),
      namedtype.NamedType("exponent2", univ.Integer()),
      namedtype.NamedType("coefficient", univ.Integer()),
      namedtype.OptionalNamedType("otherPrimeInfos", OtherPrimeInfos())
      )
