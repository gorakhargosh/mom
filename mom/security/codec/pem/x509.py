#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
:module: mom.security.codec.pem.x509
:synopsis: X.509 certificates parsing.

.. autoclass:: X509Certificate
"""

from __future__ import absolute_import

from mom import builtins
from pyasn1.codec.der import decoder
from pyasn1.codec.der import encoder
from pyasn1.type import univ

from mom.security.codec import pem
from mom.security.codec.asn1.x509 import Certificate


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


def bitarray_to_integer(bitarray):
  return int(builtins.reduce((lambda a, b: (int(a) << 1) + int(b)), bitarray))


class X509Certificate(object):
  # http://tools.ietf.org/html/rfc3279 - Section 2.3.1
  _RSA_OID = univ.ObjectIdentifier("1.2.840.113549.1.1.1")

  def __init__(self, certificate):
    self._certificate = certificate
    self._certificate_asn1 = self.decode_from_pem_certificate(certificate)

  def encode(self):
    return self.encode_to_pem_certificate(self._certificate_asn1)

  @property
  def public_key(self):
    spki = self.subject_public_key_info
    algorithm = spki.getComponentByName("algorithm")[0]
    if algorithm != self._RSA_OID:
      raise NotImplementedError("Only RSA encryption is supported: "
                                "got algorithm `%r`" % algorithm)
    modulus, exponent = self.parse_public_rsa_key_bits(
        spki.getComponentByName("subjectPublicKey"))
    return dict(
        modulus=modulus,
        exponent=exponent,
        )

  @property
  def tbs_certificate(self):
    return self._certificate_asn1.getComponentByName("tbsCertificate")

  @property
  def subject_public_key_info(self):
    return self.tbs_certificate.getComponentByName("subjectPublicKeyInfo")

  @classmethod
  def parse_public_rsa_key_bits(cls, public_key_bitstring):
    """
    Extracts the RSA modulus and exponent from a RSA public key bit string.

    :author: Arne Roomann-Kurrik     <kurrik@gmail.com>
    :param public_key_bitstring:
        ASN.1 public key bit string.
    :returns:
        Tuple of (modulus, exponent)
    """
    public_key_hex = hex(bitarray_to_integer(public_key_bitstring))[2:-1]
    public_key_asn1 = decoder.decode(public_key_hex.decode("hex"))

    if len(public_key_asn1) < 1:
      raise ValueError("Problem ASN.1 decoding public key bytes")

    if len(public_key_asn1[0]) < 2:
      raise ValueError("Couldn't obtain RSA modulus and "
                       "exponent from public key.")

    return int(public_key_asn1[0][0]), int(public_key_asn1[0][1])

  @classmethod
  def decode_from_pem_certificate(cls, certificate):
    certType = Certificate()
    der = pem.pem_to_der_certificate(certificate)
    cert_asn1 = decoder.decode(der, asn1Spec=certType)[0]
    if len(cert_asn1) < 1:
      raise ValueError("No X.509 certificate found after ASN.1 decoding.")
    return cert_asn1

  @classmethod
  def encode_to_pem_certificate(cls, certificate_asn1):
    return pem.der_to_pem_certificate(encoder.encode(certificate_asn1))


TEST_CERTIFICATES = (
    """
