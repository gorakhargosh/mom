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

from os import path
from mom import _compat
from mom import builtins
from mom import codec

if _compat.HAVE_PYTHON3:
  from mom.tests import py3kconstants as pyxkconstants
else:
  from mom.tests import py2kconstants as pyxkconstants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


b = builtins.b


TEST_DIR_PATH = path.realpath(path.abspath(path.dirname(__file__)))

IMAGES_DIR_PATH = path.join(TEST_DIR_PATH, "images")

UNICODE_STRING = pyxkconstants.UNICODE_STRING
UNICODE_STRING2 = pyxkconstants.UNICODE_STRING2
FOO = pyxkconstants.FOO
UFOO = pyxkconstants.UFOO
JSON_FOO = pyxkconstants.JSON_FOO
JSON_UFOO = pyxkconstants.JSON_UFOO
JSON_UNICODE_VALUE = pyxkconstants.JSON_UNICODE_VALUE
UNICODE_VALUE = pyxkconstants.UNICODE_VALUE
X_BYTE = pyxkconstants.X_BYTE
UTF8_BYTES = pyxkconstants.UTF8_BYTES
UTF8_BYTES2 = pyxkconstants.UTF8_BYTES2
LATIN1_BYTES = pyxkconstants.LATIN1_BYTES


PNG = b("""\
\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\x00\x00\x00\x05\
\x08\x06\x00\x00\x00\x8do&\xe5\x00\x00\x00\x1cIDAT\x08\xd7c\xf8\xff\
\xff?\xc3\x7f\x06 \x05\xc3 \x12\x84\xd01\xf1\x82X\xcd\x04\x00\x0e\
\xf55\xcb\xd1\x8e\x0e\x1f\x00\x00\x00\x00IEND\xaeB`\x82""")


PNG_DATA_URI = b("""\
data:image/png;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==""")


PNG_DATA_URI_QUOTED = b("""\
data:image/png,\
%89PNG%0D%0A%1A%0A%00%00%00%0DIHDR%00%00%00%05%00%00%00%05%08%06%00%00%00%8\
Do%26%E5%00%00%00%1CIDAT%08%D7c%F8%FF%FF%3F%C3%7F%06%20%05%C3%20%12%84%D01\
%F1%82X%CD%04%00%0E%F55%CB%D1%8E%0E%1F%00%00%00%00IEND%AEB%60%82""")


SAMPLE_DATA_URI = b("""\
data:text/css;charset=utf-8;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==""")


NO_META_DATA_URI = b("""\
data:;base64,\
iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBK\
E0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==""")


RFC_BASE64_GIF = b("""R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw\
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz\
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp\
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl\
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis\
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH\
hhx4dbgYKAAA7""")
RFC_GIF = codec.base64_decode(RFC_BASE64_GIF)


RFC_GIF_DATA_URI = b("""\
data:image/gif;base64,R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw\
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz\
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp\
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl\
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis\
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH\
hhx4dbgYKAAA7""")


RFC_NOTE_DATA_URI = b("data:,A%20brief%20note")
RFC_NOTE_DECODED = (b("A brief note"), (b("text"), b("plain"),
                                        {b("charset"): b("US-ASCII")}))

# Images for testing data URIs.
IMAGES_FILE_GIF_PATH = path.join(IMAGES_DIR_PATH, "file.gif")
IMAGES_FILE_PNG_PATH = path.join(IMAGES_DIR_PATH, "file.png")
IMAGES_FILE_JPG_PATH = path.join(IMAGES_DIR_PATH, "file.jpg")

