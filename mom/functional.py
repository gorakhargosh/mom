#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Aum Gam Ganapataye Namah
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
:module: mom.functional
:synopsis: Functional programming primitives.

Higher-order functions
-----------------------
These functions accept other functions as arguments and apply them over
specific types of data structures. Here's an example of how to find the
youngest person and the oldest person from among people. Place it into a
Python module and run it::

    import mom.functional
    from mom.functional import reject, partition, difference, pluck, reduce

    people = [
        {"name" : "Harry",    "age" : 100},
        {"name" : "Hermione", "age" : 16},
        {"name" : "Rob",      "age" : 200},
    ]
    def youngest(person1, person2):
        '''Comparator that returns the youngest of two people.'''
        return person1 if person1["age"] <= person2["age"] else person2

    def oldest(person1, person2):
        '''Comparator that returns the oldest of two people.'''
        return person1 if person1["age"] >= person2["age"] else person2

    who_youngest = reduce(youngest, people)
    who_oldest = reduce(oldest, people)

    print(who_youngest)
    # -> {"age" : 16, "name" : "Hermione"}
    print(who_oldest)
    # -> {"age" : 200, "name" : "Rob"}

    # More examples.
    # Now let's list all the names of the people.
    print(pluck(people, "name"))
    # -> ('Harry', 'Hermione', 'Rob')

    # Let's weed out all people who don't have an "H" in their names.
    print(reject(lambda name: "H" not in name, pluck(people, "name")))
    # -> ('Harry', 'Hermione')

    # Or let's partition them into two groups
    print(partition(lambda name: "H" in name, pluck(people, "name")))
    # -> (['Harry', 'Hermione'], ['Rob'])

    # Let's find all the members of a module that are not exported to wildcard
    # imports by its ``__all__`` member.
    print(difference(dir(mom.functional), mom.functional.__all__))
    # -> ['__all__', '__builtins__', ... 'repeat', 'takewhile']


Higher-order functions are extremely useful where you want to express yourself
succinctly instead of writing a ton of for and while loops.

.. WARNING:: About consuming iterators multiple times

    Now before you go all guns blazing with this set of functions, please note
    that Python generators/iterators are for single use only. Attempting to use
    the same iterator multiple times will cause unexpected behavior in your
    code.

    Be careful.


Terminology
-----------
* A **predicate** is a function that returns the truth value of its argument.
* A **walker** is a function that consumes one or more items from a sequence
  at a time.
* A **transform** is a function that transforms its arguments to produce a
  result.
* **Lazy evaluation** is evaluation delayed until the last possible instant.
* **Materialized iterables** are iterables that take up memory equal to their
  size.
* **Non-materialized iterables** are iterables (usually generators) that are
  computed lazily.

Iteration and aggregation
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: each
.. autofunction:: reduce

Logic and search
~~~~~~~~~~~~~~~~
.. autofunction:: every
.. autofunction:: find
.. autofunction:: none
.. autofunction:: some

Filtering
~~~~~~~~~
.. autofunction:: ireject
.. autofunction:: iselect
.. autofunction:: partition
.. autofunction:: reject
.. autofunction:: select

Counting
~~~~~~~~
.. autofunction:: leading
.. autofunction:: tally
.. autofunction:: trailing

Function-generators
~~~~~~~~~~~~~~~~~~~
.. autofunction:: complement
.. autofunction:: compose

Iterators
---------
These functions take iterators as arguments.

.. autofunction:: eat


Iterable sequences
------------------
These functions allow you to filter, manipulate, slice, index, etc.
iterable sequences.

Indexing and slicing
~~~~~~~~~~~~~~~~~~~~
.. autofunction:: chunks
.. autofunction:: first
.. autofunction:: ichunks
.. autofunction:: ipeel
.. autofunction:: irest
.. autofunction:: last
.. autofunction:: nth
.. autofunction:: peel
.. autofunction:: rest
.. autofunction:: round_robin
.. autofunction:: take
.. autofunction:: ncycles


