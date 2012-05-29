#!/usr/bin/env python
# Copyright (c) 2010 Gavin Andresen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Obtained from https://github.com/gavinandresen/bitcointools/

"""Encode/decode base58 in the same way that Bitcoin does

The original code has been ported to run on Python 2.x and Python 3.x.
However, the implementation is still a broken one. DO NOT USE.
"""

from __future__ import absolute_import

from mom import _compat
from mom import builtins


b = builtins.b
ZERO_BYTE = _compat.ZERO_BYTE
EMPTY_BYTE = _compat.EMPTY_BYTE


ALPHABET = b("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
BASE = len(ALPHABET)

if _compat.HAVE_PYTHON3:
  def _chr(c):
    return builtins.byte(c)
else:
  def _chr(c):
    return c


def b58encode_bitcoin(v):
  """ encode v, which is a string of bytes, to base58.
  """

  long_value = 0
  for i, c in enumerate(v[::-1]):
    long_value += (256 ** i) * builtins.byte_ord(c)

  result = EMPTY_BYTE
  while long_value >= BASE:
    div, mod = divmod(long_value, BASE)
    result = _chr(ALPHABET[mod]) + result
    long_value = div
  result = _chr(ALPHABET[long_value]) + result

  # Bitcoin does a little leading-zero-compression:
  # leading 0-bytes in the input become leading-1s
  nPad = 0
  for c in v:
    if c == ZERO_BYTE: nPad += 1
    else: break

  return (_chr(ALPHABET[0]) * nPad) + result


def b58decode_bitcoin(encoded, length=None):
  """ decode v into a string of len bytes
  """
  long_value = 0
  for i, c in enumerate(encoded[::-1]):
    long_value += ALPHABET.find(_chr(c)) * (BASE ** i)

  result = EMPTY_BYTE
  while long_value >= 256:
    div, mod = divmod(long_value, 256)
    result = builtins.byte(mod) + result
    long_value = div
  result = builtins.byte(long_value) + result

  nPad = 0
  for c in encoded:
    if c == ALPHABET[0]: nPad += 1
    else: break

  result = builtins.byte(0) * nPad + result
  if length is not None and len(result) != length:
    return None

  return result