# Binary data for the images/file.gif file.
IMAGES_FILE_GIF = b("""\
GIF87a \x00 \x00\xf7\x00\x00IL}OS\x7fY\\\x7fYhyLO\x81LP\x81VZ\x89VZ\
\x89VZ\x89VZ\x89Cl\x95\\a\x8a\\a\x8a]d\x91^r\x88Vu\x93Vu\x93K|\xadN\
\x7f\xb0U|\xa8eh\x86eh\x86eh\x86eh\x86ei\x95ei\x95ei\x95fr\x80ir\x9air\
\x9awx\x8bwx\x8bsw\x99sw\x99sw\x99L\x83\xb6L\x83\xb6Z\x81\xabU\x88\xb9U\
\x88\xb9U\x88\xb9U\x88\xb9}\x86\x9a}\x86\x9af\x83\xa1k\x90\xb5|\x8b\
\xaa|\x8b\xaau\x95\xb8u\x95\xb8u\x95\xb8u\x95\xb8X\x8e\xc0X\x8e\xc0]\
\x91\xc2h\x98\xc7h\x98\xc7h\x98\xc7h\x98\xc7r\x9c\xc5r\x9c\xc5w\xa2\
\xcdw\xa2\xcd}\xa7\xd0}\xa7\xd0\x83\x83\x87\x83\x83\x87\x82\x88\x9e\
\x82\x88\x9e\x97\x97\x98\x97\x97\x98\x87\x8b\xac\x87\x8b\xac\x87\x8b\
\xac\x8d\x97\xa9\x8d\x97\xa9\x8d\x97\xa9\x87\x99\xb7\x87\x99\xb7\x87\
\x99\xb7\x87\x99\xb7\x87\x99\xb7\x97\x9d\xa3\x97\x9d\xa3\x99\x9c\xb8\
\x99\x9c\xb8\x8e\xa3\xbf\x9c\xa1\xa6\x98\xa9\xbc\x98\xa9\xbc\xa5\xa6\
\xa7\xa5\xa6\xa7\xa5\xa6\xa7\xa6\xab\xb6\xa6\xab\xb6\xa6\xab\xb6\xa6\
\xab\xb6\xaa\xb2\xbb\xaa\xb2\xbb\xaa\xb2\xbb\xb6\xb7\xb8\xb6\xb7\xb8\
\xb6\xb7\xb8\x87\xa7\xc7\x87\xa7\xc7\x87\xa7\xc7\x85\xad\xd3\x85\xad\
\xd3\x8c\xb2\xd7\x8c\xb2\xd7\x95\xaa\xc5\x95\xaa\xc5\x95\xaa\xc5\x95\
\xaa\xc5\x9a\xb1\xc8\x9a\xb1\xc8\x9a\xb1\xc8\x96\xb9\xdb\x96\xb9\xdb\
\x96\xb9\xdb\xa6\xa8\xc1\xa6\xa8\xc1\xa6\xa8\xc1\xa7\xb8\xc9\xa7\xb8\
\xc9\xa7\xb8\xc9\xa7\xb8\xc9\xa5\xbb\xd5\xa5\xbb\xd5\xa5\xbb\xd5\xb2\
\xb8\xc6\xb2\xb8\xc6\xb2\xb8\xc6\xb2\xb8\xc6\xbe\xbf\xd1\x9f\xc0\xe1\
\xa7\xc0\xdb\xa7\xc0\xdb\xbb\xc2\xc9\xbb\xc2\xc9\xbb\xc2\xc9\xb7\xc6\
\xd6\xb7\xc6\xd6\xb7\xc6\xd6\xb7\xc6\xd6\xaa\xc7\xe4\xaa\xc7\xe4\xaa\
\xc7\xe4\xaa\xc7\xe4\xb4\xce\xe9\xb4\xce\xe9\xba\xd2\xea\xba\xd2\xea\
\xba\xd2\xea\xbe\xd7\xf0\xbe\xd7\xf0\xc5\xc6\xc7\xc5\xc6\xc7\xc5\xc6\
\xc7\xc5\xc6\xc7\xc7\xc9\xd6\xc7\xc9\xd6\xc7\xc9\xd6\xc7\xc9\xd6\xc7\
\xc9\xd6\xcb\xd2\xda\xcb\xd2\xda\xcb\xd2\xda\xd6\xd7\xd8\xd6\xd7\xd8\
\xd6\xd7\xd8\xd6\xd7\xd8\xc7\xd8\xe9\xc7\xd8\xe9\xc7\xd8\xe9\xc7\xd8\
\xe9\xc7\xd8\xe9\xc6\xdd\xf4\xd3\xdc\xe7\xd3\xdc\xe7\xd3\xdc\xe7\xcd\
\xe2\xf6\xcd\xe2\xf6\xda\xe3\xeb\xda\xe3\xeb\xd8\xe8\xf8\xd8\xe8\xf8\
\xd8\xe8\xf8\xd8\xe8\xf8\xd8\xe8\xf8\xd8\xe8\xf8\xe7\xe8\xe8\xe7\xe8\
\xe8\xe7\xe8\xe8\xe7\xe8\xe8\xe6\xed\xf4\xe6\xed\xf4\xe6\xed\xf4\xe6\
\xf1\xfd\xe6\xf1\xfd\xf9\xfa\xfa\xf9\xfa\xfa\xf9\xfa\xfa\x00\x00\x00\
\x00\x00\x00\x00\x00\x000\x0c\x01\x00\x00\x00p\xe3\xbf_\xff\x7f\x00\
\x00\xfe\xff\xff\xff\xff\xff\xff\xff\xa0\xcfrt\xff\x7f\x00\x00 \x00\
\x00\x00\x00\x00\x00\x00\x00\xdaj\x01\x01\x00\x00\x00\xc0\xe0v\x01\
\x01\x00\x00\x00\x10\xe4\xbf_\xff\x7f\x00\x00/\xe0\xf5\x8c\xff\x7f\
\x00\x00=\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\
\x00\xdaj\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00h\xe2j\
\x01\x01\x00\x00\x00P\xe2j\x01\x01\x00\x00\x00`\xe2j\x01\x01\x00\x00\
\x00X\xe2j\x01\x01\x00\x00\x00!\xf9\x04\x01\x00\x00\xcb\x00,\x00\x00\
\x00\x00 \x00 \x00\x00\x08\xff\x00\x97\t\x1cH\xb0\xa0\xc1\x83\x08\
\x13*\\\x98\x10\x19\xa8#\x1c\x0c\x140\x80\xe1\x08(d\x0c\x0f"\xa3b\
\x80J\xa9a\xc8\x90\r\x93\xd5\xe8HG\x8c\x19\x05\x82Z h\xd8\xad[!\x91ua\
\xc5J\x96\xac&\x06@\xa5\xc4\xc3a\xd80T\x1f\x91\x95\xba\xd2\x88\x95\
\xa6K K5\xc0\xc3\x10\xcf\x11d\x9cJ\x95\x12\x94\x8bL\xa3\\\xa0h\xfe\
\x04\xf5k\x18\x08\xa6\tA\x81\x10\x9a\x0bYWc\xb7\x8c\xe5Z\xcbJQ\x17\
\x90\xc3~5\xd0\xa9\x11CL\x91\xa5\x14\x19\xdb\xab\x96U\xa9\xbbqQ-@Y\
\x10\x8f\xa0\xbb\xa8\x14\xa5\xe5\xbb\xf6n\xc8_\xbf\x94\x80%\x88lpL2T\
\xf9\xee\xcd\xf5S\x89\xa2R\xbf\xccB6@X%\x95\x98Q53\x96z\xab\x91\x1b7\
\x82 \xff\x02Aw\xe0\x11Y\xc8P\xa1\xc2\x92K\xb5\xda\xb2we\xeb\xeer\
\xa4 \x07dR\xe4\xec\xd1T\xab7c\xce\x8e\x91}F\xa5DP\x83\x82\xa4\xf7\
\\\xba\xa4)V\xf3\xb5kkE\xff\x17\x19F7\x16\x03\x05\x0btE\x15\x89{,\
\xef\xb5\xe2\x8b\x8f>\xac\x8b\xa2\rr\x08`\xbf\x05\xbb\xd1HY\x9a\
\x04xT%09\xf6Kb,\xc8\x81\x1eA\x18\xb0rH\x1dr\xc4\xc4J%\x14V\x12\xc9\
\x1f\x9ct\x11FH\x81q\xf2\x80\x15\x18\x14t\xc4\x1f\x91\xb0\xc1\xca]\
\xa0D\x12\xc9!\x0f\xaa\xc1\x86\x1a>\xfdr\x0b*\x03\xc0\xe0Bq\x04\x81\
\xe2\xc2%j\x14\x18\xd30\x88\xd4Q\x07\x1b/\xfe`\x88\x8c\xa8\x90\xa1\
\x80\x15\x1c\xd4&\x102\x06\xf0\xb8GtC\x10\xa9\xc6\x0f=\xf4 \xc7\x8c\
\xa5h1\x81\x15\xa4\x19\x84G\x13\x91\xf4\xf0WL\xa8\xecp%\x96;\xdc\xb0\
\x07P\x9ch\xd1\x04\x07\x93Q\xd6\x00"l\xec\x80JW\xc3p\xb2C\x96m\xde`\
\x03\x16\xa0\xc4\xe9\x00N\xa5\x11dH\x03\x91\xfc\xa0\x08da<p\xc3\xa4\
\x82\xd2`B\x0b\x9c("\x05N-i\x14\x19\x07\x88(\xa2\x9b\n6\x94J\x83\xa5#\
\x8c \x01\x19d(\xb1\xc0\x10\\%\x96\xba\xccO\x9c\xa8\xb0\x80!\xa8h\xa1\
\x80\t\xbc\xa6:B\x04\x11\x94\xa0\xc4\x10\x06\x80@\x06\'{\x1aD+\x19C\
\x140\x04\x16r\xec`\x83\t\x12HPB\x0bV0I\x80\x07Z\x1c\x8b\xca0\x06\x99\
\x85\n\'d\x14AA\x01\x1c4a\x85\x1br\xb8\xd1\x84\x0b\r\x14@A\x10E\xd8\
\xb7\xa7\xac\xcb\x88K\xae\x16Ex @\x00\x05\x00\x00@\x00\x02l@o\xb7\xc8\
\x86\xd6\xd0\x81\xa5\xec\xcbo\x11\x10C\xacE\xb7\x8a\x80\x82JH\x0c=\xa6\
\x1b\'\x99*\xe21\xc7\xa5\xdc\x9bRA\x80\x81\x14\x93B\x01\x01\x00;""")


