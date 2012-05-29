#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import unittest2

from mom import builtins
from mom import functional


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


class Test_some(unittest2.TestCase):
  def test_valid(self):
    self.assertTrue(functional.some(lambda w: w > 0, [0, -1, 4, 6]))

    self.assertFalse(functional.some(lambda w: w > 0, [0, -1, -4, 0]))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.some, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional.some, lambda w: w > 0, 5)
    self.assertRaises(TypeError, functional.some, lambda w: w > 0, True)


class Test__some1(unittest2.TestCase):
  def test_valid(self):
    self.assertTrue(functional._some1(lambda w: w > 0, [0, -1, 4, 6]))

    self.assertFalse(functional._some1(lambda w: w > 0, [0, -1, -4, 0]))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional._some1, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional._some1, lambda w: w > 0, 5)
    self.assertRaises(TypeError, functional._some1, lambda w: w > 0, True)


class Test__some2(unittest2.TestCase):
  def test_valid(self):
    self.assertTrue(functional._some2(lambda w: w > 0, [0, -1, 4, 6]))

    self.assertFalse(functional._some2(lambda w: w > 0, [0, -1, -4, 0]))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional._some2, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional._some2, lambda w: w > 0, 5)
    self.assertRaises(TypeError, functional._some2, lambda w: w > 0, True)


class Test_every(unittest2.TestCase):
  def test_valid(self):
    self.assertTrue(functional.every(lambda w: w > 0, [1, 1, 4, 6]))
    self.assertFalse(functional.every(lambda w: w > 0, [0, -1, 4, 6]))
    self.assertFalse(functional.every(lambda w: w > 0, [0, -1, -4, 0]))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.every, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional.every, lambda w: w > 0, 5)
    self.assertRaises(TypeError, functional.every, lambda w: w > 0, True)


class Test_none(unittest2.TestCase):
  def test_valid(self):
    self.assertTrue(functional.none(lambda w: w < 1, [1, 1, 4, 6]))
    self.assertFalse(functional.none(lambda w: w > 0, [0, -1, 4, 6]))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.none, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional.none, lambda w: w > 0, 5)
    self.assertRaises(TypeError, functional.none, lambda w: w > 0, True)


class Test_find(unittest2.TestCase):
  def test_valid_index(self):
    self.assertEqual(functional.find(lambda w: w > 2, [0, 1, 2, 3, 4, 5]), 3)

  def test_not_found(self):
    self.assertEqual(functional.find(lambda w: w > 50, range(5)), -1)

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.find, lambda w: w > 2, None)
    self.assertRaises(TypeError, functional.find, lambda w: w > 2, 5)
    self.assertRaises(TypeError, functional.find, lambda w: w > 2, True)


class Test__leading(unittest2.TestCase):
  def test_count(self):
    self.assertEqual(functional._leading(lambda w: w > 0, [0, 0, 1]), 0)
    self.assertEqual(functional._leading(lambda w: w > 1, [2, 2, 3, 0, 5]), 3)
    self.assertEqual(functional._leading(lambda w: ord(w) >= ord("c"), "abalskjd"), 0)
    self.assertEqual(functional._leading(lambda w: ord(w) >= ord("c"), "cuddleya"), 7)

  def test_start(self):
    self.assertEqual(functional._leading(lambda w: w == "0", "0001"), 3)
    self.assertEqual(functional._leading(lambda w: w == "0", "0001"), 3)
    self.assertEqual(functional._leading(lambda w: w == "0", "0001", 1), 2)

  def test_full_count(self):
    self.assertEqual(functional._leading(lambda w: w > 0, range(1, 10)), 9)

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional._leading, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional._leading, lambda w: w > 0, 3)
    self.assertRaises(TypeError, functional._leading, lambda w: w > 0, True)


