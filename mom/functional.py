#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.functional
:synopsis: Functional programming primitives.

Higher-order functions
-----------------------
These functions accept other functions as arguments and apply them over
specific types of data structures.

Boolean logic and search
~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: every
.. autofunction:: find
.. autofunction:: none
.. autofunction:: some

Filtering
~~~~~~~~~
.. autofunction:: ireject
.. autofunction:: iselect
.. autofunction:: reject
.. autofunction:: select

Counting
~~~~~~~~
.. autofunction:: leading
.. autofunction:: trailing

Function-generators
~~~~~~~~~~~~~~~~~~~
.. autofunction:: compose


Iteration helpers
-----------------
.. autofunction:: chunks
.. autofunction:: compact
.. autofunction:: first
.. autofunction:: ichunks
.. autofunction:: last
.. autofunction:: rest


Utility tests
-------------
.. autofunction:: is_even
.. autofunction:: is_negative
.. autofunction:: is_odd
.. autofunction:: is_positive


Dictionaries and dictionary sequences
-------------------------------------
.. autofunction:: invert_dict
.. autofunction:: map_dict
.. autofunction:: pluck
.. autofunction:: reject_dict
.. autofunction:: select_dict

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
    "chunks",
    "compact",
    "compose",
    "every",
    "find",
    "first",
    "ichunks",
    "invert_dict",
    "ireject",
    "is_even",
    "is_negative",
    "is_odd",
    "is_positive",
    "iselect",
    "last",
    "leading",
    "map_dict",
    "none",
    "pluck",
    "reject",
    "reject_dict",
    "rest",
    "select",
    "select_dict",
    "some",
    "trailing",
]

from itertools import ifilter, islice, takewhile, ifilterfalse
from mom._builtins import range


# Higher-order functions.

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
    return every(lambda w: not func(w), iterable)


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


def leading(func, iterable, start=0):
    """
    Returns the number of leading elements in the iterable for which
    :func:`func` is true.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :param start:
        Number of items to skip before starting counting.
    """
    i = 0L
    for _ in takewhile(func, islice(iterable, start, None, 1)):
        i += 1L
    return i


def trailing(func, iterable, start=-1):
    """
    Returns the number of trailing elements in the iterable for which
    :func:`func` is true.

    :param func:
        Function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :param start:
        If skip is negative, -1 indicates starting from the last item.
        Therefore, -2 would mean start counting from the second last item.
        If skip is 0 or positive, it indicates the number of items to skip
        before beginning to count.
    """
    start = abs(start + 1) if start < 0 else start
    return leading(func, reversed(iterable), start)


def select(func, iterable):
    """
    Select all items from the sequence for which func(item) is true.

        select(function or None, sequence) -> list, tuple, or string

    :param func:
        Truth test function. If func is ``None``, select all truthy items.
    :param iterable:
        Iterable.
    :returns:
        A sequence of all items for which func(item) is true.
    """
    return filter(func, iterable)


def iselect(func, iterable):
    """
    Select all items from the sequence for which func(item) is true.

        iselect(function or None, sequence) --> ifilter object

    :param func:
        Truth test function. If func is ``None``, select all truthy items.
    :param iterable:
        Iterable.
    :returns:
        A sequence of all items for which func(item) is true.
    """
    return ifilter(func, iterable)


def reject(func, iterable):
    """
    Reject all items from the sequence for which func(item) is true.

        select(function or None, sequence) -> list, tuple, or string

    :param func:
        Truth test function. If func is ``None``, reject all truthy items.
    :param iterable:
        If sequence is a tuple or string, return the same type, else return a
        list.
    :returns:
        A sequence of all items for which func(item) is false.
    """
    return filter(lambda w: not (func or bool)(w), iterable)


def ireject(func, iterable):
    """
    Reject all items from the sequence for which func(item) is true.

        ireject(function or None, sequence) --> ifilterfalse object

    :param func:
        Truth test function. If func is ``None``, reject all truthy items.
    :param iterable:
        If sequence is a tuple or string, return the same type, else return a
        list.
    :returns:
        A sequence of all items for which func(item) is false.
    """
    return ifilterfalse(func, iterable)


def compose(*funcs):
    """
    Composes a sequence of functions such that

        compose(g(), f(), s()) -> g(f(s()))

    :param funcs:
        An iterable of functions.
    :returns:
        A composition function.
    """
    def composition(*args_tuple):
        args = list(args_tuple)
        for func in reversed(funcs):
            args = [func(*args)]
        return args[0]
    return composition


# Dictionaries
def map_dict(func, dictionary):
    """
    Maps over a dictionary of key, value pairs.

    :param func:
        Function that accepts a single argument of type ``(key, value)``
        and returns a ``(new key, new value)`` pair.
    :returns:
        New dictionary of ``(new key, new value)`` pairs.
    """
    return dict(map(func, dictionary.items()))


def select_dict(func, dictionary):
    """
    Select a dictionary.

    :param func:
        Function that accepts a single argument of type ``(key, value)``
        and returns ``True`` for selectable elements.
    :returns:
        New dictionary of selected ``(key, value)`` pairs.
    """
    return dict(select(func or all, dictionary.items()))


def reject_dict(func, dictionary):
    """
    Select a dictionary.

    :param func:
        Function that accepts a single argument of type ``(key, value)``
        and returns ``True`` for rejected elements.
    :returns:
        New dictionary of selected ``(key, value)`` pairs.
    """
    return dict(reject(func or all, dictionary.items()))


def invert_dict(dictionary):
    """
    Inverts a dictionary.

    :param dictionary:
        Dictionary to invert.
    :returns:
        New dictionary with the keys and values switched.
    """
    return map_dict(lambda (k, v): (v, k), dictionary)


# Sequences of dictionaries
def pluck(iterable_of_dict, key):
    """
    Plucks values for a given key from a series of dictionaries.

    :param iterable_of_dict:
        Iterable sequence of dictionaries.
    :param key:
        The key to fetch.
    :returns:
        Iterable of values for the key.
    """
    return map(lambda w: w[key], iterable_of_dict)


# Utility test functions.
def is_even(num):
    """
    Determines whether a number is even.

    :param num:
        Integer
    :returns:
        ``True`` if even; ``False`` otherwise.
    """
    return not (num & 1L)


def is_odd(num):
    """
    Determines whether a number is odd.

    :param num:
        Integer
    :returns:
        ``True`` if odd; ``False`` otherwise.
    """
    return bool(num & 1L)


def is_positive(num):
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


def is_negative(num):
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


# Sequences
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


def last(iterable):
    """
    Returns the last element out of an iterable.

    :param iterable:
        Iterable sequence.
    :returns:
        Last element of the iterable sequence.
    """
    return iterable[-1]


def ichunks(size, iterable):
    """
    Splits an iterable into an iterable of chunks each of specified chunk size.

    :param size:
        Chunk size.
    :param iterable:
        The iterable to split.
    :returns:
        Generator of sequences each of the specified chunk size.
    """
    for i in range(0, len(iterable), size):
        yield islice(iterable, i, i + size)


def chunks(size, iterable):
    """
    Splits an iterable into an iterable of chunks each of specified chunk size.

    :param size:
        Chunk size.
    :param iterable:
        The iterable to split.
    :returns:
        Generator of sequences each of the specified chunk size.
    """
    for i in range(0, len(iterable), size):
        yield iterable[i:i+size]


def compact(iterable):
    """
    Returns a new iterable with all the falsy values discarded.
    """
    return select(None, iterable)