# Data URI for the images/file.gif file.
IMAGES_FILE_GIF_DATA_URI = b("""\
data:image/gif;base64,R0lGODdhIAAgAPcAAElMfU9Tf1lcf1loeUxPgUxQgVZaiV\
ZaiVZaiVZaiUNslVxhilxhil1kkV5yiFZ1k1Z1k0t8rU5/sFV8qGVohmVohmVohmVohm\
VplWVplWVplWZygGlymmlymnd4i3d4i3N3mXN3mXN3mUyDtkyDtlqBq1WIuVWIuVWIuV\
WIuX2Gmn2GmmaDoWuQtXyLqnyLqnWVuHWVuHWVuHWVuFiOwFiOwF2RwmiYx2iYx2iYx2\
iYx3KcxXKcxXeizXeizX2n0H2n0IODh4ODh4KInoKInpeXmJeXmIeLrIeLrIeLrI2XqY\
2XqY2XqYeZt4eZt4eZt4eZt4eZt5edo5edo5mcuJmcuI6jv5yhppipvJipvKWmp6Wmp6\
Wmp6artqartqartqartqqyu6qyu6qyu7a3uLa3uLa3uIenx4enx4enx4Wt04Wt04yy14\
yy15WqxZWqxZWqxZWqxZqxyJqxyJqxyJa525a525a526aowaaowaaowae4yae4yae4ya\
e4yaW71aW71aW71bK4xrK4xrK4xrK4xr6/0Z/A4afA26fA27vCybvCybvCybfG1rfG1r\
fG1rfG1qrH5KrH5KrH5KrH5LTO6bTO6brS6rrS6rrS6r7X8L7X8MXGx8XGx8XGx8XGx8\
fJ1sfJ1sfJ1sfJ1sfJ1svS2svS2svS2tbX2NbX2NbX2NbX2MfY6cfY6cfY6cfY6cfY6c\
bd9NPc59Pc59Pc583i9s3i9trj69rj69jo+Njo+Njo+Njo+Njo+Njo+Ofo6Ofo6Ofo6O\
fo6Obt9Obt9Obt9Obx/ebx/fn6+vn6+vn6+gAAAAAAAAAAADAMAQAAAHDjv1//fwAA/v\
////////+gz3J0/38AACAAAAAAAAAAANpqAQEAAADA4HYBAQAAABDkv1//fwAAL+D1jP\
9/AAA9AAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAADaagEBAAAAAAAAAAAAAA\
Bo4moBAQAAAFDiagEBAAAAYOJqAQEAAABY4moBAQAAACH5BAEAAMsALAAAAAAgACAAAA\
j/AJcJHEiwoMGDCBMqXJgQGagjHAwUMIDhCChkDA8io2KASqlhyJANk9XoSEeMGQWCWi\
Bo2K1bIZF1YcVKlqwmBkClxMNh2DBUH5GVutKIlaZLIEs1wMMQzxFknEqVEpSLTKNcoG\
j+BPVrGAimCUGBEJoLWVdjt4zlWstKUReQw3410KkRQ0yRpRQZ26uWVam7cVEtQFkQj6\
C7qBSl5bv2bshfv5SAJYhscEwyVPnuzfVTiaJSv8xCNkBYJZWYUTUzlnqrkRs3giD/Ak\
F34BFZyFChwpJLtdqyd2Xr7nKkIAdkUuTs0VSrN2POjpF9RqVEUIOCpPdcuqQpVvO1a2\
tF/xcZRjcWAwULdEUViXss77Xii48+rIuiDXIIYL8Fu9FIWZoEeFQlMDn2S2IsyIEeQR\
iwckgdcsTESiUUVhLJH5x0EUZIgXHygBUYFHTEH5GwwcpdoEQSySEPqsGGGj79cgsqA8\
DgQnEEgeLCJWoUGNMwiNRRBxsv/mCIjKiQoYAVHNQmEDIG8LhHdEMQqcYPPfQgx4ylaD\
GBFaQZhEcTkfTwV0yo7HAlljvcsAdQnGjRBAeTUdYAImzsgEpXw3CyQ5Zt3mADFqDE6Q\
BOpRFkSAOR/KAIZGE8cMOkgtJgQgucKCIFTi1pFBkHiCiimwo2lEqDpSOMIAEZZCixwB\
BcJZa6zE+cqLCAIahooYAJvKY6QgQRlKDEEAaAQAYnexpEKxlDFDAEFnLsYIMJEkhQQg\
tWMEmAB1oci8owBpmFCidkFEFBARw0YYUbcrjRhAsNFEBBEEXYt6esy4hLrhZFeCBAAA\
UAAEAAAmxAb7fIhtbQgaXsy28REEOsRbeKgIJKSAw9phsnmSriMcel3JtSQYCBFJNCAQ\
EAOw==""")

