#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#


"""
:module: mom.string
:synopsis: string module compatibility.

"""

from __future__ import absolute_import

try:
    from string import lowercase, uppercase, letters
    ascii_lowercase = lowercase
    ascii_uppercase = uppercase
    ascii_letters = letters
except ImportError:
    from string import ascii_lowercase, ascii_uppercase, ascii_letters
    ascii_lowercase = ascii_lowercase
    ascii_uppercase = ascii_uppercase
    ascii_letters = ascii_letters
    
from string import digits, punctuation, printable, whitespace

digits = digits
punctuation = punctuation
printable = printable
whitespace = whitespace
