#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.net.ip import ipv4_to_integer, integer_to_ipv4, parse_ipv4

test_ips = '''\
0.0.0.0
127.0.0.1
83.198.135.28
83.126.35.59
192.168.1.1
194.168.1.255
196.25.210.14
64.22.109.113
'''.splitlines()

test_tuples = [
    (0, 0, 0, 0),
    (127,0,0,1),
    (83, 198, 135, 28),
    (83, 126, 35, 59),
    (192, 168, 1, 1),
    (194, 168, 1, 255),
    (196, 25, 210, 14),
    (64, 22, 109, 113),
]

ip_ints = [
    0,
    2130706433,
    1405519644,
    1400775483,
    3232235777,
    3265790463,
    3290026510,
    1075211633,
]


class Test_parse_ipv4(unittest2.TestCase):
    def test_parsing(self):
        for ip_addr, ip_tuple in zip(test_ips, test_tuples):
            self.assertEqual(parse_ipv4(ip_addr), ip_tuple)

    def test_OverflowError_when_component_greater_than_255(self):
        self.assertRaises(OverflowError, parse_ipv4, "256.256.256.256")

    def test_AttributeError_when_None(self):
        self.assertRaises(AttributeError, parse_ipv4, None)

    def test_ValueError_when_invalid_ip_address_format(self):
        # Non-integral components.
        self.assertRaises(ValueError, parse_ipv4, "a.b.c.d")
        # Tuple unpacking.
        self.assertRaises(ValueError, parse_ipv4, "127.0.0")

class Test_ipv4_to_integer(unittest2.TestCase):
    def test_ipv4_to_integer(self):
        for ip_addr, ip_int in zip(test_ips, ip_ints):
            self.assertEqual(ipv4_to_integer(ip_addr), ip_int)

    def test_OverflowError_when_component_greater_than_255(self):
        self.assertRaises(OverflowError, ipv4_to_integer, "256.256.256.256")

    def test_AttributeError_when_None(self):
        self.assertRaises(AttributeError, ipv4_to_integer, None)

    def test_ValueError_when_invalid_ip_address_format(self):
        # Non-integral components.
        self.assertRaises(ValueError, ipv4_to_integer, "a.b.c.d")
        # Tuple unpacking.
        self.assertRaises(ValueError, ipv4_to_integer, "127.0.0")

class Test_integer_to_ipv4(unittest2.TestCase):
    def test_integer_to_ipv4(self):
        for ip_addr, ip_int in zip(test_ips, ip_ints):
            self.assertEqual(integer_to_ipv4(ip_int), ip_addr)

