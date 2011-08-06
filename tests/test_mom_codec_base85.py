#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from mom.builtins import b

from mom.codec.base85 import b85decode, b85encode, b85_rfc1924_encode, b85_rfc1924_decode

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


class Test_base85_encode(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(b85encode(raw, None, None), encoded)

    def test_encoding_wikipedia(self):
        self.assertEqual(b85encode(b("Man "), None, None), "9jqo^")
        self.assertEqual(b85encode(b("sure"), None, None), "F*2M7")

    def test_check_padding(self):
        self.assertEqual(b85encode(b("."), None, None, True), "/cYkO")
        self.assertEqual(b85encode(b("."), None, None), "/c")

class Test_base85_decode(unittest2.TestCase):
    def test_decoder(self):
        self.assertEqual(b85decode(encoded), raw)

    def test_decoder_ignores_whitespace_by_default(self):
        self.assertEqual(b85decode(encoded_with_whitespace), raw)

    def test_decoder_ignores_ends_by_default(self):
        self.assertEqual(b85decode(encoded_with_ends_and_whitespace), raw)

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

class Test_codec_identity(unittest2.TestCase):
    def test_identity(self):
        zero_bytes = '\x00\x00\x00\x00\x00'
        self.assertEqual(b85decode(b85encode(zero_bytes)), zero_bytes)

ipv6_address = '1080:0:0:0:8:800:200C:417A'
ipv6_number = 21932261930451111902915077091070067066L
ipv6_raw_bytes = '\x10\x80\x00\x00\x00\x00\x00\x00\x00\x08\x08\x00 \x0cAz'
ipv6_encoded = '4)+k&C#VzJ4br>0wv%Yp'

# Wikipedia example.
ipv6_number_2 = 2**128 - 1  # 340282366920938463463374607431768211455L
ipv6_encoded_2 = '=r54lj&NUUO~Hi%c2ym0'


class Test_base85_rfc1924_encoding(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(b85_rfc1924_encode(ipv6_number), ipv6_encoded)
        self.assertEqual(b85_rfc1924_encode(ipv6_number_2), ipv6_encoded_2)

    def test_decoding(self):
        self.assertEqual(b85_rfc1924_decode(ipv6_encoded), ipv6_number)
        self.assertEqual(b85_rfc1924_decode(ipv6_encoded_2), ipv6_number_2)

    def test_codec_identity(self):
        self.assertEqual(b85_rfc1924_decode(b85_rfc1924_encode(ipv6_number)),
                         ipv6_number)
        self.assertEqual(b85_rfc1924_decode(b85_rfc1924_encode(ipv6_number_2)),
                         ipv6_number_2)
