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

.. autofunction:: group

"""

try:
    _RANGE = xrange
except NameError:
    _RANGE = range


def group(sequence, chunk_size):
    """
    Splits a sequence into a list of sequences each of size specified by
    ``chunk_size``.

    :param sequence:
        The sequence to split.
    :param chunk_size:
        The chunk size.
    :returns:
        Generator of sequences each of size ``chunk_size``.
    """
    for i in _RANGE(0, len(sequence), chunk_size):
        yield sequence[i:i+chunk_size]