class Test_leading(unittest2.TestCase):
  def test_count(self):
    self.assertEqual(functional.leading(lambda w: w > 0, [0, 0, 1]), 0)
    self.assertEqual(functional.leading(lambda w: w > 1, [2, 2, 3, 0, 5]), 3)
    self.assertEqual(functional.leading(lambda w: ord(w) >= ord("c"), "abalskjd"), 0)
    self.assertEqual(functional.leading(lambda w: ord(w) >= ord("c"), "cuddleya"), 7)

  def test_start(self):
    self.assertEqual(functional.leading(lambda w: w == "0", "0001"), 3)
    self.assertEqual(functional.leading(lambda w: w == "0", "0001"), 3)
    self.assertEqual(functional.leading(lambda w: w == "0", "0001", 1), 2)

  def test_full_count(self):
    self.assertEqual(functional.leading(lambda w: w > 0, range(1, 10)), 9)

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.leading, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional.leading, lambda w: w > 0, 3)
    self.assertRaises(TypeError, functional.leading, lambda w: w > 0, True)


class Test_trailing(unittest2.TestCase):
  def test_count(self):
    self.assertEqual(functional.trailing(lambda w: w > 0, [0, 0, 1]), 1)
    self.assertEqual(functional.trailing(lambda w: w > 1, [2, 0, 2, 3, 5]), 3)
    self.assertEqual(functional.trailing(lambda w: ord(w) >= ord("c"), "abalskjd"), 5)
    self.assertEqual(functional.trailing(lambda w: ord(w) >= ord("c"), "cuddleya"), 0)

  def test_end(self):
    self.assertEqual(functional.trailing(lambda w: w == "0", "0001"), 0)
    self.assertEqual(functional.trailing(lambda w: w == "0", "1000", -1), 3)
    self.assertEqual(functional.trailing(lambda w: w == "0", "1000", -2), 2)
    self.assertEqual(functional.trailing(lambda w: w == "0", "1000", 0), 3)
    self.assertEqual(functional.trailing(lambda w: w == "0", "1000", 1), 2)
    self.assertEqual(functional.trailing(lambda w: w == "0", "1000", 2), 1)

  def test_full_count(self):
    self.assertEqual(functional.trailing((lambda w: w > 0), range(1, 10)), 9)

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.trailing, lambda w: w > 0, None)
    self.assertRaises(TypeError, functional.trailing, lambda w: w > 0, 3)
    self.assertRaises(TypeError, functional.trailing, lambda w: w > 0, True)


class Test_select(unittest2.TestCase):
  def test_select(self):
    self.assertEqual(functional.select(builtins.is_even, [1, 2, 3, 4, 5, 6]), [2, 4, 6])
    self.assertEqual(functional.select(None, [0, "", 1, None, 2]), [1, 2])


class Test_reject(unittest2.TestCase):
  def test_reject(self):
    self.assertEqual(functional.reject(builtins.is_even, [1, 2, 3, 4, 5, 6]), [1, 3, 5])
    self.assertEqual(functional.reject(None, [0, "", 1, None, 2]), [0, "", None])


class Test_iselect(unittest2.TestCase):
  def test_iselect(self):
    self.assertEqual(list(functional.iselect(builtins.is_even, [1, 2, 3, 4, 5, 6])), [2, 4, 6])
    self.assertEqual(list(functional.iselect(None, [0, "", 1, None, 2])), [1, 2])


class Test_ireject(unittest2.TestCase):
  def test_ireject(self):
    self.assertEqual(list(functional.ireject(builtins.is_even, [1, 2, 3, 4, 5, 6])), [1, 3, 5])
    self.assertEqual(list(functional.ireject(None, [0, "", 1, None, 2])),
      [0, "", None])


class Test_map_dict(unittest2.TestCase):
  def test_map(self):
    d = {
      "a": "aye",
      "b": 5,
      "C": 0,
      8: 5,
      }

    def _uppercase_key(key, value):
      if isinstance(key, str):
        return key.upper(), value
      else:
        return key, value

    self.assertDictEqual(functional.map_dict(None, d), d)
    self.assertDictEqual(functional.map_dict(lambda k, v: (k, v), d), d)
    self.assertDictEqual(functional.map_dict(_uppercase_key, d), {
      "A": "aye",
      "B": 5,
      "C": 0,
      8: 5,
      })

  def test_AttributeError_if_not_dict(self):
    self.assertRaises(AttributeError, functional.map_dict, None, None)
    self.assertRaises(AttributeError, functional.map_dict, None, (1, ))
    self.assertRaises(AttributeError, functional.map_dict, None, 5)


