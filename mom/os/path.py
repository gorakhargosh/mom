#!/usr/bin/env python
# -*- coding: utf-8 -*-
# path.py: Path functions.
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
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

"""
:module: mom.os.path
:synopsis: Directory walking, listing, and path sanitizing functions.

Functions
---------
.. autofunction:: get_dir_walker
.. autofunction:: walk
.. autofunction:: listdir
.. autofunction:: list_directories
.. autofunction:: list_files
.. autofunction:: absolute_path
.. autofunction:: real_absolute_path
.. autofunction:: parent_dir_path
"""

from __future__ import absolute_import

import os.path
from functools import partial
from mom._compat import next

__all__ = [
    'get_dir_walker',
    'walk',
    'listdir',
    'list_directories',
    'list_files',
    'absolute_path',
    'real_absolute_path',
    'parent_dir_path',
]


def get_dir_walker(recursive, topdown=True, followlinks=False):
    """
    Returns a recursive or a non-recursive directory walker.

    :param recursive:
    ``True`` produces a recursive walker; ``False`` produces a non-recursive
    walker.
    :returns:
    A walker function.
    """
    if recursive:
        walk = partial(os.walk, topdown=topdown, followlinks=followlinks)
    else:
        def walk(path, topdown=topdown, followlinks=followlinks):
            next(os.walk(path, topdown=topdown, followlinks=followlinks))
    return walk


def walk(dir_pathname, recursive=True, topdown=True, followlinks=False):
    """
    Walks a directory tree optionally recursively. Works exactly like
    :func:`os.walk` only adding the `recursive` argument.

    :param dir_pathname:
    The directory to traverse.
    :param recursive:
    ``True`` for walking recursively through the directory tree;
    ``False`` otherwise.
    :param topdown:
    Please see the documentation for :func:`os.walk`
    :param followlinks:
    Please see the documentation for :func:`os.walk`
    """
    walk_func = get_dir_walker(recursive, topdown, followlinks)
    for root, dirnames, filenames in walk_func(dir_pathname):
        yield (root, dirnames, filenames)


def listdir(dir_pathname,
            recursive=True,
            topdown=True,
            followlinks=False):
    """
    Enlists all items using their absolute paths in a directory, optionally
    recursively.

    :param dir_pathname:
    The directory to traverse.
    :param recursive:
    ``True`` for walking recursively through the directory tree;
    ``False`` otherwise.
    :param topdown:
    Please see the documentation for :func:`os.walk`
    :param followlinks:
    Please see the documentation for :func:`os.walk`
    """
    for root, dirnames, filenames\
    in walk(dir_pathname, recursive, topdown, followlinks):
        for dirname in dirnames:
            yield absolute_path(os.path.join(root, dirname))
        for filename in filenames:
            yield absolute_path(os.path.join(root, filename))


def list_directories(dir_pathname,
                     recursive=True,
                     topdown=True,
                     followlinks=False):
    """
    Enlists all the directories using their absolute paths within the specified
    directory, optionally recursively.

    :param dir_pathname:
    The directory to traverse.
    :param recursive:
    ``True`` for walking recursively through the directory tree;
    ``False`` otherwise.
    :param topdown:
    Please see the documentation for :func:`os.walk`
    :param followlinks:
    Please see the documentation for :func:`os.walk`
    """
    for root, dirnames, filenames\
    in walk(dir_pathname, recursive, topdown, followlinks):
        for dirname in dirnames:
            yield absolute_path(os.path.join(root, dirname))


def list_files(dir_pathname,
               recursive=True,
               topdown=True,
               followlinks=False):
    """
    Enlists all the files using their absolute paths within the specified
    directory, optionally recursively.

    :param dir_pathname:
    The directory to traverse.
    :param recursive:
    ``True`` for walking recursively through the directory tree;
    ``False`` otherwise.
    :param topdown:
    Please see the documentation for :func:`os.walk`
    :param followlinks:
    Please see the documentation for :func:`os.walk`
    """
    for root, dirnames, filenames\
    in walk(dir_pathname, recursive, topdown, followlinks):
        for filename in filenames:
            yield absolute_path(os.path.join(root, filename))


def absolute_path(path):
    """
    Returns the absolute path for the given path and normalizes the path.

    :param path:
    Path for which the absolute normalized path will be found.
    :returns:
    Absolute normalized path.
    """
    return os.path.abspath(os.path.normpath(path))


def real_absolute_path(path):
    """
    Returns the real absolute normalized path for the given path.

    :param path:
    Path for which the real absolute normalized path will be found.
    :returns:
    Real absolute normalized path.
    """
    return os.path.realpath(absolute_path(path))


def parent_dir_path(path):
    """
    Returns the parent directory path.

    :param path:
    Path for which the parent directory will be obtained.
    :returns:
    Parent directory path.
    """
    return absolute_path(os.path.dirname(path))

