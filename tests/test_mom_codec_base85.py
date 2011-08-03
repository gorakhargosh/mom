#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
from mom.builtins import b

from mom.codec.base85 import b85decode, b85encode

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
