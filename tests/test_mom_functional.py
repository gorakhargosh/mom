#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.builtins import is_even
from mom.functional import \
    leading, some, trailing, every, \
    find, none,\
    select, reject, ireject, iselect, \
    chunks, map_dict, select_dict, reject_dict, invert_dict, \
    pluck, first, last, rest, truthy, compose, contains, \
    difference, without, _contains_fallback, complement, each, \
    reduce, identity, flatten, flatten1, unique, _some1, _some2, \
    union, nth, intersection, take, round_robin, tally, _leading, partition, falsy


class Test_some(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(some(lambda w: w > 0, [0, -1, 4, 6]))

        self.assertFalse(some(lambda w: w > 0, [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, some, lambda w: w > 0, None)
        self.assertRaises(TypeError, some, lambda w: w > 0, 5)
        self.assertRaises(TypeError, some, lambda w: w > 0, True)


class Test__some1(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(_some1(lambda w: w > 0, [0, -1, 4, 6]))

        self.assertFalse(_some1(lambda w: w > 0, [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, _some1, lambda w: w > 0, None)
        self.assertRaises(TypeError, _some1, lambda w: w > 0, 5)
        self.assertRaises(TypeError, _some1, lambda w: w > 0, True)

class Test__some2(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(_some2(lambda w: w > 0, [0, -1, 4, 6]))

        self.assertFalse(_some2(lambda w: w > 0, [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, _some2, lambda w: w > 0, None)
        self.assertRaises(TypeError, _some2, lambda w: w > 0, 5)
        self.assertRaises(TypeError, _some2, lambda w: w > 0, True)


class Test_every(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(every(lambda w: w > 0, [1, 1, 4, 6]))
        self.assertFalse(every(lambda w: w > 0, [0, -1, 4, 6]))
        self.assertFalse(every(lambda w: w > 0, [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, every, lambda w: w > 0, None)
        self.assertRaises(TypeError, every, lambda w: w > 0, 5)
        self.assertRaises(TypeError, every, lambda w: w > 0, True)


class Test_none(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(none(lambda w: w < 1, [1, 1, 4, 6]))
        self.assertFalse(none(lambda w: w > 0, [0, -1, 4, 6]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, none, lambda w: w > 0, None)
        self.assertRaises(TypeError, none, lambda w: w > 0, 5)
        self.assertRaises(TypeError, none, lambda w: w > 0, True)


class Test_find(unittest2.TestCase):
    def test_valid_index(self):
        self.assertEqual(find(lambda w: w > 2, [0, 1, 2, 3, 4, 5]), 3)

    def test_not_found(self):
        self.assertEqual(find(lambda w: w > 50, range(5)), -1)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, find, lambda w: w > 2, None)
        self.assertRaises(TypeError, find, lambda w: w > 2, 5)
        self.assertRaises(TypeError, find, lambda w: w > 2, True)


class Test__leading(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(_leading(lambda w: w > 0, [0, 0, 1]), 0)
        self.assertEqual(_leading(lambda w: w > 1, [2, 2, 3, 0, 5]), 3)
        self.assertEqual(_leading(lambda w: ord(w) >= ord('c'), "abalskjd"), 0)
        self.assertEqual(_leading(lambda w: ord(w) >= ord('c'), "cuddleya"), 7)

    def test_start(self):
        self.assertEqual(_leading(lambda w: w == "0", "0001"), 3)
        self.assertEqual(_leading(lambda w: w == "0", "0001", 0), 3)
        self.assertEqual(_leading(lambda w: w == "0", "0001", 1), 2)

    def test_full_count(self):
        self.assertEqual(_leading(lambda w: w > 0, range(1, 10)), 9)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, _leading, lambda w: w > 0, None)
        self.assertRaises(TypeError, _leading, lambda w: w > 0, 3)
        self.assertRaises(TypeError, _leading, lambda w: w > 0, True)

class Test_leading(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(leading(lambda w: w > 0, [0, 0, 1]), 0)
        self.assertEqual(leading(lambda w: w > 1, [2, 2, 3, 0, 5]), 3)
        self.assertEqual(leading(lambda w: ord(w) >= ord('c'), "abalskjd"), 0)
        self.assertEqual(leading(lambda w: ord(w) >= ord('c'), "cuddleya"), 7)

    def test_start(self):
        self.assertEqual(leading(lambda w: w == "0", "0001"), 3)
        self.assertEqual(leading(lambda w: w == "0", "0001", 0), 3)
        self.assertEqual(leading(lambda w: w == "0", "0001", 1), 2)

    def test_full_count(self):
        self.assertEqual(leading(lambda w: w > 0, range(1, 10)), 9)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, leading, lambda w: w > 0, None)
        self.assertRaises(TypeError, leading, lambda w: w > 0, 3)
        self.assertRaises(TypeError, leading, lambda w: w > 0, True)

class Test_trailing(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(trailing(lambda w: w > 0, [0, 0, 1]), 1)
        self.assertEqual(trailing(lambda w: w > 1, [2, 0, 2, 3, 5]), 3)
        self.assertEqual(trailing(lambda w: ord(w) >= ord('c'), "abalskjd"), 5)
        self.assertEqual(trailing(lambda w: ord(w) >= ord('c'), "cuddleya"), 0)

    def test_end(self):
        self.assertEqual(trailing(lambda w: w == "0", "0001"), 0)
        self.assertEqual(trailing(lambda w: w == "0", "1000", -1), 3)
        self.assertEqual(trailing(lambda w: w == "0", "1000", -2), 2)
        self.assertEqual(trailing(lambda w: w == "0", "1000", 0), 3)
        self.assertEqual(trailing(lambda w: w == "0", "1000", 1), 2)
        self.assertEqual(trailing(lambda w: w == "0", "1000", 2), 1)

    def test_full_count(self):
        self.assertEqual(trailing((lambda w: w > 0), range(1, 10)), 9)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, trailing, lambda w: w > 0, None)
        self.assertRaises(TypeError, trailing, lambda w: w > 0, 3)
        self.assertRaises(TypeError, trailing, lambda w: w > 0, True)


class Test_select(unittest2.TestCase):
    def test_select(self):
        self.assertEqual(select(is_even, [1, 2, 3, 4, 5, 6]), [2, 4, 6])
        self.assertEqual(select(None, [0, "", 1, None, 2]), [1, 2])

class Test_reject(unittest2.TestCase):
    def test_reject(self):
        self.assertEqual(reject(is_even, [1, 2, 3, 4, 5, 6]), [1, 3, 5])
        self.assertEqual(reject(None, [0, "", 1, None, 2]), [0, "", None])


class Test_iselect(unittest2.TestCase):
    def test_iselect(self):
        self.assertEqual(list(iselect(is_even, [1, 2, 3, 4, 5, 6])), [2, 4, 6])
        self.assertEqual(list(iselect(None, [0, "", 1, None, 2])), [1, 2])

class Test_ireject(unittest2.TestCase):
    def test_ireject(self):
        self.assertEqual(list(ireject(is_even, [1, 2, 3, 4, 5, 6])), [1, 3, 5])
        self.assertEqual(list(ireject(None, [0, "", 1, None, 2])),
            [0, "", None])


class Test_map_dict(unittest2.TestCase):
    def test_map(self):
        d = {
            "a": "aye",
            "b": 5,
            "C": 0,
            8: 5,
        }

        def _uppercase_key(pair):
            if isinstance(pair[0], str):
                return pair[0].upper(), pair[1]
            else:
                return pair[0], pair[1]
        self.assertDictEqual(map_dict(None, d), d)
        self.assertDictEqual(map_dict(lambda w: w, d), d)
        self.assertDictEqual(map_dict(_uppercase_key, d), {
            "A": "aye",
            "B": 5,
            "C": 0,
            8: 5,
        })

    def test_AttributeError_if_not_dict(self):
        self.assertRaises(AttributeError, map_dict, None, None)
        self.assertRaises(AttributeError, map_dict, None, (1, ))
        self.assertRaises(AttributeError, map_dict, None, 5)

class Test_select_dict(unittest2.TestCase):
    def test_select_dict(self):
        d = {
            1: "one",
            2: "two",
            3: "three",
            8: "eight",
        }
        self.assertDictEqual(select_dict(None, dict(a="a", b="b", c=None)),
                             dict(a="a", b="b"))
        self.assertDictEqual(select_dict(lambda w: is_even(w[0]), d), {
            2: "two",
            8: "eight",
        })

    def test_AttributeError_if_not_dict(self):
        self.assertRaises(AttributeError, select_dict, None, None)
        self.assertRaises(AttributeError, select_dict, None, (1, ))
        self.assertRaises(AttributeError, select_dict, None, 5)

class Test_reject_dict(unittest2.TestCase):
    def test_reject_dict(self):
        d = {
            1: "one",
            2: "two",
            3: "three",
            8: "eight",
            5: None,
        }
        self.assertDictEqual(reject_dict(None, dict(a="a", b="b", c=None)),
                             dict(c=None))
        self.assertDictEqual(reject_dict(lambda w: is_even(w[0]), d), {
            1: "one",
            3: "three",
            5: None,
        })

    def test_AttributeError_if_not_dict(self):
        self.assertRaises(AttributeError, reject_dict, None, None)
        self.assertRaises(AttributeError, reject_dict, None, (1, ))
        self.assertRaises(AttributeError, reject_dict, None, 5)


class Test_invert_dict(unittest2.TestCase):
    def test_inversion(self):
        d = dict(a=1, b=2)
        self.assertDictEqual(invert_dict(d), {
            1: "a",
            2: "b",
        })
        self.assertEqual(invert_dict(dict(a=(1, 2))), {(1, 2): "a"})

    def test_TypeError_when_unhashable_type(self):
        self.assertRaises(TypeError, invert_dict, dict(a=(1, 2), b=[1, 2]))


class Test_pluck(unittest2.TestCase):
    def test_property(self):
        fruits = [
            {"name": 'mango', "taste": "sweet"},
            {"name": 'orange', "taste": "tangy"},
            {"name": 'banana', "taste": "sweet"},
        ]
        self.assertEqual(pluck(fruits, "name"), ("mango", "orange", "banana"))

    def test_TypeError_when_not_iterable_of_dicts(self):
        self.assertRaises(TypeError, pluck, ("foo", "blah"))

    def test_KeyError_when_missing_key(self):
        self.assertRaises(KeyError, pluck,
            [dict(a="something"), dict(b="something")], "a")

    def test_default_when_missing_key(self):
        self.assertEqual(
            pluck([dict(a="something"), dict(b="something")], "a", None),
            ("something", None)
        )
        self.assertEqual(
            pluck([dict(a="something"), dict(b="something")], "a", default=None),
            ("something", None)
        )


class Test_chunks(unittest2.TestCase):
    def test_valid_grouping(self):
        got = chunks("aaaabbbbccccdddd", 4)
        expected = (("a", ) * 4, ("b",) * 4, ("c",) * 4, ("d",) * 4)
        for g, e in zip(map(tuple, got), expected):
            self.assertEqual(g, e)

        got = chunks([1, 1, 1, 2, 2, 2, 3, 3, 3], 3)
        expected = [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        for g, e in zip(map(tuple, got), expected):
            self.assertEqual(g, e)

    def test_filler(self):
        got = chunks("aaaabbbccccddd", 4, "-")
        expected = (("a", "a", "a", "a"),
                    ("b", "b", "b", "c"),
                    ("c", "c", "c", "d"),
                    ("d", "d", "-", "-"))
        for g, e in zip(map(tuple, got), expected):
            self.assertEqual(g, e)

        got = chunks("aaaabbbbccccdddd", 4, None)
        expected = (("a", ) * 4, ("b",) * 4, ("c",) * 4, ("d",) * 4)
        for g, e in zip(map(tuple, got), expected):
            self.assertEqual(g, e)

    def test_filler_None(self):
        got = chunks("aaaabbbccccddd", 4, None)
        expected = (("a", "a", "a", "a"),
                    ("b", "b", "b", "c"),
                    ("c", "c", "c", "d"),
                    ("d", "d", None, None))
        for g, e in zip(map(tuple, got), expected):
            self.assertEqual(g, e)

#    def test_TypeError_when_filler_not_iterable(self):
#        self.assertRaises(TypeError, map, tuple, chunks("aabbc", 2, 3))

    def test_returns_generator_object(self):
        self.assertEqual(type(chunks("aaaabbbb", 4)).__name__, "generator")

    def test_odd_ball_grouping(self):
        got = chunks("aaabb", 3)
        expected = [("a",) * 3, ("b",) * 2]
        for g, e in zip(map(tuple, got), expected):
            self.assertEqual(g, e)


class Test_each(unittest2.TestCase):
    def test_each(self):
        d = {}
        def _copy_to_dict(i, x):
            d[i] = x
        each(_copy_to_dict, [1, 2, 3])
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
        each(_copy_dict, sample)
        self.assertDictEqual(d, sample)


    def test_TypeError_when_not_callable(self):
        self.assertRaises(TypeError, each, None, range(5))


class Test_seq(unittest2.TestCase):
    def test_first(self):
        self.assertEqual(first(range(10)), 0)

    def test_last(self):
        self.assertEqual(last(range(10)), 9)

    def test_rest(self):
        self.assertEqual(list(rest(range(10))), range(1, 10))


class Test_truthy(unittest2.TestCase):
    def test_truthy(self):
        self.assertEqual(truthy([1, 0, 0, 1, None, True, False, {}]),
            [1, 1, True])
        self.assertEqual(truthy((0, 1, 2, False, None, True)), (1, 2, True))


class Test_falsy(unittest2.TestCase):
    def test_falsy(self):
        self.assertEqual(falsy([1, 0, 0, 1, None, True, False, {}]),
            [0, 0, None, False, {}])
        self.assertEqual(falsy((0, 1, 2, False, None, True)), (0, False, None))


class Test_compose(unittest2.TestCase):
    def test_composition(self):
        greet = lambda name: "hi: " + name
        exclaim = lambda statement: statement + "!"
        welcome = compose(exclaim, greet)
        self.assertEqual(welcome("moe"), "hi: moe!")


    def test_numerical_composition(self):
        plus1 = lambda w: w + 1
        times2 = lambda w: w * 2

        self.assertEqual(compose(plus1, times2)(5), 11)
        self.assertEqual(compose(times2, plus1)(5), 12)


class Test_contains(unittest2.TestCase):
    def test_contains_value(self):
        self.assertTrue(contains(range(4), 3))
        self.assertFalse(contains(range(4), 43))
        self.assertTrue(contains({"a": 4, "b": 5}, "a"))
        self.assertFalse(contains({"a": 4, "b": 5}, "c"))
        self.assertTrue(contains(set([1, 2, 3]), 3))
        self.assertFalse(contains(set([1, 2, 3]), 5))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, contains, None, 4)
        self.assertRaises(TypeError, contains, True, 4)
        self.assertRaises(TypeError, contains, 0, 4)


class Test__contains(unittest2.TestCase):
    def test__contains_value(self):
        self.assertTrue(_contains_fallback(range(4), 3))
        self.assertFalse(_contains_fallback(range(4), 43))
        self.assertTrue(_contains_fallback({"a": 4, "b": 5}, "a"))
        self.assertFalse(_contains_fallback({"a": 4, "b": 5}, "c"))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, _contains_fallback, None, 4)
        self.assertRaises(TypeError, _contains_fallback, True, 4)
        self.assertRaises(TypeError, _contains_fallback, 0, 4)


class Test_difference(unittest2.TestCase):
    def test_difference(self):
        self.assertEqual(difference(range(1, 6), [5, 2, 10]), [1, 3, 4])
        self.assertEqual(difference("abcdefg", "abc"), "defg")
        self.assertEqual(difference("abcdefg", "xyz"), "abcdefg")

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, difference, None, None)
        self.assertRaises(TypeError, difference, None, True)
        self.assertRaises(TypeError, difference, None, 0)
        self.assertRaises(TypeError, difference, 0, None)
        self.assertRaises(TypeError, difference, 0, True)
        self.assertRaises(TypeError, difference, 0, 0)


class Test_without(unittest2.TestCase):
    def test_without(self):
        self.assertEqual(without(range(1, 6), *[5, 2, 10]), [1, 3, 4])
        self.assertEqual(without("abcdefg", *list("abc")), "defg")
        self.assertEqual(without("abcdefg", *list("xyz")), "abcdefg")


    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, without, None, None)
        self.assertRaises(TypeError, without, None, True)
        self.assertRaises(TypeError, without, None, 0)
        self.assertRaises(TypeError, without, 0, None)
        self.assertRaises(TypeError, without, 0, True)
        self.assertRaises(TypeError, without, 0, 0)


class Test_complement(unittest2.TestCase):
    def test_complementary_function(self):
        def tru(x):
            return True
        fals = complement(tru)
        ahem = complement(fals)
        self.assertFalse(fals(5))
        self.assertTrue(ahem(5))


class Test_reduce(unittest2.TestCase):
    def test_reduce(self):
        self.assertEqual(reduce(lambda x, y: x + y, [1, 2, 3]), 6)

    def test_TypeError(self):
        self.assertRaises(TypeError, reduce, None, range(5))
        self.assertRaises(TypeError, reduce, lambda x, y: x + y, None)


class Test_identity(unittest2.TestCase):
    def test_identity(self):
        self.assertEqual(identity(True), True)
        self.assertEqual(identity(False), False)
        self.assertEqual(identity(0), 0)
        self.assertEqual(identity({}), {})
        self.assertEqual(identity(None), None)

class Test_flatten(unittest2.TestCase):
    def test_flattened(self):
        self.assertEqual(
            flatten([[0, 1, 2], (0, 6, (5, 4), ('a', 'b')), (7, 8)]),
            [0, 1, 2, 0, 6, 5, 4, 'a', 'b', 7, 8]
        )

class Test_flatten1(unittest2.TestCase):
    def test_flattened_one_level(self):
        self.assertEqual(
            flatten1((1, (0, 5, ('a', 'b')), (3, 4))),
            [1, 0, 5, ('a', 'b'), 3, 4]
        )


class Test_unique(unittest2.TestCase):
    def test_uniques(self):
        self.assertEqual(unique('aabbccyyyyyyyyyyyyyyyyy', True),
            ["a", "b", "c", "y"])
        self.assertEqual(unique('google', False),
            ["g", "o", "l", "e"])
        self.assertEqual(unique(""), "")

class Test_union(unittest2.TestCase):
    def test_union(self):
        self.assertEqual(
            union("google", "yahoo"),
            ["g", "o", "l", "e", "y", "a", "h"]
        )


class Test_nth(unittest2.TestCase):
    def test_nth(self):
        self.assertEqual(nth("abcd", 0), "a")
        self.assertEqual(nth("abcd", 3), "d")
        self.assertEqual(nth("abcd", 4, None), None)
        self.assertEqual(nth("abcd", 4), None)


class Test_intersection(unittest2.TestCase):
    def test_intersection(self):
        self.assertEqual(intersection([1, 2, 3, 0], [0, 2, 3]), [2, 3, 0])
        self.assertEqual(intersection([1, 5, 4], [0, 2, 3]), [])


class Test_take(unittest2.TestCase):
    def test_take(self):
        self.assertEqual(take([1, 2, 3, 4, 5], 3), (1, 2, 3))


class Test_round_robin(unittest2.TestCase):
    def test_round_robin(self):
        self.assertEqual(list(round_robin("ABC", "D", "EF")),
                        ["A", "D", "E", "B", "F", "C"])


class Test_tally(unittest2.TestCase):
    def test_tally(self):
        self.assertEqual(tally(lambda w: w > 10, range(10, 40)), 29)


class Test_partition(unittest2.TestCase):
    def test_partition(self):
        self.assertEqual(partition(lambda w: w > 5, range(10)),
                         ([6, 7, 8, 9], [0, 1, 2, 3, 4, 5]))

    def test_not_iterable(self):
        self.assertRaises(TypeError, partition, bool, None)


if __name__ == '__main__':
    unittest2.main()