class Test_select_dict(unittest2.TestCase):
  def test_select_dict(self):
    d = {
      1: "one",
      2: "two",
      3: "three",
      8: "eight",
      }
    self.assertDictEqual(functional.select_dict(None, dict(a="a", b="b", c=None)),
                         dict(a="a", b="b"))
    self.assertDictEqual(functional.select_dict(lambda k, v: builtins.is_even(k), d), {
      2: "two",
      8: "eight",
      })

  def test_AttributeError_if_not_dict(self):
    self.assertRaises(AttributeError, functional.select_dict, None, None)
    self.assertRaises(AttributeError, functional.select_dict, None, (1, ))
    self.assertRaises(AttributeError, functional.select_dict, None, 5)


class Test_reject_dict(unittest2.TestCase):
  def test_reject_dict(self):
    d = {
      1: "one",
      2: "two",
      3: "three",
      8: "eight",
      5: None,
      }
    self.assertDictEqual(functional.reject_dict(None, dict(a="a", b="b", c=None)),
                         dict(c=None))
    self.assertDictEqual(functional.reject_dict(lambda k, v: builtins.is_even(k), d), {
      1: "one",
      3: "three",
      5: None,
      })

  def test_AttributeError_if_not_dict(self):
    self.assertRaises(AttributeError, functional.reject_dict, None, None)
    self.assertRaises(AttributeError, functional.reject_dict, None, (1, ))
    self.assertRaises(AttributeError, functional.reject_dict, None, 5)


class Test_invert_dict(unittest2.TestCase):
  def test_inversion(self):
    d = dict(a=1, b=2)
    self.assertDictEqual(functional.invert_dict(d), {
      1: "a",
      2: "b",
      })
    self.assertEqual(functional.invert_dict(dict(a=(1, 2))), {(1, 2): "a"})

  def test_TypeError_when_unhashable_type(self):
    self.assertRaises(TypeError, functional.invert_dict, dict(a=(1, 2), b=[1, 2]))


class Test_pluck(unittest2.TestCase):
  def test_property(self):
    fruits = [
        {"name": "mango", "taste": "sweet"},
        {"name": "orange", "taste": "tangy"},
        {"name": "banana", "taste": "sweet"},
    ]
    self.assertEqual(functional.pluck(fruits, "name"), ("mango", "orange", "banana"))
    self.assertEqual(tuple(functional.ipluck(fruits, "name")),
      ("mango", "orange", "banana"))

  def test_TypeError_when_not_iterable_of_dicts(self):
    self.assertRaises(TypeError, functional.pluck, ("foo", "blah"))

  def test_KeyError_when_missing_key(self):
    self.assertRaises(KeyError, functional.pluck,
      [dict(a="something"), dict(b="something")], "a")

  def test_default_when_missing_key(self):
    self.assertEqual(
      functional.pluck([dict(a="something"), dict(b="something")], "a", None),
      ("something", None)
    )
    self.assertEqual(
      functional.pluck([dict(a="something"), dict(b="something")], "a", default=None),
      ("something", None)
    )