# Binary data for the images/file.png file.
IMAGES_FILE_PNG = b("""\
\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\
\x00\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x08\x82IDATX\x85\xe5\x97[l\x1c\xd5\x1d\xc6\x7fs\xd9]\xef\xae\xd7\
\xf6\xc6kc\x878v\x9c\xc4ML.`\xd3\x04\xe3&A\t)\xd7\x16\x04\x0f \x9eR*Z\
\xb5*R\xa9\xe0\xa1\x0fEj\xa5\xaa\x17\x1e\xb8\x14\xa9-\x12I[\x15ZZ\xa0%\
\xe2NR\x02\x98$\xe4b\x93\xc4!1q\x9c\xf8\x92\xf5\xfa\xba\xb6ww.g\xce\xcc\
\xf4a\xc7&\x0e\x0e*j\xdfz\xa4O\xa3\x9d9:\xff\xdf\xf9\xbe3g\xcf\xc0\xff\
{S\xbeL\xe7\xd6\xd6\xef\xc4\xc2\xe1\xd0M\xa1\x92\xe8\xbd\x8a\xa2\\\xe3IY\
\xe5\xbaNB\xd5B9U\xd5\xc6<\xdf\xefr\x85\xf5W!\x9c\xb7\x8e\x1e}\xc6\xf8\
\x9f\x01\xdcp\xc3\x0f+\x1cWy\xb4$\xa2\x7fo\xeb\x8d-\xda\xf5_[\x1fZ\xb1\
\xbc\x86\xb2x\x84PHg4k\x90\x1e/\xd0w~\x84\x03\xefu\xe6O\x1c\xf9Ds\xa4\
\xf7\xbbHH\xf9\xd9\xbe}OL\xfdW\x00\xed\xed\x0f\xde\xa5\x87C\xbb\xbe\xf5\
\xc07c\xb7\xde\xdc\xa2\x8fgsh\xb8\xac\\\xb6d\xae\xcfo\x9f\xfd3\xcdm7\xa3\
\xf8\x1ea]\x05\xcf\xe5\xd5W:\xc4\x07o~hI\xcf\xdbq\xa0\xe3\xa9\x7f\\n|\
\xed\x8b\x8ao\xda\xf4\xd0O\xeb\xea\xafxb\xe7\xce\x87c\xcb\x1b\xab\xd5\
\xfe\x81Af\n&\x89\xaa%$c\x1a\x07\x0f\x1d\xe6\x85\x97w\xb3d\xe5:"\xf1$\
\x86\xed\x92\xcd\xd9\xac\xac\x8d\xb2\xad\xbdI\xbb\xfa\xab_\x89\x1c9\
\xd4sg*uMhh\xf0\xa3}_\n`\xd3\x96\x1f\xfdxc\xdbU?y\xecW\xdf\x0e\x1f8r\
\x8c)\xc3\x05U\xa3\xff\xc205\xb5\xb5\xbc\xbf\xf7mf\xdc\x18\x1b6\xdf\
\x84\x95\x9f\xc2St\xf4P\x98\xb5u%d\xc7\xd2\x9c:;\xc8\xaa\xc6\xc5\xdcy\
\xc7\xf5\xfa\xd1\xae3\xed\x89\xc4\x1a98p\xb0\xe3\xd2:\x0bF\xb0i\xd3\
\x83\xb7\xd55\\\xf9\xd2\x1fw>\x1c\xd9\xdfu\x9ahu#-u\x11\xd2\xe9\x0c\
\x86^NII\x8c\xa9\xc9\tb\x89r\x1c\xc7\xc5r$\x9e\xe7aN\x8d2\x9c\x19a\
\xf4\xc2y\xee\xba\xe3V\x16%\xa2\x98\xa6\x89m;<\xf0\xdd\'\xed\xc9\xf1\
\xdc\xdd\xfb\xf7\xff\xe6\xb5/\x04hk{(Z\x9a\x08\x0f\xbe\xf8\xe2\xa3\
\x95\x89\xd2(\x00\xb9|\x01G\x08N\x9d\xeea|\xda\xa4\xb5}+\x00\xae\xebb;.\
\x96\x90d\xc7G\xd1\x9d)\xdaZ\xd7\xa2\xaa*\x00\x9e\xe7\x91\xcb\xe5\x10B0:\
\x9a\xe5\xfb?\xf8\xfd\xa4\x14,9p\xe0qs\xb6\x9ez)@\xb8\x84Gv\xdc\x7fK\
\xb2,\x11\x9b\xbb\x97(\x8d\x93\x1e\xce0\x9a\x93,]\xb9\x1a\x1f\xf0\x01U\
\xd3PU\x15EU(O\xa6X\xbbj\x05\x96m#\x1c\xa78\xb8\xaa\xa2i\x1aRJ*+\xcb\
\xb8a\xeb\xea$\xaa\xfb\xf0e\x1dhk{(\x1a\x8d\xebco\xbd\xf1\x8b\xb8\xa6\
\x15\xd9|\xdf\xe7\xf9\x17\xfe\x8e\x0c\x95\xb1\xe1\xfa\xcd\xc4c\xf1y\
\xc0\x8et1l\x87\xda\xa8\xa0\xefl//\xef9D\xebU\xcb\xa9MU\xb0\xac\xfeJ\
\x92\x15\xe5\xe4r9\x0c\xc3\xc0\xf7a\xc7\xfdO\x1a\xae\xa3\xa5f]\x98\xe7\
\x80\xef;\xdbo\xdc\xde\x12\xd6\xf5\xcf\xd6\xe6\xbf\xf6}@\xb2~\x1d[\xb6\
\xddB,\x1a\x9f\x9b\xfd\xac<\xdf\xc7\xf7}\x8e\xf7\xf4\xe3):;\xee\xbd\
\x135\xb1\x98\x8e\xd3\x13\xec|\xb3\x9b\x97^\xdf\x87\xa2(x\x9e\x87\xaek45\
\xd5F|\xdf\xd9>;\xbe>\xcf\xfeh\xe4\xbe\x9b\xb6\xb7\x86\\\xd7\xe5\xe3\
\xe3\xdd(\x8aB\xe7\xb9)\xb6}\xbd\x1d\xcf\x07U\t\xaa\xce\x01\xfbH\xb7x\
\xa3uM#\xe5\xa5\xc5\xd8\x16W\xc6\xb9yc#\xc3\xa3Y\xa2\x11\x1d\xdf\xf7\
\xb0,\x1b[\x08\xae\xdb\xb8B;\xdd\x93\xb9\x0f\xd8\xfd9\x00M\xd364.\xab\
\xe5\xe7\x8f?C\xe4\x8aU\xc4\xc3*k\xafm\xc7r$y[!Q\xa2\xcd+\xee8.B\xba\
\xa4\xc2\x82\xf2\xd2\xb2\xb9ge\x89R\x00V\xd4\xd7\xb2\xfb\x8d=T.JR\x1a\
\r\xf1\xb7\xd7\x8f\xd0\xbc\xb4\x1aW\xca\x8d\xb3}\xe7E\xe0I\x99\x8aF#\
\xa4\x966\xd3\xdc\xd4Hu\xfd*\xa4\xafb\xda\x0e3\x86 \x9b\x17XBb\t\x89iKL!\
\xb1\x85$U^\xc2B\xcd\xf3<\xbe\xb6\xb1\x95\xaeO\x87\x89\x84\xc3\xdc\
\xb5u=c\x05\x89\xaaj\x15\x0b\x028BF3c\x93\xdcs\xe3z\xaa\xf4i\xf2\x05\
\x13\xcb\x96\x18\x96\x83a\n\xa6\xf2\x82\xb1i\x9b\xa9\xbcM\xde\x14\x18\
\xb6\x83\xe2\xfbD\xc2\xe1\x05\x01\x1c\xc7\xc1\xf7=t\xcf\xa4\xb7?\xcd/\
\x9f\xfe\x13^(\x01\x9e_:\xdbg^\x04\xaa\xa6\xe6\xc7\r\xb5\xe2\xd97\x0e\
\xb1r\x91O4.\xd8\xd8\xb0\x92\xd1\xf1\t,bL\x98!TE).>\xcf\xc3u}\x1c)\x89\
\xcbQ\x9a\x9b\x1a?7{!\x04B\x08\xda[Vs~(\x83R\xb1\x1c\xe9\xaa\xa0*\xf9\
\x05\x01P\xb5\xb1\x89l\xbe\xa2\xb2f)C\xb6Kdl\x88\xba\xeaV\xea\xaa\xcb\
(\x14\x0c>\xfc$\xc3\x84\x13\x0b\n\xf8H\xd7CH\x97\xbd\xa39\xd2\xe9\x0f\
\xf9\xb4\xb7\x8fxi)\xf7\xdd};RJl\xdb\xc6\xb6mTUAE29\x9d#?\x93\xc7\xf7\
\x19[0\x02\xf0\xba\xce\x9e\xcb\x90\x88hXBr\xed\xd5k\xe6\x9e\xc4\xe31\
\xb6\xb5\xd4\x93\xf0\'1,A\xde\xb4\xc9\x9b6\x86)\xb0\xfc\x08\xef\x9eS\
\xb9\x10\xbe\x8an\xa3\x8e\x99|\x01\xd34\xb1,k\x0e\xe2\xe9?\xfc\x93%\rM\
\x8cg&}U\xf1;\x17\x04\x90\xb6\xf3\\\xe7\xc1\x13\xb9Ty\x04\xc3r\xa8\x9a\
\xbf\xe7\xa0i\x1a\xb7\xb77\xf3\x8du\t\x14k\x8a\x82Y\x04)\x98\x02_+\xc1\
\x12.\x86\xe5\xd0q\xe4\x14\xa6i\xce\xe9\x93\x9e^\xc6\xd4\xa5\xd4$c\xa4\
\xfb\x06\xf3\x9e\xeb?\xbf \x80\xa2\x84\xde9\xddu\x1a\xc5\xf3\xd0\x14\x9f\
\x03\xc7z\x91Rri\xab\\TN\xf7\xe1\xf7\xc9\x1b\xc5\xe2\x05SP\xb0Dq\xb1\xda\
\x0e}\x99\xe2\xceg\x18\x06\xa6i2==\xc3\xa2d%a\xc5c"=\x8e\xa2\x84\xde\x99\
\x9b\xd4\xc5\x03\x0f\r\x1d\x94\xf5\r\x1bCy\xdbk[\xbb\xaeQ?\xdcgP\xee\x8dQ\
\x99,\xc7\xf3<\xfc`\xd7\xeb>y\x9a\x83\x83\x80\x1e\xc5\n^E[\x14_KK8,K\x85\
\xa8-\xd3\xe6\x1c\x18\x19\x19E\x8d\x94\xd3w\xa2\xcf,LN\xfdz\xff\xfe\xa7\
\xf6^f\r\x80\x14\xeac\xc7:\x8e\xce\xb8\x96IM2\xc6\xae\x8e\tz\xfb\xce3333\
\xa7t&\x83C8p\xe03\x17\x8cY\x17r\xd3\x14\n\x05\x0c\xc3\xa0\xb7\xef<{\x8e\
\x9c\'\xa2\xc0\xf0\xd9\xa1\xbc\xe7\x85\x1f\x9b\x17\xeb\xa5\x00CC\x07e\xaar\
\xf5@\x7f\xcf\xe0m\x9b\xb7^\x13\x9a4|\xaa"&e\xb10B\x08\xde~\xb7\x83]\xaf\
\x1d%\x9cZ\x8e\xed\xb8\xd8\xc1\xc6d9\x12\xcb.\xaa`\x984\xd7\xe8\x98\xa6\
\xc9\x85\xf4\x08\xe5W4\xf1\xd1;\x87\x8d\xec\xf8\xe0#\x9d\x9d\xbb\xce\x00\
\xd6e\x01\x80\xd8\xf0p\xd7xiYC,\xdd?\xbe~\xf3\x96\xf5\xba"\rJ\xc3 \x84`\
\xf7\xdeC\x98\xa9\r\x08\'\xb0>\xb8ZB"\x84\x83\xe7X\xcc\xe4m\x9a\xab$\xaa\
\xa6\xd2?\x9c\xe7H\xc7\x19{4=\xf0\x97\x93\xdd/\xbe\x02\xb8\x80\x13hA\x808\
\x90\x18\x19>\xd6\x1b\tUW\x9c;5\xd0\xb4\xb9}\xb5^]Y\xc6\xde\xf7\x0f\xb2\
\xe7d\x0e\xa2\xa9"\x80#\x11\x8eD\n\x07OX\xf8\x8e\x85/L\x12a\x88\xf8\x16=}c\
\x1c\xde\xdf/2Cg\xdf<\xd9\xfd\xd2s\x80\x08\xe4\x00\xe6\xe5\x00"@\x14\x88\
\x8ed\xba\xcfx24\xf5q\xd7XKzdB-\xa9\xaaU\x96\xafZ\x8b\xea\xbb8\xc2\xc6\
\x976\xd26\t+\x92R\xddgq2\xcc\xea%\x15\xd4\xa7\xe2\xf4\x1c\x1ftOu\xf6\
\xcb\x81s\x87\x9e?\xdb\xbb\xe7u\xc0\x08d\x029\xc0\x86\x85\xcf\x84\x11\
\xa0\x12X\x14(\x19\x8b%\x974,\xdbrOEE\xddu\xd5Kk\xa8kZ\x16J\xa6*()\t\xa1\
\x875,\xc3\xc2,\x18L\x8cLr\xa1w@fG\xb3d\xb3\x03\x9d\xe7\xfa\xde{\xd5\xb2f\
\xd2@\x16\x98\x0c4\x01\x0c\x03\xde\xe5\x00\x08\x1c\xa8\x04*.RY(\x14\xaf\
\xaa\xa9Y\xd3\xb2\xa8\xb2\xe1\xdap\xa4\xacVQ\xf5\x98\x86\x12v=\xcf\xf1|i\
\x08{fdb\xfc\xdc\xf1\x91\x91\x13\xc7\xa5\xb4&\x81\x99@S\x81&\x80L\xb0\x0e\
\xf8"\x80\xd9x\x92@9\x90\x08T\n\xc4\x02\xc0\x08\xc5\xff\x92\xd9\x18=\x8a\
\xd9\x8a\xc0f\x03(\x04vO\x03#\xc1\xef\x8b\x8e4\xff\xd9\xa7\x99\x1a\x14,\
\x0b J\x02\x85\x02\x80\xd9\xbd\xc4\x0bf&(\xe6[\x08f=\x97\xf7B\xedK}\x9c^\
\x04\xa4_T\\%8\x1e\x06\x002\xb8\xfa\x97\x1b\xe0\xe2\xf6o\x10\x98\x84o}\
\xf1E\xf7\x00\x00\x00\x00IEND\xaeB`\x82""")


