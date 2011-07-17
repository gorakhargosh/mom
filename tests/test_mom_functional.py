#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.functional import \
    leading, some, trailing, _trailing, every, find


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

class Test__trailing(unittest2.TestCase):
    def test_count(self):
        self.assertEqual(_trailing((lambda w: w > 0), [0, 0, 1]), 1)
        self.assertEqual(_trailing((lambda w: w > 1), [2, 0, 2, 3, 5]), 3)
        self.assertEqual(_trailing((lambda w: ord(w) >= ord('c')), "abalskjd"), 5)
        self.assertEqual(_trailing((lambda w: ord(w) >= ord('c')), "cuddleya"), 0)

    def test_TypeError_when_not_iterable(self):
        self.assertRaises(TypeError, _trailing, (lambda w: w > 0), None)
        self.assertRaises(TypeError, _trailing, (lambda w: w > 0), 3)
        self.assertRaises(TypeError, _trailing, (lambda w: w > 0), True)

    def test_full_count(self):
        self.assertEqual(_trailing((lambda w: w > 0), range(1, 10)), 9)

if __name__ == '__main__':
  unittest2.main()
