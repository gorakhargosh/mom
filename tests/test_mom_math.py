#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2

from mom.math import gcd, lcm, is_prime, _pure_is_prime, \
    generate_random_prime, generate_random_safe_prime
from mom._prime_sieve import make_prime_sieve

class Test__pure_is_prime(unittest2.TestCase):
    def test_pure_is_prime_for_sieves(self):
        for i in [10, 100, 1000, 10000]:
            sieve = make_prime_sieve(i)
            odds = []
            for x in sieve:
                if not _pure_is_prime(x, _sieve=[2, 3]):
                    odds.append(x)
            self.assertEqual(odds, [])

    def test_non_prime_by_sieve(self):
        self.assertFalse(_pure_is_prime(100))
        
class Test_generate_random_prime(unittest2.TestCase):
    def test_generate_random_prime(self):
        for x in range(100):
            self.assertTrue(is_prime(generate_random_prime(64)))
        
class Test_generate_random_safe_prime(unittest2.TestCase):
    def test_generate_random_safe_prime(self):
        for x in range(20):
            self.assertTrue(is_prime(generate_random_safe_prime(64)))
        

class Test_gcd(unittest2.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(54, 24), 6)

    def test_gcd_swap(self):
        self.assertEqual(gcd(24, 54), 6)

class Test_lcm(unittest2.TestCase):
    def test_lcm(self):
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(6, 4), 12)
        self.assertEqual(lcm(21, 6), 42)
        
