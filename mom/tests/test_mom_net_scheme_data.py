#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import unittest2
from mom.builtins import b
from mom.codec import base64_decode
from mom.net.scheme.data import data_urlencode, data_urlparse
from mom.tests.constants import UNICODE_STRING


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


PNG_BIN = b('''\
\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\
\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\
\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\
\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82''')

PNG_DATA_URI = b('''\
data:image/png;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==''')

PNG_DATA_URI_QUOTED = b('''\
data:image/png,\
%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%00%05%00%00%00%05%08%06%00%00%00%8\
Do%26%E5%00%00%00%1CIDAT%08%D7c%F8%FF%FF%3F%C3%7F%06%20%05%C3%20%12%84%D01\
%F1%82X%CD%04%00%0E%F55%CB%D1%8E%0E%1F%00%00%00%00IEND%AEB%60%82''')

SAMPLE_DATA_URI = b('''\
data:text/css;charset=utf-8;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==''')

NO_META_DATA_URI = b('''\
data:;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==''')

RFC_BASE64_GIF = b('''R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw\
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz\
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp\
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl\
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis\
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH\
hhx4dbgYKAAA7''')
RFC_GIF = base64_decode(RFC_BASE64_GIF)

RFC_GIF_DATA_URI = b('''\
data:image/gif;base64,R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw\
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz\
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp\
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl\
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis\
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH\
hhx4dbgYKAAA7''')

RFC_NOTE_DATA_URI = b('data:,A%20brief%20note')
RFC_NOTE_DECODED = (b('A brief note'), (b('text'), b('plain'),
                                          {b('charset'): b('US-ASCII')}))

class Test_encoding(unittest2.TestCase):
  def test_encoding(self):
    self.assertEqual(data_urlencode(PNG_BIN, b('image/png'), charset=None),
                     PNG_DATA_URI)
    self.assertEqual(data_urlencode(PNG_BIN, b('image/png'),
                                    charset=None, encoder=None),
                     PNG_DATA_URI_QUOTED)

    self.assertEqual(data_urlencode(RFC_GIF, b('image/gif'),
                                    charset=None),
                     RFC_GIF_DATA_URI)
    #        self.assertEqual(dataurl_encode(rfc_gif, b('image/gif'),
    #                                        charset=None),
    #                         rfc_gif_data_url_quoted)
    self.assertEqual(data_urlencode(b('A brief note'),
                                    b(''),
                                    b(''), None), RFC_NOTE_DATA_URI)


  def test_raises_TypeError_when_not_raw_bytes(self):
    self.assertRaises(TypeError,
                      data_urlencode, UNICODE_STRING, b('text/plain'),
                      b("utf-8"))
    self.assertRaises(TypeError,
                      data_urlencode, None, b('text/plain'), b("utf-8"))


class Test_identity(unittest2.TestCase):
  def test_identity(self):
    self.assertEqual(
      data_urlparse(data_urlencode(PNG_BIN, b('image/png'), charset=None)),
      (PNG_BIN, (b('image'), b('png'), {}))
    )
    self.assertEqual(
      data_urlparse(data_urlencode(PNG_BIN, b('image/png'),
                                   charset=None, encoder=None)),
      (PNG_BIN, (b('image'), b('png'), {}))
    )


class Test_parsing(unittest2.TestCase):
  def test_parsing(self):
    raw_bytes, mime_type = data_urlparse(SAMPLE_DATA_URI)
    self.assertEqual(raw_bytes, PNG_BIN)
    self.assertEqual(mime_type[:2], (b('text'), b('css')))
    self.assertDictEqual(mime_type[2], {
      b('charset'): b('utf-8'),
      })
    raw_bytes, mime_type = data_urlparse(RFC_NOTE_DATA_URI)
    self.assertEqual(raw_bytes, b('A brief note'))
    self.assertEqual(mime_type[:2], (b('text'), b('plain')))
    self.assertDictEqual(mime_type[2], {
      b('charset'): b('US-ASCII'),
      })


  def test_parsing_no_metadata(self):
    raw_bytes, mime_type = data_urlparse(NO_META_DATA_URI)
    self.assertEqual(raw_bytes, PNG_BIN)
    self.assertEqual(mime_type[:2], (b('text'), b('plain')))
    self.assertDictEqual(mime_type[2], {
      b('charset'): b('US-ASCII'),
      })


  def test_raises_TypeError_when_not_raw_bytes(self):
    self.assertRaises(TypeError, data_urlparse, UNICODE_STRING)
    self.assertRaises(TypeError, data_urlparse, None)
