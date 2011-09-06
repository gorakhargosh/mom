#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
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
from mom.builtins import b
from mom.codec._alt_base import ipv6_b85encode_naive, ipv6_b85decode_naive
from mom.tests.constants import unicode_string
from mom.tests.test_mom_builtins import unicode_string2

from mom.codec.base85 import b85decode, b85encode, ipv6_b85encode, \
    ipv6_b85decode, ASCII85_PREFIX, ASCII85_SUFFIX, rfc1924_b85encode, \
    rfc1924_b85decode, _check_compact_char_occurrence

raw = b("""Man is distinguished, not only by his reason, but by this
singular passion from other animals, which is a lust of the
mind, that by a perseverance of delight in the continued and
indefatigable generation of knowledge, exceeds the short
vehemence of any carnal pleasure.""").replace(b('\n'), b(' '))

encoded = b("""\
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c""")

encoded_with_ends = b("""\
<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>""")

encoded_with_whitespace = b("""
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c""")

encoded_with_ends_and_whitespace = b("""
<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>""")


#ipv6_address = '1080:0:0:0:8:800:200C:417A'
ipv6_number = 21932261930451111902915077091070067066
ipv6_raw_bytes = b('\x10\x80\x00\x00\x00\x00\x00\x00\x00\x08\x08\x00 \x0cAz')
ipv6_encoded = b('4)+k&C#VzJ4br>0wv%Yp')

# Wikipedia example.
#ipv6_number_2 = 2**128 - 1  # 340282366920938463463374607431768211455L
ipv6_number_2 = (1 << 128) - 1
ipv6_encoded_2 = b('=r54lj&NUUO~Hi%c2ym0')

#ipv6_address_3 = '2607:f8f0:610:4000:214:38ff:feee:b65a'
ipv6_number_3 = 50552058972053811105097158630017250906
ipv6_encoded_3 = b('B7RDhRib#Y+VwlwuPBOG')


# Mercurial uses RFC1924 character set, but does not encode it like
# IPv6.
mercurial_bytes = b('\t\x91{W\xa80\xb1')
mercurial_encoded = b('36XnOs4%e')

random_256_bytes = b('''U\x94<Q\x1d\xad\xe4\xe3\xd1\xd1\xddR\xfb d\
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
\x817\x1a\xb58\x01\xfc\x80\xc5\x9e3\x80\xa4*''')

random_256_mercurial = b('''\
Rg^qY9j)Z!(b3&f`ygZiQZ}t>q64JC$C9B{7#Xf`4gRXs5pQC$c~$_iv6wth756_kzsL)\
{Qs?n<WZ*h9;+@$^CUzWlP9(O<|H3~pqQPVf4OMVW{b+&Hb94mME}a8B<9*y~TmgS)?0_\
nJP~S%^2nctEE{RO%e*LA$c!dYgM}Y9tlPJ4E2cZsR6fKCO6~YSb`x62iVSbb}N}zi@Z(\
k@dH-SoyjoEmHp<s3<?%{<7obj;ILU8yGE6lKRGRLY&4PWkYaXYUN6@$1xSt+uV<yCWj5\
g$TWj7G_bnOj`Mv0;Ev;h~$@<!XU98nrk9{D8%tGk~Nj''')

random_odd_bytes = os.urandom(3333)

# 31 bytes each.
random_bytes_list = [
    b('a)X\xfb$$\xd1Q\xbe\xad\xb7\n\xf9\x99_\xc9\x90\xaf\rT\
\xcf\x8d\xaaF\x0cz\xa8\xf2\x11\xd0\x1e'),
    b('Ep\xf7a&\xbd\xce.\x16BV~N;\xbe|\x80\xadZ\xc9\xbc\xf1\
\xf7\xec\x15>\x1c\xb0\xd9\xcd&')
]
rfc_encoded_bytes_list = [
    b('VJTSqBqY&MzOA<k`I%qIkgp9?&yA`^40@>Y5zrn'),
    b('MR50FCcVxs7D85jPCLGQfUR1|yz%$!6+RrW+07;'),
]


class Test_check_compact_char_occurrence(unittest2.TestCase):
    def test_valid(self):
        self.assertEqual(
            _check_compact_char_occurrence(b('z12345z12345zz123!'),
                                           b('z')), None
        )

    def test_ValueError_when_invalid_index(self):
        self.assertRaises(ValueError, _check_compact_char_occurrence,
                          b('z12345z12345zz123z!'), b('z'), 5)

