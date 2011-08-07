#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.net.http.datauri import datauri_encode, datauri_decode

png = '''\
\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\
\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\
\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\
\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82'''

png_data_uri = '''\
data:image/png;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='''

png_data_uri_quoted = '''\
data:image/png,\
%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%00%05%00%00%00%05%08\
%06%00%00%00%8Do%26%E5%00%00%00%1CIDAT%08%D7c%F8%FF%FF%3F%C3\
%7F%06+%05%C3+%12%84%D01%F1%82X%CD%04%00%0E%F55%CB%D1%8E%0E%1F\
%00%00%00%00IEND%AEB%60%82'''

sample_data_uri = '''\
data:text/css;charset=utf-8;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='''

no_meta_data_uri = '''\
data:;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='''


class Test_encoding(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(datauri_encode(png, 'image/png', charset=None),
                         png_data_uri)
        self.assertEqual(datauri_encode(png, 'image/png',
                                        charset=None, encoder=None),
                         png_data_uri_quoted)

class Test_identity(unittest2.TestCase):
    def test_identity(self):
        self.assertEqual(
            datauri_decode(datauri_encode(png, 'image/png', charset=None)),
            (png, ('image', 'png', {}))
        )
        self.assertEqual(
            datauri_decode(datauri_encode(png, 'image/png',
                                          charset=None, encoder=None)),
            (png, ('image', 'png', {}))
        )

class Test_decoding(unittest2.TestCase):
    def test_decoding(self):
        raw_bytes, mime_type = datauri_decode(sample_data_uri)
        self.assertEqual(raw_bytes, png)
        self.assertEqual(mime_type[:2], ('text', 'css'))
        self.assertDictEqual(mime_type[2], {
            'charset': 'utf-8',
        })

    def test_decoding_no_metadata(self):
        raw_bytes, mime_type = datauri_decode(no_meta_data_uri)
        self.assertEqual(raw_bytes, png)
        self.assertEqual(mime_type[:2], ('text', 'plain'))
        self.assertDictEqual(mime_type[2], {
            'charset': 'US-ASCII',
        })