-----BEGIN CERTIFICATE-----
MIIDHzCCAoigAwIBAgIQZMuxK+KKS5wF/rjXp3z/KTANBgkqhkiG9w0BAQUFADCB
hzELMAkGA1UEBhMCWkExIjAgBgNVBAgTGUZPUiBURVNUSU5HIFBVUlBPU0VTIE9O
TFkxHTAbBgNVBAoTFFRoYXd0ZSBDZXJ0aWZpY2F0aW9uMRcwFQYDVQQLEw5URVNU
IFRFU1QgVEVTVDEcMBoGA1UEAxMTVGhhd3RlIFRlc3QgQ0EgUm9vdDAeFw0wODAz
MjYwMDEyMDdaFw0wODA0MTYwMDEyMDdaMIGuMRcwFQYDVQQKEw5oaTVtb2R1bGVz
LmNvbTEZMBcGA1UECxMQRG9tYWluIFZhbGlkYXRlZDE7MDkGA1UECxMyR28gdG8g
aHR0cHM6Ly93d3cudGhhd3RlLmNvbS9yZXBvc2l0b3J5L2luZGV4Lmh0bWwxIjAg
BgNVBAsTGVRoYXd0ZSBTU0wxMjMgY2VydGlmaWNhdGUxFzAVBgNVBAMTDmhpNW1v
ZHVsZXMuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCZgdrYsECeGO/Y
srDfaO/vIyMq7+DYdAmImzwg35wnti3Dr3B6kS6OeRiBAIUTvdZXX3XitJFxVlDF
H/PbRimm0d3eQvSfW3+0xIhF9C3E9QFj6LWBz6bBlh5p0pSXygAZ9AXR1OMM2lDR
R9hwQp1YVjzJk3hYW2qD591auROQvwIDAQABo2MwYTAMBgNVHRMBAf8EAjAAMB0G
A1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAyBggrBgEFBQcBAQQmMCQwIgYI
KwYBBQUHMAGGFmh0dHA6Ly9vY3NwLnRoYXd0ZS5jb20wDQYJKoZIhvcNAQEFBQAD
gYEABdPtdX56mPwSfPMzgSLH7RueLZi5HXqW2krojWsOv3VFnayQKuzXdy5DZrMY
/tI2AUPXicvBW3GjTfSKmUNvsOXUIC8az3K3iTs1KKekUaidLRlaRZIO0FVEJH5u
gO9HqAcXxrx99/3agvAVTKAFBFJtiWD1i1LkYeqKrPQOPo8=
-----END CERTIFICATE-----""",
    # OAuth 1.0 test case.
    """
-----BEGIN CERTIFICATE-----
MIIBpjCCAQ+gAwIBAgIBATANBgkqhkiG9w0BAQUFADAZMRcwFQYDVQQDDA5UZXN0
IFByaW5jaXBhbDAeFw03MDAxMDEwODAwMDBaFw0zODEyMzEwODAwMDBaMBkxFzAV
BgNVBAMMDlRlc3QgUHJpbmNpcGFsMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKB
gQC0YjCwIfYoprq/FQO6lb3asXrxLlJFuCvtinTF5p0GxvQGu5O3gYytUvtC2JlY
zypSRjVxwxrsuRcP3e641SdASwfrmzyvIgP08N4S0IFzEURkV1wp/IpH7kH41Etb
mUmrXSwfNZsnQRE5SYSOhh+LcK2wyQkdgcMv11l4KoBkcwIDAQABMA0GCSqGSIb3
DQEBBQUAA4GBAGZLPEuJ5SiJ2ryq+CmEGOXfvlTtEL2nuGtr9PewxkgnOjZpUy+d
4TvuXJbNQc8f4AMWL/tO9w0Fk80rWKp9ea8/df4qMq5qlFWlx6yOLQxumNOmECKb
WpkUQDIDJEoFUzKMVuJf4KO/FJ345+BNLGgbJ6WujreoM1X/gYfdnJ/J
-----END CERTIFICATE-----"""
    )

# pylint: disable-msg=C0301
TEST_PUBLIC_KEYS = (
    (126669640320683290646795148731116725859129871317489646670977486626744987251277308188134951784112892388851824395559423655294483477900467304936849324412630428474313221323982004833431306952809970692055204065814102382627007630050419900189287007179961309761697749877767089292033899335453619375029318017462636143731,
     65537),
    (107796453724127466436509607023300853823148671381186269695418299876688451275586863210602390910751033980089586659623213376886118860658943925516474941572267483546063696504972995209865305723609365133051508378295496906014585319487318439832859683449024036092870160203868280352941275868168286901714810544167406768319,
     65537),
    )
# pylint: enable-msg=C0301
