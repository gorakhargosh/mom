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

from mom import _compat


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


if not _compat.HAVE_PYTHON3:
  import unittest2

  from mom.security.codec import pem


  PRIVATE_KEY = """
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
-----END PRIVATE KEY-----"""

  PRIVATE_RSA_KEY = """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

  PRIVATE_KEY_DER = """0\x82\x02v\x02\x01\x000\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x04\x82\x02`0\x82\x02\\\x02\x01\x00\x02\x81\x81\x00\xb4b0\xb0!\xf6(\xa6\xba\xbf\x15\x03\xba\x95\xbd\xda\xb1z\xf1.RE\xb8+\xed\x8at\xc5\xe6\x9d\x06\xc6\xf4\x06\xbb\x93\xb7\x81\x8c\xadR\xfbB\xd8\x99X\xcf*RF5q\xc3\x1a\xec\xb9\x17\x0f\xdd\xee\xb8\xd5\'@K\x07\xeb\x9b<\xaf"\x03\xf4\xf0\xde\x12\xd0\x81s\x11DdW\\)\xfc\x8aG\xeeA\xf8\xd4K[\x99I\xab],\x1f5\x9b\'A\x119I\x84\x8e\x86\x1f\x8bp\xad\xb0\xc9\t\x1d\x81\xc3/\xd7Yx*\x80ds\x02\x03\x01\x00\x01\x02\x81\x80XY[eyL\xda\xbeF\xeb><\xb4O\x91L\xa2\xef\x07_\xdb\xb6\x00-\xab\xcb\xcb\xc3\xfe^\xdc\xa9\xe7m\xc0\xc3\xe9\xf6N\xd3\xb9\xb8\r\x16\x8f\x8d\x1a\xf2\xac\x97l\xa7\xca\x9a\xcee\x1dq\x8d\x0e\xd6\x82\xb8\x15\x07\xe9\xa6\xb9\'\x0e3\xfeGU\xc7\x85\xb8dC\x85\x84\xc29\xb1>\xcbY1FZ\ray\xf1\xdd\xe8\xb5\xcd\xb7\x98,\xf0\x87v\x1cQan\xd3\xd2\xa72\x9c\xd9\xb0\xae}9\xfc\xa3\xb6D\xb8\xe0@\xd6\xa5\xb1\x02A\x00\xd7\x80\xdd\x0e\r\xba\n\xb2\xe1\x00T\x08@\xb4\xf5*\xb2\x95=\x8a\xf4Z\xeb"\xda\x8b\xd9\x02\x9c\xf6\xfd\x19\xcc\xed\xae\xc2YBn\r\x1d\xc2\x95n`\xf6\x17b\xf8\xa44q\xe0\xf9\xa0\x96\x17\xe5W\xb1\xbfk\xa4\xfb\x02A\x00\xd6G\xd4\xd3\xe0\xe4]\xce\x88\xfe5\xc7\'\xaaC,\x0el\xed\xd0G\xcdh\x03\xb0\x1c\xe9\x95\'dU\x06\xcaOs\x1by\x88\xde\x07#\xb1\xcdxn\x94\xe5\x8b\x05\x05\xbf\xbf\x19\x96\xe0|\x14\xf7\x92\x93FX\xf4\xe9\x02@H\xfa\x01a\x8d\xf2oG\r\xfc\x9fx?\xf9G\x80\x93\x03\x08\xd92PK\x89\xfc\xfa\x18\x9d\xd2\xeb\xac\xdf\xfc\xce\x8c<\x92\x1fu\xc7\tI\xe8r}q8\x902d\xe0\xc1\xa3\x8e\xc4\xfb\xae\xd1\xe25u\xfe\x0c\xdb\x02A\x00\x92RZ\xb2\x94O\\\xff;\xec\xdb,3\x99\xc0d\xc54\xfc\xef\xcd\x18&~\xde3\xe0\rI\xe8\xe9f\xc9\x9f\x97*\x9b\xc3*Z\x15\xb5\xc4i\x08\x9a\x04d\xf9\xf9\x03\x06\xab\xa2\xab\x88\x0f\x89?=\xf2;\xac\x81\x02@w\x96k\xaf\xa4<\x00\xef\xf4\x8a\xca\xff\xdd\xa6\xba;\xa3KC\x12\x12,\xa7\x0f\x0eM\x8d9\xc7\x00}/\xf1:\xd7\xce\xcf\x8b\t`\xcd\xfe\x06\xce\x08\xa3\xdf\x9ddd\x83\x08\x0ex/\r7xt\xcdB\x08R\xd0"""

  CERTIFICATE = """\
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

  CERTIFICATE_DER = """0\x82\x01\xa60\x82\x01\x0f\xa0\x03\x02\x01\x02\x02\x01\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000\x191\x170\x15\x06\x03U\x04\x03\x0c\x0eTest Principal0\x1e\x17\r700101080000Z\x17\r381231080000Z0\x191\x170\x15\x06\x03U\x04\x03\x0c\x0eTest Principal0\x81\x9f0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x81\x8d\x000\x81\x89\x02\x81\x81\x00\xb4b0\xb0!\xf6(\xa6\xba\xbf\x15\x03\xba\x95\xbd\xda\xb1z\xf1.RE\xb8+\xed\x8at\xc5\xe6\x9d\x06\xc6\xf4\x06\xbb\x93\xb7\x81\x8c\xadR\xfbB\xd8\x99X\xcf*RF5q\xc3\x1a\xec\xb9\x17\x0f\xdd\xee\xb8\xd5\'@K\x07\xeb\x9b<\xaf"\x03\xf4\xf0\xde\x12\xd0\x81s\x11DdW\\)\xfc\x8aG\xeeA\xf8\xd4K[\x99I\xab],\x1f5\x9b\'A\x119I\x84\x8e\x86\x1f\x8bp\xad\xb0\xc9\t\x1d\x81\xc3/\xd7Yx*\x80ds\x02\x03\x01\x00\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x00\x03\x81\x81\x00fK<K\x89\xe5(\x89\xda\xbc\xaa\xf8)\x84\x18\xe5\xdf\xbeT\xed\x10\xbd\xa7\xb8kk\xf4\xf7\xb0\xc6H\':6iS/\x9d\xe1;\xee\\\x96\xcdA\xcf\x1f\xe0\x03\x16/\xfbN\xf7\r\x05\x93\xcd+X\xaa}y\xaf?u\xfe*2\xaej\x94U\xa5\xc7\xac\x8e-\x0cn\x98\xd3\xa6\x10"\x9bZ\x99\x14@2\x03$J\x05S2\x8cV\xe2_\xe0\xa3\xbf\x14\x9d\xf8\xe7\xe0M,h\x1b\'\xa5\xae\x8e\xb7\xa83U\xff\x81\x87\xdd\x9c\x9f\xc9"""

  PUBLIC_KEY = """\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC0YjCwIfYoprq/FQO6lb3asXrx
LlJFuCvtinTF5p0GxvQGu5O3gYytUvtC2JlYzypSRjVxwxrsuRcP3e641SdASwfr
mzyvIgP08N4S0IFzEURkV1wp/IpH7kH41EtbmUmrXSwfNZsnQRE5SYSOhh+LcK2w
yQkdgcMv11l4KoBkcwIDAQAB
-----END PUBLIC KEY-----"""

  PUBLIC_KEY_DER = """0\x81\x9f0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x81\x8d\x000\x81\x89\x02\x81\x81\x00\xb4b0\xb0!\xf6(\xa6\xba\xbf\x15\x03\xba\x95\xbd\xda\xb1z\xf1.RE\xb8+\xed\x8at\xc5\xe6\x9d\x06\xc6\xf4\x06\xbb\x93\xb7\x81\x8c\xadR\xfbB\xd8\x99X\xcf*RF5q\xc3\x1a\xec\xb9\x17\x0f\xdd\xee\xb8\xd5\'@K\x07\xeb\x9b<\xaf"\x03\xf4\xf0\xde\x12\xd0\x81s\x11DdW\\)\xfc\x8aG\xeeA\xf8\xd4K[\x99I\xab],\x1f5\x9b\'A\x119I\x84\x8e\x86\x1f\x8bp\xad\xb0\xc9\t\x1d\x81\xc3/\xd7Yx*\x80ds\x02\x03\x01\x00\x01"""

  CERTIFICATE_WITHOUT_SUFFIX = """\
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
"""

  CERTIFICATE_WITHOUT_PREFIX = """\
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


  class Test_pem_to_der_private_key(unittest2.TestCase):
    def test_decode(self):
      self.assertEqual(pem.pem_to_der_private_key(PRIVATE_KEY),
                       PRIVATE_KEY_DER)

  class Test_pem_to_der_private_rsa_key(unittest2.TestCase):
    def test_decode(self):
      self.assertEqual(pem.pem_to_der_private_rsa_key(PRIVATE_RSA_KEY),
                       PRIVATE_KEY_DER)

  class Test_pem_to_der_public_key(unittest2.TestCase):
    def test_decode(self):
      self.assertEqual(pem.pem_to_der_public_key(PUBLIC_KEY), PUBLIC_KEY_DER)

  class Test_pem_to_der_certificate(unittest2.TestCase):
    def test_decode(self):
      self.assertEqual(pem.pem_to_der_certificate(CERTIFICATE), CERTIFICATE_DER)

  class Test_pem_der_codec(unittest2.TestCase):
    def test_codec_identity(self):
      self.assertEqual(pem.der_to_pem_public_key(
        pem.pem_to_der_public_key(PUBLIC_KEY)).strip(), PUBLIC_KEY.strip())
      self.assertEqual(pem.der_to_pem_certificate(
        pem.pem_to_der_certificate(CERTIFICATE)).strip(), CERTIFICATE.strip())
      self.assertEqual(pem.der_to_pem_private_key(
        pem.pem_to_der_private_key(PRIVATE_KEY)).strip(), PRIVATE_KEY.strip())
      self.assertEqual(pem.der_to_pem_private_rsa_key(
        pem.pem_to_der_private_rsa_key(PRIVATE_RSA_KEY)).strip(),
                       PRIVATE_RSA_KEY.strip())

    def test_ValueError_on_missing_suffix(self):
      self.assertRaises(ValueError, pem.pem_to_der_certificate,
                        CERTIFICATE_WITHOUT_SUFFIX)

    def test_ValueError_on_missing_prefix(self):
      self.assertRaises(ValueError, pem.pem_to_der_certificate,
                        CERTIFICATE_WITHOUT_PREFIX)

  class Test_cert_time_in_seconds(unittest2.TestCase):
    def test_format(self):
      self.assertEqual(pem.cert_time_to_seconds("Jul 17 18:24:41 2011 GMT"),
                       1310907281.0)
