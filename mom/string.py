#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#


"""
:module: mom.string
:synopsis: string module compatibility.

"""

from __future__ import absolute_import

ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
ascii_letters = ascii_lowercase + ascii_uppercase
digits = "0123456789"

punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
printable = '0123456789abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
whitespace = '\t\n\x0b\x0c\r '