class Test_ichunks(unittest2.TestCase):
  def test_valid_grouping(self):
    got = functional.ichunks("aaaabbbbccccdddd", 4)
    expected = (("a", ) * 4, ("b",) * 4, ("c",) * 4, ("d",) * 4)
    self.assertEqual(tuple(map(tuple, got)), expected)

    got = functional.ichunks([1, 1, 1, 2, 2, 2, 3, 3, 3], 3)
    expected = ((1, 1, 1), (2, 2, 2), (3, 3, 3))
    self.assertEqual(tuple(map(tuple, got)), expected)

  def test_filler(self):
    got = functional.ichunks("aaaabbbccccddd", 4, "-")
    expected = (("a", "a", "a", "a"),
                ("b", "b", "b", "c"),
                ("c", "c", "c", "d"),
                ("d", "d", "-", "-"))
    self.assertEqual(tuple(map(tuple, got)), expected)

    got = functional.ichunks("aaaabbbbccccdddd", 4, None)
    expected = (("a", ) * 4, ("b",) * 4, ("c",) * 4, ("d",) * 4)
    self.assertEqual(tuple(map(tuple, got)), expected)

  def test_filler_None(self):
    got = functional.ichunks("aaaabbbccccddd", 4, None)
    expected = (("a", "a", "a", "a"),
                ("b", "b", "b", "c"),
                ("c", "c", "c", "d"),
                ("d", "d", None, None))
    self.assertEqual(tuple(map(tuple, got)), expected)

  def test_returns_generator_object(self):
    self.assertEqual(type(functional.ichunks("aaaabbbb", 4)).__name__, "generator")

  def test_odd_ball_grouping(self):
    got = functional.ichunks("aaabb", 3)
    expected = (("a",) * 3, ("b",) * 2)
    self.assertEqual(tuple(map(tuple, got)), expected)


class Test_chunks(unittest2.TestCase):
  def test_valid_grouping(self):
    got = functional.chunks("aaaabbbbccccdddd", 4)
    expected = ["aaaa", "bbbb", "cccc", "dddd"]
    self.assertEqual(list(got), expected)

    got = functional.chunks([1, 1, 1, 2, 2, 2, 3, 3, 3], 3)
    expected = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    self.assertEqual(list(got), expected)

  def test_filler(self):
    got = functional.chunks("aaaabbbccccddd", 4, "-")
    self.assertEqual(list(got), ["aaaa", "bbbc", "cccd", "dd--"])

    self.assertEqual(tuple(functional.chunks((1, 1, 1, 2, 2), 3, (True,))),
      ((1, 1, 1, ), (2, 2, True)))

  def test_filler_iterable_not_same_type_as_filler(self):
    #self.assertRaises(TypeError, list, functional.chunks("aaaabbbccccddd", 4, None))
    self.assertRaises(TypeError, tuple, functional.chunks((1, 1, 1, 2, 2), 3, [None, ]))

  def test_filler_None(self):
    got = functional.chunks("aaaabbbccccddd", 4, None)
    self.assertEqual(list(got), ["aaaa", "bbbc", "cccd", "dd"])

    self.assertEqual(tuple(functional.chunks((1, 1, 1, 2, 2), 3, None)),
      ((1, 1, 1, ), (2, 2, None)))

    self.assertEqual(tuple(functional.chunks([1, 1, 1, 2, 2], 3, None)),
      ([1, 1, 1, ], [2, 2, None]))


  def test_returns_generator_object(self):
    self.assertEqual(type(functional.chunks("aaaabbbb", 4)).__name__, "generator")

  def test_odd_ball_grouping(self):
    got = functional.chunks("aaabb", 3)
    self.assertEqual(list(got), ["aaa", "bb"])


class Test_each(unittest2.TestCase):
  def test_each(self):
    d = {}

    def _copy_to_dict(i, x):
      d[i] = x

    functional.each(_copy_to_dict, [1, 2, 3])
    self.assertEqual(d, {
      0: 1,
      1: 2,
      2: 3,
      })

  def test_dict_each(self):
    d = {}
    sample = dict(a="1", b="2")

    def _copy_dict(k, v):
      d[k] = v

    functional.each(_copy_dict, sample)
    self.assertDictEqual(d, sample)


  def test_TypeError_when_not_callable(self):
    self.assertRaises(TypeError, functional.each, None, range(5))


class Test_seq(unittest2.TestCase):
  def test_head(self):
    self.assertEqual(functional.head(range(10)), 0)

  def test_last(self):
    self.assertEqual(functional.last(range(10)), 9)

  def test_itail(self):
    self.assertEqual(list(functional.itail(range(10))), list(range(1, 10)))

  def test_tail(self):
    self.assertEqual(functional.tail(list(range(10))), list(range(1, 10)))


