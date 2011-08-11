#!/bin/sh

echo "integer_to_bytes speed test"
echo "python2.5"
python2.5 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
python2.5 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
python2.5 -mtimeit -s'from mom.codec.integer import _integer_to_bytes_array_based; n = 1<<4096' '_integer_to_bytes_array_based(n)'
echo "python2.6"
python2.6 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n, 516)'
python2.6 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n, 516)'
python2.6 -mtimeit -s'from mom.codec.integer import _integer_to_bytes_array_based; n = 1<<4096' '_integer_to_bytes_array_based(n)'
echo "python2.7"
python2.7 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
python2.7 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
python2.7 -mtimeit -s'from mom.codec.integer import _integer_to_bytes_array_based; n = 1<<4096' '_integer_to_bytes_array_based(n)'
echo "python3.2"
python3 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
python3 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
python3 -mtimeit -s'from mom.codec.integer import _integer_to_bytes_array_based; n = 1<<4096' '_integer_to_bytes_array_based(n)'
echo "pypy"
pypy -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
pypy -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
pypy -mtimeit -s'from mom.codec.integer import _integer_to_bytes_array_based; n = 1<<4096' '_integer_to_bytes_array_based(n)'



echo "bytes_to_integer speed test"
echo "python2.5"
python2.5 -mtimeit -s'from mom.codec.integer import bytes_to_integer; import os; n = os.urandom(4003)' 'bytes_to_integer(n)'
python2.5 -mtimeit -s'from mom.codec.integer import _bytes_to_integer; import os; n = os.urandom(4003)' '_bytes_to_integer(n)'
echo "python2.6"
python2.6 -mtimeit -s'from mom.codec.integer import bytes_to_integer; import os; n = os.urandom(4003)' 'bytes_to_integer(n)'
python2.6 -mtimeit -s'from mom.codec.integer import _bytes_to_integer; import os; n = os.urandom(4003)' '_bytes_to_integer(n)'
echo "python2.7"
python2.7 -mtimeit -s'from mom.codec.integer import bytes_to_integer; import os; n = os.urandom(4003)' 'bytes_to_integer(n)'
python2.7 -mtimeit -s'from mom.codec.integer import _bytes_to_integer; import os; n = os.urandom(4003)' '_bytes_to_integer(n)'
echo "python3.2"
python3 -mtimeit -s'from mom.codec.integer import bytes_to_integer; import os; n = os.urandom(4003)' 'bytes_to_integer(n)'
python3 -mtimeit -s'from mom.codec.integer import _bytes_to_integer; import os; n = os.urandom(4003)' '_bytes_to_integer(n)'
echo "pypy"
pypy -mtimeit -s'from mom.codec.integer import bytes_to_integer; import os; n = os.urandom(4003)' 'bytes_to_integer(n)'
pypy -mtimeit -s'from mom.codec.integer import _bytes_to_integer; import os; n = os.urandom(4003)' '_bytes_to_integer(n)'
