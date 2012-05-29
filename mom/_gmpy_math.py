#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Public domain.


"""GMPY-based functions."""


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


try:
  import gmpy2 as gmpy

  HAVE_GMPY = True
except ImportError:
  try:
    import gmpy

    HAVE_GMPY = True
  except ImportError:
    gmpy = None
    HAVE_GMPY = False


if HAVE_GMPY:

  def pow_mod(base, power, modulus):
    """Calculates:

        base**pow mod modulus

    :param base:
        Base
    :param power:
        Power
    :param modulus:
        Modulus
    :returns:
        base**pow mod modulus
    """
    base = gmpy.mpz(base)
    power = gmpy.mpz(power)
    modulus = gmpy.mpz(modulus)
    result = pow(base, power, modulus)
    return int(result)

  def is_prime(num, *unused_args, **unused_kwargs):
    """Determines whether an integer is prime."""
    return gmpy.is_prime(num)
