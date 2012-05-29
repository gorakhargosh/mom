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

  from mom.security import codec
  from mom.tests import test_mom_security_codec_pem
  from pyasn1.error import SubstrateUnderrunError

  PRIVATE_KEY = test_mom_security_codec_pem.PRIVATE_KEY
  PUBLIC_KEY = test_mom_security_codec_pem.PUBLIC_KEY
  CERTIFICATE = test_mom_security_codec_pem.CERTIFICATE


  PRIVATE_KEY_DECODED = {
    "coefficient": 6263309813628295397107400643432350851721956841159071320214251700452060114366343340155171376140395643703716902907125213041289999255650845147022475122987728
    ,
    "exponent1": 3822093812252919639580364669476622791207236895386024347699409509479994135036937701181018285803044904622661246121518351058015126950695870028830018671348955
    ,
    "exponent2": 7663489069477237650921539283392475888713419180290444291436091339476564305244313755637841647317265985369733335137037584327090234814990380934645339788127361
    ,
    "modulus": 126669640320683290646795148731116725859129871317489646670977486626744987251277308188134951784112892388851824395559423655294483477900467304936849324412630428474313221323982004833431306952809970692055204065814102382627007630050419900189287007179961309761697749877767089292033899335453619375029318017462636143731
    ,
    "prime1": 11286827475943747777190031061302637221977591331181628336645618033739934917672950305154796350050653535540726809672687251533778100075147804897014055497868539
    ,
    "prime2": 11222785197227603770299537898098245716808441026517135491773487623240874036306681055667617716308358528851810278532267433054266015352833942512376019701789929
    ,
    "privateExponent": 62040813352054762141560911837894865241805540983262892236320038195704523334585811305536472791220833007152520122572927352660293042970033721732272250245220614325662189223664266754362230405256661079259461762606569479150278994918928461540639220666195615058859592860192738580413744039865489807787295497665583162801
    ,
    "publicExponent": 65537,
    "version": 0,
    }

  PUBLIC_KEY_DECODED = {
    "exponent": 65537,
    "modulus": 126669640320683290646795148731116725859129871317489646670977486626744987251277308188134951784112892388851824395559423655294483477900467304936849324412630428474313221323982004833431306952809970692055204065814102382627007630050419900189287007179961309761697749877767089292033899335453619375029318017462636143731
    ,
    }

  JUNK = """\
eqp1iAIIh89/WHE3rfwNVPeBl2ZU9ywUk9vvhUot8yuCrlprR6avhfIkUm1LCSqi
tqEwJqVmtJHmkM4VDFr6uiLknVaJYJ+SvK0mRlml5ACre1FH1rMBgvs3G+cvPNA9
13Vh5VW/eHAzCLiqXEc74azybwhrQWeiRTlEE6BSlQ0Zg5zz2VhsAQN4KPxrD1lP
6QqUnv2zjAJFdkQ6CJunnor7OSKCMbaxXA1oxbLq6ykTtWV0lUizu6VzIdQrpf9S
GTIO4YiCb/3s8pyNiCPXXG4QtBhkxwX7yU4nnRvk/ic0fmSQntk5lwBFqDG6mIzc
WXwfsXB8r6Sm2Vxvzin5Yj4PZXrXztLj43gG/30HF2/Lcy9jGEllU9RPirJn5Q5n
Y5OwicxAO3nrXbjAivf0dZLJpXAPG60BPha3qlvFuB0BsO1HVeQYagKqCbywm6l5
5lJbTjYTVpqLMMORd0k8YBKJVNfr9whAjffmHtEtWpBt9awNgVbOREbu4Vj6E1zo
2t7kPdlL26gc9CizfjFjUS0mKbC6FCN2XgdOsGqoGg6GSu52lapaaFjmrWePrtk0
EdwAjghZAYqa6RkG8rNgIpeS8YKZjfbAb8j7ku2ACDHq50sToMvbIf3u20/o5GLb
E9CHNqx2jQiXKCSap5CO/J47dGrUDK22CruYC56rDMn7Mzcd5eF9mULLoQhq0sm0
XRjcxzF0D+B8JyB79T+zW7tjnnzpYmN5rBb4z0pLgxjakxG6bLeBU0yQ4tC90EUB
IQts3Y8dZ09A6I2+1tVo9YR/P+5RaGFXoUb4z3u+gRYdie0eBXGQPRaiyP+qae4G
SAdFjP2Eagpl2Jq010bn94deZx2pqaayphvLjDHsIWSkJ5XLvmifbB8+tmImxspY
m/bTrzYJMnXEZ8BDN1X+yQntTYDc/bdUJJbK3NfEiaDFpW4/jfyNMnflkKIv01bV
o6YHLiTMTcBBSEg/K7lnLfcJbJZ/si2tTJ/aEZXemFCxOhA9InNDigh1kSPG7Hay
fnRean9LviaVqi4tQbx/iWGq8glrW493RY3qsO8rBfos8H2EzEivOaRySrDgQrrV
px44E0Pi3+ebE8vHTKi6IPrYt+IJMRpmSbBqXgxQbiNWLUSbTause1lfk/5nLk/W
DomqFwRLb+/FQzRpW2S3XJ3ThTuls8U5i9PcQQcW+vjIPmpgTxsW9JuEvjjCpCl0
cTfUdnrMUw7Q/Jxa1VCpn7RzeHlTLrSXkdq3xVB9gq6DG+umJRfsKPLmw9t5TbD1
CIfb09GR/D1+6ogCfayqZoXe/xaRRjM3nzOLP4Z4ouMyZC7krj/UsItg0Y8FS0Wq
gZU88x/X78LlryEvfB0KH/GuULo6ziAzsSsB5Okfm68lFLdaNWA2d3f8lPvQNmL3
bZI="""

  JUNK_PRIVATE_KEY = """\
    -----BEGIN PRIVATE KEY-----
    %s
    -----END PRIVATE KEY-----""" % JUNK
  JUNK_PUBLIC_KEY = """\
    -----BEGIN PUBLIC KEY-----
    %s
    -----END PUBLIC KEY-----""" % JUNK
  JUNK_CERTIFICATE = """\
    -----BEGIN CERTIFICATE-----
    %s
    -----END CERTIFICATE-----""" % JUNK


  class Test_public_key_pem_decode(unittest2.TestCase):
    def test_decode(self):
      self.assertDictEqual(codec.public_key_pem_decode(PUBLIC_KEY),
                           PUBLIC_KEY_DECODED)
      self.assertDictEqual(codec.public_key_pem_decode(CERTIFICATE),
                           PUBLIC_KEY_DECODED)

    def test_NotImplementedError_when_not_public_key(self):
      self.assertRaises(NotImplementedError,
                        codec.public_key_pem_decode, PRIVATE_KEY)

    def test_fails_on_junk(self):
      self.assertRaises(SubstrateUnderrunError,
                        codec.public_key_pem_decode, JUNK_PUBLIC_KEY)
      self.assertRaises(SubstrateUnderrunError,
                        codec.public_key_pem_decode, JUNK_CERTIFICATE)

  class Test_private_key_pem_decode(unittest2.TestCase):
    def test_decode(self):
      self.assertDictEqual(codec.private_key_pem_decode(PRIVATE_KEY),
                           PRIVATE_KEY_DECODED)

    def test_NotImplementedError_when_not_private_key(self):
      self.assertRaises(NotImplementedError,
                        codec.private_key_pem_decode, PUBLIC_KEY)
      self.assertRaises(NotImplementedError,
                        codec.private_key_pem_decode, CERTIFICATE)

    def test_fails_on_junk(self):
      self.assertRaises(SubstrateUnderrunError,
                        codec.private_key_pem_decode, JUNK_PRIVATE_KEY)
