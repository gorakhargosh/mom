#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest2
from mom.builtins import b

from mom.codec.base85 import b85decode, b85encode, ipv6_b85encode, \
    ipv6_b85decode, ASCII85_PREFIX, ASCII85_SUFFIX, rfc1924_b85encode, \
    rfc1924_b85decode, check_compact_char_occurrence

raw = """Man is distinguished, not only by his reason, but by this
singular passion from other animals, which is a lust of the
mind, that by a perseverance of delight in the continued and
indefatigable generation of knowledge, exceeds the short
vehemence of any carnal pleasure.""".replace('\n', ' ')

encoded = """\
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c"""

encoded_with_ends = """\
<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>"""

encoded_with_whitespace = """
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c"""

encoded_with_ends_and_whitespace = """
<~9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c~>"""


ipv6_address = '1080:0:0:0:8:800:200C:417A'
ipv6_number = 21932261930451111902915077091070067066L
ipv6_raw_bytes = '\x10\x80\x00\x00\x00\x00\x00\x00\x00\x08\x08\x00 \x0cAz'
ipv6_encoded = '4)+k&C#VzJ4br>0wv%Yp'

# Wikipedia example.
ipv6_number_2 = 2**128 - 1  # 340282366920938463463374607431768211455L
ipv6_encoded_2 = '=r54lj&NUUO~Hi%c2ym0'

# Mercurial uses RFC1924 character set, but does not encode it like
# IPv6.
mercurial_bytes = '\t\x91{W\xa80\xb1'
mercurial_encoded = '36XnOs4%e'

random_256_bytes = '''U\x94<Q\x1d\xad\xe4\xe3\xd1\xd1\xddR\xfb d\
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
\x817\x1a\xb58\x01\xfc\x80\xc5\x9e3\x80\xa4*'''

random_256_mercurial = '''\
Rg^qY9j)Z!(b3&f`ygZiQZ}t>q64JC$C9B{7#Xf`4gRXs5pQC$c~$_iv6wth756_kzsL)\
{Qs?n<WZ*h9;+@$^CUzWlP9(O<|H3~pqQPVf4OMVW{b+&Hb94mME}a8B<9*y~TmgS)?0_\
nJP~S%^2nctEE{RO%e*LA$c!dYgM}Y9tlPJ4E2cZsR6fKCO6~YSb`x62iVSbb}N}zi@Z(\
k@dH-SoyjoEmHp<s3<?%{<7obj;ILU8yGE6lKRGRLY&4PWkYaXYUN6@$1xSt+uV<yCWj5\
g$TWj7G_bnOj`Mv0;Ev;h~$@<!XU98nrk9{D8%tGk~Nj'''

random_odd_bytes = os.urandom(33333)


class Test_check_compact_char_occurrence(unittest2.TestCase):
    def test_valid(self):
        self.assertEqual(
            check_compact_char_occurrence('z12345z12345zz123!'), None
        )

    def test_ValueError_when_invalid_index(self):
        self.assertRaises(ValueError, check_compact_char_occurrence,
                          'z12345z12345zz123z!')

