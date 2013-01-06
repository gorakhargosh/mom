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

import functools
import os

from mom import builtins


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "absolute_path",
    "get_dir_walker",
    "list_directories",
    "list_files",
    "listdir",
    "parent_dir_path",
    "real_absolute_path",
    "walk",
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
    walker = functools.partial(os.walk,
                               topdown=topdown,
                               followlinks=followlinks)
  else:

    def walker(path, topdown=topdown, followlinks=followlinks):
      """Alternative walker."""
      yield builtins.next(os.walk(path,
                                  topdown=topdown,
                                  followlinks=followlinks))
  return walker


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
  for root, dir_names, file_names in walk_func(dir_pathname):
    yield (root, dir_names, file_names)


def listdir(dir_pathname,
            recursive=True,
            topdown=True,
            followlinks=False):
  """
  Enlists all items using their absolute paths in a directory, optionally
  non-recursively.

  :param dir_pathname:
      The directory to traverse.
  :param recursive:
      ``True`` (default) for walking recursively through the directory tree;
      ``False`` otherwise.
  :param topdown:
      Please see the documentation for :func:`os.walk`
  :param followlinks:
      Please see the documentation for :func:`os.walk`
  """
  for root, dir_names, file_names in walk(dir_pathname,
                                          recursive, topdown, followlinks):
    for dir_name in dir_names:
      yield absolute_path(os.path.join(root, dir_name))
    for file_name in file_names:
      yield absolute_path(os.path.join(root, file_name))


def list_directories(dir_pathname, recursive=True, topdown=True,
                     followlinks=False):
  """
  Enlists all the directories using their absolute paths within the
  specified directory, optionally non-recursively.

  :param dir_pathname:
      The directory to traverse.
  :param recursive:
      ``True`` (default) for walking recursively through the directory
      tree; ``False`` otherwise.
  :param topdown:
      Please see the documentation for :func:`os.walk`
  :param followlinks:
      Please see the documentation for :func:`os.walk`
  """
  for root, dir_names, _ in walk(dir_pathname, recursive, topdown, followlinks):
    for dir_name in dir_names:
      yield absolute_path(os.path.join(root, dir_name))


def list_files(dir_pathname, recursive=True, topdown=True, followlinks=False):
  """
  Enlists all the files using their absolute paths within the
  specified directory, optionally recursively.

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
  for root, _, file_names in walk(dir_pathname,
                                  recursive, topdown, followlinks):
    for file_name in file_names:
      yield absolute_path(os.path.join(root, file_name))


def absolute_path(path):
  """
  Returns the absolute path for the given path and normalizes the
  path.

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
