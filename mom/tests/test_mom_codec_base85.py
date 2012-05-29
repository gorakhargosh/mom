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

import os
import unittest2

from mom import builtins
from mom.codec import _alt_base
from mom.codec import base85
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b


RAW = b("""Man is distinguished, not only by his reason, but by this
singular passion from other animals, which is a lust of the
mind, that by a perseverance of delight in the continued and
indefatigable generation of knowledge, exceeds the short
vehemence of any carnal pleasure.""").replace(b("\n"), b(" "))

ENCODED = b("""\
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c""")

ENCODED_WITH_ENDS = b("""\
<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>""")

ENCODED_WITH_WHITESPACE = b("""
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c""")

ENCODED_WITH_ENDS_AND_WHITESPACE = b("""
<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>""")


#ipv6_address = "1080:0:0:0:8:800:200C:417A"
IPV6_NUMBER = 21932261930451111902915077091070067066
IPV6_RAW_BYTES = b("\x10\x80\x00\x00\x00\x00\x00\x00\x00\x08\x08\x00 \x0cAz")
IPV6_ENCODED = b("4)+k&C#VzJ4br>0wv%Yp")

# Wikipedia example.
#ipv6_number_2 = 2**128 - 1  # 340282366920938463463374607431768211455L
IPV6_NUMBER_2 = (1 << 128) - 1
IPV6_ENCODED_2 = b("=r54lj&NUUO~Hi%c2ym0")

#ipv6_address_3 = "2607:f8f0:610:4000:214:38ff:feee:b65a"
IPV6_NUMBER_3 = 50552058972053811105097158630017250906
IPV6_ENCODED_3 = b("B7RDhRib#Y+VwlwuPBOG")


# Mercurial uses RFC1924 character set, but does not encode it like
# IPv6.
MERCURIAL_BYTES = b("\t\x91{W\xa80\xb1")
MERCURIAL_ENCODED = b("36XnOs4%e")

RANDOM_256_BYTES = b("""U\x94<Q\x1d\xad\xe4\xe3\xd1\xd1\xddR\xfb d\
\x01R6\xadj\xa2\x03\xa4\xc1\xc7\x92\xa1U\x18\x19\xaep\r\xfe\xaa\
\xd4\x11ob\xb2yV\x00\xb1\xb1\x98<O\x15\xf7?7\xbf\xc8\x0b\xbdR\
\xe7\xf1rd\xe0:4\xe2\x9d\xd9I&v\x1cvN$\xb6\xca\xff\xc2?1\xa2\
\xc1d\x0b\rUpM\xfdh\x81\xd3st\x04\xd4.\x9d\x03<\xe3}\xdck\\\x01\
\x7fg\xec\x80*{P\xdfG,\x08\x08w\x86.\x89L\xe7~\xfd\xa5\xc8x\x85\
\x07\xcfG\x80\xf0\xd3\x93(\xbbA\x07\xa1\x0ed\x14-\x88\xa3\x15\
\xc2\n\xed\xfb\x13\x02\x1ba~\x944J\xa0{<o_(07\x81J\x8e\x8d\xd9x\
\x86\xa1`v&\xee\xe1\x85\x06\x9c\xf1\xb0\xd2Bp\xf8\x0f+\xcc\xb0r2\
\xc7\xaaH\r_\xeeqq;\xaf\x10\x15\x83\xb8?Y)\xb2\x94\xe5Us~\x11\
\x1fBX\x8cF\xc9\x88\x99[\\\xc4\xb1a\x80P\xe1\xa1\x9b\xd8\xe5j\
\x817\x1a\xb58\x01\xfc\x80\xc5\x9e3\x80\xa4*""")

RANDOM_256_MERCURIAL = b("""\
Rg^qY9j)Z!(b3&f`ygZiQZ}t>q64JC$C9B{7#Xf`4gRXs5pQC$c~$_iv6wth756_kzsL)\
{Qs?n<WZ*h9;+@$^CUzWlP9(O<|H3~pqQPVf4OMVW{b+&Hb94mME}a8B<9*y~TmgS)?0_\
nJP~S%^2nctEE{RO%e*LA$c!dYgM}Y9tlPJ4E2cZsR6fKCO6~YSb`x62iVSbb}N}zi@Z(\
k@dH-SoyjoEmHp<s3<?%{<7obj;ILU8yGE6lKRGRLY&4PWkYaXYUN6@$1xSt+uV<yCWj5\
g$TWj7G_bnOj`Mv0;Ev;h~$@<!XU98nrk9{D8%tGk~Nj""")