# Truthy and falsy tests.
class Test_truthy(unittest2.TestCase):
  def test_truthy(self):
    self.assertEqual(functional.truthy([1, 0, 0, 1, None, True, False, {}]),
      [1, 1, True])
    self.assertEqual(functional.truthy((0, 1, 2, False, None, True)), [1, 2, True])


class Test_falsy(unittest2.TestCase):
  def test_falsy(self):
    self.assertEqual(functional.falsy([1, 0, 0, 1, None, True, False, {}]),
      [0, 0, None, False, {}])
    self.assertEqual(functional.falsy((0, 1, 2, False, None, True)), [0, False, None])


class Test_itruthy(unittest2.TestCase):
  def test_itruthy(self):
    self.assertEqual(list(functional.itruthy([1, 0, 0, 1, None, True, False, {}])),
      [1, 1, True])
    self.assertEqual(tuple(functional.itruthy((0, 1, 2, False, None, True))),
      (1, 2, True))


class Test_ifalsy(unittest2.TestCase):
  def test_ifalsy(self):
    self.assertEqual(list(functional.ifalsy([1, 0, 0, 1, None, True, False, {}])),
      [0, 0, None, False, {}])
    self.assertEqual(tuple(functional.ifalsy((0, 1, 2, False, None, True))),
      (0, False, None))

# Function generator tests.
class Test_compose(unittest2.TestCase):
  def test_composition(self):
    greet = lambda name: "hi: " + name
    exclaim = lambda statement: statement + "!"
    welcome = functional.compose(exclaim, greet)
    self.assertEqual(welcome("moe"), "hi: moe!")

  def test_numerical_composition(self):
    plus1 = lambda w: w + 1
    times2 = lambda w: w * 2

    self.assertEqual(functional.compose(plus1, times2)(5), 11)
    self.assertEqual(functional.compose(times2, plus1)(5), 12)

  def test_composition_with_one_function(self):
    def f(x): return x

    a = functional.compose(f)
    self.assertEqual(a(5), 5)


class Test__compose(unittest2.TestCase):
  def test_composition(self):
    greet = lambda name: "hi: " + name
    exclaim = lambda statement: statement + "!"
    welcome = functional._compose(exclaim, greet)
    self.assertEqual(welcome("moe"), "hi: moe!")

  def test_numerical_composition(self):
    plus1 = lambda w: w + 1
    times2 = lambda w: w * 2

    self.assertEqual(functional._compose(plus1, times2)(5), 11)
    self.assertEqual(functional._compose(times2, plus1)(5), 12)

  def test_composition_with_one_function(self):
    def f(x): return x

    a = functional._compose(f)
    self.assertEqual(a(5), 5)


class Test_complement(unittest2.TestCase):
  def test_complementary_function(self):
    def tru(x):
      return True

    fals = functional.complement(tru)
    ahem = functional.complement(fals)
    self.assertFalse(fals(5))
    self.assertTrue(ahem(5))

# Contains and omits tests
class Test_contains(unittest2.TestCase):
  def test_contains_value(self):
    self.assertTrue(functional.contains(range(4), 3))
    self.assertFalse(functional.contains(range(4), 43))
    self.assertTrue(functional.contains({"a": 4, "b": 5}, "a"))
    self.assertFalse(functional.contains({"a": 4, "b": 5}, "c"))
    self.assertTrue(functional.contains(set([1, 2, 3]), 3))
    self.assertFalse(functional.contains(set([1, 2, 3]), 5))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.contains, None, 4)
    self.assertRaises(TypeError, functional.contains, True, 4)
    self.assertRaises(TypeError, functional.contains, 0, 4)

  def test_index_ValueError_branch(self):
    class MockContainer(object):
      def __init__(self, value):
        self.value = value

      def index(self, unused_value):
        raise ValueError("Not found")

    self.assertFalse(functional.contains(MockContainer("something"), None))


