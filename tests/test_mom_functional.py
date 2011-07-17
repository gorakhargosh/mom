#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.functional import \
    leading, some, trailing, every, find, none, even, odd, positive, negative


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


class Test_even(unittest2.TestCase):
    def test_parity(self):
        self.assertTrue(even(2l))
        self.assertFalse(even(1L))
        self.assertTrue(even(-2l))
        self.assertFalse(even(-1L))

        self.assertTrue(even(0))

    def test_boolean(self):
        # Python 2.x legacy. Ew.
        self.assertFalse(even(True))
        self.assertTrue(even(False))

    def test_TypeError_when_invalid_type(self):
        self.assertRaises(TypeError, even, 2.0)
        self.assertRaises(TypeError, even, None)
        self.assertRaises(TypeError, even, object)


class Test_odd(unittest2.TestCase):
    def test_parity(self):
        self.assertTrue(odd(1l))
        self.assertFalse(odd(2L))
        self.assertTrue(odd(-1l))
        self.assertFalse(odd(-2L))

        self.assertFalse(odd(0))

    def test_boolean(self):
        # Python 2.x legacy. Ew.
        self.assertFalse(odd(False))
        self.assertTrue(odd(True))

    def test_TypeError_when_invalid_type(self):
        self.assertRaises(TypeError, odd, 2.0)
        self.assertRaises(TypeError, odd, None)
        self.assertRaises(TypeError, odd, object)


class Test_positive(unittest2.TestCase):
    def test_positive(self):
        self.assertTrue(positive(4))
        self.assertFalse(positive(-1))
        self.assertFalse(positive(0))

    def test_floats(self):
        self.assertTrue(positive(4.2))
        self.assertFalse(positive(0.0))
        self.assertFalse(positive(-1.4))

    def test_boolean(self):
        self.assertTrue(positive(True))
        self.assertFalse(positive(False))

    def test_wtf(self):
        self.assertRaises(TypeError, positive, None)
        self.assertRaises(TypeError, positive, "")
        self.assertRaises(TypeError, positive, {})
        self.assertRaises(TypeError, positive, object)


class Test_negative(unittest2.TestCase):
    def test_negative(self):
        self.assertFalse(negative(4))
        self.assertTrue(negative(-1))
        self.assertFalse(negative(0))

    def test_floats(self):
        self.assertFalse(negative(4.2))
        self.assertFalse(negative(0.0))
        self.assertTrue(negative(-1.4))

    def test_boolean(self):
        self.assertFalse(negative(True))
        self.assertFalse(negative(False))

    def test_wtf(self):
        self.assertRaises(TypeError, negative, None)
        self.assertRaises(TypeError, negative, "")
        self.assertRaises(TypeError, negative, {})
        self.assertRaises(TypeError, negative, object)


if __name__ == '__main__':
  unittest2.main()
