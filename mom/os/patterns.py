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
:module: mom.os.patterns
:synopsis: Wildcard pattern matching and filtering functions for paths.

Functions
---------
.. autofunction:: match_path
.. autofunction:: match_path_against
.. autofunction:: match_any_paths
.. autofunction:: filter_paths
"""

from __future__ import absolute_import

try:  # pragma: no cover
  # Python 2.x
  from itertools import imap as map
except ImportError:  # pragma: no cover
  pass


import fnmatch
import functools

from mom import functional


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "filter_paths",
    "match_any_paths",
    "match_path",
    "match_path_against",
    ]


def _string_lower(string):
  """
  Convenience function to lowercase a string.

  :param string:
      The string which will be lower-cased.
  :returns:
      Lower-cased copy of string s.
  """
  return string.lower()


def match_path_against(pathname, patterns, case_sensitive=True):
  """
  Determines whether the pathname matches any of the given wildcard patterns,
  optionally ignoring the case of the pathname and patterns.

  :param pathname:
      A path name that will be matched against a wildcard pattern.
  :param patterns:
      A list of wildcard patterns to match_path the filename against.
  :param case_sensitive:
      ``True`` if the matching should be case-sensitive; ``False`` otherwise.
  :returns:
      ``True`` if the pattern matches; ``False`` otherwise.
  """
  if case_sensitive:
    match_func = functools.partial(fnmatch.fnmatchcase, pathname)
    transform = functional.identity
  else:
    match_func = functools.partial(fnmatch.fnmatch, pathname.lower())
    transform = _string_lower
  return functional.some(match_func, map(transform, set(patterns)))


def _match_path(pathname,
                included_patterns,
                excluded_patterns,
                case_sensitive=True):
  """
  Internal function same as :func:`match_path` but does not check arguments.
  """
  if not case_sensitive:
    included_patterns = set(map(_string_lower, included_patterns))
    excluded_patterns = set(map(_string_lower, excluded_patterns))
  else:
    included_patterns = set(included_patterns)
    excluded_patterns = set(excluded_patterns)
  common_patterns = included_patterns & excluded_patterns
  if common_patterns:
    raise ValueError("conflicting patterns `%s` included and excluded"
                     % common_patterns)
  return (match_path_against(pathname, included_patterns, case_sensitive) and
          not match_path_against(pathname, excluded_patterns,
                                 case_sensitive))


def match_path(pathname,
               included_patterns=None,
               excluded_patterns=None,
               case_sensitive=True):
  """
  Matches a pathname against a set of acceptable and ignored patterns.

  :param pathname:
      A pathname which will be matched against a pattern.
  :param included_patterns:
      Allow filenames matching wildcard patterns specified in this list.
      If no pattern is specified, the function treats the pathname as
      a match_path.
  :param excluded_patterns:
      Ignores filenames matching wildcard patterns specified in this list.
      If no pattern is specified, the function treats the pathname as
      a match_path.
  :param case_sensitive:
      ``True`` if matching should be case-sensitive; ``False`` otherwise.
  :returns:
      ``True`` if the pathname matches; ``False`` otherwise.
  :raises:
      ValueError if included patterns and excluded patterns contain the
      same pattern.
  """
  included = ["*"] if included_patterns is None else included_patterns
  excluded = [] if excluded_patterns is None else excluded_patterns
  return _match_path(pathname, included, excluded, case_sensitive)


def filter_paths(pathnames,
                 included_patterns=None,
                 excluded_patterns=None,
                 case_sensitive=True):
  """
  Filters from a set of paths based on acceptable patterns and
  ignorable patterns.

  :param pathnames:
      A list of path names that will be filtered based on matching and
      ignored patterns.
  :param included_patterns:
      Allow filenames matching wildcard patterns specified in this list.
      If no pattern list is specified, ["*"] is used as the default pattern,
      which matches all files.
  :param excluded_patterns:
      Ignores filenames matching wildcard patterns specified in this list.
      If no pattern list is specified, no files are ignored.
  :param case_sensitive:
      ``True`` if matching should be case-sensitive; ``False`` otherwise.
  :returns:
      A list of pathnames that matched the allowable patterns and passed
      through the ignored patterns.
  """
  included = ["*"] if included_patterns is None else included_patterns
  excluded = [] if excluded_patterns is None else excluded_patterns

  for pathname in pathnames:
    # We don't call the public match_path because it checks arguments
    # and sets default values if none are found. We're already doing that
    # above.
    if _match_path(pathname, included, excluded, case_sensitive):
      yield pathname


def match_any_paths(pathnames,
                    included_patterns=None,
                    excluded_patterns=None,
                    case_sensitive=True):
  """
  Matches from a set of paths based on acceptable patterns and
  ignorable patterns.

  :param pathnames:
      A list of path names that will be filtered based on matching and
      ignored patterns.
  :param included_patterns:
      Allow filenames matching wildcard patterns specified in this list.
      If no pattern list is specified, ["*"] is used as the default pattern,
      which matches all files.
  :param excluded_patterns:
      Ignores filenames matching wildcard patterns specified in this list.
      If no pattern list is specified, no files are ignored.
  :param case_sensitive:
      ``True`` if matching should be case-sensitive; ``False`` otherwise.
  :returns:
      ``True`` if any of the paths matches; ``False`` otherwise.
  """
  included = ["*"] if included_patterns is None else included_patterns
  excluded = [] if excluded_patterns is None else excluded_patterns

  for pathname in pathnames:
    # We don't call the public match_path because it checks arguments
    # and sets default values if none are found. We're already doing that
    # above.
    if _match_path(pathname, included, excluded, case_sensitive):
      return True
  return False
