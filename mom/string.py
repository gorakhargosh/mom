#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#


"""
:module: mom.string
:synopsis: string module compatibility.

"""

from __future__ import absolute_import

ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE
DIGITS = "0123456789"

PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
PRINTABLE = '0123456789abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
WHITESPACE = '\t\n\x0b\x0c\r '