class Test_base85_encode(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(b85encode(raw), encoded)

    def test_encoding_wikipedia(self):
        self.assertEqual(b85encode(b("Man ")), b("9jqo^"))
        self.assertEqual(b85encode(b("sure")), b("F*2M7"))

    def test_check_padding(self):
        self.assertEqual(b85encode(b("."), _padding=True), b("/cYkO"))
        self.assertEqual(b85encode(b(".")), b("/c"))

    def test_TypeError_on_unicode(self):
        self.assertRaises(TypeError, b85encode, unicode_string2)

class Test_base85_decode(unittest2.TestCase):
    def test_decoder(self):
        self.assertEqual(b85decode(encoded, ASCII85_PREFIX, ASCII85_SUFFIX),
                         raw)

    def test_TypeError_on_unicode(self):
        self.assertRaises(TypeError, b85decode, unicode_string2)

    def test_decoder_ignores_whitespace_by_default(self):
        self.assertEqual(b85decode(encoded_with_whitespace), raw)

    def test_decoder_ignores_ends_by_default(self):
        self.assertEqual(b85decode(encoded_with_ends_and_whitespace,
                                   ASCII85_PREFIX, ASCII85_SUFFIX), raw)

    def test_encoding_wikipedia(self):
        self.assertEqual(b85decode(b("9jqo^")), b("Man "))
        self.assertEqual(b85decode(b("F*2M7")), b("sure"))

    def test_check_padding(self):
        self.assertEqual(b85decode(b("/c")), b("."))

    def test_decode_boundary(self):
        self.assertEqual(b85decode(b("s8W-!")), b("\xff\xff\xff\xff"))

    def test_OverflowError_when_invalid_base85_byte_found(self):
        self.assertRaises(OverflowError, b85decode, b('xy!!!'))

    def test_decodes_z_into_zero_bytes(self):
        self.assertEqual(b85decode(b('zzz')), b('\x00') * 4 * 3)

    def test_decode_zero_groups(self):
        self.assertEqual(b85decode(b('!!!!!')), b('\x00') * 4)

    def test_ValueError_when_zero_char_in_middle_of_chunk(self):
        self.assertRaises(ValueError, b85decode, b('zaz'))




class Test_codec(unittest2.TestCase):
    def test_identity(self):
        zero_bytes = b('\x00\x00\x00\x00\x00')
        self.assertEqual(b85decode(b85encode(zero_bytes)), zero_bytes)
        self.assertEqual(b85decode(b85encode(random_256_bytes)),
                         random_256_bytes)
        self.assertEqual(b85decode(b85encode(random_odd_bytes)),
                         random_odd_bytes)

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, b85encode, unicode_string)
        self.assertRaises(TypeError, b85encode, None)
        self.assertRaises(TypeError, b85decode, unicode_string)
        self.assertRaises(TypeError, b85decode, None)

    def test_raises_TypeError_when_bad_arg_types(self):
        # Prefix/suffix.
        self.assertRaises(TypeError, b85encode, b('foo'), unicode_string, None)
        self.assertRaises(TypeError, b85encode, b('foo'), None, unicode_string)
        self.assertRaises(TypeError, b85decode, b('foo'), unicode_string, None)
        self.assertRaises(TypeError, b85decode, b('foo'), None, unicode_string)

        # Compact char.
        self.assertRaises(TypeError, b85encode, b('foo'),
                          _compact_char=unicode_string)
        self.assertRaises(TypeError, b85decode, b('foo'),
                          _compact_char=unicode_string)


class Test_rfc1924_base85_encoding(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(rfc1924_b85encode(mercurial_bytes), mercurial_encoded)
        self.assertEqual(rfc1924_b85encode(random_256_bytes),
                         random_256_mercurial)
        for a, e in zip(random_bytes_list, rfc_encoded_bytes_list):
            self.assertEqual(rfc1924_b85encode(a), e)
        
    def test_decoding(self):
        self.assertEqual(rfc1924_b85decode(mercurial_encoded), mercurial_bytes)
        self.assertEqual(rfc1924_b85decode(random_256_mercurial),
                         random_256_bytes)
        self.assertEqual(rfc1924_b85decode(b('|NsC0')), b('\xff\xff\xff\xff'))
        for a, e in zip(random_bytes_list, rfc_encoded_bytes_list):
            self.assertEqual(rfc1924_b85decode(e), a)

    def test_OverflowError_when_invalid_base85_byte_found(self):
        self.assertRaises(OverflowError, rfc1924_b85decode, b(']]]]]'))

    def test_OverflowError_when_not_decodable_chunk_found(self):
        self.assertRaises(OverflowError, rfc1924_b85decode,
                          b('|NsC')) # 0x03030303

    def test_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, rfc1924_b85decode, unicode_string)
        self.assertRaises(TypeError, rfc1924_b85decode, None)
        self.assertRaises(TypeError, rfc1924_b85decode, object)
        self.assertRaises(TypeError, rfc1924_b85decode, [])
        self.assertRaises(TypeError, rfc1924_b85decode, 1)
        self.assertRaises(TypeError, rfc1924_b85decode, False)
        
        self.assertRaises(TypeError, rfc1924_b85encode, unicode_string)
        self.assertRaises(TypeError, rfc1924_b85encode, None)
        self.assertRaises(TypeError, rfc1924_b85encode, object)
        self.assertRaises(TypeError, rfc1924_b85encode, [])
        self.assertRaises(TypeError, rfc1924_b85encode, 1)
        self.assertRaises(TypeError, rfc1924_b85encode, False)

    def test_codec_identity(self):
        self.assertEqual(
            rfc1924_b85decode(rfc1924_b85encode(mercurial_bytes)),
            mercurial_bytes)
        self.assertEqual(
            rfc1924_b85decode(rfc1924_b85encode(random_256_bytes)),
            random_256_bytes)
        self.assertEqual(
            rfc1924_b85decode(rfc1924_b85encode(random_odd_bytes)),
            random_odd_bytes)

