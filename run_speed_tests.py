#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tests.speed import report

setups = [
    "from mom.codec.base58 import b58decode, b58encode; import os; b = b58encode(os.urandom(60))",
    "from mom.codec._alt_base import b58decode_naive; from mom.codec.base58 import b58encode; import os; b = b58encode(os.urandom(60))",
    None,
    "from mom.codec.base62 import b62decode, b62encode; import os; b = b62encode(os.urandom(60))",
    "from mom.codec._alt_base import b62decode_naive; from mom.codec.base62 import b62encode; import os; b = b62encode(os.urandom(60))",
    None,
    "from mom.codec.base85 import b85encode; import os; b = os.urandom(256)",
    "from mom.codec.base85 import b85decode, b85encode; import os; b = b85encode(os.urandom(256))",
    "from mom.codec.base85 import b85encode; import os; b = os.urandom(4096)",
    "from mom.codec.base85 import b85decode, b85encode; import os; b = b85encode(os.urandom(4096))",
    None,
    "from mom.builtins import integer_byte_length; n=1<<4096",
    "from mom._alt_builtins import integer_byte_length_word_aligned; n=1<<4096",
    "from mom._alt_builtins import integer_byte_length_shift_counting; n=1<<4096",
    None,
    "from mom.builtins import integer_bit_length; n=1<<4096",
    "from mom._alt_builtins import integer_bit_length_word_aligned; n=1<<4096",
    "from mom._alt_builtins import integer_bit_length_shift_counting; n=1<<4096",
    None,
    "from mom.codec.integer import uint_to_bytes; n=1<<4096",
    "from mom.codec._alt_integer import uint_to_bytes_pycrypto; n=1<<4096",
    "from mom.codec._alt_integer import uint_to_bytes_array_based; n=1<<4096",
    "from mom.codec._alt_integer import uint_to_bytes_naive; n=1<<4096",
    "from mom.codec._alt_integer import uint_to_bytes_naive_array_based; n=1<<4096",
    None,
    "import os; from mom.codec.integer import bytes_to_uint; b = os.urandom(4003)",
    "import os; from mom.codec._alt_integer import bytes_to_uint_naive; b = os.urandom(4003)",
]
statements = [
    "b58decode(b)",
    "b58decode_naive(b)",
    None,
    "b62decode(b)",
    "b62decode_naive(b)",
    None,
    "b85encode(b)",
    "b85decode(b)",
    "b85encode(b)",
    "b85decode(b)",
    None,
    "integer_byte_length(n)",
    "integer_byte_length_word_aligned(n)",
    "integer_byte_length_shift_counting(n)",
    None,
    "integer_bit_length(n)",
    "integer_bit_length_word_aligned(n)",
    "integer_bit_length_shift_counting(n)",
    None,
    "uint_to_bytes(n)",
    "uint_to_bytes_pycrypto(n)",
    "uint_to_bytes_array_based(n)",
    "uint_to_bytes_naive(n)",
    "uint_to_bytes_naive_array_based(n)",
    None,
    "bytes_to_uint(b)",
    "bytes_to_uint_naive(b)",
]


def main(setups, statements):
    print("Python %s" % sys.version)
    for setup, statement in zip(setups, statements):
        if setup is None or statement is None:
            print("")
        else:
            report(statement, setup)
    print("\n%s" % ("-" * 100))

if __name__ == "__main__":
    main(setups, statements)

