#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.functional
:synopsis: Functional programming primitives.

.. autofunction:: every
.. autofunction:: none
.. autofunction:: find
.. autofunction:: leading
.. autofunction:: trailing
.. autofunction:: some
.. autofunction:: even
.. autofunction:: odd
.. autofunction:: positive
.. autofunction:: negative
.. autofunction:: first
.. autofunction:: rest
"""

from __future__ import absolute_import

license = """\
The Apache Licence, Version 2.0

Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__ = ", ".join([
    "Yesudeep Mangalapilly",
])

__all__ = [
    "some",
    "every",
    "find",
    "leading",
    "trailing",
    "even",
    "odd",
    "none",
    "positive",
    "negative",
    "first",
    "rest",
]


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


def none(func, iterable):
    """
    Determines whether :func:`func` is false for all elements in in iterable.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        ``True`` if :func:`func` is false for all elements in the iterable.
    """
    return every((lambda w: not func(w)), iterable)


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


def even(num):
    """
    Determines whether a number is even.

    :param num:
        Integer
    :returns:
        ``True`` if even; ``False`` otherwise.
    """
    return not (num & 1L)


def odd(num):
    """
    Determines whether a number is odd.

    :param num:
        Integer
    :returns:
        ``True`` if odd; ``False`` otherwise.
    """
    return bool(num & 1L)


def positive(num):
    """
    Determines whether a number is positive.

    :param num:
        Number
    :returns:
        ``True`` if positive; ``False`` otherwise.
    """
    if not isinstance(num, (int, long, bool, float)):
        raise TypeError("unsupported operand type: %r", type(num).__name__)
    return num > 0


def negative(num):
    """
    Determines whether a number is negative.

    :param num:
        Number
    :returns:
        ``True`` if positive; ``False`` otherwise.
    """
    if not isinstance(num, (int, long, bool, float)):
        raise TypeError("unsupported operand type: %r", type(num).__name__)
    return num < 0


def first(iterable):
    """
    Returns the first element out of an iterable.

    :param iterable:
        Iterable sequence.
    :returns:
        First element of the iterable sequence.
    """
    return iterable[0]


def rest(iterable):
    """
    Returns all elements excluding the first out of an iterable.

    :param iterable:
        Iterable sequence.
    :returns:
        All elements of the iterable sequence excluding the first.
    """
    return iterable[1:]

