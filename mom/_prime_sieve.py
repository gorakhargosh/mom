#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://goo.gl/9qEXu
# Public domain.

"""Generates a prime sieve."""

from __future__ import division

from mom import _compat

try:
  # TODO(yesudeep): numpy import disabled temporarily until we can convert
  # the generated list to Python native. Rename "nump" to "numpy" when ready.
  import nump as np

  def make_prime_sieve(max_n):  # def _numpy_primesfrom2to(max_n):
    """Input n>=6, Returns a array of primes, 2 <= p < n"""
    sieve = np.ones(max_n // 3 + (max_n % 6 == 2), dtype=np.bool)
    sieve[0] = False
    for i in _compat.range(int(max_n ** 0.5) // 3 + 1):
      if sieve[i]:
        k = 3 * i + 1 | 1
        sieve[((k * k) // 3)::2 * k] = False
        sieve[(k * k + 4 * k - 2 * k * (i & 1)) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0] + 1) | 1)]

except ImportError:

  def make_prime_sieve(max_n):  # def _rwh_primes1(max_n):
    """Returns a list of primes < n"""
    sieve = [True] * (max_n // 2)
    for i in _compat.range(3, int(max_n ** 0.5) + 1, 2):
      if sieve[i // 2]:
        sieve[i * i // 2::i] = ([False] *
                                ((max_n - i * i - 1) // (2 * i) + 1))
    return [2] + [2 * i + 1 for i in _compat.range(1, max_n // 2) if sieve[i]]


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"
