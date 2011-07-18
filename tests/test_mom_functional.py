#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.functional import \
    leading, some, trailing, every, \
    find, none, is_even, is_odd, is_positive, \
    is_negative, select, reject, ireject, iselect, \
    chunks, map_dict, select_dict, reject_dict, invert_dict, pluck, each


class Test_some(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(some(lambda w: w > 0, [0, -1, 4, 6]))

        self.assertFalse(some(lambda w: w > 0, [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, some, lambda w: w > 0, None)
        self.assertRaises(TypeError, some, lambda w: w > 0, 5)
        self.assertRaises(TypeError, some, lambda w: w > 0, True)

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


class Test_leading(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(leading(lambda w: w > 0, [0, 0, 1]), 0)
        self.assertEqual(leading(lambda w: w > 1, [2, 2, 3, 0, 5]), 3)
        self.assertEqual(leading(lambda w: ord(w) >= ord('c'), "abalskjd"), 0)
        self.assertEqual(leading(lambda w: ord(w) >= ord('c'), "cuddleya"), 7)

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

    def test_full_count(self):
        self.assertEqual(trailing((lambda w: w > 0), range(1, 10)), 9)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, trailing, lambda w: w > 0, None)
        self.assertRaises(TypeError, trailing, lambda w: w > 0, 3)
        self.assertRaises(TypeError, trailing, lambda w: w > 0, True)


class Test_is_even(unittest2.TestCase):
    def test_parity(self):
        self.assertTrue(is_even(2l))
        self.assertFalse(is_even(1L))
        self.assertTrue(is_even(-2l))
        self.assertFalse(is_even(-1L))

        self.assertTrue(is_even(0))

    def test_boolean(self):
        # Python 2.x legacy. Ew.
        self.assertFalse(is_even(True))
        self.assertTrue(is_even(False))

    def test_TypeError_when_invalid_type(self):
        self.assertRaises(TypeError, is_even, 2.0)
        self.assertRaises(TypeError, is_even, None)
        self.assertRaises(TypeError, is_even, object)


class Test_is_odd(unittest2.TestCase):
    def test_parity(self):
        self.assertTrue(is_odd(1l))
        self.assertFalse(is_odd(2L))
        self.assertTrue(is_odd(-1l))
        self.assertFalse(is_odd(-2L))

        self.assertFalse(is_odd(0))

    def test_boolean(self):
        # Python 2.x legacy. Ew.
        self.assertFalse(is_odd(False))
        self.assertTrue(is_odd(True))

    def test_TypeError_when_invalid_type(self):
        self.assertRaises(TypeError, is_odd, 2.0)
        self.assertRaises(TypeError, is_odd, None)
        self.assertRaises(TypeError, is_odd, object)


class Test_is_positive(unittest2.TestCase):
    def test_positive(self):
        self.assertTrue(is_positive(4))
        self.assertFalse(is_positive(-1))
        self.assertFalse(is_positive(0))

    def test_floats(self):
        self.assertTrue(is_positive(4.2))
        self.assertFalse(is_positive(0.0))
        self.assertFalse(is_positive(-1.4))

    def test_boolean(self):
        self.assertTrue(is_positive(True))
        self.assertFalse(is_positive(False))

    def test_wtf(self):
        self.assertRaises(TypeError, is_positive, None)
        self.assertRaises(TypeError, is_positive, "")
        self.assertRaises(TypeError, is_positive, {})
        self.assertRaises(TypeError, is_positive, object)


class Test_is_negative(unittest2.TestCase):
    def test_negative(self):
        self.assertFalse(is_negative(4))
        self.assertTrue(is_negative(-1))
        self.assertFalse(is_negative(0))

    def test_floats(self):
        self.assertFalse(is_negative(4.2))
        self.assertFalse(is_negative(0.0))
        self.assertTrue(is_negative(-1.4))

    def test_boolean(self):
        self.assertFalse(is_negative(True))
        self.assertFalse(is_negative(False))

    def test_wtf(self):
        self.assertRaises(TypeError, is_negative, None)
        self.assertRaises(TypeError, is_negative, "")
        self.assertRaises(TypeError, is_negative, {})
        self.assertRaises(TypeError, is_negative, object)


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
        self.assertEqual(list(ireject(None, [0, "", 1, None, 2])), [0, "", None])


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
        self.assertDictEqual(select_dict(None, dict(a="a", b="b", c=None)), dict(a="a", b="b"))
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
        self.assertDictEqual(reject_dict(None, dict(a="a", b="b", c=None)), dict(c=None))
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
        self.assertEqual(pluck(fruits, "name"), ["mango", "orange", "banana"])

    def test_TypeError_when_not_iterable_of_dicts(self):
        self.assertRaises(TypeError, pluck, ["foo", "blah"])

    def test_KeyError_when_missing_key(self):
        self.assertRaises(KeyError, pluck, [dict(a="something"), dict(b="something")], "a")


class Test_chunks(unittest2.TestCase):
    def test_valid_grouping(self):
        self.assertEqual(list(chunks(4, "aaaabbbbccccdddd")),
                         ["aaaa", "bbbb", "cccc", "dddd"])
        self.assertEqual(list(chunks(3, [1, 1, 1, 2, 2, 2, 3, 3, 3])),
                         [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

    def test_returns_generator_object(self):
        self.assertEqual(type(chunks(4, "aaaabbbb")).__name__, "generator")

    def test_odd_ball_grouping(self):
        self.assertEqual(list(chunks(3, "aaabb")), ["aaa", "bb"])


class Test_each(unittest2.TestCase):
    def test_each(self):
        count = [0]
        def _sum(x):
            count[0] += x
        each(_sum, [1, 2, 3])
        self.assertEqual(count, [6])

    def test_TypeError_when_not_callable(self):
        self.assertRaises(TypeError, each, None, range(5))


if __name__ == '__main__':
  unittest2.main()
