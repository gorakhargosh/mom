#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.itertools import chunks


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
