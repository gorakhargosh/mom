#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.functional import \
    leading, some, trailing, every, find, none, is_even, is_odd, is_positive, is_negative, select, reject, ireject, iselect


class Test_some(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(some((lambda w: w > 0), [0, -1, 4, 6]))

        self.assertFalse(some((lambda w: w > 0), [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, some, (lambda w: w > 0), None)
        self.assertRaises(TypeError, some, (lambda w: w > 0), 5)
        self.assertRaises(TypeError, some, (lambda w: w > 0), True)

class Test_every(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(every((lambda w: w > 0), [1, 1, 4, 6]))
        self.assertFalse(every((lambda w: w > 0), [0, -1, 4, 6]))
        self.assertFalse(every((lambda w: w > 0), [0, -1, -4, 0]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, every, (lambda w: w > 0), None)
        self.assertRaises(TypeError, every, (lambda w: w > 0), 5)
        self.assertRaises(TypeError, every, (lambda w: w > 0), True)


class Test_none(unittest2.TestCase):
    def test_valid(self):
        self.assertTrue(none((lambda w: w < 1), [1, 1, 4, 6]))
        self.assertFalse(none((lambda w: w > 0), [0, -1, 4, 6]))

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, none, (lambda w: w > 0), None)
        self.assertRaises(TypeError, none, (lambda w: w > 0), 5)
        self.assertRaises(TypeError, none, (lambda w: w > 0), True)


class Test_find(unittest2.TestCase):
    def test_valid_index(self):
        self.assertEqual(find((lambda w: w > 2), [0, 1, 2, 3, 4, 5]), 3)

    def test_not_found(self):
        self.assertEqual(find((lambda w: w > 50), range(5)), -1)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, find, (lambda w: w > 2), None)
        self.assertRaises(TypeError, find, (lambda w: w > 2), 5)
        self.assertRaises(TypeError, find, (lambda w: w > 2), True)


class Test_leading(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(leading((lambda w: w > 0), [0, 0, 1]), 0)
        self.assertEqual(leading((lambda w: w > 1), [2, 2, 3, 0, 5]), 3)
        self.assertEqual(leading((lambda w: ord(w) >= ord('c')), "abalskjd"), 0)
        self.assertEqual(leading((lambda w: ord(w) >= ord('c')), "cuddleya"), 7)

    def test_full_count(self):
        self.assertEqual(leading((lambda w: w > 0), range(1, 10)), 9)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, leading, (lambda w: w > 0), None)
        self.assertRaises(TypeError, leading, (lambda w: w > 0), 3)
        self.assertRaises(TypeError, leading, (lambda w: w > 0), True)

class Test_trailing(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(trailing((lambda w: w > 0), [0, 0, 1]), 1)
        self.assertEqual(trailing((lambda w: w > 1), [2, 0, 2, 3, 5]), 3)
        self.assertEqual(trailing((lambda w: ord(w) >= ord('c')), "abalskjd"), 5)
        self.assertEqual(trailing((lambda w: ord(w) >= ord('c')), "cuddleya"), 0)

    def test_full_count(self):
        self.assertEqual(trailing((lambda w: w > 0), range(1, 10)), 9)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, trailing, (lambda w: w > 0), None)
        self.assertRaises(TypeError, trailing, (lambda w: w > 0), 3)
        self.assertRaises(TypeError, trailing, (lambda w: w > 0), True)


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


if __name__ == '__main__':
  unittest2.main()