RANDOM_ODD_BYTES = os.urandom(3333)

# 31 bytes each.
RANDOM_BYTES_LIST = [
  b("a)X\xfb$$\xd1Q\xbe\xad\xb7\n\xf9\x99_\xc9\x90\xaf\rT\
\xcf\x8d\xaaF\x0cz\xa8\xf2\x11\xd0\x1e"),
  b("Ep\xf7a&\xbd\xce.\x16BV~N;\xbe|\x80\xadZ\xc9\xbc\xf1\
\xf7\xec\x15>\x1c\xb0\xd9\xcd&")
]
RFC_ENCODED_BYTES_LIST = [
  b("VJTSqBqY&MzOA<k`I%qIkgp9?&yA`^40@>Y5zrn"),
  b("MR50FCcVxs7D85jPCLGQfUR1|yz%$!6+RrW+07;"),
  ]


class Test_check_compact_char_occurrence(unittest2.TestCase):
  def test_valid(self):
    self.assertEqual(
      base85._check_compact_char_occurrence(b("z12345z12345zz123!"),
                                     b("z")), None
    )

  def test_ValueError_when_invalid_index(self):
    self.assertRaises(ValueError, base85._check_compact_char_occurrence,
                      b("z12345z12345zz123z!"), b("z"), 5)


class Test_base85_encode(unittest2.TestCase):
  def test_encoding(self):
    self.assertEqual(base85.b85encode(RAW), ENCODED)

  def test_encoding_wikipedia(self):
    self.assertEqual(base85.b85encode(b("Man ")), b("9jqo^"))
    self.assertEqual(base85.b85encode(b("sure")), b("F*2M7"))

  def test_check_padding(self):
    self.assertEqual(base85.b85encode(b("."), _padding=True), b("/cYkO"))
    self.assertEqual(base85.b85encode(b(".")), b("/c"))

  def test_TypeError_on_unicode(self):
    self.assertRaises(TypeError, base85.b85encode, constants.UNICODE_STRING2)


class Test_base85_decode(unittest2.TestCase):
  def test_decoder(self):
    self.assertEqual(base85.b85decode(ENCODED, base85.ASCII85_PREFIX, base85.ASCII85_SUFFIX),
                     RAW)

  def test_TypeError_on_unicode(self):
    self.assertRaises(TypeError, base85.b85decode, constants.UNICODE_STRING2)

  def test_decoder_ignores_whitespace_by_default(self):
    self.assertEqual(base85.b85decode(ENCODED_WITH_WHITESPACE), RAW)

  def test_decoder_ignores_ends_by_default(self):
    self.assertEqual(base85.b85decode(ENCODED_WITH_ENDS_AND_WHITESPACE,
                               base85.ASCII85_PREFIX, base85.ASCII85_SUFFIX), RAW)

  def test_encoding_wikipedia(self):
    self.assertEqual(base85.b85decode(b("9jqo^")), b("Man "))
    self.assertEqual(base85.b85decode(b("F*2M7")), b("sure"))

  def test_check_padding(self):
    self.assertEqual(base85.b85decode(b("/c")), b("."))

  def test_decode_boundary(self):
    self.assertEqual(base85.b85decode(b("s8W-!")), b("\xff\xff\xff\xff"))

  def test_OverflowError_when_invalid_base85_byte_found(self):
    self.assertRaises(OverflowError, base85.b85decode, b("xy!!!"))

  def test_decodes_z_into_zero_bytes(self):
    self.assertEqual(base85.b85decode(b("zzz")), b("\x00") * 4 * 3)

  def test_decode_zero_groups(self):
    self.assertEqual(base85.b85decode(b("!!!!!")), b("\x00") * 4)

  def test_ValueError_when_zero_char_in_middle_of_chunk(self):
    self.assertRaises(ValueError, base85.b85decode, b("zaz"))


