#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.itertools import group


class Test_group(unittest2.TestCase):
    def test_valid_grouping(self):
        self.assertEqual(list(group("aaaabbbbccccdddd", 4)),
                         ["aaaa", "bbbb", "cccc", "dddd"])
        self.assertEqual(list(group([1, 1, 1, 2, 2, 2, 3, 3, 3], 3)),
                         [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

    def test_returns_generator_object(self):
        self.assertTrue("generator" in repr(type(group("aaaabbbb", 4))))

    def test_odd_ball_grouping(self):
        self.assertEqual(list(group("aaabb", 3)), ["aaa", "bb"])
