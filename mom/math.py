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

""":synopsis: Math routines.
:module: mom.math

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
.. autofunction:: is_prime(num, iterations=5, sieve=sieve)
"""

from __future__ import absolute_import
from __future__ import division

from mom import builtins
from mom import prime_sieve
from mom.security import random


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "gcd",
    "generate_random_prime",
    "generate_random_safe_prime",
    "inverse_mod",
    "is_prime",
    "lcm",
    "pow_mod",
    ]


def gcd(num_a, num_b):
  """Calculates the greatest common divisor.

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
  """Least common multiple.

  :param num_a:
      Integer value.
  :param num_b:
      Integer value.
  :returns:
      Least common multiple.
  """
  return (num_a * num_b) // gcd(num_a, num_b)


def inverse_mod(num_a, num_b):
  """Returns inverse of a mod b, zero if none

  Uses Extended Euclidean Algorithm

  :param num_a:
      Long value
  :param num_b:
      Long value
  :returns:
      Inverse of a mod b, zero if none.
  """
  num_c, num_d = num_a, num_b
  num_uc, num_ud = 1, 0
  while num_c:
    quotient = num_d // num_c
    num_c, num_d = num_d - (quotient * num_c), num_c
    num_uc, num_ud = num_ud - (quotient * num_uc), num_uc
  if num_d == 1:
    return num_ud % num_b
  return 0


def exact_log2(number):
  """Find and return an unsigned integer i >= 0 such that ``number == 2**i``. If
  no such integer exists, this function raises ValueError.

  .. NOTE:
      It essentially answers this question:

      "How many times would you have to multiply 2 into itself to
      get the given number?"

  Taken from PyCrypto.

  :param number:
      Unsigned integer.
  :returns:
      An integer i >= 0 such that number == 2**i.
  """
  num = number
  if num <= 0:
    raise ValueError("Cannot compute logarithm of non-positive integer")
  i = 0
  while num:
    if (num & 1) and num != 1:
      raise ValueError("No solution could be found")
    i += 1
    num >>= 1
  i -= 1
  #assert number == (1 << i)
  return i


def _pure_pow_mod(base, power, modulus):
  """Calculates:
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

  # NOTE(TREV): Added support for negative exponents
  negative_result = False
  if power < 0:
    power *= -1
    negative_result = True

  #exp2 = 2**n_bit_scan
  exp2 = 1 << n_bit_scan
  mask = exp2 - 1

  # Break power into a list of digits of nBitScan bits.
  # The list is recursive so easy to read in reverse direction.
  nibbles = None
  while power:
    nibbles = int(power & mask), nibbles
    power >>= n_bit_scan

  # Make a table of powers of base up to 2**nBitScan - 1
  low_powers = [1]
  for i in builtins.range(1, exp2):
    low_powers.append((low_powers[i - 1] * base) % modulus)

  # To exponentiate by the first nibble, look it up in the table
  nib, nibbles = nibbles
  prod = low_powers[nib]

  # For the rest, square nBitScan times, then multiply by
  # base^nibble
  while nibbles:
    nib, nibbles = nibbles
    for i in builtins.range(n_bit_scan):
      prod = (prod * prod) % modulus
    if nib: prod = (prod * low_powers[nib]) % modulus

  # NOTE(TREV): Added support for negative exponents
  if negative_result:
    prod_inv = inverse_mod(prod, modulus)
    # Check to make sure the inverse is correct
    assert (prod * prod_inv) % modulus == 1
    return prod_inv
  return prod


def _pure_is_prime(num, iterations=5, _sieve=prime_sieve.SIEVE):
  """Determines whether a number is prime.

  :param num:
      Number
  :param iterations:
      Number of iterations.
  :returns:
      ``True`` if prime; ``False`` otherwise.
  """

  # Trial division with sieve
  for prime_number in _sieve:
    if prime_number >= num:
      return True
    if not num % prime_number:
      return False
    # Passed trial division, proceed to Rabin-Miller
  # Rabin-Miller implemented per Ferguson & Schneier
  # Compute s, t for Rabin-Miller
  num_s, num_t = num - 1, 0
  while not num_s % 2:
    num_s, num_t = num_s // 2, num_t + 1
    # Repeat Rabin-Miller x times
  base = 2  # Use 2 as a base for first iteration speedup, per HAC
  for _ in builtins.range(iterations):
    num_v = _pure_pow_mod(base, num_s, num)
    if num_v == 1:
      continue
    i = 0
    while num_v != num - 1:
      if i == num_t - 1:
        return False
      else:
        num_v, i = _pure_pow_mod(num_v, 2, num), i + 1
    base = random.generate_random_uint_between(2, num)
  return True


try:
  from mom._gmpy_math import is_prime as _is_prime
  from mom._gmpy_math import pow_mod as _pow_mod
except ImportError:
  _pow_mod = _pure_pow_mod
  _is_prime = _pure_is_prime

pow_mod = _pow_mod
is_prime = _is_prime


def generate_random_prime(bits):
  """Generates a random prime number.

  :param bits:
      Number of bits.
  :return:
      Prime number long value.
  """
  assert not bits < 10

  # The 1.5 ensures the 2 MSBs are set
  # Thus, when used for p,q in RSA, n will have its MSB set
  #
  # Since 30 is lcm(2,3,5), we'll set our test numbers to
  # 29 % 30 and keep them there
  # low = (2 ** (bits-1)) * 3 // 2
  # high = 2 ** bits - 30
  low = (1 << (bits - 1)) * 3 // 2
  high = (1 << bits) - 30
  random_uint = random.generate_random_uint_between(low, high)
  random_uint += 29 - (random_uint % 30)
  while 1:
    random_uint += 30
    if random_uint >= high:
      random_uint = random.generate_random_uint_between(low, high)
      random_uint += 29 - (random_uint % 30)
    if is_prime(random_uint):
      return random_uint


def generate_random_safe_prime(bits):
  """Unused at the moment.

  Generates a random prime number.

  :param bits:
      Number of bits.
  :return:
      Prime number long value.
  """
  assert not bits < 10

  # The 1.5 ensures the 2 MSBs are set
  # Thus, when used for p,q in RSA, n will have its MSB set
  #
  # Since 30 is lcm(2,3,5), we'll set our test numbers to
  # 29 % 30 and keep them there
  # low = (2 ** (bits-2)) * 3 // 2
  # high = (2 ** (bits-1)) - 30
  low = (1 << (bits - 2)) * 3 // 2
  high = (1 << (bits - 1)) - 30
  random_uint = random.generate_random_uint_between(low, high)
  random_uint += 29 - (random_uint % 30)
  while 1:
    random_uint += 30
    if random_uint >= high:
      random_uint = random.generate_random_uint_between(low, high)
      random_uint += 29 - (random_uint % 30)
      # Ideas from Tom Wu's SRP code
    # Do trial division on p and q before Rabin-Miller
    if is_prime(random_uint, 0):
      possible_prime = (2 * random_uint) + 1
      if is_prime(possible_prime):
        if is_prime(random_uint):
          return possible_prime
