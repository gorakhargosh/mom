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

"""
:module: mom.math
:synopsis: Math routines.

Math
----
.. autofunction:: gcd
.. autofunction:: inverse_mod
.. autofunction:: lcm
.. autofunction:: pow_mod

Primes
------
.. autofunction:: generate_random_prime
.. autofunction:: generate_random_safe_prime
.. autofunction:: is_prime
"""

from __future__ import absolute_import, division
from mom.security.random import generate_random_uint_between
from mom._prime_sieve import sieve

__all__ = [
    "gcd",
    "lcm",
    "pow_mod",
    "inverse_mod",
    "is_prime",
    "generate_random_prime",
    "generate_random_safe_prime",
]

def gcd(num_a, num_b):
    """
    Calculates the greatest common divisor.

    Non-recursive fast implementation.

    :param num_a:
        Long value.
    :param num_b:
        Long value.
    :returns:
        Greatest common divisor.
    """
    num_a, num_b = max(num_a, num_b), min(num_a, num_b)
    while num_b:
        num_a, num_b = num_b, (num_a % num_b)
    return num_a


def lcm(num_a, num_b):
    """
    Least common multiple.

    :param num_a:
        Long value.
    :param v:
        Long value.
    :returns:
        Least common multiple.
    """
    return (num_a * num_b) // gcd(num_a, num_b)


def inverse_mod(num_a, num_b):
    """
    Returns inverse of a mod b, zero if none

    Uses Extended Euclidean Algorithm

    :param num_a:
        Long value
    :param num_b:
        Long value
    :returns:
        Inverse of a mod b, zero if none.
    """
    num_c, num_d = num_a, num_b
    uc, ud = 1, 0
    while num_c:
        quotient = num_d // num_c
        num_c, num_d = num_d - (quotient * num_c), num_c
        uc, ud = ud - (quotient * uc), uc
    if num_d == 1:
        return ud % num_b
    return 0


def _pure_pow_mod(base, power, modulus):
    """
    Calculates:
        base**pow mod modulus

    Uses multi bit scanning with nBitScan bits at a time.
    From Bryan G. Olson's post to comp.lang.python

    Does left-to-right instead of pow()'s right-to-left,
    thus about 30% faster than the python built-in with small bases

    :param base:
        Base
    :param power:
        Power
    :param modulus:
        Modulus
    :returns:
        base**pow mod modulus
    """
    n_bit_scan = 5

    #TREV - Added support for negative exponents
    negative_result = False
    if power < 0:
        power *= -1
        negative_result = True

    exp2 = 2**n_bit_scan
    mask = exp2 - 1

    # Break power into a list of digits of nBitScan bits.
    # The list is recursive so easy to read in reverse direction.
    nibbles = None
    while power:
        nibbles = int(power & mask), nibbles
        power >>= n_bit_scan

    # Make a table of powers of base up to 2**nBitScan - 1
    low_powers = [1]
    for i in xrange(1, exp2):
        low_powers.append((low_powers[i-1] * base) % modulus)

    # To exponentiate by the first nibble, look it up in the table
    nib, nibbles = nibbles
    prod = low_powers[nib]

    # For the rest, square nBitScan times, then multiply by
    # base^nibble
    while nibbles:
        nib, nibbles = nibbles
        for i in xrange(n_bit_scan):
            prod = (prod * prod) % modulus
        if nib: prod = (prod * low_powers[nib]) % modulus

    #TREV - Added support for negative exponents
    if negative_result:
        prodInv = inverse_mod(prod, modulus)
        #Check to make sure the inverse is correct
        assert (prod * prodInv) % modulus == 1
        return prodInv
    return prod


def _pure_is_prime(num, iterations=5, _sieve=sieve):
    """
    Determines whether a number is prime.

    :param num:
        Number
    :param iterations:
        Number of iterations.
    :returns:
        ``True`` if prime; ``False`` otherwise.
    """

    #Trial division with sieve
    for x in _sieve:
        if x >= num:
            return True
        if not num % x:
            return False
    #Passed trial division, proceed to Rabin-Miller
    #Rabin-Miller implemented per Ferguson & Schneier
    #Compute s, t for Rabin-Miller
    s, t = num-1, 0
    while not s % 2:
        s, t = s // 2, t+1
    #Repeat Rabin-Miller x times
    a = 2 #Use 2 as a base for first iteration speedup, per HAC
    for count in range(iterations):
        v = _pure_pow_mod(a, s, num)
        if v == 1:
            continue
        i = 0
        while v != num-1:
            if i == t-1:
                return False
            else:
                v, i = _pure_pow_mod(v, 2, num), i+1
        a = generate_random_uint_between(2, num)
    return True

try:
    from mom._gmpy_math import is_prime as _is_prime, pow_mod as _pow_mod
except ImportError:
    _pow_mod = _pure_pow_mod
    _is_prime = _pure_is_prime

pow_mod = _pow_mod
is_prime = _is_prime


def generate_random_prime(bits):
    """
    Generates a random prime number.

    :param bits:
        Number of bits.
    :return:
        Prime number long value.
    """
    assert not bits < 10

    #The 1.5 ensures the 2 MSBs are set
    #Thus, when used for p,q in RSA, n will have its MSB set
    #
    #Since 30 is lcm(2,3,5), we'll set our test numbers to
    #29 % 30 and keep them there
    #low = (2 ** (bits-1)) * 3 // 2
    #high = 2 ** bits - 30
    low = (1 << (bits - 1)) * 3 // 2
    high = (1 << bits) - 30
    p = generate_random_uint_between(low, high)
    p += 29 - (p % 30)
    while 1:
        p += 30
        if p >= high:
            p = generate_random_uint_between(low, high)
            p += 29 - (p % 30)
        if is_prime(p):
            return p


def generate_random_safe_prime(bits):
    """
    Unused at the moment.

    Generates a random prime number.

    :param bits:
        Number of bits.
    :return:
        Prime number long value.
    """
    assert not bits < 10

    #The 1.5 ensures the 2 MSBs are set
    #Thus, when used for p,q in RSA, n will have its MSB set
    #
    #Since 30 is lcm(2,3,5), we'll set our test numbers to
    #29 % 30 and keep them there
    low = (2 ** (bits-2)) * 3 // 2
    high = (2 ** (bits-1)) - 30
    q = generate_random_uint_between(low, high)
    q += 29 - (q % 30)
    while 1:
        q += 30
        if q >= high:
            q = generate_random_uint_between(low, high)
            q += 29 - (q % 30)
        #Ideas from Tom Wu's SRP code
        #Do trial division on p and q before Rabin-Miller
        if is_prime(q, 0):
            p = (2 * q) + 1
            if is_prime(p):
                if is_prime(q):
                    return p
