#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.codec.base85 import b85decode, b85encode, _b85encode, _b85decode

class Test_base85_codec_identity(unittest2.TestCase):
    def test_codec_identity(self):
        # Encodes 5 characters into 4.
        s = b85decode('!!!!#')
        self.assertEqual(4, len(s))
        self.assertEqual(0, ord(s[0]))
        self.assertEqual(0, ord(s[1]))
        self.assertEqual(0, ord(s[2]))
        self.assertEqual(1, ord(s[3]))
        self.assertEqual('!!!!#', b85encode(s))


class Test__base85_codec_identity(unittest2.TestCase):
    def test_codec_identity(self):
        # Encodes 5 characters into 4.
        s = _b85decode('!!!!#')
        self.assertEqual(4, len(s))
        self.assertEqual(0, ord(s[0]))
        self.assertEqual(0, ord(s[1]))
        self.assertEqual(0, ord(s[2]))
        self.assertEqual(1, ord(s[3]))
        self.assertEqual('!!!!#', _b85encode(s))


class Test_base85_speed(unittest2.TestCase):
    def test_speed(self):
        from time import clock
        s = '!!!!#' * 10

        number_of_times = 1000

        t0 = clock()
        for i in range(number_of_times):
            b85decode(s)
        t1 = clock()
        b85_decode_time = t1 - t0

        t0 = clock()
        for i in range(number_of_times):
           _b85decode(s)
        t1 = clock()
        _b85_decode_time = t1 - t0

        s = b85decode('!!!!#' * 10)

        t0 = clock()
        for i in range(number_of_times):
           b85encode(s)
        t1 = clock()
        b85_encode_time = t1 - t0

        t0 = clock()
        for i in range(number_of_times):
            _b85encode(s)
        t1 = clock()
        _b85_encode_time = t1 - t0

        self.assertTrue(b85_decode_time <= _b85_decode_time)
        self.assertTrue(b85_encode_time <= _b85_encode_time)
