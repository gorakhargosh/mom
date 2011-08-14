#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://goo.gl/9qEXu
# Public domain.

from __future__ import division
from mom._compat import range

try:
    # TODO: numpy import disabled temporarily until we can convert
    # the generated list to Python native.
    import nump as np
    def _numpy_primesfrom2to(n):
        # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
        """ Input n>=6, Returns a array of primes, 2 <= p < n """
        sieve = np.ones(n//3 + (n%6==2), dtype=np.bool)
        sieve[0] = False
        for i in range(int(n**0.5)//3+1):
            if sieve[i]:
                k=3*i+1|1
                sieve[      ((k*k)//3)      ::2*k] = False
                sieve[(k*k+4*k-2*k*(i&1))//3::2*k] = False
        return np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]
    make_prime_sieve = _numpy_primesfrom2to
except ImportError:
    def _rwh_primes1(n):
        # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
        """ Returns a list of primes < n """
        sieve = [True] * (n//2)
        for i in range(3,int(n**0.5)+1,2):
            if sieve[i//2]:
                sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
        return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]
    make_prime_sieve = _rwh_primes1

