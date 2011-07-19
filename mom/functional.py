#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Aum Gam Ganapataye Namah
"""
:module: mom.functional
:synopsis: Functional programming primitives.

Higher-order functions
-----------------------
These functions accept other functions as arguments and apply them over
specific types of data structures. Here's an example of how to find the
youngest person and the oldest person from among people::

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
    -> {"age" : 16, "name" : "Hermione"}
    print(who_oldest)
    -> {"age" : 200, "name" : "Rob"}

Higher-order functions are extremely useful where you want to express yourself
succinctly instead of writing a ton of for and while loops.

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

Iterable sequences
------------------
Indexing and slicing
~~~~~~~~~~~~~~~~~~~~
.. autofunction:: first
.. autofunction:: last
.. autofunction:: rest
.. autofunction:: take
.. autofunction:: nth
.. autofunction:: chunks
.. autofunction:: round_robin

Manipulation, filtering, union and difference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: contains
.. autofunction:: difference
.. autofunction:: falsy
.. autofunction:: flatten
.. autofunction:: flatten1
.. autofunction:: intersection
.. autofunction:: truthy
.. autofunction:: union
.. autofunction:: unique
.. autofunction:: without

Dictionaries and dictionary sequences
-------------------------------------
.. autofunction:: invert_dict
.. autofunction:: map_dict
.. autofunction:: pluck
.. autofunction:: reject_dict
.. autofunction:: select_dict

Utility functions
-----------------
.. autofunction:: identity
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
    "identity",
    "intersection",
    "invert_dict",
    "ireject",
    "iselect",
    "last",
    "leading",
    "map_dict",
    "none",
    "nth",
    "partition",
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

from functools import partial
from itertools import \
    ifilter, islice, takewhile, ifilterfalse, dropwhile, chain, cycle, imap, repeat
from mom._builtins import range, dict_each, reduce as _reduce, next


# Higher-order functions that generate other functions.

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


def complement(predicate):
    """
    Generates a complementary predicate function for the given predicate
    function.

    :param predicate:
        Predicate function.
    :returns:
        Complementary predicate function.
    """
    def f(*args, **kwargs):
        return not predicate(*args, **kwargs)
    return f


# Higher-order functions.

def reduce(iterator, iterable, *args):
    """
    Aggregate a sequence of items into a single item. Python equivalent of
    Haskell's left fold.

    Please see Python documentation for reduce. There is no change in behavior.
    This is simply a wrapper function.

    If you need reduce_right (right fold)::

        reduce_right = foldr = lambda f, i: lambda s: reduce(f, s, i)

    :param iterator:
        Function with signature::

            f(x, y)
    :param iterable:
        Iterable sequence.
    :param initial:
        Initial value.
    :returns:
        Aggregated item.
    """
    return _reduce(iterator, iterable, *args)


def each(iterator, iterable):
    """
    Iterates over iterable yielding each item in turn to the iterator.

    :param iterator:
        The method signature is as follows:

            f(x, y)

        where ``x, y`` is a ``key, value`` pair if iterable is a dictionary,
        otherwise ``x, y`` is an ``index, item`` pair.
    :param iterable:
        Iterable sequence or dictionary.
    """
    if isinstance(iterable, dict):
        dict_each(iterator, iterable)
    else:
        for index, item in enumerate(iterable):
            iterator(index, item)


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

    Taken from the Python documentation.

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
    :returns:
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
    :returns:
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
def map_dict(iterator, dictionary):
    """
    Maps over a dictionary of key, value pairs.

    :param iterator:
        Function that accepts a single argument of type ``(key, value)``
        and returns a ``(new key, new value)`` pair.
    :returns:
        New dictionary of ``(new key, new value)`` pairs.
    """
    return dict(map(iterator, dictionary.items()))


def select_dict(predicate, dictionary):
    """
    Select a dictionary.

    :param predicate:
        Predicate function that accepts a single argument of type
        ``(key, value)`` and returns ``True`` for selectable elements.
    :returns:
        New dictionary of selected ``(key, value)`` pairs.
    """
    return dict(select(predicate or all, dictionary.items()))


def reject_dict(predicate, dictionary):
    """
    Select a dictionary.

    :param predicate:
        Predicate function that accepts a single argument of type
        ``(key, value)`` and returns ``True`` for rejected elements.
    :returns:
        New dictionary of selected ``(key, value)`` pairs.
    """
    return dict(reject(predicate or all, dictionary.items()))


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
    if args or kwargs:
        default = kwargs['default'] if kwargs else args[0]
        def _get_value_from_dict(d):
            return d.get(key, default)
    else:
        _get_value_from_dict = lambda w: w[key]
    return tuple(imap(_get_value_from_dict, dicts))


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
    if getattr(iterable, "index", None):
        try:
            return iterable.index(item) >= 0
        except ValueError:
            return False
    elif getattr(iterable, "has_key", None):
        return iterable.has_key(item)
    elif getattr(iterable, "__contains__", None):
        return iterable.__contains__(item)
    else:
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


def difference(iterable1, iterable2):
    """
    Difference between one iterable and another.
    Items from the first iterable are included in the difference.

        iterable1 - iterable2 = difference

    :param iterable1:
        Iterable sequence.
    :param iterable2:
        Iterable sequence.
    :returns:
        Iterable sequence containing the difference between the two given
        iterables.

    Example
    -------
    Say you want to figure out whether you have listed all the members
    of a Python module you want to export in its ``__all__`` member to another
    module that uses a wildcard import like this::

        from yourmodule import *

    Maintaining the ``__all__`` member of module can be a pain, but you can use
    this function to your aid. For example, for this module, you could do::

        >> import mom.functional
        >> difference(dir(mom.functional), mom.functional.__all__)
        ['__all__',
         '__author__',
         '__builtins__',
         '__doc__',
         '__file__',
         '__name__',
         '__package__',
         '_contains_fallback',
         '_leading',
         '_reduce',
         '_some1',
         '_some2',
         'absolute_import',
         'chain',
         'cycle',
         'dict_each',
         'dropwhile',
         'ifilter',
         'ifilterfalse',
         'imap',
         'is_sequence',
         'islice',
         'license',
         'next',
         'partial',
         'range',
         'takewhile']

    See how that helps? Now you can be sure you are exporting exactly what
    you need to.
    """
    return select(partial(complement(contains), iterable2), iterable1)


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
    return nth(iterable, len(iterable)-1)


def chunks(iterable, size, pad=None):
    """
    Splits an iterable into an iterable of chunks each of specified size.

    :param iterable:
        The iterable to split.
    :param size:
        Chunk size.
    :param pad:
        Default ``None``, which means no padding will be appended.

        If a pad iterable is specified it will be appended to the end if the
        size is not an integral multiple of the length of the iterable:

            map(tuple, chunks("aaabccd", 3, "-"))
            -> [("a", "a", "a"), ("b", "c", "c"), ("d", "-", "-")]

            map(tuple, chunks("aaabccd", 3, [None]))
            -> [("a", "a", "a"), ("b", "c", "c"), ("d", None, None)]

    :returns:
        Generates a sequence of chunk iterators each having the specified chunk
        size.
    """
    length = len(iterable)
    range_ = range(0, length, size)
    if pad:
        remainder = length % size
        if remainder:
            last_index = length - remainder
            for i in range_:
                it = islice(iterable, i, i + size)
                if last_index == i:
                    yield chain(it, pad * (size - remainder))
                else:
                    yield it
        else:
            for i in range_:
                yield islice(iterable, i, i + size)
    else:
        for i in range_:
            yield islice(iterable, i, i + size)


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
    return select(bool, iterable)


def falsy(iterable):
    """
    Returns a iterable with only the falsy values.

    Example::

        falsy((0, 1, 2, False, None, True)) -> (0, False, None)

    :param iterable:
        Iterable sequence.
    :returns:
        Iterable with false values.
    """
    return reject(bool, iterable)


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
    if iterable:
        def _unique(memo, item):
            cond = last(memo) != item if is_sorted else not contains(memo, item)
            if cond:
                memo.append(item)
            return memo
        return _reduce(_unique, rest(iterable), [first(iterable)])
    else:
        return iterable


def union(*iterables):
    """
    Returns the union of given iterable sequences.

    :param iterables:
        Variable number of input iterable sequences.
    :returns:
        Union of the iterable sequences.
    """
    return unique(iter(chain(*iterables)))


def intersection(*iterables):
    """
    Returns the intersection of given iterable sequences.

    :param iterables:
        Variable number of input iterable sequences.
    :returns:
        Intersection of the iterable sequences in the order of appearance
        in the first sequence.
    """
    def f(item):
        return every(partial(contains, item=item), iterables[1:])
    return filter(f, unique(iterables[0]))


def take(iterable, n):
    """
    Return first n items of the iterable as a tuple.

    Taken from the Python documentation.

    :param n:
        The number of items to obtain.
    :param iterable:
        Iterable sequence.
    :returns:
        First n items of the iterable as a tuple.
    """
    return tuple(islice(iterable, 0, n, 1))


def round_robin(*iterables):
    """
    Returns items from the iterables in a round-robin fashion.

    Taken from the Python documentation.
    Recipe credited to George Sakkis

    Example::

        round_robin('ABC', 'D', 'EF') --> A D E B F C"

    :param iterables:
        Variable number of inputs for iterable sequences.
    :returns:
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



# Utility functions
def identity(arg):
    """
    Identity function. Produces what it consumes.

    :param arg:
        Argument
    :returns:
        Argument.
    """
    return arg
