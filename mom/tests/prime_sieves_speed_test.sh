#!/bin/sh

PYTHON=python2.7

$PYTHON -mtimeit -s'import primes' 'primes.sieveOfEratosthenes(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.ambi_sieve(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.ambi_sieve_plain(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.sundaram3(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.sieve_wheel_30(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.primesfrom3to(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.primesfrom2to(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.rwh_primes(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.rwh_primes1(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.rwh_primes2(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.get_primes_erat(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.make_prime_sieve(1000000)'
$PYTHON -mtimeit -s'import primes' 'primes.primes_upto2_gen3(1000000)'
