#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tests.speed import report

setups = [
    "from mom.codec.integer import integer_to_bytes; n=1<<4096",
    "from mom.codec.integer import _integer_to_bytes; n=1<<4096",
    "from mom.codec.integer import _integer_to_bytes_array_based; n=1<<4096",
    None,
    "import os; from mom.codec.integer import bytes_to_integer; b = os.urandom(4003)",
    "import os; from mom.codec.integer import _bytes_to_integer; b = os.urandom(4003)",
]
statements = [
    "integer_to_bytes(n)",
    "_integer_to_bytes(n)",
    "_integer_to_bytes_array_based(n)",
    None,
    "bytes_to_integer(b)",
    "_bytes_to_integer(b)",
]


def main(setups, statements):
    print("Python %s" % sys.version)
    for setup, statement in zip(setups, statements):
        if setup is None or statement is None:
            print("")
        else:
            report(statement, setup)
    print("\n------------------------------------------------------\n")

if __name__ == "__main__":
    main(setups, statements)

