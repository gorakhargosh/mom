#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#


"""
:module: mom.string
:synopsis: string module compatibility.

"""

from __future__ import absolute_import

from string import punctuation, printable, whitespace

ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
ascii_letters = ascii_lowercase + ascii_uppercase
digits = "0123456789"

punctuation = punctuation
printable = printable
whitespace = whitespace