class Test_omits(unittest2.TestCase):
  def test_omits_value(self):
    self.assertFalse(functional.omits(range(4), 3))
    self.assertTrue(functional.omits(range(4), 43))
    self.assertFalse(functional.omits({"a": 4, "b": 5}, "a"))
    self.assertTrue(functional.omits({"a": 4, "b": 5}, "c"))
    self.assertFalse(functional.omits(set([1, 2, 3]), 3))
    self.assertTrue(functional.omits(set([1, 2, 3]), 5))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.omits, None, 4)
    self.assertRaises(TypeError, functional.omits, True, 4)
    self.assertRaises(TypeError, functional.omits, 0, 4)


class Test__contains(unittest2.TestCase):
  def test__contains_value(self):
    self.assertTrue(functional._contains_fallback(range(4), 3))
    self.assertFalse(functional._contains_fallback(range(4), 43))
    self.assertTrue(functional._contains_fallback({"a": 4, "b": 5}, "a"))
    self.assertFalse(functional._contains_fallback({"a": 4, "b": 5}, "c"))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional._contains_fallback, None, 4)
    self.assertRaises(TypeError, functional._contains_fallback, True, 4)
    self.assertRaises(TypeError, functional._contains_fallback, 0, 4)

# Unique, functional.union, difference, and without tests.
class Test_difference(unittest2.TestCase):
  def test_difference(self):
    self.assertEqual(functional.difference(range(1, 6), [5, 2, 10]), [1, 3, 4])
    self.assertEqual(functional.difference("abcdefg", "abc"), list("defg"))
    self.assertEqual(functional.difference("abcdefg", "xyz"), list("abcdefg"))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.difference, None, None)
    self.assertRaises(TypeError, functional.difference, None, True)
    self.assertRaises(TypeError, functional.difference, None, 0)
    self.assertRaises(TypeError, functional.difference, 0, None)
    self.assertRaises(TypeError, functional.difference, 0, True)
    self.assertRaises(TypeError, functional.difference, 0, 0)


class Test_idifference(unittest2.TestCase):
  def test_idifference(self):
    self.assertEqual(list(functional.idifference(range(1, 6), [5, 2, 10])), [1, 3, 4])
    self.assertEqual("".join(functional.idifference("abcdefg", "abc")), "defg")
    self.assertEqual("".join(functional.idifference("abcdefg", "xyz")), "abcdefg")

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.idifference, None, None)
    self.assertRaises(TypeError, functional.idifference, None, True)
    self.assertRaises(TypeError, functional.idifference, None, 0)
    self.assertRaises(TypeError, functional.idifference, 0, None)
    self.assertRaises(TypeError, functional.idifference, 0, True)
    self.assertRaises(TypeError, functional.idifference, 0, 0)


class Test_without(unittest2.TestCase):
  def test_without(self):
    self.assertEqual(functional.without(range(1, 6), *[5, 2, 10]), [1, 3, 4])
    self.assertEqual(functional.without("abcdefg", *list("abc")), list("defg"))
    self.assertEqual(functional.without("abcdefg", *list("xyz")), list("abcdefg"))

  def test_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.without, None, None)
    self.assertRaises(TypeError, functional.without, None, True)
    self.assertRaises(TypeError, functional.without, None, 0)
    self.assertRaises(TypeError, functional.without, 0, None)
    self.assertRaises(TypeError, functional.without, 0, True)
    self.assertRaises(TypeError, functional.without, 0, 0)


class Test_unique(unittest2.TestCase):
  def test_uniques(self):
    self.assertEqual(functional.unique("aabbccyyyyyyyyyyyyyyyyy", True),
      ["a", "b", "c", "y"])
    self.assertEqual(functional.unique("google"),
      ["g", "o", "l", "e"])
    self.assertEqual(functional.unique(""), "")


class Test_union(unittest2.TestCase):
  def test_union(self):
    self.assertEqual(
      functional.union("google", "yahoo"),
      ["g", "o", "l", "e", "y", "a", "h"]
    )
    self.assertEqual(
      functional.union("google"),
      "google",
      )


