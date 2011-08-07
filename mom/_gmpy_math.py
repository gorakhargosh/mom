#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Public domain.

try:
    import gmpy2 as gmpy
    have_gmpy = True
except ImportError:
    try:
        import gmpy
        have_gmpy = True
    except ImportError:
        have_gmpy = False

if have_gmpy:
    def pow_mod(base, power, modulus):
        """
        Calculates:

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

    def is_prime(num, *args, **kwargs):
        return gmpy.is_prime(num)
