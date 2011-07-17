#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.functional
:synopsis: Handy things for functional style programming.

.. autofunction:: every
.. autofunction:: find
.. autofunction:: leading
.. autofunction:: trailing
.. autofunction:: reverse
.. autofunction:: some
.. autofunction:: sort
"""

from __future__ import nested_scopes, absolute_import

license = """\
New BSD License

Copyright (c) 2005, Google Inc.
Copyright (c) 2011 Yesudeep Mangalapilly
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.
    * Neither the name of Google Inc. nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = ", ".join([
    "Ade Oshineye",
    "Chris DiBona",
    "Dan Bentley",
    "Nathaniel Manista",
    "Yesudeep Mangalapilly",
])

__all__ = [
    "some",
    "every",
    "find",
    "leading",
    "trailing",
]

import math as _math

from mom._builtins import range


def some(func, iterable):
    """
    Determines whether :func:`func` applied to any element of the iterable is
    true.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        ``True`` if :func:`func` applied to any element of the iterable is true;
        ``False`` otherwise.
    """
    for x in iterable:
        if func(x):
            return True
    return False


def every(func, iterable):
    """
    Determines whether :func:`func` is true for all elements in the iterable.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        ``True`` if :func:`func` is true for all elements in the iterable.
    """
    for x in iterable:
        if not func(x):
            return False
    return True


def find(func, iterable, start=0):
    """
    Determines the first index where :func:`func` is true for an element in
    the iterable.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :param start:
        Start index.
    :returns:
        -1 if not found; index (>= start) if found.
    """
    for i in range(start, len(iterable)):
        if func(iterable[i]):
            return i
    return -1


def leading(func, iterable):
    """
    Returns the number of leading elements in the iterable for which
    :func:`func` is true.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    """
    i = 0
    for x in iterable:
        if not func(x):
           break
        i += 1
    return i


def trailing(func, iterable):
    """
    Returns the number of trailing elements in the iterable for which
    :func:`func` is true.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    """
    return leading(func, reversed(iterable))


def _trailing(func, iterable):
    """
    Returns the number of trailing elements in the iterable for which
    :func:`func` is true.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    """
    n = len(iterable)
    for i in range(n - 1, -1, -1):
        if not func(iterable[i]):
            return (n - 1) - i
    return len(iterable)