class Test_reduce(unittest2.TestCase):
  def test_reduce(self):
    self.assertEqual(functional.reduce(lambda x, y: x + y, [1, 2, 3]), 6)

  def test_TypeError(self):
    self.assertRaises(TypeError, functional.reduce, None, range(5))
    self.assertRaises(TypeError, functional.reduce, lambda x, y: x + y, None)


class Test_identity(unittest2.TestCase):
  def test_identity(self):
    self.assertEqual(functional.identity(True), True)
    self.assertEqual(functional.identity(False), False)
    self.assertEqual(functional.identity(0), 0)
    self.assertEqual(functional.identity({}), {})
    self.assertEqual(functional.identity(None), None)


class Test_flatten(unittest2.TestCase):
  def test_flattened(self):
    self.assertEqual(
      functional.flatten([[0, 1, 2], (0, 6, (5, 4), ("a", "b")), (7, 8)]),
      [0, 1, 2, 0, 6, 5, 4, "a", "b", 7, 8]
    )


class Test_flatten1(unittest2.TestCase):
  def test_flattened_one_level(self):
    self.assertEqual(
      functional.flatten1((1, (0, 5, ("a", "b")), (3, 4))),
      [1, 0, 5, ("a", "b"), 3, 4]
    )


class Test_nth(unittest2.TestCase):
  def test_nth(self):
    self.assertEqual(functional.nth("abcd", 0), "a")
    self.assertEqual(functional.nth("abcd", 3), "d")
    self.assertEqual(functional.nth("abcd", 4), None)
    self.assertEqual(functional.nth("abcd", 4), None)


class Test_intersection(unittest2.TestCase):
  def test_intersection(self):
    self.assertEqual(functional.intersection([1, 2, 3]), [1, 2, 3])
    self.assertEqual(functional.intersection([1, 2, 3, 0], [0, 2, 3]), [2, 3, 0])
    self.assertEqual(functional.intersection([1, 5, 4], [0, 2, 3]), [])

  def test_single_iterable(self):
    self.assertEqual(functional.intersection([1, 2, 3]), [1, 2, 3])


class Test_take(unittest2.TestCase):
  def test_take(self):
    self.assertEqual(functional.take([1, 2, 3, 4, 5], 3), (1, 2, 3))


class Test_round_robin(unittest2.TestCase):
  def test_round_robin(self):
    self.assertEqual(list(functional.round_robin("ABC", "D", "EF")),
      ["A", "D", "E", "B", "F", "C"])


class Test_tally(unittest2.TestCase):
  def test_tally(self):
    self.assertEqual(functional.tally(lambda w: w > 10, range(10, 40)), 29)


class Test_partition(unittest2.TestCase):
  def test_partition(self):
    self.assertEqual(functional.partition(lambda w: w > 5, range(10)),
      ([6, 7, 8, 9], [0, 1, 2, 3, 4, 5]))

  def test_not_iterable(self):
    self.assertRaises(TypeError, functional.partition, bool, None)


class Test_peel(unittest2.TestCase):
  def test_ipeel(self):
    self.assertEqual(list(functional.ipeel("abbbc")), ["b", "b", "b"])
    self.assertEqual(list(functional.ipeel("")), [])
    self.assertEqual(list(functional.ipeel("a")), [])
    self.assertEqual(list(functional.ipeel("a", 34)), [])

  def test_ValueError_when_negative_count(self):
    self.assertRaises(ValueError, functional.ipeel, "abbbc", -1)
    self.assertRaises(ValueError, functional.peel, "abbbc", -1)

  def test_peel(self):
    self.assertEqual(functional.peel("abbbc"), "bbb")
    self.assertEqual(functional.peel(0), 0)
    self.assertEqual(functional.peel(""), "")
    self.assertEqual(functional.peel("a"), "")
    self.assertEqual(functional.peel("a", 34), "")


