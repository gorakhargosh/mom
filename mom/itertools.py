#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: mom.itertools
:synopsis: Iteration tool helpers.

Tools useful for iterating over sequences.

.. autofunction:: chunks

"""

from mom._builtins import _RANGE

def chunks(sequence, size):
    """
    Splits a sequence into a list of sequences each of specified chunk size.

    :param sequence:
        The sequence to split.
    :param size:
        Chunk size.
    :returns:
        Generator of sequences each of the specified chunk size.
    """
    for i in _RANGE(0, len(sequence), size):
        yield sequence[i:i+size]


