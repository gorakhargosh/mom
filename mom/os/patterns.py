#!/usr/bin/env python
# -*- coding: utf-8 -*-
# patterns.py: Common wildcard searching/filtering functionality for files.
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
:module: mom.os.patterns
:synopsis: Wildcard pattern matching and filtering functions for paths.

Functions
---------
.. autofunction:: match_path
.. autofunction:: match_path_against
.. autofunction:: filter_paths
"""

from __future__ import absolute_import
from fnmatch import fnmatch, fnmatchcase

__all__ = ['match_path',
           'match_path_against',
           'match_any_paths',
           'filter_paths']


def _string_lower(s):
    """
    Convenience function to lowercase a string (the :mod:`string` module is
    deprecated/removed in Python 3.0).

    :param s:
        The string which will be lowercased.
    :returns:
        Lowercased copy of string s.
    """
    return s.lower()


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

    Doctests::
        >>> match_path_against("/home/username/foobar/blah.py", ["*.py", "*.txt"], False)
        True
        >>> match_path_against("/home/username/foobar/blah.py", ["*.PY", "*.txt"], True)
        False
        >>> match_path_against("/home/username/foobar/blah.py", ["*.PY", "*.txt"], False)
        True
        >>> match_path_against("C:\\windows\\blah\\BLAH.PY", ["*.py", "*.txt"], True)
        False
        >>> match_path_against("C:\\windows\\blah\\BLAH.PY", ["*.py", "*.txt"], False)
        True
    """
    if case_sensitive:
        match_func = fnmatchcase
        pattern_transform_func = (lambda w: w)
    else:
        match_func = fnmatch
        pathname = pathname.lower()
        pattern_transform_func = _string_lower
    for pattern in set(patterns):
        pattern = pattern_transform_func(pattern)
        if match_func(pathname, pattern):
            return True
    return False


def _match_path(pathname,
                included_patterns,
                excluded_patterns,
                case_sensitive=True):
    """Internal function same as :func:`match_path` but does not check arguments.

    Doctests::
        >>> _match_path("/users/gorakhargosh/foobar.py", ["*.py"], ["*.PY"], True)
        True
        >>> _match_path("/users/gorakhargosh/FOOBAR.PY", ["*.py"], ["*.PY"], True)
        False
        >>> _match_path("/users/gorakhargosh/foobar/", ["*.py"], ["*.txt"], False)
        False
        >>> _match_path("/users/gorakhargosh/FOOBAR.PY", ["*.py"], ["*.PY"], False)
        Traceback (most recent call last):
            ...
        ValueError: conflicting patterns `set(['*.py'])` included and excluded
    """
    if not case_sensitive:
        included_patterns = set(map(_string_lower, included_patterns))
        excluded_patterns = set(map(_string_lower, excluded_patterns))
    else:
        included_patterns = set(included_patterns)
        excluded_patterns = set(excluded_patterns)
    common_patterns = included_patterns & excluded_patterns
    if common_patterns:
        raise ValueError('conflicting patterns `%s` included and excluded'\
                         % common_patterns)
    return (match_path_against(pathname, included_patterns, case_sensitive)\
            and not match_path_against(pathname, excluded_patterns,
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

    Doctests::
        >>> match_path("/Users/gorakhargosh/foobar.py")
        True
        >>> match_path("/Users/gorakhargosh/foobar.py", case_sensitive=False)
        True
        >>> match_path("/users/gorakhargosh/foobar.py", ["*.py"], ["*.PY"], True)
        True
        >>> match_path("/users/gorakhargosh/FOOBAR.PY", ["*.py"], ["*.PY"], True)
        False
        >>> match_path("/users/gorakhargosh/foobar/", ["*.py"], ["*.txt"], False)
        False
        >>> match_path("/users/gorakhargosh/FOOBAR.PY", ["*.py"], ["*.PY"], False)
        Traceback (most recent call last):
            ...
        ValueError: conflicting patterns `set(['*.py'])` included and excluded
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

    Doctests::
        >>> pathnames = set(["/users/gorakhargosh/foobar.py", "/var/cache/pdnsd.status", "/etc/pdnsd.conf", "/usr/local/bin/python"])
        >>> set(filter_paths(pathnames)) == pathnames
        True
        >>> set(filter_paths(pathnames, case_sensitive=False)) == pathnames
        True
        >>> set(filter_paths(pathnames, ["*.py", "*.conf"], ["*.status"], case_sensitive=True)) == set(["/users/gorakhargosh/foobar.py", "/etc/pdnsd.conf"])
        True
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

    Doctests::
        >>> pathnames = set(["/users/gorakhargosh/foobar.py", "/var/cache/pdnsd.status", "/etc/pdnsd.conf", "/usr/local/bin/python"])
        >>> match_any_paths(pathnames)
        True
        >>> match_any_paths(pathnames, case_sensitive=False)
        True
        >>> match_any_paths(pathnames, ["*.py", "*.conf"], ["*.status"], case_sensitive=True)
        True
        >>> match_any_paths(pathnames, ["*.txt"], case_sensitive=False)
        False
        >>> match_any_paths(pathnames, ["*.txt"], case_sensitive=True)
        False
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