class Test_base85_encode(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(b85encode(raw), encoded)

    def test_encoding_wikipedia(self):
        self.assertEqual(b85encode(b("Man ")), "9jqo^")
        self.assertEqual(b85encode(b("sure")), "F*2M7")

    def test_check_padding(self):
        self.assertEqual(b85encode(b("."), _padding=True), "/cYkO")
        self.assertEqual(b85encode(b(".")), "/c")

    def test_TypeError_on_Unicode(self):
        self.assertRaises(TypeError, b85encode, u"深入")

class Test_base85_decode(unittest2.TestCase):
    def test_decoder(self):
        self.assertEqual(b85decode(encoded, ASCII85_PREFIX, ASCII85_SUFFIX), raw)

    def test_decoding_unicode_raises_UnicodeEncodeError(self):
        self.assertRaises(UnicodeEncodeError, b85decode, u"深入")

    def test_decoder_ignores_whitespace_by_default(self):
        self.assertEqual(b85decode(encoded_with_whitespace), raw)

    def test_decoder_ignores_ends_by_default(self):
        self.assertEqual(b85decode(encoded_with_ends_and_whitespace,
                                   ASCII85_PREFIX, ASCII85_SUFFIX), raw)

    def test_encoding_wikipedia(self):
        self.assertEqual(b85decode(b("9jqo^")), "Man ")
        self.assertEqual(b85decode(b("F*2M7")), "sure")

    def test_check_padding(self):
        self.assertEqual(b85decode(b("/c")), ".")

    def test_decode_boundary(self):
        self.assertEqual(b85decode(b("s8W-!")), "\xff\xff\xff\xff")

    def test_OverflowError_when_not_decodable_chunk_found(self):
        self.assertRaises(OverflowError, b85decode, b('xy!!!'))

    def test_decodes_z_into_zero_bytes(self):
        self.assertEqual(b85decode('zzz'), '\x00' * 4 * 3)

    def test_decode_zero_groups(self):
        self.assertEqual(b85decode('!!!!!'), '\x00' * 4)

    def test_ValueError_when_zero_char_in_middle_of_chunk(self):
        self.assertRaises(ValueError, b85decode, 'zaz')


class Test_codec_identity(unittest2.TestCase):
    def test_identity(self):
        zero_bytes = '\x00\x00\x00\x00\x00'
        self.assertEqual(b85decode(b85encode(zero_bytes)), zero_bytes)
        self.assertEqual(b85decode(b85encode(random_256_bytes)),
                         random_256_bytes)
        self.assertEqual(b85decode(b85encode(random_odd_bytes)),
                         random_odd_bytes)

class Test_rfc1924_base85_encoding(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(rfc1924_b85encode(mercurial_bytes), mercurial_encoded)
        self.assertEqual(rfc1924_b85encode(random_256_bytes),
                         random_256_mercurial)

    def test_decoding(self):
        self.assertEqual(rfc1924_b85decode(mercurial_encoded), mercurial_bytes)
        self.assertEqual(rfc1924_b85decode(random_256_mercurial),
                         random_256_bytes)
        self.assertEqual(rfc1924_b85decode(b('|NsC0')), '\xff\xff\xff\xff')

    def test_OverflowError_when_not_decodable_chunk_found(self):
        self.assertRaises(OverflowError, rfc1924_b85decode, b(']]]]]'))
        self.assertRaises(OverflowError, rfc1924_b85decode,
                          b('|NsC')) # 0x03030303

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

    def test_decoding(self):
        self.assertEqual(ipv6_b85decode(ipv6_encoded), ipv6_number)
        self.assertEqual(ipv6_b85decode(ipv6_encoded_2), ipv6_number_2)

    def test_decoding_unicode_raises_UnicodeEncodeError(self):
        self.assertRaises(UnicodeEncodeError, ipv6_b85decode, u"深入")

    def test_codec_identity(self):
        self.assertEqual(ipv6_b85decode(ipv6_b85encode(ipv6_number)),
                         ipv6_number)
        self.assertEqual(ipv6_b85decode(ipv6_b85encode(ipv6_number_2)),
                         ipv6_number_2)

    def test_ValueError_when_negative(self):
        self.assertRaises(ValueError, ipv6_b85encode, -1)

    def test_OverflowError_when_greater_than_128_bit(self):
        self.assertRaises(OverflowError, ipv6_b85encode, 2**128)

    def test_ValueError_when_encoded_length_not_20(self):
        self.assertRaises(ValueError, ipv6_b85decode,
                          '=r54lj&NUUO~Hi%c2ym0=')

    def test_TypeError_when_not_number(self):
        self.assertRaises(TypeError, ipv6_b85encode, None)

    def test_ValueError_when_whitespace_found(self):
        self.assertRaises(ValueError, ipv6_b85decode, '=r54lj&\nUUO Hi%c2ym0')
        