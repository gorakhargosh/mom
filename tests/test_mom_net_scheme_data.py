#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest2
from mom.builtins import b
from mom.codec import base64_decode
from mom.net.scheme.data import data_urlencode, data_urlparse
from tests.test_mom_builtins import unicode_string

png = b('''\
\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\
\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\
\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\
\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82''')

png_data_url = b('''\
data:image/png;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==''')

png_data_url_quoted = b('''\
data:image/png,\
%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%00%05%00%00%00%05%08%06%00%00%00%8\
Do%26%E5%00%00%00%1CIDAT%08%D7c%F8%FF%FF%3F%C3%7F%06%20%05%C3%20%12%84%D01\
%F1%82X%CD%04%00%0E%F55%CB%D1%8E%0E%1F%00%00%00%00IEND%AEB%60%82''')

sample_data_url = b('''\
data:text/css;charset=utf-8;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==''')

no_meta_data_url = b('''\
data:;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==''')

rfc_base64_gif = b('''R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw\
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz\
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp\
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl\
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis\
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH\
hhx4dbgYKAAA7''')
rfc_gif = base64_decode(rfc_base64_gif)

rfc_gif_data_url = b('''\
data:image/gif;base64,R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw\
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz\
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp\
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl\
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis\
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH\
hhx4dbgYKAAA7''')

rfc_note_data_url = b('data:,A%20brief%20note')
rfc_note_decoded = (b('A brief note'), (b('text'), b('plain'),
                                        {b('charset'): b('US-ASCII')}))

class Test_encoding(unittest2.TestCase):
    def test_encoding(self):
        self.assertEqual(data_urlencode(png, b('image/png'), charset=None),
                         png_data_url)
        self.assertEqual(data_urlencode(png, b('image/png'),
                                        charset=None, encoder=None),
                         png_data_url_quoted)

        self.assertEqual(data_urlencode(rfc_gif, b('image/gif'),
                                        charset=None),
                         rfc_gif_data_url)
#        self.assertEqual(dataurl_encode(rfc_gif, b('image/gif'),
#                                        charset=None),
#                         rfc_gif_data_url_quoted)
        self.assertEqual(data_urlencode(b('A brief note'),
                                        b(''),
                                        b(''), None), rfc_note_data_url)
        

    def test_raises_TypeError_when_not_raw_bytes(self):
        self.assertRaises(TypeError,
            data_urlencode, unicode_string, b('text/plain'), b("utf-8"))
        self.assertRaises(TypeError,
            data_urlencode, None, b('text/plain'), b("utf-8"))


class Test_identity(unittest2.TestCase):
    def test_identity(self):
        self.assertEqual(
            data_urlparse(data_urlencode(png, b('image/png'), charset=None)),
            (png, (b('image'), b('png'), {}))
        )
        self.assertEqual(
            data_urlparse(data_urlencode(png, b('image/png'),
                                          charset=None, encoder=None)),
            (png, (b('image'), b('png'), {}))
        )


class Test_decoding(unittest2.TestCase):
    def test_decoding(self):
        raw_bytes, mime_type = data_urlparse(sample_data_url)
        self.assertEqual(raw_bytes, png)
        self.assertEqual(mime_type[:2], (b('text'), b('css')))
        self.assertDictEqual(mime_type[2], {
            b('charset'): b('utf-8'),
        })
        raw_bytes, mime_type = data_urlparse(rfc_note_data_url)
        self.assertEqual(raw_bytes, b('A brief note'))
        self.assertEqual(mime_type[:2], (b('text'), b('plain')))
        self.assertDictEqual(mime_type[2], {
            b('charset'): b('US-ASCII'),
        })


    def test_decoding_no_metadata(self):
        raw_bytes, mime_type = data_urlparse(no_meta_data_url)
        self.assertEqual(raw_bytes, png)
        self.assertEqual(mime_type[:2], (b('text'), b('plain')))
        self.assertDictEqual(mime_type[2], {
            b('charset'): b('US-ASCII'),
        })


