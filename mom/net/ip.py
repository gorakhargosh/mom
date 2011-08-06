#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 David Wilson <dw@botanicus.net>
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# MIT License
# -----------
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
:module: mom.net.ip
:synopsis: IP functions.

.. autofunction:: ipv4_to_integer
.. autofunction:: integer_to_ipv4
"""


__all__ = [
    "ipv4_to_integer",
    "integer_to_ipv4",
]


def ipv4_to_integer(ip_addr):
    """
    Converts an IPv4 address to integral representation.

    :param ip_addr:
        IPv4 address as a string.
    :returns:
        Integral representation.
    """
    a, b, c, d = map(int, ip_addr.split("."))
    if a > 255 or b > 255 or c > 255 or d > 255:
        raise OverflowError(
            "IPv4 address component cannot be greater than 255: " \
            "got %r." % repr((a, b, c, d))
        )
    return (a << 24) | (b << 16) | (c << 8) | d


def integer_to_ipv4(num):
    """
    Converts an IPv4 integral representation to its IPv4 dotted string
    representation.

    :param num:
        Integral representation.
    :returns:
        IPv4 address string.
    """
    return '%d.%d.%d.%d' % (
        (num >> 24) & 0xff,
        (num >> 16) & 0xff,
        (num >> 8) & 0xff,
        (num & 0xff),
    )