class Test_codec(unittest2.TestCase):
  def test_identity(self):
    zero_bytes = b("\x00\x00\x00\x00\x00")
    self.assertEqual(base85.b85decode(base85.b85encode(zero_bytes)), zero_bytes)
    self.assertEqual(base85.b85decode(base85.b85encode(RANDOM_256_BYTES)),
                     RANDOM_256_BYTES)
    self.assertEqual(base85.b85decode(base85.b85encode(RANDOM_ODD_BYTES)),
                     RANDOM_ODD_BYTES)

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, base85.b85encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base85.b85encode, None)
    self.assertRaises(TypeError, base85.b85decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base85.b85decode, None)

  def test_raises_TypeError_when_bad_arg_types(self):
    # Prefix/suffix.
    self.assertRaises(TypeError, base85.b85encode, b("foo"), constants.UNICODE_STRING, None)
    self.assertRaises(TypeError, base85.b85encode, b("foo"), None, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base85.b85decode, b("foo"), constants.UNICODE_STRING, None)
    self.assertRaises(TypeError, base85.b85decode, b("foo"), None, constants.UNICODE_STRING)

    # Compact char.
    self.assertRaises(TypeError, base85.b85encode, b("foo"),
                      _compact_char=constants.UNICODE_STRING)
    self.assertRaises(TypeError, base85.b85decode, b("foo"),
                      _compact_char=constants.UNICODE_STRING)


class Test_rfc1924_base85_encoding(unittest2.TestCase):
  def test_encoding(self):
    self.assertEqual(base85.rfc1924_b85encode(MERCURIAL_BYTES), MERCURIAL_ENCODED)
    self.assertEqual(base85.rfc1924_b85encode(RANDOM_256_BYTES),
                     RANDOM_256_MERCURIAL)
    for a, e in zip(RANDOM_BYTES_LIST, RFC_ENCODED_BYTES_LIST):
      self.assertEqual(base85.rfc1924_b85encode(a), e)

  def test_decoding(self):
    self.assertEqual(base85.rfc1924_b85decode(MERCURIAL_ENCODED), MERCURIAL_BYTES)
    self.assertEqual(base85.rfc1924_b85decode(RANDOM_256_MERCURIAL),
                     RANDOM_256_BYTES)
    self.assertEqual(base85.rfc1924_b85decode(b("|NsC0")), b("\xff\xff\xff\xff"))
    for a, e in zip(RANDOM_BYTES_LIST, RFC_ENCODED_BYTES_LIST):
      self.assertEqual(base85.rfc1924_b85decode(e), a)

  def test_OverflowError_when_invalid_base85_byte_found(self):
    self.assertRaises(OverflowError, base85.rfc1924_b85decode, b("]]]]]"))

  def test_OverflowError_when_not_decodable_chunk_found(self):
    self.assertRaises(OverflowError, base85.rfc1924_b85decode,
                      b("|NsC")) # 0x03030303

  def test_TypeError_when_not_bytes(self):
    self.assertRaises(TypeError, base85.rfc1924_b85decode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base85.rfc1924_b85decode, None)
    self.assertRaises(TypeError, base85.rfc1924_b85decode, object)
    self.assertRaises(TypeError, base85.rfc1924_b85decode, [])
    self.assertRaises(TypeError, base85.rfc1924_b85decode, 1)
    self.assertRaises(TypeError, base85.rfc1924_b85decode, False)

    self.assertRaises(TypeError, base85.rfc1924_b85encode, constants.UNICODE_STRING)
    self.assertRaises(TypeError, base85.rfc1924_b85encode, None)
    self.assertRaises(TypeError, base85.rfc1924_b85encode, object)
    self.assertRaises(TypeError, base85.rfc1924_b85encode, [])
    self.assertRaises(TypeError, base85.rfc1924_b85encode, 1)
    self.assertRaises(TypeError, base85.rfc1924_b85encode, False)

  def test_codec_identity(self):
    self.assertEqual(
      base85.rfc1924_b85decode(base85.rfc1924_b85encode(MERCURIAL_BYTES)),
      MERCURIAL_BYTES)
    self.assertEqual(
      base85.rfc1924_b85decode(base85.rfc1924_b85encode(RANDOM_256_BYTES)),
      RANDOM_256_BYTES)
    self.assertEqual(
      base85.rfc1924_b85decode(base85.rfc1924_b85encode(RANDOM_ODD_BYTES)),
      RANDOM_ODD_BYTES)


