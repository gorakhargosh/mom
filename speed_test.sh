#!/bin/sh

echo "integer_to_bytes speed test"
echo "python2.5"
python2.5 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
python2.5 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
echo "python2.6"
python2.6 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n, 516)'
python2.6 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n, 516)'
echo "python2.7"
python2.7 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
python2.7 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
echo "python3.2"
python3 -mtimeit -s'from mom.codec.integer import integer_to_bytes; n = 1<<4096' 'integer_to_bytes(n)'
python3 -mtimeit -s'from mom.codec.integer import _integer_to_bytes; n = 1<<4096' '_integer_to_bytes(n)'
