#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2

from mom.builtins import b
from mom.codec import base64_encode, hex_encode
from mom.security.hash import sha1_hex_digest, md5_digest, \
    sha1_digest, sha1_base64_digest, md5_hex_digest, md5_base64_digest, \
    hmac_sha1_digest, hmac_sha1_base64_digest
from mom.tests.constants import unicode_string, unicode_string2

input_md5_digest = b('\xe8\x0bP\x17\t\x89P\xfcX\xaa\xd8<\x8c\x14\x97\x8e')
input_sha1_digest = b('\x1f\x8a\xc1\x0f#\xc5\xb5\xbc\x11g\xbd\xa8K\x83>\\\x05zw\xd2')
inputs = [b("ab"), b("cd"), b("ef")]
unicode_inputs = [unicode_string, unicode_string2]

# HMAC-SHA1 data.
key = b("kd94hf93k423kf44&pfkkdhi9sl3r4s00")
base_string = b("""GET&\
http%3A%2F%2Fphotos.example.net%2Fphotos&\
file%3Dvacation.jpg%26\
oauth_consumer_key%3Ddpf43f3p2l4k3l03%26\
oauth_nonce%3DchapoH%26\
oauth_signature_method%3DHMAC-SHA1%26\
oauth_timestamp%3D137131202%26\
oauth_token%3Dnnch734d00sl2jdk%26\
size%3Doriginal""")
expected_hmac_sha1_digest = b('1\xdaPqO"=%#Z\x83\x7fP3,+k.\x8b\xd2')
expected_hmac_sha1_base64_digest = b("MdpQcU8iPSUjWoN/UDMsK2sui9I=")


class Test_sha1_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(sha1_digest(*inputs), input_sha1_digest)

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, sha1_digest, *unicode_inputs)

class Test_sha1_hex_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(sha1_hex_digest(*inputs), hex_encode(input_sha1_digest))

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, sha1_hex_digest, *unicode_inputs)

class Test_sha1_base64_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(sha1_base64_digest(*inputs), base64_encode(input_sha1_digest))

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, sha1_base64_digest, *unicode_inputs)

class Test_md5_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(md5_digest(*inputs), input_md5_digest)

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, md5_digest, *unicode_inputs)

class Test_md5_hex_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(md5_hex_digest(*inputs), hex_encode(input_md5_digest))

class Test_md5_base64_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(md5_base64_digest(*inputs), base64_encode(input_md5_digest))

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, md5_base64_digest, *unicode_inputs)

class Test_hmac_sha1_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(hmac_sha1_digest(key, base_string), expected_hmac_sha1_digest)

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, hmac_sha1_digest, *unicode_inputs)

class Test_hmac_sha1_base64_digest(unittest2.TestCase):
    def test_value(self):
        self.assertEqual(hmac_sha1_base64_digest(key, base_string), expected_hmac_sha1_base64_digest)

    def test_raises_TypeError_when_not_bytes(self):
        self.assertRaises(TypeError, hmac_sha1_base64_digest, *unicode_inputs)
