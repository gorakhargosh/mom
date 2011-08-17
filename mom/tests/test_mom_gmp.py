#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Noah Watkins <noah@noahdesu.com>
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# MIT License
# -----------
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


from __future__ import absolute_import

import unittest2
from mom import gmp

#TODO inplace long += gmp
class Test_integer_init(unittest2.TestCase):
    def setUp(self):
        self.large_gmp = gmp.Integer(4294967300L)
        self.large_neg_gmp = gmp.Integer(-4294967300L)
        self.inst = gmp.Integer(10L)

    def test_SetPyLong(self):
        self.inst.set(5000000000L)
        self.assertEqual(self.inst, gmp.Integer(5000000000L))

    def test_SetGmpInt(self):
        self.inst.set(self.large_gmp)
        self.assertEqual(self.inst, self.large_gmp)

    def test_SetNegative(self):
        self.inst.set(-5000000000L)
        self.assertEqual(self.inst, gmp.Integer(-5000000000L))
        self.inst.set(self.large_neg_gmp)
        self.assertEqual(self.inst, self.large_neg_gmp)


class Test_IntegerAddition(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(199L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.small_neg_gmp = gmp.Integer(-199L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_SimpleAddition(self):
        self.assertEqual(self.small_gmp + self.small_gmp,
                         gmp.Integer(199L + 199L))

    def test_LargeAddition(self):
        self.assertEqual(self.large_gmp + self.large_gmp,
                         gmp.Integer(5000000000L + 5000000000L))
        self.assertEqual(self.large_gmp + self.large_gmp + self.large_gmp,
                         gmp.Integer(5000000000L * 3))

    def test_PyLongAddition(self):
        self.assertEqual(self.small_gmp + 150L, gmp.Integer(199L + 150L))
        self.assertEqual(self.large_gmp + 150L, gmp.Integer(5000000000L + 150L))

    def test_PyLongReverseAddition(self):
        self.assertEqual(150L + self.small_gmp, gmp.Integer(199L + 150L))
        self.assertEqual(150L + self.large_gmp, gmp.Integer(5000000000L + 150L))

    def test_AdditionWithNegatives(self):
        self.assertEqual(self.large_gmp + self.large_neg_gmp, gmp.Integer(0L))
        self.assertEqual(self.large_gmp + self.small_neg_gmp,
                         gmp.Integer(5000000000L + -199L))
        self.assertEqual(self.small_gmp + self.large_neg_gmp,
                         gmp.Integer(199L + -5000000000L))
        self.assertEqual(self.large_neg_gmp + self.large_neg_gmp,
                         gmp.Integer(-5000000000 + -5000000000L))
        self.assertEqual(self.large_gmp + -6000000000L,
                         gmp.Integer(5000000000 + -6000000000L))
        self.assertEqual(6000000000L + self.large_neg_gmp,
                         gmp.Integer(6000000000 + -5000000000L))

    def test_InPlaceAddition(self):
        #Test_ in-place addition
        i = self.small_gmp
        i += self.small_gmp
        self.assertEqual(i, gmp.Integer(199L + 199L))
        i += 5000000000L
        self.assertEqual(i, gmp.Integer(199L + 199L + 5000000000L))


class Test_IntegerSubtraction(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(199L)
        self.small_gmp2 = gmp.Integer(250L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(5000500500L)
        self.small_neg_gmp = gmp.Integer(-199L)
        self.small_neg_gmp2 = gmp.Integer(-250L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_SimpleSubtraction(self):
        self.assertEqual(self.small_gmp2 - self.small_gmp,
                         gmp.Integer(250L - 199L))
        self.assertEqual(self.small_gmp - self.small_gmp2,
                         gmp.Integer(199L - 250L))

    def test_LargeSubtraction(self):
        self.assertEqual(self.large_gmp2 - self.large_gmp,
                         gmp.Integer(5000500500L - 5000000000L))
        self.assertEqual(self.large_gmp - self.large_gmp2,
                         gmp.Integer(5000000000L - 5000500500L))
        self.assertEqual(self.large_gmp - self.large_gmp - self.large_gmp,
                         self.large_neg_gmp)
        self.assertEqual(
            self.large_neg_gmp - self.large_neg_gmp - self.large_neg_gmp,
            self.large_gmp)

    def test_PyLongSubtraction(self):
        self.assertEqual(self.small_gmp - 20L, gmp.Integer(199L - 20L))
        self.assertEqual(self.small_gmp - 5000000000L,
                         gmp.Integer(199L - 5000000000L))
        self.assertEqual(self.large_gmp - 20L, gmp.Integer(5000000000L - 20L))

    def test_PyLongReverseSubtraction(self):
        self.assertEqual(250L - self.small_gmp, gmp.Integer(250L - 199L))
        self.assertEqual(20L - self.small_gmp, gmp.Integer(20L - 199L))
        self.assertEqual(20L - self.large_gmp, gmp.Integer(20L - 5000000000L))

    def test_NegativeSubtraction(self):
        self.assertEqual(self.small_neg_gmp2 - self.small_gmp,
                         gmp.Integer(-250L - 199L))
        self.assertEqual(self.small_neg_gmp2 - self.small_neg_gmp,
                         gmp.Integer(-250L - -199L))
        self.assertEqual(self.small_gmp2 - self.small_neg_gmp,
                         gmp.Integer(250L - -199L))
        self.assertEqual(self.large_gmp - -500000L,
                         gmp.Integer(5000000000L - -500000L))
        self.assertEqual(-500000L - self.large_neg_gmp,
                         gmp.Integer(-500000L - -5000000000L))

    def test_InPlaceSubtraction(self):
        i = self.small_gmp
        i -= self.small_gmp
        self.assertEqual(i, gmp.Integer(0L))
        i -= 5000000000L
        self.assertEqual(i, gmp.Integer(-5000000000L))


class Test_IntegerMultiplication(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(199L)
        self.small_gmp2 = gmp.Integer(250L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(5000500500L)
        self.small_neg_gmp = gmp.Integer(-199L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_SimpleMultiplication(self):
        self.assertEqual(self.small_gmp * self.small_gmp,
                         gmp.Integer(199L * 199L))

    def test_LargeMultiplication(self):
        self.assertEqual(self.large_gmp * self.large_gmp,
                         gmp.Integer(5000000000L * 5000000000L))
        self.assertEqual(self.large_gmp * self.large_gmp * self.large_gmp,
                         gmp.Integer(5000000000L * 5000000000L * 5000000000L))

    def test_PyLongMultiplication(self):
        self.assertEqual(self.small_gmp * 150L, gmp.Integer(199L * 150L))
        self.assertEqual(self.large_gmp * 150L, gmp.Integer(5000000000L * 150L))

    def test_PyLongReverseMultiplication(self):
        self.assertEqual(150L * self.small_gmp, gmp.Integer(199L * 150L))
        self.assertEqual(150L * self.large_gmp, gmp.Integer(5000000000L * 150L))

    def test_NegativeMultiplication(self):
        self.assertEqual(self.large_gmp * self.large_neg_gmp,
                         gmp.Integer(5000000000L * -5000000000L))
        self.assertEqual(self.large_gmp * -5000000000L,
                         gmp.Integer(5000000000L * -5000000000L))

    def test_InPlaceMultiplication(self):
        i = self.small_gmp
        i *= self.small_gmp
        self.assertEqual(i, gmp.Integer(199L * 199L))
        i *= 5000000000L
        self.assertEqual(i, 199L * 199L * 5000000000L)


class Test_IntegerDivision(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(19L)
        self.small_gmp2 = gmp.Integer(250L)
        self.small_gmp3 = gmp.Integer(50L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(5000500500L)
        self.small_neg_gmp = gmp.Integer(-19L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_SimpleDivision(self):
        self.assertEqual(self.small_gmp2 / self.small_gmp,
                         gmp.Integer(250L / 19L))
        self.assertEqual(self.small_gmp2 / self.small_gmp3,
                         gmp.Integer(250L / 50L))
        self.assertEqual(self.small_gmp / self.small_gmp2,
                         gmp.Integer(19L / 250L))

    def test_LargeDivision(self):
        self.assertEqual(self.large_gmp2 / self.large_gmp,
                         gmp.Integer(5000500500L / 5000000000L))
        self.assertEqual(self.large_gmp / self.small_gmp,
                         gmp.Integer(5000000000L / 19L))
        self.assertEqual(self.large_gmp / self.small_gmp / self.small_gmp,
                         gmp.Integer(5000000000L / 19L / 19L))

    def test_PyLongDivision(self):
        self.assertEqual(self.small_gmp2 / 50L, gmp.Integer(250L / 50L))
        self.assertEqual(self.large_gmp / 50L, gmp.Integer(5000000000L / 50L))

    def test_PyLongReverseDivision(self):
        self.assertEqual(5000000000L / self.small_gmp3,
                         gmp.Integer(5000000000L / 50L))
        self.assertEqual(5000500500L / self.large_gmp,
                         gmp.Integer(5000500500L / 5000000000L))

    def test_NegativeDivision(self):
        self.assertEqual(self.large_gmp / self.small_neg_gmp,
                         gmp.Integer(5000000000L / -19L))
        self.assertEqual(self.large_neg_gmp / self.small_neg_gmp,
                         gmp.Integer(-5000000000L / -19L))
        self.assertEqual(self.large_neg_gmp / self.small_gmp,
                         gmp.Integer(-5000000000L / 19L))
        self.assertEqual(self.large_neg_gmp / 50L,
                         gmp.Integer(-5000000000L / 50L))
        self.assertEqual(self.large_gmp / -50L, gmp.Integer(5000000000L / -50L))

    def test_InPlaceDivision(self):
        i = self.large_gmp
        i /= self.small_gmp
        self.assertEqual(i, gmp.Integer(5000000000L / 19L))
        i /= 19L
        self.assertEqual(i, gmp.Integer(5000000000L / 19L / 19L))


class Test_IntegerMod(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(19L)
        self.small_gmp2 = gmp.Integer(250L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(5000500500L)
        self.small_neg_gmp = gmp.Integer(-19L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_SimpleMod(self):
        self.assertEqual(self.small_gmp2 % self.small_gmp,
                         gmp.Integer(250L % 19L))
        self.assertEqual(self.small_gmp % self.small_gmp2,
                         gmp.Integer(19L % 250L))

    def test_LargeMod(self):
        self.assertEqual(self.large_gmp % self.small_gmp2,
                         gmp.Integer(5000000000L % 250L))
        self.assertEqual(self.large_gmp2 % self.large_gmp,
                         gmp.Integer(5000500500L % 5000000000L))
        self.assertEqual(self.large_gmp % self.small_gmp2 % self.small_gmp,
                         gmp.Integer(5000000000L % 250L % 19L))

    def test_PyLongMod(self):
        self.assertEqual(self.small_gmp2 % 19L, gmp.Integer(250L % 19L))
        self.assertEqual(self.large_gmp % 19L, gmp.Integer(5000000000L % 19L))

    def test_PyLongReverseMod(self):
        self.assertEqual(250L % self.small_gmp, gmp.Integer(250L % 19L))
        self.assertEqual(5000500500L % self.large_gmp,
                         gmp.Integer(5000500500L % 5000000000L))

    def test_NegativeMod(self):
        self.assertEqual(self.large_gmp % self.small_neg_gmp,
                         gmp.Integer(5000000000L % 19L))
        self.assertEqual(self.large_neg_gmp % self.small_neg_gmp,
                         gmp.Integer(-5000000000L % -19L))
        self.assertEqual(self.large_neg_gmp % self.small_gmp,
                         gmp.Integer(-5000000000L % 19L))
        self.assertEqual(self.large_gmp % self.small_neg_py,
                         gmp.Integer(5000000000L % -19L))

    def test_InPlaceMod(self):
        i = self.large_gmp
        i %= self.small_gmp
        self.assertEqual(i, gmp.Integer(5000000000L % 19L))
        i %= 4L
        self.assertEqual(i, gmp.Integer(5000000000L % 19L % 4L))


class Test_IntegerStringFormat(unittest2.TestCase):
    def setUp(self):
        self.large_gmp = gmp.Integer(5123456789L)
        self.large_neg_gmp = gmp.Integer(-5123456789L)

    def test_StringFormat(self):
        self.assertEqual(str(self.large_gmp), "5123456789")
        self.assertEqual(repr(self.large_gmp), "5123456789")
        #TODO error stirng

    def test_NegativeStringFormat(self):
        self.assertEqual(str(self.large_neg_gmp), "-5123456789")
        self.assertEqual(repr(self.large_neg_gmp), "-5123456789")

    def test_StringParsing(self):
        self.assertEqual(gmp.Integer(str(5123456789L)), self.large_gmp)
        self.assertEqual(gmp.Integer(str(-5123456789L)), self.large_neg_gmp)


class Test_IntegerComparison(unittest2.TestCase):
    def setUp(self):
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(50000000001L)

    def test_LessThan(self):
        self.assertTrue(self.large_gmp < self.large_gmp2)
        self.assertFalse(self.large_gmp < self.large_gmp)
        self.assertFalse(self.large_gmp2 < self.large_gmp)

    def test_LessThanPyLong(self):
        self.assertTrue(self.large_gmp < 5000000001L)
        self.assertFalse(self.large_gmp < 5000000000L)
        self.assertFalse(self.large_gmp2 < 5000000000L)

    def test_PyLongLessThan(self):
        self.assertTrue(5000000000L < self.large_gmp2)
        self.assertFalse(5000000000L < self.large_gmp)
        self.assertFalse(5000000001L < self.large_gmp)

    def test_LessThanEqual(self):
        self.assertTrue(self.large_gmp <= self.large_gmp2)
        self.assertTrue(self.large_gmp <= self.large_gmp)
        self.assertFalse(self.large_gmp2 <= self.large_gmp)

    def test_LessThanEqualPyLong(self):
        self.assertTrue(self.large_gmp <= 5000000001L)
        self.assertTrue(self.large_gmp <= 5000000000L)
        self.assertFalse(self.large_gmp2 <= 5000000000L)

    def test_PyLongLessThanEqual(self):
        self.assertTrue(5000000000L <= self.large_gmp2)
        self.assertTrue(5000000000L <= self.large_gmp)
        self.assertFalse(5000000001L <= self.large_gmp)

    def test_GreaterThan(self):
        self.assertFalse(self.large_gmp > self.large_gmp2)
        self.assertFalse(self.large_gmp > self.large_gmp)
        self.assertTrue(self.large_gmp2 > self.large_gmp)

    def test_GreaterThanPyLong(self):
        self.assertFalse(self.large_gmp > 5000000001L)
        self.assertFalse(self.large_gmp > 5000000000L)
        self.assertTrue(self.large_gmp2 > 5000000000L)

    def test_PyLongGreaterThan(self):
        self.assertFalse(5000000000L > self.large_gmp2)
        self.assertFalse(5000000000L > self.large_gmp)
        self.assertTrue(5000000001L > self.large_gmp)

    def test_GreaterThanEqual(self):
        self.assertFalse(self.large_gmp >= self.large_gmp2)
        self.assertTrue(self.large_gmp >= self.large_gmp)
        self.assertTrue(self.large_gmp2 >= self.large_gmp)

    def test_GreaterThanEqualPyLong(self):
        self.assertFalse(self.large_gmp >= 5000000001L)
        self.assertTrue(self.large_gmp >= 5000000000L)
        self.assertTrue(self.large_gmp2 >= 5000000000L)

    def test_PyLongGreaterThanEqual(self):
        self.assertFalse(5000000000L >= self.large_gmp2)
        self.assertTrue(5000000000L >= self.large_gmp)
        self.assertTrue(5000000001L >= self.large_gmp)

    def test_Equals(self):
        self.assertFalse(self.large_gmp == self.large_gmp2)
        self.assertTrue(self.large_gmp == self.large_gmp)
        self.assertFalse(self.large_gmp2 == self.large_gmp)

    def test_EqualsPyLong(self):
        self.assertFalse(self.large_gmp == 5000000001L)
        self.assertTrue(self.large_gmp == 5000000000L)
        self.assertFalse(self.large_gmp2 == 5000000000L)

    def test_PyLongEquals(self):
        self.assertFalse(5000000000L == self.large_gmp2)
        self.assertTrue(5000000000L == self.large_gmp)
        self.assertFalse(5000000001L == self.large_gmp)

    def test_NotEquals(self):
        self.assertTrue(self.large_gmp != self.large_gmp2)
        self.assertFalse(self.large_gmp != self.large_gmp)
        self.assertTrue(self.large_gmp2 != self.large_gmp)

    def test_NotEqualsPyLong(self):
        self.assertTrue(self.large_gmp != 5000000001L)
        self.assertFalse(self.large_gmp != 5000000000L)
        self.assertTrue(self.large_gmp2 != 5000000000L)

    def test_PyLongNotEquals(self):
        self.assertTrue(5000000000L != self.large_gmp2)
        self.assertFalse(5000000000L != self.large_gmp)
        self.assertTrue(5000000001L != self.large_gmp)


class Test_IntegerBitOps(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(19L)
        self.small_gmp2 = gmp.Integer(250L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(5000500500L)
        self.small_neg_gmp = gmp.Integer(-19L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_And(self):
        self.assertEqual(self.large_gmp & self.large_gmp, self.large_gmp)
        self.assertEqual(self.large_gmp & self.small_gmp,
                         gmp.Integer(5000000000L & 19L))
        self.assertEqual(self.large_gmp & 250L, gmp.Integer(5000000000L & 250L))
        self.assertEqual(self.large_neg_gmp & self.small_neg_gmp,
                         gmp.Integer(-5000000000L & -19L))

    def test_InPlaceAnd(self):
        i = self.large_gmp
        i &= self.small_gmp
        self.assertEqual(i, 5000000000L & 19L)
        i &= 250L
        self.assertEqual(i, 5000000000L & 19L & 250L)

    def test_Or(self):
        self.assertEqual(self.large_gmp | gmp.Integer(0L), self.large_gmp)
        self.assertEqual(gmp.Integer(0L) | self.large_gmp, self.large_gmp)
        self.assertEqual(self.large_gmp | self.small_gmp,
                         gmp.Integer(5000000000L | 19L))
        self.assertEqual(self.large_gmp | 250L, gmp.Integer(5000000000L | 250L))
        self.assertEqual(self.large_neg_gmp | self.small_neg_gmp,
                         gmp.Integer(-5000000000L | -19L))

    def test_InPlaceOr(self):
        i = self.large_gmp
        i |= self.small_gmp
        self.assertEqual(i, gmp.Integer(5000000000L | 19L))
        i |= 250L
        self.assertEqual(i, gmp.Integer(5000000000L | 19L | 250L))

    def test_Xor(self):
        self.assertEqual(self.large_gmp ^ self.large_gmp, gmp.Integer(0L))
        self.assertEqual(self.large_gmp ^ gmp.Integer(0), self.large_gmp)
        self.assertEqual(gmp.Integer(0) ^ self.large_gmp, self.large_gmp)
        self.assertEqual(self.large_gmp ^ self.small_gmp,
                         gmp.Integer(5000000000L ^ 19L))
        self.assertEqual(self.large_gmp ^ 250L, gmp.Integer(5000000000L ^ 250L))
        self.assertEqual(self.large_neg_gmp ^ self.small_neg_gmp,
                         gmp.Integer(-5000000000L ^ -19L))

    def test_InPlaceXor(self):
        i = self.large_gmp
        i ^= self.small_gmp
        self.assertEqual(i, gmp.Integer(5000000000L ^ 19L))
        i ^= 250L
        self.assertEqual(i, gmp.Integer(5000000000L ^ 19L ^ 250L))


class Test_IntegerAdditionals(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Integer(19L)
        self.ssmall_gmp2 = gmp.Integer(250L)
        self.large_gmp = gmp.Integer(5000000000L)
        self.large_gmp2 = gmp.Integer(5000500500L)
        self.small_neg_gmp = gmp.Integer(-19L)
        self.large_neg_gmp = gmp.Integer(-5000000000L)

    def test_Negation(self):
        self.assertEqual(-self.large_gmp, self.large_neg_gmp);
        self.assertEqual(-self.large_neg_gmp, self.large_gmp);
        self.assertEqual(-gmp.Integer(0L), gmp.Integer(0L));

    def test_Absolute(self):
        self.assertEqual(abs(self.large_gmp), self.large_gmp);
        self.assertEqual(abs(self.large_neg_gmp), self.large_gmp);
        self.assertEqual(abs(gmp.Integer(0L)), gmp.Integer(0L));


class Test_IntegerErrorCases(unittest2.TestCase):
    def test_DivisionBy0(self):
        #TODO Removed for now - crashes in c
        i = gmp.Integer(1L)
        self.assertTrue(0)
        #self.assertRaises(ValueError, gmp.Integer(1L) / gmp.Integer(0L))
        #self.assertRaises(ValueError, i /= gmp.Integer(0L))

    def test_ModBy0(self):
        #TODO Removed for now - crashes in c
        i = gmp.Integer(1L)
        self.assertTrue(0)
        #self.assertRaises(ValueError, gmp.Integer(1L) % gmp.Integer(0L))
        #self.assertRaises(ValueError, i %= gmp.Integer(0L))


class Test_IntegerPyTypeCompatibility(unittest2.TestCase):
    def test_IntCompatibility(self):
        print "TODO: Test_s for interation with python ints"

    def test_BoolCompatibility(self):
        print "TODO: Test_s for interation with python Booleans"

    def test_FloatCompatibility(self):
        print "TODO: Test_s for interation with python floats"

    def test_ComplexCompatibility(self):
        print "TODO: Test_s for interation with python complex"

        #TODO iteration with range


class Test_FloatInit(unittest2.TestCase):

#TODO compare with epsilon

    def setUp(self):
        self.inst = gmp.Float(10.0)
        self.large_gmp = gmp.Float(5000000000.0000000005)
        self.large_neg_gmp = gmp.Float(-5000000000.0000000005)

    def test_Set(self):
        self.inst.set(self.large_gmp)
        self.assertEqual(self.inst, gmp.Float(5000000000.0000000005))

    def test_SetPyFloat(self):
        self.inst.set(101.101)
        self.assertEqual(self.inst, gmp.Float(101.101))

    def test_SetNegative(self):
        self.inst.set(-101.101)
        self.assertEqual(self.inst, gmp.Float(-101.101))
        self.inst.set(self.large_neg_gmp)
        self.assertEqual(self.inst, gmp.Float(-5000000000.0000000005))


class Test_FloatStringFormatting(unittest2.TestCase):
    def test_StringParsing(self):
        self.assertEqual(gmp.Float("1.1"), gmp.Float(1.1))
        self.assertEqual(gmp.Float(".1"), gmp.Float(0.1))
        self.assertEqual(gmp.Float("1"), gmp.Float(1.0))
        self.assertEqual(gmp.Float(str(1010101.10101)),
                         gmp.Float(1010101.10101))

    def test_StringNegativeParsing(self):
        self.assertEqual(gmp.Float("-1.1"), gmp.Float(-1.1))
        self.assertEqual(gmp.Float("-.1"), gmp.Float(-0.1))
        self.assertEqual(gmp.Float("-1"), gmp.Float(-1.0))
        self.assertEqual(gmp.Float(str(-1010101.10101)),
                         gmp.Float(-1010101.10101))

    def test_StringFormatting(self):
        self.assertEqual(str(gmp.Float(1.1)), str(1.1))
        self.assertEqual(str(gmp.Float("5000000000.0000000005")),
                         "5000000000.0000000005")
        self.assertEqual(repr(gmp.Float(1.1)), str(1.1))
        self.assertEqual(repr(gmp.Float("5000000000.0000000005")),
                         "5000000000.0000000005")

    def test_StringNegativeFormatting(self):
        self.assertEqual(str(gmp.Float(-1.1)), str(-1.1))
        self.assertEqual(str(gmp.Float("-5000000000.0000000005")),
                         "-5000000000.0000000005")
        self.assertEqual(repr(gmp.Float(-1.1)), str(-1.1))
        self.assertEqual(repr(gmp.Float("-5000000000.0000000005")),
                         "-5000000000.0000000005")
        #TODO errors


class Test_FloatAddition(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Float(10.1)
        self.small_gmp2 = gmp.Float(12.2)
        self.large_gmp = gmp.Float("4294967300.10")
        self.small_neg_gmp = gmp.Float(-10.1)
        self.large_neg_gmp = gmp.Float("-4294967300.10")
        self.prec_gmp = gmp.Float("10.4294967300101010")

    def test_SimpleAddition(self):
        self.assertEqual(self.small_gmp + self.small_gmp2, gmp.Float(22.3))

    def test_LargeAddition(self):
        self.assertEqual(self.large_gmp + self.large_gmp,
                         gmp.Float("8589934600.20"))
        self.assertEqual(self.large_gmp + self.large_gmp + self.large_gmp,
                         gmp.Float("12884901900.30"))

    def test_PreciseAddition(self):
        self.assertEqual(self.prec_gmp + self.prec_gmp,
                         gmp.Float("20.8589934600202020"))
        self.assertEqual(self.prec_gmp + self.small_gmp,
                         gmp.Float("20.5294967300101010"))

    def test_PyFloatAddition(self):
        self.assertEqual(self.small_gmp + 10.1, gmp.Float(20.2))
        self.assertEqual(self.large_gmp + 10.1, gmp.Float(4294967310.2))
        self.assertEqual(self.prec_gmp + 10.1, gmp.Float("20.5294967300101010"))

    def test_PyFloatReverseAddition(self):
        self.assertEqual(10.1 + self.small_gmp, gmp.Float(20.2))
        self.assertEqual(10.1 + self.large_gmp, gmp.Float(4294967310.2))
        self.assertEqual(10.1 + self.prec_gmp, gmp.Float("20.5294967300101010"))

    def test_NegativeAddition(self):
        self.assertEqual(self.large_gmp + self.large_neg_gmp, gmp.Float(0.0))
        self.assertEqual(self.large_neg_gmp + self.large_gmp, gmp.Float(0.0))
        self.assertEqual(self.small_gmp + self.large_neg_gmp,
                         gmp.Float("-4294967290.0"))
        self.assertEqual(self.large_gmp + self.small_neg_gmp,
                         gmp.Float("4294967290.0"))
        self.assertEqual(self.small_gmp + -10.1, gmp.Float(0.0))
        self.assertEqual(self.small_gmp + -11.2, gmp.Float(-1.1))
        self.assertEqual(10.1 + self.small_neg_gmp, gmp.Float(0.0))
        self.assertEqual(11.2 + self.small_neg_gmp, gmp.Float(1.1))

    def test_InPlaceAddition(self):
        i = gmp.Float(10.1)
        i += gmp.Float("4294967300.10")
        self.assertEqual(i, gmp.Float("4294967310.20"))
        i += 10.1
        self.assertEqual(i, gmp.Float("4294967320.30"))
        i += self.prec_gmp
        self.assertEqual(i, gmp.Float("4294967330.729496730010101"))


class Test_FloatSubtraction(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Float(10.1)
        self.small_gmp2 = gmp.Float(12.2)
        self.large_gmp = gmp.Float("4294967300.10")
        self.small_neg_gmp = gmp.Float(-10.1)
        self.large_neg_gmp = gmp.Float("-4294967300.10")
        self.prec_gmp = gmp.Float("10.429496730010")

    def test_SimpleSubtraction(self):
        self.assertEqual(self.small_gmp2 - self.small_gmp, gmp.Float(2.1))
        self.assertEqual(self.small_gmp - self.small_gmp2, gmp.Float(-2.1))

    def test_LargeSubtraction(self):
        self.assertEqual(self.large_gmp - self.small_gmp,
                         gmp.Float("4294967290"))
        self.assertEqual(self.large_gmp - self.small_gmp - self.small_gmp,
                         gmp.Float("4294967279.9"))
        self.assertEqual(self.small_gmp - self.large_gmp,
                         gmp.Float("-4294967290"))

    def test_PreciseSubtraction(self):
        self.assertEqual(self.prec_gmp - self.prec_gmp, gmp.Float(0))
        self.assertEqual(self.prec_gmp - self.small_gmp,
                         gmp.Float("0.329496730010"))

    def test_PyFloatSubtraction(self):
        self.assertEqual(self.small_gmp2 - 10.1, gmp.Float(2.1))
        self.assertEqual(self.small_gmp - 12.2, gmp.Float(-2.1))
        self.assertEqual(self.large_gmp - 10.1, gmp.Float("4294967290"))
        self.assertEqual(self.prec_gmp - 10.1, gmp.Float("0.329496730010"))

    def test_PyFloatReverseSubtraction(self):
        self.assertEqual(12.2 - self.small_gmp, gmp.Float(2.1))
        self.assertEqual(10.1 - self.small_gmp2, gmp.Float(-2.1))
        self.assertEqual(10.1 - self.large_gmp, gmp.Float("-4294967290"))
        self.assertEqual(10.1 - self.prec_gmp, gmp.Float("-0.329496730010"))

    def test_NegativeSubtraction(self):
        self.assertEqual(self.small_neg_gmp - self.large_neg_gmp,
                         gmp.Float("4294967290"))
        self.assertEqual(self.large_neg_gmp - self.small_neg_gmp,
                         gmp.Float("-4294967290"))
        self.assertEqual(self.large_gmp - self.large_neg_gmp,
                         gmp.Float("8589934600.2"))
        self.assertEqual(self.large_gmp - self.small_neg_gmp,
                         gmp.Float("4294967310.2"))
        self.assertEqual(self.small_gmp - self.large_neg_gmp,
                         gmp.Float("-4294967310.2"))
        self.assertEqual(self.small_gmp - -10.1, gmp.Float(20.2))

    def test_InPlaceSubtraction(self):
        i = gmp.Float(10.1)
        i += gmp.Float("4294967300.10")
        self.assertEqual(i, gmp.Float("4294967310.20"))
        i += 10.1
        self.assertEqual(i, gmp.Float("4294967320.30"))


class Test_FloatMultiplication(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Float(10.1)
        self.small_gmp2 = gmp.Float(12.2)
        self.large_gmp = gmp.Float("4294967300.10")
        self.small_neg_gmp = gmp.Float(-10.1)
        self.large_neg_gmp = gmp.Float("-4294967300.10")
        self.prec_gmp = gmp.Float("10.4294967300101010")

    def test_SimpleMultiplication(self):
        self.assertEqual(self.small_gmp * self.small_gmp, gmp.Float(102.01))

    def test_LargeMultiplication(self):
        self.assertEqual(self.large_gmp * self.large_gmp,
                         gmp.Float("18446744108928283460.01"))
        self.assertEqual(self.large_gmp * self.large_gmp * self.large_gmp,
                         gmp.Float("79228162741159289916766636019.001"))

    def test_PreciseMultiplication(self):
        self.assertEqual(self.prec_gmp * self.small_gmp,
                         gmp.Float("105.3379169731020201"))
        self.assertEqual(self.prec_gmp * self.large_gmp,
                         gmp.Float("44794347411.8932621376983101"))
        self.assertEqual(self.prec_gmp * self.prec_gmp,
                         gmp.Float("108.774402041291389592939562030201"))

    def test_PyFloatMultiplication(self):
        self.assertEqual(self.small_gmp * 10.1, gmp.Float(102.01))
        self.assertEqual(self.large_gmp * 10.1, gmp.Float("43379169731.01"))
        self.assertEqual(self.prec_gmp * 10.1,
                         gmp.Float("105.3379169731020201"))

    def test_PyFloatReverseMultiplication(self):
        self.assertEqual(10.1 * self.small_gmp, gmp.Float(102.01))
        self.assertEqual(10.1 * self.large_gmp, gmp.Float("43379169731.01"))
        self.assertEqual(10.1 * self.prec_gmp,
                         gmp.Float("105.3379169731020201"))

    def test_NegativeMultiplication(self):
        self.assertEqual(self.large_gmp * self.large_neg_gmp,
                         gmp.Float("-18446744108928283460.01"))
        self.assertEqual(self.large_neg_gmp * self.large_gmp,
                         gmp.Float("-18446744108928283460.01"))
        self.assertEqual(self.large_gmp * -10.1, gmp.Float("-43379169731.01"))
        self.assertEqual(10.1 * self.large_neg_gmp,
                         gmp.Float("-43379169731.01"))

    def test_InPlaceMultiplication(self):
        i = self.small_gmp
        i *= self.small_gmp
        self.assertEqual(i, gmp.Float(102.01))
        i *= 10.1
        self.assertEqual(i, gmp.Float(1030.301))


class Test_FloatDivision(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Float(0.2)
        self.small_gmp2 = gmp.Float(122.2)
        self.large_gmp = gmp.Float("4294967300.10")
        self.small_neg_gmp = gmp.Float(-0.2)
        self.large_neg_gmp = gmp.Float("-4294967300.10")
        self.prec_gmp = gmp.Float("10.4294967300101010")

    def test_SimpleDivision(self):
        self.assertEqual(self.small_gmp2 / self.small_gmp,
                         gmp.Float(122.2 / 0.2))
        self.assertEqual(self.small_gmp / self.small_gmp2,
                         gmp.Float(10.1 / 122.2))

    def test_LargeDivision(self):
        self.assertEqual(self.large_gmp / self.small_gmp,
                         gmp.Float("21474836500.5"))
        self.assertEqual(self.large_gmp / self.large_gmp, gmp.Float("1"))

    def test_PreciseDivision(self):
        self.assertEqual(self.prec_gmp / self.small_gmp,
                         gmp.Float("52.147483650050505"))
        self.assertEqual(self.prec_gmp / self.prec_gmp, gmp.Float("1"))

    def test_PyFloatDivision(self):
        self.assertEqual(self.small_gmp2 / 0.2, gmp.Float(122.2 / 2))
        self.assertEqual(self.large_gmp / 0.2, gmp.Float("2147483650.05"))
        self.assertEqual(self.prec_gmp / 0.2, gmp.Float("52.147483650050505"))

    def test_PyFloatDivision(self):
        self.assertEqual(100.5 / self.small_gmp, gmp.Float(100.5 / 2.0))

    def test_NegativeDivision(self):
        self.assertEqual(self.large_gmp / self.small_neg_gmp,
                         gmp.Float("-21474836500.5"))
        self.assertEqual(self.large_neg_gmp / self.small_neg_gmp,
                         gmp.Float("21474836500.5"))
        self.assertEqual(self.large_neg_gmp / self.small_gmp,
                         gmp.Float("-21474836500.5"))
        self.assertEqual(self.prec_gmp / self.small_neg_gmp,
                         gmp.Float("-52.147483650050505"))
        self.assertEqual(self.large_gmp / 0.2, gmp.Float("-21474836500.5"))

    def test_InPlaceDivision(self):
        i = self.large_gmp
        i /= self.small_gmp
        self.assertEqual(i, gmp.Float("21474836500.5"))
        i /= 10.0
        self.assertEqual(i, gmp.Float("2147483650.05"))


class Test_FloatComparison(unittest2.TestCase):
    def setUp(self):
        self.large_gmp = gmp.Float("5000000.0000000005")
        self.large_gmp2 = gmp.Float("5000000.000000001")
        self.large_gmp3 = gmp.Float(5000000.1)


    def test_LessThan(self):
        self.assertTrue(self.large_gmp < self.large_gmp2)
        self.assertFalse(self.large_gmp < self.large_gmp)
        self.assertFalse(self.large_gmp2 < self.large_gmp)

    def test_LessThanPyFloat(self):
        self.assertTrue(self.large_gmp < 5000000.1)
        self.assertFalse(self.large_gmp < 5000000.0)
        self.assertFalse(self.large_gmp3 < 5000000.1)

    def test_PyFloatLessThan(self):
        self.assertTrue(5000000.0 < self.large_gmp)
        self.assertFalse(5000000.1 < self.large_gmp)
        self.assertFalse(5000000.1 < self.large_gmp3)

    def test_LessThanEqual(self):
        self.assertTrue(self.large_gmp <= self.large_gmp2)
        self.assertTrue(self.large_gmp <= self.large_gmp)
        self.assertFalse(self.large_gmp2 <= self.large_gmp)

    def test_LessThanEqualPyFloat(self):
        self.assertTrue(self.large_gmp <= 5000000.1)
        self.assertFalse(self.large_gmp <= 5000000.0)
        self.assertTrue(self.large_gmp3 < 5000000.1)

    def test_PyFloatLessThanEqual(self):
        self.assertTrue(5000000.0 <= self.large_gmp)
        self.assertFalse(5000000.1 <= self.large_gmp)
        self.assertTrue(5000000.1 <= self.large_gmp3)

    def test_GreaterThan(self):
        self.assertFalse(self.large_gmp > self.large_gmp2)
        self.assertFalse(self.large_gmp > self.large_gmp)
        self.assertTrue(self.large_gmp2 > self.large_gmp)

    def test_GreaterThanPyFloat(self):
        self.assertFalse(self.large_gmp > 5000000.1)
        self.assertTrue(self.large_gmp > 5000000.0)
        self.assertFalse(self.large_gmp3 > 5000000.1)

    def test_PyFloatGreaterThan(self):
        self.assertFalse(5000000.0 > self.large_gmp)
        self.assertTrue(5000000.1 > self.large_gmp)
        self.assertFalse(5000000.1 > self.large_gmp3)

    def test_GreaterThanEqual(self):
        self.assertFalse(self.large_gmp >= self.large_gmp2)
        self.assertTrue(self.large_gmp >= self.large_gmp)
        self.assertTrue(self.large_gmp2 >= self.large_gmp)

    def test_GreaterThanEqualPyFloat(self):
        self.assertFalse(self.large_gmp >= 5000000.1)
        self.assertTrue(self.large_gmp >= 5000000.0)
        self.assertTrue(self.large_gmp3 >= 5000000.1)

    def test_PyFloatGreaterThanEqual(self):
        self.assertFalse(5000000.0 >= self.large_gmp)
        self.assertTrue(5000000.1 >= self.large_gmp)
        self.assertTrue(5000000.1 >= self.large_gmp3)

    def test_Equals(self):
        self.assertFalse(self.large_gmp == self.large_gmp2)
        self.assertTrue(self.large_gmp == self.large_gmp)
        self.assertFalse(self.large_gmp2 == self.large_gmp)

    def test_EqualsPyFloat(self):
        self.assertFalse(self.large_gmp == 5000000.1)
        self.assertFalse(self.large_gmp == 5000000.0)
        self.assertTrue(self.large_gmp3 == 5000000.1)

    def test_PyFloatEquals(self):
        self.assertFalse(5000000.1 == self.large_gmp)
        self.assertTrue(5000000.1 == self.large_gmp3)
        self.assertFalse(5000000.0 == self.large_gmp)

    def test_NotEquals(self):
        self.assertTrue(self.large_gmp != self.large_gmp2)
        self.assertFalse(self.large_gmp != self.large_gmp)
        self.assertTrue(self.large_gmp2 != self.large_gmp)

    def test_NotEqualsPyFloat(self):
        self.assertTrue(self.large_gmp != 5000000.1)
        self.assertFalse(self.large_gmp3 != 5000000.1)
        self.assertTrue(self.large_gmp != 5000000.0)

    def test_PyFloatNotEquals(self):
        self.assertTrue(5000000.1 != self.large_gmp)
        self.assertFalse(5000000.1 != self.large_gmp3)
        self.assertTrue(5000000.0 != self.large_gmp)


class Test_FloatAdditionals(unittest2.TestCase):
    def setUp(self):
        self.small_gmp = gmp.Float(10.1)
        self.small_gmp2 = gmp.Float(12.2)
        self.large_gmp = gmp.Float("4294967300.10")
        self.small_neg_gmp = gmp.Float(-10.1)
        self.large_neg_gmp = gmp.Float("-4294967300.10")
        self.prec_gmp = gmp.Float("10.4294967300101010")
        self.prec_neg_gmp = gmp.Float("-10.4294967300101010")

    def test_Negation(self):
        self.assertEqual(-self.large_gmp, self.large_neg_gmp);
        self.assertEqual(-self.large_neg_gmp, self.large_gmp);
        self.assertEqual(-self.prec_gmp, self.prec_neg_gmp);
        self.assertEqual(-self.prec_neg_gmp, self.prec_gmp);
        self.assertEqual(-gmp.Float(0.0), gmp.Float(0.0));

    def test_Absolute(self):
        self.assertEqual(abs(self.large_gmp), self.large_gmp);
        self.assertEqual(abs(self.large_neg_gmp), self.large_gmp);
        self.assertEqual(abs(self.prec_gmp), self.prec_gmp);
        self.assertEqual(abs(self.prec_neg_gmp), self.prec_gmp);
        self.assertEqual(abs(gmp.Float(0.0)), gmp.Float(0.0));


class Test_FloatErrorCases(unittest2.TestCase):
    def test_DivisionBy0(self):
        #TODO Removed for now - crashes in c
        i = gmp.Float(0.1)
        self.assertTrue(0)
        #self.assertRaises(ValueError, gmp.Float(0.1) / gmp.Float(0.0))
        #self.assertRaises(ValueError, i /= gmp.Float(0.0))

    def test_ModBy0(self):
        #TODO Removed for now - crashes in c
        i = gmp.Float(0.1)
        self.assertTrue(0)
        #self.assertRaises(ValueError, gmp.Float(0.1) % gmp.Float(0.0))
        #self.assertRaises(ValueError, i %= gmp.Float(0.0))


class Test_FloatPyTypeCompatibility(unittest2.TestCase):
    def test_IntCompatibility(self):
        print "TODO: Test_s for interation with python ints"

    def test_BoolCompatibility(self):
        print "TODO: Test_s for interation with python Booleans"

    def test_LongCompatibility(self):
        print "TODO: Test_s for interation with python longs"

    def test_ComplexCompatibility(self):
        print "TODO: Test_s for interation with python complex"

