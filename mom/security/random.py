#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: mom.security.random
:synopsis: Random number, bits, bytes, string, sequence, & password generation.

Bits and bytes
---------------------------
.. autofunction:: generate_random_bits
.. autofunction:: generate_random_bytes

Numbers
-------
.. autofunction:: generate_random_ulong_atmost
.. autofunction:: generate_random_ulong_exactly
.. autofunction:: generate_random_ulong_between

Sequences and choices
---------------------
.. autofunction:: random_choice
.. autofunction:: generate_random_sequence
.. autofunction:: generate_random_sequence_strong

Strings
-------
.. autofunction:: generate_random_string
.. autofunction:: generate_random_password
.. autofunction:: generate_random_hex_string

Utility
-------
.. autofunction:: calculate_entropy

"""

from __future__ import absolute_import, division

import string
import os
from mom.builtins import long_bit_length, is_integer
from mom.codec import \
    hex_encode, \
    bytes_to_long


__all__ = [
    "generate_random_bits",
    "generate_random_bytes",
    "generate_random_hex_string",
    "generate_random_ulong_atmost",
    "generate_random_ulong_exactly",
    "generate_random_ulong_between",
    "generate_random_string",
    "generate_random_password",
    "generate_random_sequence",
    "generate_random_sequence_strong",
    "random_choice",
    "calculate_entropy",
    "HEXADECIMAL_DIGITS",
    "DIGITS",
    "LOWERCASE_ALPHA",
    "UPPERCASE_ALPHA",
    "LOWERCASE_ALPHANUMERIC",
    "UPPERCASE_ALPHANUMERIC",
    "ALPHA",
    "ALPHANUMERIC",
    "ASCII_PRINTABLE",
    "ALL_PRINTABLE",
    "PUNCTUATION",
    ]


try:
    # Operating system unsigned random.
    os.urandom(1)
    def generate_random_bytes(count):
        """
        Generates a random byte string with ``count`` bytes.

        :param count:
            Number of bytes.
        :returns:
            Random byte string.
        """
        return os.urandom(count)
except AttributeError:
    try:
        __urandom_device__ = open("/dev/urandom", "rb")
        def generate_random_bytes(count):
            """
            Generates a random byte string with ``count`` bytes.

            :param count:
                Number of bytes.
            :returns:
                Random byte string.
            """
            return __urandom_device__.read(count)
    except IOError:
        #Else get Win32 CryptoAPI PRNG
        try:
            import win32prng
            def generate_random_bytes(count):
                """
                Generates a random byte string with ``count`` bytes.

                :param count:
                    Number of bytes.
                :returns:
                    Random byte string.
                """
                random_bytes = win32prng.generate_random_bytes(count)
                assert len(random_bytes) == count
                return random_bytes
        except ImportError:
            # What the fuck?!
            def generate_random_bytes(_):
                """
                WTF.

                :returns:
                    WTF.
                """
                raise NotImplementedError("What the fuck?! No PRNG available.")


def generate_random_bits(n_bits, rand_func=generate_random_bytes):
    """
    Generates the specified number of random bits as a byte string.
    For example::

        f(x) -> y such that
        f(16) ->           1111 1111 1111 1111; bytes_to_long(y) => 65535L
        f(17) -> 0000 0001 1111 1111 1111 1111; bytes_to_long(y) => 131071L

    :param n_bits:
        Number of random bits.

        if n is divisible by 8, (n / 8) bytes will be returned.
        if n is not divisible by 8, ((n / 8) + 1) bytes will be returned
        and the prefixed offset-byte will have `(n % 8)` number of random bits,
        (that is, `8 - (n % 8)` high bits will be cleared).

        The range of the numbers is 0 to (2**n)-1 inclusive.
    :param rand_func:
        Random bytes generator function.
    :returns:
        Bytes.
    """
    if not is_integer(n_bits):
        raise TypeError("unsupported operand type: %r" % type(n_bits).__name__)
    if n_bits <= 0:
        raise ValueError("number of bits must be greater than 0.")
    # Doesn't perform any floating-point operations.
    q, r = divmod(n_bits, 8)
    random_bytes = rand_func(q)
    if r:
        offset = ord(rand_func(1)) >> (8 - r)
        random_bytes = chr(offset) + random_bytes
    return random_bytes


def generate_random_ulong_atmost(n_bits, rand_func=generate_random_bytes):
    """
    Generates a random unsigned long with `n_bits` random bits.

    :param n_bits:
        Number of random bits to be generated at most.
    :param rand_func:
        Random bytes generator function.
    :returns:
        Returns an unsigned long integer with at most `n_bits` random bits.
        The generated unsigned long integer will be between 0 and
        (2**n_bits)-1 both inclusive.
    """
    if not is_integer(n_bits):
        raise TypeError("unsupported operand type: %r" % type(n_bits).__name__)
    if n_bits <= 0:
        raise ValueError("number of bits must be greater than 0.")
    # Doesn't perform any floating-point operations.
    q, r = divmod(n_bits, 8)
    if r:
        q += 1
    random_bytes = rand_func(q)
    mask = (1L << n_bits) - 1
    return mask & bytes_to_long(random_bytes)


def generate_random_ulong_exactly(n_bits, rand_func=generate_random_bytes):
    """
    Generates a random unsigned long with `n_bits` random bits.

    :param n_bits:
        Number of random bits.
    :param rand_func:
        Random bytes generator function.
    :returns:
        Returns an unsigned long integer with `n_bits` random bits.
        The generated unsigned long integer will be between 2**(n_bits-1) and
         (2**n_bits)-1 both inclusive.
    """
    # Doesn't perform any floating-point operations.
    value = bytes_to_long(generate_random_bits(n_bits, rand_func=rand_func))
    #assert(value >= 0 and value < (2L ** n_bits))
    # Set the high bit to ensure bit length.
    #value |= 2L ** (n_bits - 1)
    value |= 1L << (n_bits - 1)
    #assert(long_bit_length(value) >= n_bits)
    return value


# Taken from PyCrypto.
def generate_random_ulong_between(low, high, rand_func=generate_random_bytes):
    """
    Generates a random long integer between low and high, not including high.

    :param low:
        Low
    :param high:
        High
    :param rand_func:
        Random bytes generator function.
    :returns:
        Random unsigned long integer value.
    """
    if not (is_integer(low) and is_integer(high)):
        raise TypeError("unsupported operand types(s): %r and %r" \
                        % (type(low).__name__, type(high).__name__))
    if low >= high:
        raise ValueError("high value must be greater than low value.")
    r = high - low - 1
    bits = long_bit_length(r)
    value = generate_random_ulong_atmost(bits, rand_func=rand_func)
    while value > r:
        value = generate_random_ulong_atmost(bits, rand_func=rand_func)
    return low + value


def generate_random_hex_string(length=8, rand_func=generate_random_bytes):
    """
    Generates a random ASCII-encoded hexadecimal string of an even length.

    :param length:
        Length of the string to be returned. Default 32.
        The length MUST be a positive even number.
    :param rand_func:
        Random bytes generator function.
    :returns:
        A string representation of a randomly-generated hexadecimal string.
    """
    #if length % 2 or length <= 0:
    if length & 1L or length <= 0:
        raise ValueError(
            "This function expects a positive even number "\
            "length: got length `%r`." % length)
    return hex_encode(rand_func(length >> 1))


def random_choice(sequence):
    """
    Randomly chooses an element from the given non-empty sequence.

    :param sequence:
        Non-empty sequence to randomly choose an element from.
    :returns:
        Randomly chosen element.
    """
    return sequence[generate_random_ulong_between(0, len(sequence))]


def generate_random_sequence(length, pool):
    """
    Generates a random sequence of given length using the sequence
    pool specified.

    :param length:
        The length of the random sequence.
    :param pool:
        A sequence of elements to be used as the pool from which
        random elements will be chosen.
    :returns:
        A list of elements randomly chosen from the pool.
    """
    if not is_integer(length):
        raise TypeError("Length must be a positive integer: got `%r`" % \
                        type(length).__name__)
    if length <= 0:
        raise ValueError("length must be a positive integer: got %d" % length)
    return [random_choice(pool) for _ in range(length)]


HEXADECIMAL_DIGITS = string.digits + "abcdef"
DIGITS = string.digits
LOWERCASE_ALPHA = string.lowercase
UPPERCASE_ALPHA = string.uppercase
LOWERCASE_ALPHANUMERIC = string.lowercase + string.digits
UPPERCASE_ALPHANUMERIC = string.uppercase + string.digits
ALPHA = string.letters
ALPHANUMERIC = string.letters + string.digits
ASCII_PRINTABLE = string.letters + string.digits + string.punctuation
ALL_PRINTABLE = string.printable
PUNCTUATION = string.punctuation

def generate_random_string(length, characters=ALPHANUMERIC):
    """
    Generates a random string of given length using the sequence
    pool specified.

    Don't use this to generate passwords. Use generate_random_password instead.

    Entropy:

         H = log2(N**L)

    where:

    * H is the entropy in bits.
    * N is the possible symbol count
    * L is length of string of symbols

    Entropy chart::

        -----------------------------------------------------------------
        Symbol set              Symbol Count (N)  Entropy per symbol (H)
        -----------------------------------------------------------------
        HEXADECIMAL_DIGITS      16                4.0000 bits
        DIGITS                  10                3.3219 bits
        LOWERCASE_ALPHA         26                4.7004 bits
        UPPERCASE_ALPHA         26                4.7004 bits
        PUNCTUATION             32                5.0000 bits
        LOWERCASE_ALPHANUMERIC  36                5.1699 bits
        UPPERCASE_ALPHANUMERIC  36                5.1699 bits
        ALPHA                   52                5.7004 bits
        ALPHANUMERIC            62                5.9542 bits
        ASCII_PRINTABLE         94                6.5546 bits
        ALL_PRINTABLE           100               6.6438 bits

    :param length:
        The length of the random sequence.
    :param characters:
        A sequence of characters to be used as the pool from which
        random characters will be chosen. Default case-sensitive alpha-numeric
        characters.
    :returns:
        A list of elements randomly chosen from the pool.
    """
    return "".join(generate_random_sequence(length, characters))


def calculate_entropy(length, pool=ALPHANUMERIC):
    """
    Determines the entropy of the given sequence length and the pool.

    :param length:
        The length of the generated random sequence.
    :param pool:
        The pool of unique elements used to generate the sequence.
    :returns:
        The entropy (in bits) of the random sequence.
    """
    from math import log

    pool = set(pool)
    log_of_2 = 0.6931471805599453
    entropy = length * (log(len(pool)) / log_of_2)

    return entropy


def generate_random_sequence_strong(entropy, pool):
    """
    Generates a random sequence based on entropy.

    If you're using this to generate passwords based on entropy:
    http://en.wikipedia.org/wiki/Password_strength

    :param entropy:
        Desired entropy in bits.
    :param pool:
        The pool of unique elements from which to randomly choose.
    :returns:
        Randomly generated sequence with specified entropy.
    """
    from math import log, ceil

    pool = list(set(pool))
    log_of_2 = 0.6931471805599453
    length = long(ceil((log_of_2 / log(len(pool))) * entropy))

    return generate_random_sequence(length, pool)


def generate_random_password(entropy, pool=ASCII_PRINTABLE):
    """
    Generates a password based on entropy.

    If you're using this to generate passwords based on entropy:
    http://en.wikipedia.org/wiki/Password_strength

    :param entropy:
        Desired entropy in bits. Choose at least 64 to have a decent password.
    :param pool:
        The pool of unique characters from which to randomly choose.
    :returns:
        Randomly generated password with specified entropy.
    """
    return ''.join(generate_random_sequence_strong(entropy, pool))