class Test_base85_ipv6_encoding(unittest2.TestCase):
  def test_encoding(self):
    self.assertEqual(base85.ipv6_b85encode(IPV6_NUMBER), IPV6_ENCODED)
    self.assertEqual(base85.ipv6_b85encode(IPV6_NUMBER_2), IPV6_ENCODED_2)
    self.assertEqual(base85.ipv6_b85encode(IPV6_NUMBER_3), IPV6_ENCODED_3)

    self.assertEqual(_alt_base.ipv6_b85encode_naive(IPV6_NUMBER), IPV6_ENCODED)
    self.assertEqual(_alt_base.ipv6_b85encode_naive(IPV6_NUMBER_2), IPV6_ENCODED_2)
    self.assertEqual(_alt_base.ipv6_b85encode_naive(IPV6_NUMBER_3), IPV6_ENCODED_3)

  def test_decoding(self):
    self.assertEqual(base85.ipv6_b85decode(IPV6_ENCODED), IPV6_NUMBER)
    self.assertEqual(base85.ipv6_b85decode(IPV6_ENCODED_2), IPV6_NUMBER_2)
    self.assertEqual(base85.ipv6_b85decode(IPV6_ENCODED_3), IPV6_NUMBER_3)

    self.assertEqual(_alt_base.ipv6_b85decode_naive(IPV6_ENCODED), IPV6_NUMBER)
    self.assertEqual(_alt_base.ipv6_b85decode_naive(IPV6_ENCODED_2), IPV6_NUMBER_2)
    self.assertEqual(_alt_base.ipv6_b85decode_naive(IPV6_ENCODED_3), IPV6_NUMBER_3)

  def test_TypeError_when_unicode(self):
    self.assertRaises(TypeError, base85.ipv6_b85decode, constants.UNICODE_STRING2)
    self.assertRaises(TypeError, _alt_base.ipv6_b85decode_naive, constants.UNICODE_STRING2)

  def test_codec_identity(self):
    self.assertEqual(base85.ipv6_b85decode(base85.ipv6_b85encode(IPV6_NUMBER)),
                     IPV6_NUMBER)
    self.assertEqual(base85.ipv6_b85decode(base85.ipv6_b85encode(IPV6_NUMBER_2)),
                     IPV6_NUMBER_2)
    self.assertEqual(base85.ipv6_b85decode(base85.ipv6_b85encode(IPV6_NUMBER_3)),
                     IPV6_NUMBER_3)

    self.assertEqual(_alt_base.ipv6_b85decode_naive(_alt_base.ipv6_b85encode_naive(IPV6_NUMBER)),
                     IPV6_NUMBER)
    self.assertEqual(_alt_base.ipv6_b85decode_naive(_alt_base.ipv6_b85encode_naive(IPV6_NUMBER_2)),
                     IPV6_NUMBER_2)
    self.assertEqual(_alt_base.ipv6_b85decode_naive(_alt_base.ipv6_b85encode_naive(IPV6_NUMBER_3)),
                     IPV6_NUMBER_3)

  def test_ValueError_when_negative(self):
    self.assertRaises(ValueError, base85.ipv6_b85encode, -1)
    self.assertRaises(ValueError, _alt_base.ipv6_b85encode_naive, -1)

  def test_OverflowError_when_greater_than_128_bit(self):
    self.assertRaises(OverflowError, base85.ipv6_b85encode, 1 << 128)
    self.assertRaises(OverflowError, _alt_base.ipv6_b85encode_naive, 1 << 128)

  def test_ValueError_when_encoded_length_not_20(self):
    self.assertRaises(ValueError, base85.ipv6_b85decode,
                      b("=r54lj&NUUO~Hi%c2ym0="))
    self.assertRaises(ValueError, base85.ipv6_b85decode,
                      b("=r54lj&NUUO="))

    self.assertRaises(ValueError, _alt_base.ipv6_b85decode_naive,
                      b("=r54lj&NUUO~Hi%c2ym0="))
    self.assertRaises(ValueError, _alt_base.ipv6_b85decode_naive,
                      b("=r54lj&NUUO="))

  def test_TypeError_when_not_number(self):
    self.assertRaises(TypeError, base85.ipv6_b85encode, None)
    self.assertRaises(TypeError, _alt_base.ipv6_b85encode_naive, None)

  def test_ignores_whitespace(self):
    self.assertEqual(base85.ipv6_b85decode(b("=r5\t4lj&\nNUUO~   Hi%c2ym \x0b 0")),
                     IPV6_NUMBER_2)
    self.assertEqual(
      _alt_base.ipv6_b85decode_naive(b("=r5\t4lj&\nNUUO~   Hi%c2ym \x0b 0")),
      IPV6_NUMBER_2)

  def test_OverflowError_when_stray_characters_found(self):
    self.assertRaises(OverflowError, base85.ipv6_b85decode,
                      b("=r54lj&NUUO~Hi,./:[]"))
    self.assertRaises(OverflowError, _alt_base.ipv6_b85decode_naive,
                      b("=r54lj&NUUO~Hi,./:[]"))