Manipulation, filtering, union and difference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: contains
.. autofunction:: difference
.. autofunction:: falsy
.. autofunction:: flatten
.. autofunction:: flatten1
.. autofunction:: idifference
.. autofunction:: ifalsy
.. autofunction:: intersection
.. autofunction:: itruthy
.. autofunction:: omits
.. autofunction:: truthy
.. autofunction:: union
.. autofunction:: unique
.. autofunction:: without

Dictionaries and dictionary sequences
-------------------------------------
.. autofunction:: invert_dict
.. autofunction:: ipluck
.. autofunction:: map_dict
.. autofunction:: pluck
.. autofunction:: reject_dict
.. autofunction:: select_dict

Predicates, transforms, and walkers
-----------------------------------
.. autofunction:: identity
.. autofunction:: loob
"""

from __future__ import absolute_import
import collections

from functools import partial
from itertools import\
    ifilter, islice, takewhile,\
    ifilterfalse, dropwhile,\
    cycle, imap, repeat

from mom.itertools import chain
from mom.builtins import is_bytes_or_unicode
from mom._compat import range, dict_each, reduce as _reduce, next


__all__ = [
    "chunks",
    "complement",
    "compose",
    "contains",
    "difference",
    "each",
    "every",
    "falsy",
    "find",
    "first",
    "flatten",
    "flatten1",
    "ichunks",
    "identity",
    "idifference",
    "eat",
    "ifalsy",
    "intersection",
    "invert_dict",
    "ipeel",
    "ipluck",
    "ireject",
    "irest",
    "iselect",
    "itruthy",
    "last",
    "leading",
    "loob",
    "map_dict",
    "ncycles",
    "none",
    "nth",
    "omits",
    "partition",
    "peel",
    "pluck",
    "reduce",
    "reject",
    "reject_dict",
    "rest",
    "round_robin",
    "select",
    "select_dict",
    "some",
    "take",
    "tally",
    "trailing",
    "truthy",
    "union",
    "unique",
    "without",
    ]


# Higher-order functions that generate other functions.

def compose(function, *functions):
    """
    Composes a sequence of functions such that::

        compose(g, f, s) -> g(f(s()))

    :param functions:
        An iterable of functions.
    :returns:
        A composition function.
    """

    def _composition(a, b):
        def wrap(*args, **kwargs):
            return a(b(*args, **kwargs))

        return wrap

    return _reduce(_composition, functions, function)


def _compose(function, *functions):
    """
    Alternative implementation.

    Composes a sequence of functions such that::

        compose(g(), f(), s()) -> g(f(s()))

    :param functions:
        An iterable of functions.
    :returns:
        A composition function.
    """
    functions = (function, ) + functions if functions else (function, )

    def _composition(*args_tuple):
        args = list(args_tuple)
        for function in reversed(functions):
            args = [function(*args)]
        return args[0]

    return _composition


def complement(predicate):
    """
    Generates a complementary predicate function for the given predicate
    function.

    :param predicate:
        Predicate function.
    :returns:
        Complementary predicate function.
    """

    def _negate(*args, **kwargs):
        return not predicate(*args, **kwargs)

    return _negate


# Higher-order functions.

def reduce(transform, iterable, *args):
    """
    Aggregate a sequence of items into a single item. Python equivalent of
    Haskell's left fold.

    Please see Python documentation for reduce. There is no change in behavior.
    This is simply a wrapper function.

    If you need reduce_right (right fold)::

        reduce_right = foldr = lambda f, i: lambda s: reduce(f, s, i)

    :param transform:
        Function with signature::

            f(x, y)
    :param iterable:
        Iterable sequence.
    :param initial:
        Initial value.
    :returns:
        Aggregated item.
    """
    return _reduce(transform, iterable, *args)


def each(walker, iterable):
    """
    Iterates over iterable yielding each item in turn to the walker function.

    :param walker:
        The method signature is as follows:

            f(x, y)

        where ``x, y`` is a ``key, value`` pair if iterable is a dictionary,
        otherwise ``x, y`` is an ``index, item`` pair.
    :param iterable:
        Iterable sequence or dictionary.
    """
    if isinstance(iterable, dict):
        dict_each(walker, iterable)
    else:
        for index, item in enumerate(iterable):
            walker(index, item)


def some(predicate, iterable):
    """
    Determines whether the predicate applied to any element of the iterable
    is true.

    :param predicate:
        Predicate function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        ``True`` if the predicate applied to any element of the iterable
        is true; ``False`` otherwise.
    """
    for x in iterable:
        if predicate(x):
            return True
    return False


def _some1(predicate, iterable):
    """Alternative implementation of :func:`some`."""
    return any(imap(predicate, iterable))


def _some2(predicate, iterable):
    """Alternative implementation of :func:`some`."""
    result = False
    for x in dropwhile(complement(predicate), iterable):
        result = True
    return result


def every(predicate, iterable):
    """
    Determines whether the predicate is true for all elements in the iterable.

    :param predicate:
        Predicate function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        ``True`` if the predicate is true for all elements in the iterable.
    """
    # Equivalent to
    # return all(map(predicate, iterable))
    # but the following short-circuits.
    for x in iterable:
        if not predicate(x):
            return False
    return True


def none(predicate, iterable):
    """
    Determines whether the predicate is false for all elements in in iterable.

    :param predicate:
        Predicate function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        ``True`` if the predicate is false for all elements in the iterable.
    """
    return every(complement(predicate), iterable)


def find(predicate, iterable, start=0):
    """
    Determines the first index where the predicate is true for an element in
    the iterable.

    :param predicate:
        Predicate function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :param start:
        Start index.
    :returns:
        -1 if not found; index (>= start) if found.
    """
    for i in range(start, len(iterable)):
        if predicate(iterable[i]):
            return i
    return -1


def leading(predicate, iterable, start=0):
    """
    Returns the number of leading elements in the iterable for which
    the predicate is true.

    :param predicate:
        Predicate function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :param start:
        Start index. (Number of items to skip before starting counting.)
    """
    i = 0L
    for _ in takewhile(predicate, islice(iterable, start, None, 1)):
        i += 1L
    return i


def _leading(predicate, iterable, start=0):
    """Alternative implementation of :func:`leading`."""
    return len(map(identity,
                   takewhile(predicate, islice(iterable, start, None, 1))))


def trailing(predicate, iterable, start=-1):
    """
    Returns the number of trailing elements in the iterable for which
    the predicate is true.

    :param predicate:
        Predicate function of the form::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :param start:
        If start is negative, -1 indicates starting from the last item.
        Therefore, -2 would mean start counting from the second last item.
        If start is 0 or positive, it indicates the number of items to skip
        before beginning to count.
    """
    start = abs(start + 1) if start < 0 else start
    return leading(predicate, reversed(iterable), start)


def tally(predicate, iterable):
    """
    Count how many times the predicate is true.

    Taken from the Python documentation. Under the PSF license.

    :param predicate:
        Predicate function.
    :param iterable:
        Iterable sequence.
    :returns:
        The number of times a predicate is true.
    """
    return sum(imap(predicate, iterable))


def select(predicate, iterable):
    """
    Select all items from the sequence for which the predicate is true.

        select(function or None, sequence) -> list, tuple, or string

    :param predicate:
        Predicate function. If ``None``, select all truthy items.
    :param iterable:
        Iterable.
    :returns:
        A sequence of all items for which the predicate is true.
    """
    return filter(predicate, iterable)


def iselect(predicate, iterable):
    """
    Select all items from the sequence for which the predicate is true.

        iselect(function or None, sequence) --> ifilter object

    :param predicate:
        Predicate function. If ``None``, select all truthy items.
    :param iterable:
        Iterable.
    :yields:
        A sequence of all items for which the predicate is true.
    """
    return ifilter(predicate, iterable)


def reject(predicate, iterable):
    """
    Reject all items from the sequence for which the predicate is true.

        select(function or None, sequence) -> list, tuple, or string

    :param predicate:
        Predicate function. If ``None``, reject all truthy items.
    :param iterable:
        If sequence is a tuple or string, return the same type, else return a
        list.
    :returns:
        A sequence of all items for which the predicate is false.
    """
    return filter(complement(predicate or bool), iterable)


def ireject(predicate, iterable):
    """
    Reject all items from the sequence for which the predicate is true.

        ireject(function or None, sequence) --> ifilterfalse object

    :param predicate:
        Predicate function. If ``None``, reject all truthy items.
    :param iterable:
        If sequence is a tuple or string, return the same type, else return a
        list.
    :yields:
        A sequence of all items for which the predicate is false.
    """
    return ifilterfalse(predicate, iterable)


def partition(predicate, iterable):
    """
    Partitions an iterable into two iterables where for the elements of
    one iterable the predicate is true and for those of the other it is false.

    :param predicate:
        Function of the format::

            f(x) -> bool
    :param iterable:
        Iterable sequence.
    :returns:
        Tuple (selected, rejected)
    """

    def _partitioner(memo, item):
        part = memo[0] if predicate(item) else memo[1]
        part.append(item)
        return memo

    return tuple(_reduce(_partitioner, iterable, [[], []]))


# Dictionaries
def map_dict(transform, dictionary):
    """
    Maps over a dictionary of key, value pairs.

    :param transform:
        Function that accepts a single argument of type ``(key, value)``
        and returns a ``(new key, new value)`` pair.
    :returns:
        New dictionary of ``(new key, new value)`` pairs.
    """
    return dict(map(transform, dictionary.items()))


def select_dict(predicate, dictionary):
    """
    Select a dictionary.

    :param predicate:
        Predicate function that accepts a single argument of type
        ``(key, value)`` and returns ``True`` for selectable elements.
    :returns:
        New dictionary of selected ``(key, value)`` pairs.
    """
    return dict(ifilter(predicate or all, dictionary.items()))


def reject_dict(predicate, dictionary):
    """
    Select a dictionary.

    :param predicate:
        Predicate function that accepts a single argument of type
        ``(key, value)`` and returns ``True`` for rejected elements.
    :returns:
        New dictionary of selected ``(key, value)`` pairs.
    """
    return dict(ifilterfalse(predicate or all, dictionary.items()))


def invert_dict(dictionary):
    """
    Inverts a dictionary.

    :param dictionary:
        Dictionary to invert.
    :returns:
        New dictionary with the keys and values switched.
    """

    def _switch(t):
        k, v = t
        return v, k

    return map_dict(_switch, dictionary)


# Sequences of dictionaries
def pluck(dicts, key, *args, **kwargs):
    """
    Plucks values for a given key from a series of dictionaries.

    :param dicts:
        Iterable sequence of dictionaries.
    :param key:
        The key to fetch.
    :param default:
        The default value to use when a key is not found. If this value is
        not specified, a KeyError will be raised when a key is not found.
    :returns:
        Tuple of values for the key.
    """
    return tuple(ipluck(dicts, key, *args, **kwargs))


def ipluck(dicts, key, *args, **kwargs):
    """
    Plucks values for a given key from a series of dictionaries as an iterator.

    :param dicts:
        Iterable sequence of dictionaries.
    :param key:
        The key to fetch.
    :param default:
        The default value to use when a key is not found. If this value is
        not specified, a KeyError will be raised when a key is not found.
    :yields:
        Iterator of values for the key.
    """
    if args or kwargs:
        default = kwargs['default'] if kwargs else args[0]

        def _get_value_from_dict(d):
            return d.get(key, default)
    else:
        _get_value_from_dict = lambda w: w[key]
    return imap(_get_value_from_dict, dicts)


# Sequences

def contains(iterable, item):
    """
    Determines whether the iterable contains the value specified.

    :param iterable:
        Iterable sequence.
    :param item:
        The value to find.
    :returns:
        ``True`` if the iterable sequence contains the value; ``False``
        otherwise.
    """
    try:
        return iterable.__contains__(item)
    except AttributeError:
        try:
            try:
                return iterable.index(item) >= 0
            except ValueError:
                return False
        except AttributeError:
            return _contains_fallback(iterable, item)


def _contains_fallback(iterable, item):
    """
    Fallback to determine whether the iterable contains the value specified.

    Uses a loop instead of built-in methods.

    :param iterable:
        Iterable sequence.
    :param item:
        The value to find.
    :returns:
        ``True`` if the iterable sequence contains the value; ``False``
        otherwise.
    """
    for x in iter(iterable):
        if x == item:
            return True
    return False


def omits(iterable, item):
    """
    Determines whether the iterable omits the value specified.

    :param iterable:
        Iterable sequence.
    :param item:
        The value to find.
    :returns:
        ``True`` if the iterable sequence omits the value; ``False``
        otherwise.
    """
    return not contains(iterable, item)


def difference(iterable1, iterable2):
    """
    Difference between one iterable and another.
    Items from the first iterable are included in the difference.

        iterable1 - iterable2 = difference

    For example, here is how to find out what your Python module exports
    to other modules using wildcard imports::

        >> difference(dir(mom.functional), mom.functional.__all__)
        ['__all__',
         # Elided...
         'range',
         'takewhile']

    :param iterable1:
        Iterable sequence.
    :param iterable2:
        Iterable sequence.
    :returns:
        Iterable sequence containing the difference between the two given
        iterables.
    """
    return filter(partial(omits, iterable2), iterable1)


def idifference(iterable1, iterable2):
    """
    Difference between one iterable and another.
    Items from the first iterable are included in the difference.

        iterable1 - iterable2 = difference

    :param iterable1:
        Iterable sequence.
    :param iterable2:
        Iterable sequence.
    :yields:
        Generator for the difference between the two given iterables.
    """
    return ifilter(partial(omits, iterable2), iterable1)


def without(iterable, *values):
    """
    Returns the iterable without the values specified.

    :param iterable:
        Iterable sequence.
    :param values:
        Variable number of input values.
    :returns:
        Iterable sequence without the values specified.
    """
    return difference(iterable, values)


def first(iterable):
    """
    Returns the first element out of an iterable.

    :param iterable:
        Iterable sequence.
    :returns:
        First element of the iterable sequence.
    """
    return nth(iterable, 0)


def rest(iterable):
    """
    Returns all elements excluding the first out of an iterable.

    :param iterable:
        Iterable sequence.
    :returns:
        All elements of the iterable sequence excluding the first.
    """
    return iterable[1:]


def irest(iterable):
    """
    Returns an iterator for all elements excluding the first out of an iterable.

    :param iterable:
        Iterable sequence.
    :yields:
        Iterator for all elements of the iterable sequence excluding the first.
    """
    return islice(iterable, 1, None, 1)


def nth(iterable, n, default=None):
    """
    Returns the nth element out of an iterable.

    :param iterable:
        Iterable sequence.
    :param n:
        Index
    :param default:
        If not found, this or ``None`` will be returned.
    :returns:
        nth element of the iterable sequence.
    """
    return next(islice(iterable, n, None), default)


def last(iterable):
    """
    Returns the last element out of an iterable.

    :param iterable:
        Iterable sequence.
    :returns:
        Last element of the iterable sequence.
    """
    return nth(iterable, len(iterable) - 1)


def peel(iterable, count=1):
    """
    Returns the meat of an iterable by peeling off the specified number of
    elements from both ends.

    :param iterable:
        Iterable sequence.
    :param count:
        The number of elements to remove from each end.
    :returns:
        Peeled sequence.
    """
    if count < 0:
        raise ValueError("peel count cannot be negative: %r" % count)
    if not iterable:
        return iterable
    return iterable[count:-count]


def ipeel(iterable, count=1):
    """
    Returns an iterator for the meat of an iterable by peeling off the specified
    number of elements from both ends.

    :param iterable:
        Iterable sequence.
    :param count:
        The number of elements to remove from each end.
    :yields:
        Peel iterator.
    """
    if count < 0:
        raise ValueError("peel count cannot be negative: %r" % count)
    if not iterable:
        return iter([])
    try:
        return islice(iterable, count, len(iterable) - count, 1)
    except ValueError:
        return iter([])


def ichunks(iterable, size, *args, **kwargs):
    """
    Splits an iterable into iterators for chunks each of specified size.

    :param iterable:
        The iterable to split. Must be an ordered sequence to guarantee order.
    :param size:
        Chunk size.
    :param padding:
        If a pad value is specified appropriate multiples of it will be
        appended to the end of the iterator if the size is not an integral
        multiple of the length of the iterable:

            map(tuple, ichunks("aaabccd", 3, "-"))
            -> [("a", "a", "a"), ("b", "c", "c"), ("d", "-", "-")]

            map(tuple, ichunks("aaabccd", 3, None))
            -> [("a", "a", "a"), ("b", "c", "c"), ("d", None, None)]

        If no padding is specified, nothing will be appended if the chunk
        size is not an integral multiple of the length of the iterable. That is,
        the last chunk will have chunk size less than the specified chunk size.
    :yields:
        Generator of chunk iterators.
    """
    length = len(iterable)
    if args or kwargs:
        padding = kwargs["padding"] if kwargs else args[0]
        for i in range(0, length, size):
            yield islice(chain(iterable,
                               repeat(padding, (size - (length % size)))),
                         i, i + size)
    else:
        for i in range(0, length, size):
            yield islice(iterable, i, i + size)


def chunks(iterable, size, *args, **kwargs):
    """
    Splits an iterable into materialized chunks each of specified size.

    :param iterable:
        The iterable to split. Must be an ordered sequence to guarantee order.
    :param size:
        Chunk size.
    :param padding:
        This must be an iterable or None. So if you want a ``True`` filler,
        use [True] or (True, ) depending on whether the iterable is a list or
        a tuple. Essentially, it must be the same type as the iterable.

        If a pad value is specified appropriate multiples of it will be
        concatenated at the end of the iterable if the size is not an integral
        multiple of the length of the iterable:

            tuple(chunks("aaabccd", 3, "-"))
            -> ("aaa", "bcc", "d--")

            tuple(chunks((1, 1, 1, 2, 2), 3, (None,)))
            -> ((1, 1, 1, ), (2, 2, None))

        If no padding is specified, nothing will be appended if the chunk
        size is not an integral multiple of the length of the iterable. That is,
        the last chunk will have chunk size less than the specified chunk size.
    :yields:
        Generator of materialized chunks.
    """
    length = len(iterable)
    if args or kwargs:
        padding = kwargs["padding"] if kwargs else args[0]
        if padding is None:
            if is_bytes_or_unicode(iterable):
                padding = ""
            elif isinstance(iterable, tuple):
                padding = (padding,)
            else:
                iterable = list(iterable)
                padding = [padding]
        it = iterable + (padding * (size - (length % size)))
        for i in range(0, length, size):
            yield it[i:i + size]
    else:
        for i in range(0, length, size):
            yield iterable[i:i + size]


def truthy(iterable):
    """
    Returns a iterable with only the truthy values.

    Example::

        truthy((0, 1, 2, False, None, True)) -> (1, 2, True)

    :param iterable:
        Iterable sequence.
    :returns:
        Iterable with truthy values.
    """
    return filter(bool, iterable)


def itruthy(iterable):
    """
    Returns an iterator to for an iterable with only the truthy values.

    Example::

        tuple(itruthy((0, 1, 2, False, None, True))) -> (1, 2, True)

    :param iterable:
        Iterable sequence.
    :yields:
        Iterator for an iterable with truthy values.
    """
    return ifilter(bool, iterable)


def falsy(iterable):
    """
    Returns a iterable with only the falsy values.

    Example::

        falsy((0, 1, 2, False, None, True)) -> (0, False, None)

    :param iterable:
        Iterable sequence.
    :returns:
        Iterable with falsy values.
    """
    return filter(loob, iterable)


def ifalsy(iterable):
    """
    Returns a iterator for an iterable with only the falsy values.

    Example::

        tuple(ifalsy((0, 1, 2, False, None, True))) -> (0, False, None)

    :param iterable:
        Iterable sequence.
    :yields:
        Iterator for an iterable with falsy values.
    """
    return ifilterfalse(bool, iterable)


def flatten(iterable):
    """
    Flattens nested iterables into a single iterable.

    Example::

        flatten((1, (0, 5, ('a', 'b')), (3, 4))) -> [1, 0, 5, 'a', 'b', 3, 4]

    :param iterable:
        Iterable sequence of iterables.
    :returns:
        Iterable sequence of items.
    """

    def _flatten(memo, item):
        if isinstance(item, (list, tuple)):
            return memo + _reduce(_flatten, item, [])
        else:
            memo.append(item)
            return memo

    return _reduce(_flatten, iterable, [])


def flatten1(iterable):
    """
    Flattens nested iterables into a single iterable only one level
    deep.

    Example::

        flatten1((1, (0, 5, ('a', 'b')), (3, 4))) -> [1, 0, 5, ('a', 'b'), 3, 4]

    :param iterable:
        Iterable sequence of iterables.
    :returns:
        Iterable sequence of items.
    """

    def _flatten(memo, item):
        if isinstance(item, (list, tuple)):
            return memo + list(item)
        else:
            memo.append(item)
            return memo

    return _reduce(_flatten, iterable, [])


def unique(iterable, is_sorted=False):
    """
    Returns an iterable sequence of unique values from the given iterable.

    :param iterable:
        Iterable sequence.
    :param is_sorted:
        Whether the iterable has already been sorted. Works faster if it is.
    :returns:
        Iterable sequence of unique values.
    """
    # If we used a "seen" set like the Python documentation implementation does,
    # we'd have to ensure that the elements are hashable. This implementation
    # does not have that problem. We can improve this implementation.
    if iterable:
        def _unique(memo, item):
            cond = last(memo) != item if is_sorted else omits(memo, item)
            if cond:
                memo.append(item)
            return memo

        return _reduce(_unique, irest(iterable), [first(iterable)])
    else:
        return iterable


def union(iterable, *iterables):
    """
    Returns the union of given iterable sequences.

    :param iterables:
        Variable number of input iterable sequences.
    :returns:
        Union of the iterable sequences.
    """

    if not iterables:
        return iterable

    return unique(iter(chain(iterable, *iterables)))


def intersection(iterable, *iterables):
    """
    Returns the intersection of given iterable sequences.

    :param iterables:
        Variable number of input iterable sequences.
    :returns:
        Intersection of the iterable sequences in the order of appearance
        in the first sequence.
    """

    if iterables is None:
        return iterable

    def _does_other_contain(item):
        return every(partial(contains, item=item), iterables)

    return filter(_does_other_contain, unique(iterable))


def take(iterable, n):
    """
    Return first n items of the iterable as a tuple.

    Taken from the Python documentation. Under the PSF license.

    :param n:
        The number of items to obtain.
    :param iterable:
        Iterable sequence.
    :returns:
        First n items of the iterable as a tuple.
    """
    return tuple(islice(iterable, n))


def round_robin(*iterables):
    """
    Returns items from the iterables in a round-robin fashion.

    Taken from the Python documentation. Under the PSF license.
    Recipe credited to George Sakkis

    Example::

        round_robin('ABC', 'D', 'EF') --> A D E B F C"

    :param iterables:
        Variable number of inputs for iterable sequences.
    :yields:
        Items from the iterable sequences in a round-robin fashion.
    """
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next_ in nexts:
                yield next_()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def eat(iterator, n):
    """
    Advance an iterator n-steps ahead. If n is None, eat entirely.

    Taken from the Python documentation. Under the PSF license.

    :param iterator:
        An iterator.
    :param n:
        The number of steps to advance.
    :yields:
        An iterator.
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # Feed the entire iterator into a zero-length deque.
        collections.deque(iterator)
    else:
        # Advance to the empty slice starting at position n.
        next(islice(iterator, n, n), None)


def ncycles(iterable, n):
    """
    Yields the sequence elements n times.

    Taken from the Python documentation. Under the PSF license.

    :param iterable:
        Iterable sequence.
    :param n:
        The number of times to yield the sequence.
    :yields:
        Iterator.
    """
    return chain.from_iterable(repeat(tuple(iterable), n))


# Predicates, transforms, and walkers
def identity(arg):
    """
    Identity function. Produces what it consumes.

    :param arg:
        Argument
    :returns:
        Argument.
    """
    return arg


def loob(arg):
    """
    Complement of bool.

    :param arg:
        Python value.
    :returns:
        Complementary boolean value.
    """
    return not bool(arg)