# Data URI for the images/file.png file.
IMAGES_FILE_PNG_DATA_URI = b("""\
data:image/png;base64,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""")


# Binary data for the images/file.jpg file.
IMAGES_FILE_JPG = b("""\
\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\
\xff\xdb\x00C\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\xff\xdb\x00C\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\
\xff\xc0\x00\x11\x08\x00 \x00 \x03\x01"\x00\x02\x11\x01\x03\x11\x01\
\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\
\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\
\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\
\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\
\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\
\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\
\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\
\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\
\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\
\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\
\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\
\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\
\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\
\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\
\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\
\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\
\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\
\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\
\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\
\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\
\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xfe\xef~$|F\xf0\xcf\xc2\
\xbf\t\xde\xf8\xc3\xc5S]\xfd\x8a\xde\xe3O\xd34\xed3J\xb3\x97S\xf1\x07\
\x89|E\xad\xde\xc1\xa5xw\xc2\x9e\x17\xd1\xed\xff\x00\xd2u\xaf\x13x\x93X\
\xba\xb4\xd24M.\xdf\x0fu}u\x10\x91\xe0\xb7Y\xae"\xf8\xba\xeb\xe2\'\xed\
\x03\xf1\x02W\xd4\xb5\xef\x18\xea\xff\x00\xb3\xff\x00\x85.4\xeb\xbdOM\
\xd0>\x0f\xfc>\xd1>%\xfcB\xb3K{\xd1\xa7ZYk\x1f\x11\xfe!xg\xc6\xff\x00\
\r\xfcC\xadjws\xdaA>\x91\xe0\xdf\x86\x8d\xe1\x8d\x12\xf2=M\xb4\xbf\
\x8a^=\xd0l\xdb\xc4\t\xb7\xf1\xab\xe2}\xb6\x8b\xfbJ\xe8\xf1\xea^\x1b\
\xd6\xfcac\xf0/\xe1w\x87<{\xa6xwHm)-m\xfca\xf1\xefY\xf8\xab\xe0}3\xe2&\
\xafu\xaa\\\xda\xae\x96\x9e\x07\xf0g\xc1\x8f\x88\xde\x0f\xd3\xb5\x08Z\
\xe3\xcc\x97\xe3\r\xde\x9d-\xa3\xbd\xe5\xb5\xe5\x86\xe7\x82\xf5\x9bME\
\xae|o\xe2m^\xdfP\xf1\xa6\xb3j\xc9\xa8lh\x13O\xd1,f\x95o\x07\x86\xbc9\
\x0cVvD\xe8\xb6s**\xde\xdf\xc56\xb3\xaa\xc9\n\xde\xea\xf7R\xccc\x8e\
\x1f\xa8\xcbr\xba\xb2\xa5\x1a\xab\t\x1a\x9c\xd0\x84\xea\xe2j\xc2\x9dh\
\xd1U\xa0\xe7F\x8d,=JuiJS\xa6\xe9b%Zp\x95\x94\xe3J<\x9c\xb5\x15_\x170\
\xcc\xe8\xe1\xa6\xa8\xfbe\x1a\xcfX\xd1\xb4\x93\x94c(\xa9JSR\x8b\x8co\
\xcf\x05\x15v\xfe+4\xae\xbc7@\xf8\x87\xfbR\xf8[T\xb4\x8bF\xf8\xa6\xdf\
\x11\xef\xaf5\x0b\xe8,~\x1c\xfe\xd2^\x1b\xf8w\xa4x\x8b\xc5\x11Z\xdc^\
\x9b=#D\xf1\xb7\xec\xe9\xe0o\x03[xO\\\xbb\xd3m\x7f\xb4uMt|8\xf8\xbb\
\xe1M\x11b\xbb\x8aO\xb4X$:\xec\x9ft|\x1a\xf8\xc9\xa1|d\xd05;\xdb=/W\
\xf0\x9f\x8b<)\xab\xbf\x86>"|:\xf10\xb2\x8f\xc5~\x00\xf1d6\x96\xba\
\x83\xe8\xda\xc2\xe9\xd7w\xdae\xf5\xa5\xf6\x9b}a\xad\xf8s\xc4Z-\xf6\
\xa1\xe1\xff\x00\x14xwQ\xd3u\xcd\x16\xfe\xe6\xce\xec\x14\xe1\xed\xfc\
\x01\xf1\x12X"\xf1O\x81\xbe!i\x9e\x0c\xb9\xd4\xa2K\xb94\x8b\xcf\x05\
\xe9z\xf6\x8f\xadZ\xb2\xac\xb6sx\x8e\xe6[\x9b_\x10M<0\x86\x8bM\xfe\
\xc7\xd64kM>\xd2\xfe\xed\xeelu+\xc3\x1c\xd1\xfcq\xe1O\x8c\xfa^\x9b\
\xfbq\xfc!\xd2\xb4\xe9R/\x11|[\xf0\xb7\x8d\xfe\x0f|K\xd2\xad\xa6\xd2\
\xad\xd2\xf7P\xf0^\x89\xf1\x0b\xe2g\x83u}OE\xb6\xd7\xf5\xadSM\x93\xc0\
\xda\xd7\xc2\xef\x8c\xba\x0f\x86\xe4\xba{\x8d;R\xd3~%\xeb?\xd9\x9a\
\xe7\x88F\x91s&\x93\x8e28|mJ\xf4\xa8a\xf0\xf4\xe7\x86\xa3^Q\xa9\x86\
\xa7\xec\xa5\xfe\xc5JUk<M:t\xe9\xe1\xe5\x1a\xd4\xa9W\x9c\'F2\x9a\x9ca\
\xcf8\xd2\xe6Kl\x1c\xebB\x9c%\x89\x9dF\xeb8J>\xd3\x93\x95*\xcdr\xc2\
\x9bR\x95K\xd3r\x84\x1a\xab\xcb{\xfb\xbc\xcd\xa2/\xdb\xff\x00\xc2\
\xf2xC\xe2_\x80>2\xdci\xb3j^\x14\xf1\xae\x8f\xe1\x9f\x85>(h.\x9a\
\xcekO\x15\xf8\x1b\xc4\xde&\xf1o\xc2\xfd2;\xc8\xd3v\x98\xbe7\xd1\
\xbe |f\xf0\x85\x9e\xb1%\xc5\xba\xc7\xe3K\xef\x02x~\xdcM{\xe2\x88\
\x15v\xbfj\xcf\x8b\x9f\x04\xad~\x0b\xe8?\x18<+\xad\xc5\xa5x\x87\
\xc5rh6\xfe\x11\xd1\x12\xe6\xd3\xc3\xf3x\x9a\x1d^\xf6\xd2\xefY7\
\xda\x1d\xd4Mu5\xff\x00\x874\x16\xd65k\x95\xd3\xe0K\xb5\x9e\xdf\
\xec\xfa\xa4\x82\xd5\x92\xea\xcb\xed_\xda\'\xe0\xdd\x97\xc7_\x86:\
\xf7\xc3\xedEmn,\xb5\x8bI\xed\xeel/\xd3u\x95\xf4r\xa0\xc4R\x91\x86\
\x8aX\xe5H\xe6\xb4\xb9B\x92Z\xdc\xa4w\x10\xcb\x04\xd1\xc72\x7f;\x7f\
\x1e\xbfa\x8f\xdbb\x19t}\x0e\xe3K\xbc\xf8\xcf\xe1/\x06\xd9\xdfi~\
\x0b\x9a\xf3]\xd5|3\xe2\x9d\x1bM\xd4n\xa1\xba\xbb\x82\xfb\xc4\xfa\
\x06\x93\xe2_\x0f\xf8\xb2\xe2\x7f\xb1\xd8\xc4\xfa\xef\x88|\x19u\xe2\
\xfb\x98\xad":\xaf\x89\xb5K\x87\x9ey\xfd\x9e\x1d\xcdr\xfa\xb5\xf2\
\n9\x9e:\xaeX\xb2\xaceOm\x8a\x82\x9c\xe3\x8b\xcbj(\xd4\x96\x16Q\x8c\
\\UNjP\xc3\xa9U\x9d*0\xc3\xc9\xce\xf5*\xc60<\x8c\xf7,\xc6K\r\x9cT\
\xcb\xf0\xd4q\xb5\xf1\xf8:p\xa5\x86\xaf5IS\xc7Rn\x14\xb11\xad+\xa8\
\xc6\x14\xeaJr\x8a\x8b\x94\xeaR\xa7\x15(FSg\xba\xfe\xcd_\xb6\x7f\
\x89\xbf\xe1oG\xe1;\xdf\x19\xeaw\xde\x19\xd4<\x1d\xe2K\x1b]\x03R\
\xd7/\xa6\xd2\xac$\xb4\xf2\xf5\x98n4m1\xa76q\xea)%\xbd\xca\x19\
\xbc\xa6\x95t\xdb\x9b\xe8VA\x0cPG\x17E\xfb\x14\xe9z\xdf\xed\x1b\
\xff\x00\x05\x03\xf8\x83\xf1\xce\xe6\xf5\xaf<\x17\xf0Eu\ttk\x94\
\xb6\x97M\x82\xd3Z\xd5\xbc\x1f\xaa\xfc9\xf0g\x87#\xb6\xba\xb5\xb7\
\x9fR\xbb\x9bF\xf1w\xc6\x9f\x1bk\xfa\x84\x8d-\xd5\xa5\x8f\x88\xfe\
\x1fJ\xb2\xcb\xa0\xeb\xfe\x1e\x10~v\xf8\x13\xfe\t\xe9\xfbhj\xbe#\
\xb3\xbb\xd1>\x1b\xde|0\xbbF\x9a\x15\xf1|\xfe$\xd7<e\xe2].+\xb8e\
\xb4\xb8\x97C\xbb\x93\xc3\x1e\x01\xf0\xde\x9bu%\xa4\xd3@n\xf5]\x03\
\\\x8e8\xe6\x97\xcb\xb7\x8d\x8a\xb8\xfe\x86\xbfa\xaf\xd9\x1e\xf7\
\xf6`\xf0\\ZV\xa3x\x16\xeeaqswj\x97o\x7fw}\xaaj\x0f\xe6\xea:\xc6\
\xbb\xa9<\x92\xbe\xa3\xa9\xdeK\x99&\xb8\x96{\x89\xa4r\x81\xe4\
\x89 \x8a\x11\xe9q\x8em\xc3p\xcd1\xd8\x9e\x19\x94\'\x1c~S\x1c\xb6\
\xa2\x86\x1a4i\xd2\xabV\xbc\xa7\x8e\xc5\xcaQ\xf7*U\xc4a\xd5:\x10t\
\xdc\xa4\xddLD\xab8\xb8\xc1V\xe1\xe1,\xaf>\xa3\x96ah\xf1\x1c\xd3\
\xc4a3\n\xb8\xba*8\xa9\xe2?r\xb0\xd1\xa3\x86\xa19KE\n3\x95i\xaai\
\xb8E\xc6\x8b\x83V\x92_\xff\xd9""")