class Test_loob(unittest2.TestCase):
  def test_loob(self):
    self.assertFalse(functional.loob(True))
    self.assertFalse(functional.loob("something"))
    self.assertFalse(functional.loob([1, 2]))
    self.assertFalse(functional.loob(2))
    self.assertTrue(functional.loob({}))
    self.assertTrue(functional.loob(""))
    self.assertTrue(functional.loob([]))
    self.assertTrue(functional.loob(0))
    self.assertTrue(functional.loob(False))
    self.assertTrue(functional.loob(None))


class Test_ncycles(unittest2.TestCase):
  def test_ncycles(self):
    self.assertEqual(tuple(functional.ncycles([1, 2, 3], 4)), (1, 2, 3) * 4)


class Test_eat(unittest2.TestCase):
  def test_eat(self):
    it = functional.ncycles([1, 2, 3], 4)
    functional.eat(it, 9)
    self.assertEqual(tuple(it), (1, 2, 3))
    it = functional.ncycles([1, 2, 3], 4)
    functional.eat(it, None)
    self.assertEqual(tuple(it), ())


class Test_always(unittest2.TestCase):
  def test_always_true(self):
    self.assertTrue(functional.always(False))


class Test_never(unittest2.TestCase):
  def test_never_true(self):
    self.assertFalse(functional.never(True))


class Test_partition_dict(unittest2.TestCase):
  def test_properly_partitions(self):
    args = dict(
      oauth_token="token",
      oauth_blah="blah",
      something="another",
      boobooo="booobooo",
      )
    a, b = functional.partition_dict(lambda k, v: k.startswith("oauth_"), args)
    self.assertDictEqual(a, {"oauth_token": "token", "oauth_blah": "blah"})
    self.assertDictEqual(b, {"boobooo": "booobooo", "something": "another"})


class Test_occurrences(unittest2.TestCase):
  def test_missing_element_count_is_0(self):
    d = functional.occurrences("aaaaa")
    self.assertEqual(d["c"], 0)

  def test_returns_multiset(self):
    self.assertDictEqual(dict(functional.occurrences("aaaaabbbccc")),
        {"a": 5, "b": 3, "c": 3})

  def test_returns_blank_for_empty(self):
    self.assertDictEqual(dict(functional.occurrences("")), {})

  def test_raises_TypeError_when_not_iterable(self):
    self.assertRaises(TypeError, functional.occurrences, None)


class Test_group_consecutive(unittest2.TestCase):
  def test_result(self):
    things = [("phone", "android"),
      ("phone", "iphone"),
      ("tablet", "ipad"),
      ("laptop", "dell studio"),
      ("phone", "nokia"),
      ("laptop", "macbook pro")]

    self.assertEqual(list(functional.group_consecutive(lambda w: w[0], things)),
      [(("phone", "android"), ("phone", "iphone")),
        (("tablet", "ipad"),),
        (("laptop", "dell studio"),),
        (("phone", "nokia"),),
        (("laptop", "macbook pro"),)]
    )

    self.assertEqual(list(functional.group_consecutive(lambda w: w[0],
                                            "mississippi")),
      [("m",), ("i",),
        ("s", "s"), ("i",),
        ("s", "s"), ("i",),
        ("p", "p"), ("i",)]
    )


class Test_flock(unittest2.TestCase):
  def test_result(self):
    things = [("phone", "android"),
      ("phone", "iphone"),
      ("tablet", "ipad"),
      ("laptop", "dell studio"),
      ("phone", "nokia"),
      ("laptop", "macbook pro")]

    self.assertEqual(list(functional.flock(lambda w: w[0], things)),
      [(("laptop", "dell studio"), ("laptop", "macbook pro")),
        (("phone", "android"), ("phone", "iphone"), ("phone", "nokia")),
        (("tablet", "ipad"),)]
    )

    self.assertEqual(
      list(functional.flock(lambda w: w[0], "mississippi")),
      [("i", "i", "i", "i"), ("m",), ("p", "p"), ("s", "s", "s", "s")]
    )


if __name__ == "__main__":
  unittest2.main()