class Test_base85_ipv6_encoding(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(ipv6_b85encode(ipv6_number), ipv6_encoded)
        self.assertEqual(ipv6_b85encode(ipv6_number_2), ipv6_encoded_2)
        self.assertEqual(ipv6_b85encode(ipv6_number_3), ipv6_encoded_3)

        self.assertEqual(ipv6_b85encode_naive(ipv6_number), ipv6_encoded)
        self.assertEqual(ipv6_b85encode_naive(ipv6_number_2), ipv6_encoded_2)
        self.assertEqual(ipv6_b85encode_naive(ipv6_number_3), ipv6_encoded_3)

    def test_decoding(self):
        self.assertEqual(ipv6_b85decode(ipv6_encoded), ipv6_number)
        self.assertEqual(ipv6_b85decode(ipv6_encoded_2), ipv6_number_2)
        self.assertEqual(ipv6_b85decode(ipv6_encoded_3), ipv6_number_3)

        self.assertEqual(ipv6_b85decode_naive(ipv6_encoded), ipv6_number)
        self.assertEqual(ipv6_b85decode_naive(ipv6_encoded_2), ipv6_number_2)
        self.assertEqual(ipv6_b85decode_naive(ipv6_encoded_3), ipv6_number_3)

    def test_TypeError_when_unicode(self):
        self.assertRaises(TypeError, ipv6_b85decode, unicode_string2)
        self.assertRaises(TypeError, ipv6_b85decode_naive, unicode_string2)

    def test_codec_identity(self):
        self.assertEqual(ipv6_b85decode(ipv6_b85encode(ipv6_number)),
                         ipv6_number)
        self.assertEqual(ipv6_b85decode(ipv6_b85encode(ipv6_number_2)),
                         ipv6_number_2)
        self.assertEqual(ipv6_b85decode(ipv6_b85encode(ipv6_number_3)),
                         ipv6_number_3)


        self.assertEqual(ipv6_b85decode_naive(ipv6_b85encode_naive(ipv6_number)),
                         ipv6_number)
        self.assertEqual(ipv6_b85decode_naive(ipv6_b85encode_naive(ipv6_number_2)),
                         ipv6_number_2)
        self.assertEqual(ipv6_b85decode_naive(ipv6_b85encode_naive(ipv6_number_3)),
                         ipv6_number_3)

    def test_ValueError_when_negative(self):
        self.assertRaises(ValueError, ipv6_b85encode, -1)
        self.assertRaises(ValueError, ipv6_b85encode_naive, -1)

    def test_OverflowError_when_greater_than_128_bit(self):
        self.assertRaises(OverflowError, ipv6_b85encode, 1 << 128)
        self.assertRaises(OverflowError, ipv6_b85encode_naive, 1 << 128)

    def test_ValueError_when_encoded_length_not_20(self):
        self.assertRaises(ValueError, ipv6_b85decode,
                          b('=r54lj&NUUO~Hi%c2ym0='))
        self.assertRaises(ValueError, ipv6_b85decode,
                          b('=r54lj&NUUO='))

        self.assertRaises(ValueError, ipv6_b85decode_naive,
                          b('=r54lj&NUUO~Hi%c2ym0='))
        self.assertRaises(ValueError, ipv6_b85decode_naive,
                          b('=r54lj&NUUO='))

    def test_TypeError_when_not_number(self):
        self.assertRaises(TypeError, ipv6_b85encode, None)
        self.assertRaises(TypeError, ipv6_b85encode_naive, None)

    def test_ignores_whitespace(self):
        self.assertEqual(ipv6_b85decode(b('=r5\t4lj&\nNUUO~   Hi%c2ym \x0b 0')),
                         ipv6_number_2)
        self.assertEqual(
            ipv6_b85decode_naive(b('=r5\t4lj&\nNUUO~   Hi%c2ym \x0b 0')),
            ipv6_number_2)

    def test_OverflowError_when_stray_characters_found(self):
        self.assertRaises(OverflowError, ipv6_b85decode,
                          b('=r54lj&NUUO~Hi,./:[]'))
        self.assertRaises(OverflowError, ipv6_b85decode_naive,
                          b('=r54lj&NUUO~Hi,./:[]'))
