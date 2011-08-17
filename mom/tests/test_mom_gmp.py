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


import unittest2
from mom import gmp


#TODO inplace long += gmp
class TestIntegerInit(unittest2.TestCase):

  def setUp(self):
    self.large_gmp = gmp.Integer(4294967300L)
    self.large_neg_gmp = gmp.Integer(-4294967300L)
    self.inst = gmp.Integer(10L)

  def testSetPyLong(self):
    self.inst.set(5000000000L)
    self.assertEqual(self.inst, gmp.Integer(5000000000L))

  def testSetGmpInt(self):
    self.inst.set(self.large_gmp)
    self.assertEqual(self.inst, self.large_gmp)

  def testSetNegative(self):
    self.inst.set(-5000000000L)
    self.assertEqual(self.inst, gmp.Integer(-5000000000L))
    self.inst.set(self.large_neg_gmp)
    self.assertEqual(self.inst, self.large_neg_gmp)

class TestIntegerAddition(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(199L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.small_neg_gmp = gmp.Integer(-199L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testSimpleAddition(self):
    self.assertEqual(self.small_gmp + self.small_gmp, gmp.Integer(199L + 199L))

  def testLargeAddition(self):
    self.assertEqual(self.large_gmp + self.large_gmp, gmp.Integer(5000000000L + 5000000000L))
    self.assertEqual(self.large_gmp + self.large_gmp + self.large_gmp, gmp.Integer(5000000000L * 3))

  def testPyLongAddition(self):
    self.assertEqual(self.small_gmp + 150L, gmp.Integer(199L + 150L))
    self.assertEqual(self.large_gmp + 150L, gmp.Integer(5000000000L + 150L))

  def testPyLongReverseAddition(self):
    self.assertEqual(150L + self.small_gmp, gmp.Integer(199L + 150L))
    self.assertEqual(150L + self.large_gmp, gmp.Integer(5000000000L + 150L))

  def testAdditionWithNegatives(self):
    self.assertEqual(self.large_gmp + self.large_neg_gmp, gmp.Integer(0L))
    self.assertEqual(self.large_gmp + self.small_neg_gmp, gmp.Integer(5000000000L + -199L))
    self.assertEqual(self.small_gmp + self.large_neg_gmp, gmp.Integer(199L + -5000000000L))
    self.assertEqual(self.large_neg_gmp + self.large_neg_gmp, gmp.Integer(-5000000000 + -5000000000L))
    self.assertEqual(self.large_gmp + -6000000000L, gmp.Integer(5000000000 + -6000000000L))
    self.assertEqual(6000000000L + self.large_neg_gmp, gmp.Integer(6000000000 + -5000000000L))

  def testInPlaceAddition(self):
    #Test in-place addition
    i = self.small_gmp
    i += self.small_gmp
    self.assertEqual(i, gmp.Integer(199L + 199L))
    i += 5000000000L
    self.assertEqual(i, gmp.Integer(199L + 199L + 5000000000L))

class TestIntegerSubtraction(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(199L)
    self.small_gmp2 = gmp.Integer(250L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(5000500500L)
    self.small_neg_gmp = gmp.Integer(-199L)
    self.small_neg_gmp2 = gmp.Integer(-250L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testSimpleSubtraction(self):
    self.assertEqual(self.small_gmp2 - self.small_gmp, gmp.Integer(250L - 199L))
    self.assertEqual(self.small_gmp - self.small_gmp2, gmp.Integer(199L - 250L))

  def testLargeSubtraction(self):
    self.assertEqual(self.large_gmp2 - self.large_gmp, gmp.Integer(5000500500L - 5000000000L))
    self.assertEqual(self.large_gmp - self.large_gmp2, gmp.Integer(5000000000L - 5000500500L))
    self.assertEqual(self.large_gmp - self.large_gmp - self.large_gmp, self.large_neg_gmp)
    self.assertEqual(self.large_neg_gmp - self.large_neg_gmp - self.large_neg_gmp, self.large_gmp)

  def testPyLongSubtraction(self):
    self.assertEqual(self.small_gmp - 20L, gmp.Integer(199L - 20L))
    self.assertEqual(self.small_gmp - 5000000000L, gmp.Integer(199L - 5000000000L))
    self.assertEqual(self.large_gmp - 20L, gmp.Integer(5000000000L - 20L))

  def testPyLongReverseSubtraction(self):
    self.assertEqual(250L - self.small_gmp, gmp.Integer(250L - 199L))
    self.assertEqual(20L - self.small_gmp, gmp.Integer(20L - 199L))
    self.assertEqual(20L - self.large_gmp, gmp.Integer(20L - 5000000000L))

  def testNegativeSubtraction(self):
    self.assertEqual(self.small_neg_gmp2 - self.small_gmp, gmp.Integer(-250L - 199L))
    self.assertEqual(self.small_neg_gmp2 - self.small_neg_gmp, gmp.Integer(-250L - -199L))
    self.assertEqual(self.small_gmp2 - self.small_neg_gmp, gmp.Integer(250L - -199L))
    self.assertEqual(self.large_gmp - -500000L, gmp.Integer(5000000000L - -500000L))
    self.assertEqual(-500000L - self.large_neg_gmp , gmp.Integer(-500000L - -5000000000L))

  def testInPlaceSubtraction(self):
    i = self.small_gmp
    i -= self.small_gmp
    self.assertEqual(i, gmp.Integer(0L))
    i -= 5000000000L
    self.assertEqual(i, gmp.Integer(-5000000000L))

class TestIntegerMultiplication(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(199L)
    self.small_gmp2 = gmp.Integer(250L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(5000500500L)
    self.small_neg_gmp = gmp.Integer(-199L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testSimpleMultiplication(self):
    self.assertEqual(self.small_gmp * self.small_gmp, gmp.Integer(199L * 199L))

  def testLargeMultiplication(self):
    self.assertEqual(self.large_gmp * self.large_gmp, gmp.Integer(5000000000L * 5000000000L))
    self.assertEqual(self.large_gmp * self.large_gmp * self.large_gmp, gmp.Integer(5000000000L * 5000000000L * 5000000000L))

  def testPyLongMultiplication(self):
    self.assertEqual(self.small_gmp * 150L, gmp.Integer(199L * 150L))
    self.assertEqual(self.large_gmp * 150L, gmp.Integer(5000000000L * 150L))

  def testPyLongReverseMultiplication(self):
    self.assertEqual(150L * self.small_gmp, gmp.Integer(199L * 150L))
    self.assertEqual(150L * self.large_gmp, gmp.Integer(5000000000L * 150L))

  def testNegativeMultiplication(self):
    self.assertEqual(self.large_gmp * self.large_neg_gmp, gmp.Integer(5000000000L * -5000000000L))
    self.assertEqual(self.large_gmp * -5000000000L, gmp.Integer(5000000000L * -5000000000L))

  def testInPlaceMultiplication(self):
    i = self.small_gmp
    i *= self.small_gmp
    self.assertEqual(i, gmp.Integer(199L * 199L))
    i *= 5000000000L
    self.assertEqual(i, 199L * 199L * 5000000000L)

class TestIntegerDivision(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(19L)
    self.small_gmp2 = gmp.Integer(250L)
    self.small_gmp3 = gmp.Integer(50L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(5000500500L)
    self.small_neg_gmp = gmp.Integer(-19L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testSimpleDivision(self):
    self.assertEqual(self.small_gmp2 / self.small_gmp, gmp.Integer(250L / 19L))
    self.assertEqual(self.small_gmp2 / self.small_gmp3, gmp.Integer(250L / 50L))
    self.assertEqual(self.small_gmp / self.small_gmp2, gmp.Integer(19L / 250L))

  def testLargeDivision(self):
    self.assertEqual(self.large_gmp2 / self.large_gmp, gmp.Integer(5000500500L / 5000000000L))
    self.assertEqual(self.large_gmp / self.small_gmp, gmp.Integer(5000000000L / 19L))
    self.assertEqual(self.large_gmp / self.small_gmp / self.small_gmp, gmp.Integer(5000000000L / 19L / 19L))

  def testPyLongDivision(self):
    self.assertEqual(self.small_gmp2 / 50L, gmp.Integer(250L / 50L))
    self.assertEqual(self.large_gmp / 50L, gmp.Integer(5000000000L / 50L))

  def testPyLongReverseDivision(self):
    self.assertEqual(5000000000L / self.small_gmp3, gmp.Integer(5000000000L / 50L))
    self.assertEqual(5000500500L / self.large_gmp, gmp.Integer(5000500500L / 5000000000L))

  def testNegativeDivision(self):
    self.assertEqual(self.large_gmp / self.small_neg_gmp, gmp.Integer(5000000000L / -19L))
    self.assertEqual(self.large_neg_gmp / self.small_neg_gmp, gmp.Integer(-5000000000L / -19L))
    self.assertEqual(self.large_neg_gmp / self.small_gmp, gmp.Integer(-5000000000L / 19L))
    self.assertEqual(self.large_neg_gmp / 50L, gmp.Integer(-5000000000L / 50L))
    self.assertEqual(self.large_gmp / -50L, gmp.Integer(5000000000L / -50L))

  def testInPlaceDivision(self):
    i = self.large_gmp
    i /= self.small_gmp
    self.assertEqual(i, gmp.Integer(5000000000L / 19L))
    i /= 19L
    self.assertEqual(i, gmp.Integer(5000000000L / 19L / 19L))

class TestIntegerMod(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(19L)
    self.small_gmp2 = gmp.Integer(250L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(5000500500L)
    self.small_neg_gmp = gmp.Integer(-19L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testSimpleMod(self):
    self.assertEqual(self.small_gmp2 % self.small_gmp, gmp.Integer(250L % 19L))
    self.assertEqual(self.small_gmp % self.small_gmp2, gmp.Integer(19L % 250L))

  def testLargeMod(self):
    self.assertEqual(self.large_gmp % self.small_gmp2, gmp.Integer(5000000000L % 250L))
    self.assertEqual(self.large_gmp2 % self.large_gmp, gmp.Integer(5000500500L % 5000000000L))
    self.assertEqual(self.large_gmp % self.small_gmp2 % self.small_gmp, gmp.Integer(5000000000L % 250L % 19L))

  def testPyLongMod(self):
    self.assertEqual(self.small_gmp2 % 19L, gmp.Integer(250L % 19L))
    self.assertEqual(self.large_gmp % 19L, gmp.Integer(5000000000L % 19L))

  def testPyLongReverseMod(self):
    self.assertEqual(250L % self.small_gmp, gmp.Integer(250L % 19L))
    self.assertEqual(5000500500L % self.large_gmp , gmp.Integer(5000500500L % 5000000000L))

  def testNegativeMod(self):
    self.assertEqual(self.large_gmp % self.small_neg_gmp, gmp.Integer(5000000000L % 19L))
    self.assertEqual(self.large_neg_gmp % self.small_neg_gmp, gmp.Integer(-5000000000L % -19L))
    self.assertEqual(self.large_neg_gmp % self.small_gmp, gmp.Integer(-5000000000L % 19L))
    self.assertEqual(self.large_gmp % self.small_neg_py, gmp.Integer(5000000000L % -19L))

  def testInPlaceMod(self):
    i = self.large_gmp
    i %= self.small_gmp
    self.assertEqual(i, gmp.Integer(5000000000L % 19L))
    i %= 4L
    self.assertEqual(i, gmp.Integer(5000000000L % 19L % 4L))

class TestIntegerStringFormat(unittest2.TestCase):

  def setUp(self):
    self.large_gmp = gmp.Integer(5123456789L)
    self.large_neg_gmp = gmp.Integer(-5123456789L)

  def testStringFormat(self):
    self.assertEqual(str(self.large_gmp), "5123456789")
    self.assertEqual(repr(self.large_gmp), "5123456789")
    #TODO error stirng

  def testNegativeStringFormat(self):
    self.assertEqual(str(self.large_neg_gmp), "-5123456789")
    self.assertEqual(repr(self.large_neg_gmp), "-5123456789")

  def testStringParsing(self):
    self.assertEqual(gmp.Integer(str(5123456789L)), self.large_gmp)
    self.assertEqual(gmp.Integer(str(-5123456789L)), self.large_neg_gmp)

class TestIntegerComparison(unittest2.TestCase):

  def setUp(self):
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(50000000001L)

  def testLessThan(self):
    self.assertTrue(self.large_gmp < self.large_gmp2)
    self.assertFalse(self.large_gmp < self.large_gmp)
    self.assertFalse(self.large_gmp2 < self.large_gmp)

  def testLessThanPyLong(self):
    self.assertTrue(self.large_gmp < 5000000001L)
    self.assertFalse(self.large_gmp < 5000000000L)
    self.assertFalse(self.large_gmp2 < 5000000000L)

  def testPyLongLessThan(self):
    self.assertTrue(5000000000L < self.large_gmp2)
    self.assertFalse(5000000000L < self.large_gmp)
    self.assertFalse(5000000001L < self.large_gmp)

  def testLessThanEqual(self):
    self.assertTrue(self.large_gmp <= self.large_gmp2)
    self.assertTrue(self.large_gmp <= self.large_gmp)
    self.assertFalse(self.large_gmp2 <= self.large_gmp)

  def testLessThanEqualPyLong(self):
    self.assertTrue(self.large_gmp <= 5000000001L)
    self.assertTrue(self.large_gmp <= 5000000000L)
    self.assertFalse(self.large_gmp2 <= 5000000000L)

  def testPyLongLessThanEqual(self):
    self.assertTrue(5000000000L <= self.large_gmp2)
    self.assertTrue(5000000000L <= self.large_gmp)
    self.assertFalse(5000000001L <= self.large_gmp)

  def testGreaterThan(self):
    self.assertFalse(self.large_gmp > self.large_gmp2)
    self.assertFalse(self.large_gmp > self.large_gmp)
    self.assertTrue(self.large_gmp2 > self.large_gmp)

  def testGreaterThanPyLong(self):
    self.assertFalse(self.large_gmp > 5000000001L)
    self.assertFalse(self.large_gmp > 5000000000L)
    self.assertTrue(self.large_gmp2 > 5000000000L)

  def testPyLongGreaterThan(self):
    self.assertFalse(5000000000L > self.large_gmp2)
    self.assertFalse(5000000000L > self.large_gmp)
    self.assertTrue(5000000001L > self.large_gmp)

  def testGreaterThanEqual(self):
    self.assertFalse(self.large_gmp >= self.large_gmp2)
    self.assertTrue(self.large_gmp >= self.large_gmp)
    self.assertTrue(self.large_gmp2 >= self.large_gmp)

  def testGreaterThanEqualPyLong(self):
    self.assertFalse(self.large_gmp >= 5000000001L)
    self.assertTrue(self.large_gmp >= 5000000000L)
    self.assertTrue(self.large_gmp2 >= 5000000000L)

  def testPyLongGreaterThanEqual(self):
    self.assertFalse(5000000000L >= self.large_gmp2)
    self.assertTrue(5000000000L >= self.large_gmp)
    self.assertTrue(5000000001L >= self.large_gmp)

  def testEquals(self):
    self.assertFalse(self.large_gmp == self.large_gmp2)
    self.assertTrue(self.large_gmp == self.large_gmp)
    self.assertFalse(self.large_gmp2 == self.large_gmp)

  def testEqualsPyLong(self):
    self.assertFalse(self.large_gmp == 5000000001L)
    self.assertTrue(self.large_gmp == 5000000000L)
    self.assertFalse(self.large_gmp2 == 5000000000L)

  def testPyLongEquals(self):
    self.assertFalse(5000000000L == self.large_gmp2)
    self.assertTrue(5000000000L == self.large_gmp)
    self.assertFalse(5000000001L == self.large_gmp)

  def testNotEquals(self):
    self.assertTrue(self.large_gmp != self.large_gmp2)
    self.assertFalse(self.large_gmp != self.large_gmp)
    self.assertTrue(self.large_gmp2 != self.large_gmp)

  def testNotEqualsPyLong(self):
    self.assertTrue(self.large_gmp != 5000000001L)
    self.assertFalse(self.large_gmp != 5000000000L)
    self.assertTrue(self.large_gmp2 != 5000000000L)

  def testPyLongNotEquals(self):
    self.assertTrue(5000000000L != self.large_gmp2)
    self.assertFalse(5000000000L != self.large_gmp)
    self.assertTrue(5000000001L != self.large_gmp)

class TestIntegerBitOps(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(19L)
    self.small_gmp2 = gmp.Integer(250L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(5000500500L)
    self.small_neg_gmp = gmp.Integer(-19L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testAnd(self):
    self.assertEqual(self.large_gmp & self.large_gmp, self.large_gmp)
    self.assertEqual(self.large_gmp & self.small_gmp, gmp.Integer(5000000000L & 19L))
    self.assertEqual(self.large_gmp & 250L, gmp.Integer(5000000000L & 250L))
    self.assertEqual(self.large_neg_gmp & self.small_neg_gmp, gmp.Integer(-5000000000L & -19L))

  def testInPlaceAnd(self):
    i = self.large_gmp
    i &= self.small_gmp
    self.assertEqual(i, 5000000000L & 19L)
    i &= 250L
    self.assertEqual(i, 5000000000L & 19L & 250L)

  def testOr(self):
    self.assertEqual(self.large_gmp | gmp.Integer(0L), self.large_gmp)
    self.assertEqual(gmp.Integer(0L) | self.large_gmp, self.large_gmp)
    self.assertEqual(self.large_gmp | self.small_gmp, gmp.Integer(5000000000L | 19L))
    self.assertEqual(self.large_gmp | 250L, gmp.Integer(5000000000L | 250L))
    self.assertEqual(self.large_neg_gmp | self.small_neg_gmp, gmp.Integer(-5000000000L | -19L))

  def testInPlaceOr(self):
    i = self.large_gmp
    i |= self.small_gmp
    self.assertEqual(i, gmp.Integer(5000000000L | 19L))
    i |= 250L
    self.assertEqual(i, gmp.Integer(5000000000L | 19L | 250L))

  def testXor(self):
    self.assertEqual(self.large_gmp ^ self.large_gmp, gmp.Integer(0L))
    self.assertEqual(self.large_gmp ^ gmp.Integer(0), self.large_gmp)
    self.assertEqual(gmp.Integer(0) ^ self.large_gmp, self.large_gmp)
    self.assertEqual(self.large_gmp ^ self.small_gmp, gmp.Integer(5000000000L ^ 19L))
    self.assertEqual(self.large_gmp ^ 250L, gmp.Integer(5000000000L ^ 250L))
    self.assertEqual(self.large_neg_gmp ^ self.small_neg_gmp, gmp.Integer(-5000000000L ^ -19L))

  def testInPlaceXor(self):
    i = self.large_gmp
    i ^= self.small_gmp
    self.assertEqual(i, gmp.Integer(5000000000L ^ 19L))
    i ^= 250L
    self.assertEqual(i, gmp.Integer(5000000000L ^ 19L ^ 250L))

class TestIntegerAdditionals(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Integer(19L)
    self.ssmall_gmp2 = gmp.Integer(250L)
    self.large_gmp = gmp.Integer(5000000000L)
    self.large_gmp2 = gmp.Integer(5000500500L)
    self.small_neg_gmp = gmp.Integer(-19L)
    self.large_neg_gmp = gmp.Integer(-5000000000L)

  def testNegation(self):
    self.assertEqual(-self.large_gmp, self.large_neg_gmp);
    self.assertEqual(-self.large_neg_gmp, self.large_gmp);
    self.assertEqual(-gmp.Integer(0L), gmp.Integer(0L));

  def testAbsolute(self):
    self.assertEqual(abs(self.large_gmp), self.large_gmp);
    self.assertEqual(abs(self.large_neg_gmp), self.large_gmp);
    self.assertEqual(abs(gmp.Integer(0L)), gmp.Integer(0L));

class TestIntegerErrorCases(unittest2.TestCase):

  def testDivisionBy0(self):
    #TODO Removed for now - crashes in c
    i = gmp.Integer(1L)
    self.assertTrue(0)
    #self.assertRaises(ValueError, gmp.Integer(1L) / gmp.Integer(0L))
    #self.assertRaises(ValueError, i /= gmp.Integer(0L))

  def testModBy0(self):
    #TODO Removed for now - crashes in c
    i = gmp.Integer(1L)
    self.assertTrue(0)
    #self.assertRaises(ValueError, gmp.Integer(1L) % gmp.Integer(0L))
    #self.assertRaises(ValueError, i %= gmp.Integer(0L))

class TestIntegerPyTypeCompatibility(unittest2.TestCase):

  def testIntCompatibility(self):
    print "TODO: Tests for interation with python ints"

  def testBoolCompatibility(self):
    print "TODO: Tests for interation with python Booleans"

  def testFloatCompatibility(self):
    print "TODO: Tests for interation with python floats"

  def testComplexCompatibility(self):
    print "TODO: Tests for interation with python complex"

  #TODO iteration with range








class TestFloatInit(unittest2.TestCase):

    #TODO compare with epsilon

  def setUp(self):
    self.inst = gmp.Float(10.0)
    self.large_gmp = gmp.Float(5000000000.0000000005)
    self.large_neg_gmp = gmp.Float(-5000000000.0000000005)

  def testSet(self):
    self.inst.set(self.large_gmp)
    self.assertEqual(self.inst, gmp.Float(5000000000.0000000005))

  def testSetPyFloat(self):
    self.inst.set(101.101)
    self.assertEqual(self.inst, gmp.Float(101.101))

  def testSetNegative(self):
    self.inst.set(-101.101)
    self.assertEqual(self.inst, gmp.Float(-101.101))
    self.inst.set(self.large_neg_gmp)
    self.assertEqual(self.inst, gmp.Float(-5000000000.0000000005))

class TestFloatStringFormatting(unittest2.TestCase):

  def testStringParsing(self):
    self.assertEqual(gmp.Float("1.1"), gmp.Float(1.1))
    self.assertEqual(gmp.Float(".1"), gmp.Float(0.1))
    self.assertEqual(gmp.Float("1"), gmp.Float(1.0))
    self.assertEqual(gmp.Float(str(1010101.10101)), gmp.Float(1010101.10101))

  def testStringNegativeParsing(self):
    self.assertEqual(gmp.Float("-1.1"), gmp.Float(-1.1))
    self.assertEqual(gmp.Float("-.1"), gmp.Float(-0.1))
    self.assertEqual(gmp.Float("-1"), gmp.Float(-1.0))
    self.assertEqual(gmp.Float(str(-1010101.10101)), gmp.Float(-1010101.10101))

  def testStringFormatting(self):
    self.assertEqual(str(gmp.Float(1.1)), str(1.1))
    self.assertEqual(str(gmp.Float("5000000000.0000000005")), "5000000000.0000000005")
    self.assertEqual(repr(gmp.Float(1.1)), str(1.1))
    self.assertEqual(repr(gmp.Float("5000000000.0000000005")), "5000000000.0000000005")

  def testStringNegativeFormatting(self):
    self.assertEqual(str(gmp.Float(-1.1)), str(-1.1))
    self.assertEqual(str(gmp.Float("-5000000000.0000000005")), "-5000000000.0000000005")
    self.assertEqual(repr(gmp.Float(-1.1)), str(-1.1))
    self.assertEqual(repr(gmp.Float("-5000000000.0000000005")), "-5000000000.0000000005")
  #TODO errors

class TestFloatAddition(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Float(10.1)
    self.small_gmp2 = gmp.Float(12.2)
    self.large_gmp = gmp.Float("4294967300.10")
    self.small_neg_gmp = gmp.Float(-10.1)
    self.large_neg_gmp = gmp.Float("-4294967300.10")
    self.prec_gmp  = gmp.Float("10.4294967300101010")

  def testSimpleAddition(self):
    self.assertEqual(self.small_gmp + self.small_gmp2, gmp.Float(22.3))

  def testLargeAddition(self):
    self.assertEqual(self.large_gmp + self.large_gmp, gmp.Float("8589934600.20"))
    self.assertEqual(self.large_gmp + self.large_gmp + self.large_gmp, gmp.Float("12884901900.30"))

  def testPreciseAddition(self):
    self.assertEqual(self.prec_gmp + self.prec_gmp, gmp.Float("20.8589934600202020"))
    self.assertEqual(self.prec_gmp + self.small_gmp, gmp.Float("20.5294967300101010"))

  def testPyFloatAddition(self):
    self.assertEqual(self.small_gmp + 10.1, gmp.Float(20.2))
    self.assertEqual(self.large_gmp + 10.1, gmp.Float(4294967310.2))
    self.assertEqual(self.prec_gmp + 10.1, gmp.Float("20.5294967300101010"))

  def testPyFloatReverseAddition(self):
    self.assertEqual(10.1 + self.small_gmp, gmp.Float(20.2))
    self.assertEqual(10.1 + self.large_gmp, gmp.Float(4294967310.2))
    self.assertEqual(10.1 + self.prec_gmp, gmp.Float("20.5294967300101010"))

  def testNegativeAddition(self):
    self.assertEqual(self.large_gmp + self.large_neg_gmp, gmp.Float(0.0))
    self.assertEqual(self.large_neg_gmp + self.large_gmp, gmp.Float(0.0))
    self.assertEqual(self.small_gmp + self.large_neg_gmp, gmp.Float("-4294967290.0"))
    self.assertEqual(self.large_gmp + self.small_neg_gmp, gmp.Float("4294967290.0"))
    self.assertEqual(self.small_gmp + -10.1, gmp.Float(0.0))
    self.assertEqual(self.small_gmp + -11.2, gmp.Float(-1.1))
    self.assertEqual(10.1 + self.small_neg_gmp, gmp.Float(0.0))
    self.assertEqual(11.2 + self.small_neg_gmp, gmp.Float(1.1))

  def testInPlaceAddition(self):
    i = gmp.Float(10.1)
    i += gmp.Float("4294967300.10")
    self.assertEqual(i, gmp.Float("4294967310.20"))
    i += 10.1
    self.assertEqual(i, gmp.Float("4294967320.30"))
    i += self.prec_gmp
    self.assertEqual(i, gmp.Float("4294967330.729496730010101"))

class TestFloatSubtraction(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Float(10.1)
    self.small_gmp2 = gmp.Float(12.2)
    self.large_gmp = gmp.Float("4294967300.10")
    self.small_neg_gmp = gmp.Float(-10.1)
    self.large_neg_gmp = gmp.Float("-4294967300.10")
    self.prec_gmp  = gmp.Float("10.429496730010")

  def testSimpleSubtraction(self):
    self.assertEqual(self.small_gmp2 - self.small_gmp, gmp.Float(2.1))
    self.assertEqual(self.small_gmp - self.small_gmp2, gmp.Float(-2.1))

  def testLargeSubtraction(self):
    self.assertEqual(self.large_gmp - self.small_gmp, gmp.Float("4294967290"))
    self.assertEqual(self.large_gmp - self.small_gmp - self.small_gmp, gmp.Float("4294967279.9"))
    self.assertEqual(self.small_gmp - self.large_gmp, gmp.Float("-4294967290"))

  def testPreciseSubtraction(self):
    self.assertEqual(self.prec_gmp - self.prec_gmp, gmp.Float(0))
    self.assertEqual(self.prec_gmp - self.small_gmp, gmp.Float("0.329496730010"))

  def testPyFloatSubtraction(self):
    self.assertEqual(self.small_gmp2 - 10.1, gmp.Float(2.1))
    self.assertEqual(self.small_gmp - 12.2, gmp.Float(-2.1))
    self.assertEqual(self.large_gmp - 10.1, gmp.Float("4294967290"))
    self.assertEqual(self.prec_gmp - 10.1, gmp.Float("0.329496730010"))

  def testPyFloatReverseSubtraction(self):
    self.assertEqual(12.2 - self.small_gmp, gmp.Float(2.1))
    self.assertEqual(10.1 - self.small_gmp2, gmp.Float(-2.1))
    self.assertEqual(10.1 - self.large_gmp, gmp.Float("-4294967290"))
    self.assertEqual(10.1 - self.prec_gmp, gmp.Float("-0.329496730010"))

  def testNegativeSubtraction(self):
    self.assertEqual(self.small_neg_gmp - self.large_neg_gmp, gmp.Float("4294967290"))
    self.assertEqual(self.large_neg_gmp - self.small_neg_gmp, gmp.Float("-4294967290"))
    self.assertEqual(self.large_gmp - self.large_neg_gmp, gmp.Float("8589934600.2"))
    self.assertEqual(self.large_gmp - self.small_neg_gmp, gmp.Float("4294967310.2"))
    self.assertEqual(self.small_gmp - self.large_neg_gmp, gmp.Float("-4294967310.2"))
    self.assertEqual(self.small_gmp - -10.1, gmp.Float(20.2))

  def testInPlaceSubtraction(self):
    i = gmp.Float(10.1)
    i += gmp.Float("4294967300.10")
    self.assertEqual(i, gmp.Float("4294967310.20"))
    i += 10.1
    self.assertEqual(i, gmp.Float("4294967320.30"))

class TestFloatMultiplication(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Float(10.1)
    self.small_gmp2 = gmp.Float(12.2)
    self.large_gmp = gmp.Float("4294967300.10")
    self.small_neg_gmp = gmp.Float(-10.1)
    self.large_neg_gmp = gmp.Float("-4294967300.10")
    self.prec_gmp  = gmp.Float("10.4294967300101010")

  def testSimpleMultiplication(self):
    self.assertEqual(self.small_gmp * self.small_gmp, gmp.Float(102.01))

  def testLargeMultiplication(self):
    self.assertEqual(self.large_gmp * self.large_gmp, gmp.Float("18446744108928283460.01"))
    self.assertEqual(self.large_gmp * self.large_gmp * self.large_gmp, gmp.Float("79228162741159289916766636019.001"))

  def testPreciseMultiplication(self):
    self.assertEqual(self.prec_gmp * self.small_gmp, gmp.Float("105.3379169731020201"))
    self.assertEqual(self.prec_gmp * self.large_gmp, gmp.Float("44794347411.8932621376983101"))
    self.assertEqual(self.prec_gmp * self.prec_gmp, gmp.Float("108.774402041291389592939562030201"))

  def testPyFloatMultiplication(self):
    self.assertEqual(self.small_gmp * 10.1, gmp.Float(102.01))
    self.assertEqual(self.large_gmp * 10.1, gmp.Float("43379169731.01"))
    self.assertEqual(self.prec_gmp * 10.1, gmp.Float("105.3379169731020201"))

  def testPyFloatReverseMultiplication(self):
    self.assertEqual(10.1 * self.small_gmp, gmp.Float(102.01))
    self.assertEqual(10.1 * self.large_gmp, gmp.Float("43379169731.01"))
    self.assertEqual(10.1 * self.prec_gmp, gmp.Float("105.3379169731020201"))

  def testNegativeMultiplication(self):
    self.assertEqual(self.large_gmp * self.large_neg_gmp, gmp.Float("-18446744108928283460.01"))
    self.assertEqual(self.large_neg_gmp * self.large_gmp, gmp.Float("-18446744108928283460.01"))
    self.assertEqual(self.large_gmp * -10.1, gmp.Float("-43379169731.01"))
    self.assertEqual(10.1 * self.large_neg_gmp, gmp.Float("-43379169731.01"))

  def testInPlaceMultiplication(self):
    i = self.small_gmp
    i *= self.small_gmp
    self.assertEqual(i, gmp.Float(102.01))
    i *= 10.1
    self.assertEqual(i, gmp.Float(1030.301))

class TestFloatDivision(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Float(0.2)
    self.small_gmp2 = gmp.Float(122.2)
    self.large_gmp = gmp.Float("4294967300.10")
    self.small_neg_gmp = gmp.Float(-0.2)
    self.large_neg_gmp = gmp.Float("-4294967300.10")
    self.prec_gmp  = gmp.Float("10.4294967300101010")

  def testSimpleDivision(self):
    self.assertEqual(self.small_gmp2 / self.small_gmp, gmp.Float(122.2 / 0.2))
    self.assertEqual(self.small_gmp / self.small_gmp2, gmp.Float(10.1 / 122.2))

  def testLargeDivision(self):
    self.assertEqual(self.large_gmp / self.small_gmp, gmp.Float("21474836500.5"))
    self.assertEqual(self.large_gmp / self.large_gmp, gmp.Float("1"))

  def testPreciseDivision(self):
    self.assertEqual(self.prec_gmp / self.small_gmp, gmp.Float("52.147483650050505"))
    self.assertEqual(self.prec_gmp / self.prec_gmp, gmp.Float("1"))

  def testPyFloatDivision(self):
    self.assertEqual(self.small_gmp2 / 0.2, gmp.Float(122.2 / 2))
    self.assertEqual(self.large_gmp / 0.2, gmp.Float("2147483650.05"))
    self.assertEqual(self.prec_gmp / 0.2, gmp.Float("52.147483650050505"))

  def testPyFloatDivision(self):
    self.assertEqual(100.5 / self.small_gmp, gmp.Float(100.5 / 2.0))

  def testNegativeDivision(self):
    self.assertEqual(self.large_gmp / self.small_neg_gmp, gmp.Float("-21474836500.5"))
    self.assertEqual(self.large_neg_gmp / self.small_neg_gmp, gmp.Float("21474836500.5"))
    self.assertEqual(self.large_neg_gmp / self.small_gmp, gmp.Float("-21474836500.5"))
    self.assertEqual(self.prec_gmp / self.small_neg_gmp, gmp.Float("-52.147483650050505"))
    self.assertEqual(self.large_gmp / 0.2, gmp.Float("-21474836500.5"))

  def testInPlaceDivision(self):
    i = self.large_gmp
    i /= self.small_gmp
    self.assertEqual(i, gmp.Float("21474836500.5"))
    i /= 10.0
    self.assertEqual(i, gmp.Float("2147483650.05"))

class TestFloatComparison(unittest2.TestCase):

  def setUp(self):
    self.large_gmp = gmp.Float("5000000.0000000005")
    self.large_gmp2 = gmp.Float("5000000.000000001")
    self.large_gmp3 = gmp.Float(5000000.1)


  def testLessThan(self):
    self.assertTrue(self.large_gmp < self.large_gmp2)
    self.assertFalse(self.large_gmp < self.large_gmp)
    self.assertFalse(self.large_gmp2 < self.large_gmp)

  def testLessThanPyFloat(self):
    self.assertTrue(self.large_gmp < 5000000.1)
    self.assertFalse(self.large_gmp < 5000000.0)
    self.assertFalse(self.large_gmp3 < 5000000.1)

  def testPyFloatLessThan(self):
    self.assertTrue(5000000.0 < self.large_gmp)
    self.assertFalse(5000000.1 < self.large_gmp)
    self.assertFalse(5000000.1 < self.large_gmp3)

  def testLessThanEqual(self):
    self.assertTrue(self.large_gmp <= self.large_gmp2)
    self.assertTrue(self.large_gmp <= self.large_gmp)
    self.assertFalse(self.large_gmp2 <= self.large_gmp)

  def testLessThanEqualPyFloat(self):
    self.assertTrue(self.large_gmp <= 5000000.1)
    self.assertFalse(self.large_gmp <= 5000000.0)
    self.assertTrue(self.large_gmp3 < 5000000.1)

  def testPyFloatLessThanEqual(self):
    self.assertTrue(5000000.0 <= self.large_gmp)
    self.assertFalse(5000000.1 <= self.large_gmp)
    self.assertTrue(5000000.1 <= self.large_gmp3)

  def testGreaterThan(self):
    self.assertFalse(self.large_gmp > self.large_gmp2)
    self.assertFalse(self.large_gmp > self.large_gmp)
    self.assertTrue(self.large_gmp2 > self.large_gmp)

  def testGreaterThanPyFloat(self):
    self.assertFalse(self.large_gmp > 5000000.1)
    self.assertTrue(self.large_gmp > 5000000.0)
    self.assertFalse(self.large_gmp3 > 5000000.1)

  def testPyFloatGreaterThan(self):
    self.assertFalse(5000000.0 > self.large_gmp)
    self.assertTrue(5000000.1 > self.large_gmp)
    self.assertFalse(5000000.1 > self.large_gmp3)

  def testGreaterThanEqual(self):
    self.assertFalse(self.large_gmp >= self.large_gmp2)
    self.assertTrue(self.large_gmp >= self.large_gmp)
    self.assertTrue(self.large_gmp2 >= self.large_gmp)

  def testGreaterThanEqualPyFloat(self):
    self.assertFalse(self.large_gmp >= 5000000.1)
    self.assertTrue(self.large_gmp >= 5000000.0)
    self.assertTrue(self.large_gmp3 >= 5000000.1)

  def testPyFloatGreaterThanEqual(self):
    self.assertFalse(5000000.0 >= self.large_gmp)
    self.assertTrue(5000000.1 >= self.large_gmp)
    self.assertTrue(5000000.1 >= self.large_gmp3)

  def testEquals(self):
    self.assertFalse(self.large_gmp == self.large_gmp2)
    self.assertTrue(self.large_gmp == self.large_gmp)
    self.assertFalse(self.large_gmp2 == self.large_gmp)

  def testEqualsPyFloat(self):
    self.assertFalse(self.large_gmp == 5000000.1)
    self.assertFalse(self.large_gmp == 5000000.0)
    self.assertTrue(self.large_gmp3 == 5000000.1)

  def testPyFloatEquals(self):
    self.assertFalse(5000000.1 == self.large_gmp)
    self.assertTrue(5000000.1 == self.large_gmp3)
    self.assertFalse(5000000.0 == self.large_gmp)

  def testNotEquals(self):
    self.assertTrue(self.large_gmp != self.large_gmp2)
    self.assertFalse(self.large_gmp != self.large_gmp)
    self.assertTrue(self.large_gmp2 != self.large_gmp)

  def testNotEqualsPyFloat(self):
    self.assertTrue(self.large_gmp != 5000000.1)
    self.assertFalse(self.large_gmp3 != 5000000.1)
    self.assertTrue(self.large_gmp != 5000000.0)

  def testPyFloatNotEquals(self):
    self.assertTrue(5000000.1 != self.large_gmp)
    self.assertFalse(5000000.1 != self.large_gmp3)
    self.assertTrue(5000000.0 != self.large_gmp)

class TestFloatAdditionals(unittest2.TestCase):

  def setUp(self):
    self.small_gmp = gmp.Float(10.1)
    self.small_gmp2 = gmp.Float(12.2)
    self.large_gmp = gmp.Float("4294967300.10")
    self.small_neg_gmp = gmp.Float(-10.1)
    self.large_neg_gmp = gmp.Float("-4294967300.10")
    self.prec_gmp  = gmp.Float("10.4294967300101010")
    self.prec_neg_gmp  = gmp.Float("-10.4294967300101010")

  def testNegation(self):
    self.assertEqual(-self.large_gmp, self.large_neg_gmp);
    self.assertEqual(-self.large_neg_gmp, self.large_gmp);
    self.assertEqual(-self.prec_gmp, self.prec_neg_gmp);
    self.assertEqual(-self.prec_neg_gmp, self.prec_gmp);
    self.assertEqual(-gmp.Float(0.0), gmp.Float(0.0));

  def testAbsolute(self):
    self.assertEqual(abs(self.large_gmp), self.large_gmp);
    self.assertEqual(abs(self.large_neg_gmp), self.large_gmp);
    self.assertEqual(abs(self.prec_gmp), self.prec_gmp);
    self.assertEqual(abs(self.prec_neg_gmp), self.prec_gmp);
    self.assertEqual(abs(gmp.Float(0.0)), gmp.Float(0.0));

class TestFloatErrorCases(unittest2.TestCase):

  def testDivisionBy0(self):
    #TODO Removed for now - crashes in c
    i = gmp.Float(0.1)
    self.assertTrue(0)
    #self.assertRaises(ValueError, gmp.Float(0.1) / gmp.Float(0.0))
    #self.assertRaises(ValueError, i /= gmp.Float(0.0))

  def testModBy0(self):
    #TODO Removed for now - crashes in c
    i = gmp.Float(0.1)
    self.assertTrue(0)
    #self.assertRaises(ValueError, gmp.Float(0.1) % gmp.Float(0.0))
    #self.assertRaises(ValueError, i %= gmp.Float(0.0))

class TestFloatPyTypeCompatibility(unittest2.TestCase):

  def testIntCompatibility(self):
    print "TODO: Tests for interation with python ints"

  def testBoolCompatibility(self):
    print "TODO: Tests for interation with python Booleans"

  def testLongCompatibility(self):
    print "TODO: Tests for interation with python longs"

  def testComplexCompatibility(self):
    print "TODO: Tests for interation with python complex"


if __name__ == '__main__':
  unittest2.main()
