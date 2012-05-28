#!/bin/sh
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: yesudeep@google.com (Yesudeep Mangalapilly)


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