# Data URI for the images/file.jpg file.
IMAGES_FILE_JPG_DATA_URI = b("""\
data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQE\
BAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB\
AQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBA\
QEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAAgACADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQ\
EAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUE\
GE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdI\
SUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipq\
rKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHw\
EAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAE\
CAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2\
Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXm\
JmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09f\
b3+Pn6/9oADAMBAAIRAxEAPwD+734kfEbwz8K/Cd74w8VTXf2K3uNP0zTtM0qzl1PxB4l\
8Ra3ewaV4d8KeF9Ht/wDSda8TeJNYurTSNE0u3w91fXUQkeC3Wa4i+Lrr4iftA/ECV9S1\
7xjq/wCz/wCFLjTrvU9N0D4P/D7RPiX8QrNLe9GnWllrHxH+IXhnxv8ADfxDrWp3c9pBP\
pHg34aN4Y0S8j1NtL+KXj3QbNvECbfxq+J9tov7Sujx6l4b1vxhY/Av4XeHPHumeHdIbS\
ktbfxh8e9Z+KvgfTPiJq91qlzarpaeB/BnwY+I3g/TtQha48yX4w3enS2jveW15YbngvW\
bTUWufG/ibV7fUPGms2rJqGxoE0/RLGaVbweGvDkMVnZE6LZzKire38U2s6rJCt7q91LM\
Y44fqMtyurKlGqsJGpzQhOriasKdaNFVoOdGjSw9SnVpSlOm6WIlWnCVlONKPJy1FV8XM\
Mzo4aao+2Uaz1jRtJOUYyipSlNSi4xvzwUVdv4rNK68N0D4h/tS+FtUtItG+KbfEe+vNQ\
voLH4c/tJeG/h3pHiLxRFa3F6bPSNE8bfs6eBvA1t4T1y7021/tHVNdHw4+LvhTRFiu4p\
PtFgkOuyfdHwa+MmhfGTQNTvbPS9X8J+LPCmrv4Y+Inw68TCyj8V+APFkNpa6g+jawunX\
d9pl9aX2m31hrfhzxFot9qHh/wAUeHdR03XNFv7mzuwU4e38AfESWCLxT4G+IWmeDLnUo\
ku5NIvPBel69o+tWrKstnN4juZbm18QTTwwhotN/sfWNGtNPtL+7e5sdSvDHNH8ceFPjP\
pem/tx/CHStOlSLxF8W/C3jf4PfEvSrabSrdL3UPBeifEL4meDdX1PRbbX9a1TTZPA2tf\
C74y6D4bkunuNO1LTfiXrP9ma54hGkXMmk44yOHxtSvSoYfD054ajXlGphqfspf7FSlVr\
PE06dOnh5RrUqVecJ0YympxhzzjS5ktsHOtCnCWJnUbrOEo+05OVKs1ywptSlUvTcoQaq\
8t7+7zNoi/b/wDC8nhD4l+APjLcabNqXhTxro/hn4U+KGgums5rTxX4G8TeJvFvwv0yO8\
jTdpi+N9G+IHxm8IWesSXFusfjS+8CeH7cTXviiBV2v2rPi58ErX4L6D8YPCutxaV4h8V\
yaDb+EdES5tPD83iaHV720u9ZN9od1E11Nf8AhzQW1jVrldPgS7We3+z6pILVkurL7V/a\
J+Ddl8dfhjr3w+1FbW4stYtJ7e5sL9N1lfRyoMRSkYaKWOVI5rS5QpJa3KR3EMsE0ccyf\
zt/Hr9hj9tiGXR9DuNLvPjP4S8G2d9pfgua813VfDPinRtN1G6huruC+8T6BpPiXw/4su\
J/sdjE+u+IfBl14vuYrSI6r4m1S4eeef2eHc1y+rXyCjmeOq5YsqxlT22Kgpzji8tqKNS\
WFlGMXFVOalDDqVWdKjDDyc71KsYwPIz3LMZLDZxUy/DUcbXx+DpwpYavNUlTx1JuFLEx\
rSuoxhTqSnKKi5TqUqcVKEZTZ7r+zV+2f4m/4W9H4TvfGep33hnUPB3iSxtdA1LXL6bSr\
CS08vWYbjRtMac2ceopJb3KGbymlXTbm+hWQQxQRxdF+xTpet/tG/8ABQP4g/HO5vWvPB\
fwRXUJdGuUtpdNgtNa1bwfqvw58GeHI7a6tbefUrubRvF3xp8ba/qEjS3VpY+I/h9Kssu\
g6/4eEH52+BP+Cen7aGq+I7O70T4b3nwwu0aaFfF8/iTXPGXiXS4ruGW0uJdDu5PDHgHw\
3pt1JaTTQG71XQNcjjjml8u3jYq4/oa/Ya/ZHvf2YPBcWlajeBbuYXFzd2qXb393fapqD\
+bqOsa7qTySvqOp3kuZJriWe4mkcoHkiSCKEelxjm3DcM0x2J4ZlCccflMctqKGGjRp0q\
tWvKeOxcpR9ypVxGHVOhB03KTdTESrOLjBVuHhLK8+o5ZhaPEc08RhMwq4uio4qeI/crD\
Ro4ahOUtFCjOVaappuEXGi4NWkl//2Q==""")
