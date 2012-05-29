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

""":synopsis: Decorators used throughout the library.
:module: mom.decorators

.. autofunction:: deprecated
"""

from __future__ import absolute_import

import functools
import warnings


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
    "deprecated",
    ]


def deprecated(func):
  """Marks functions as deprecated.

  This is a decorator which can be used to mark functions
  as deprecated. It will result in a warning being emitted
  when the function is used.

  Usage::

      @deprecated
      def my_func():
          pass

      @other_decorators_must_be_upper
      @deprecated
      def my_func():
          pass

  :param func:
      The function to deprecate.
  :returns:
      Deprecated function object.
  """

  @functools.wraps(func)
  def new_func(*args, **kwargs):
    """Wrapper function."""
    warnings.warn_explicit(
        "Call to deprecated function %(funcname)s." % {
            "funcname": func.__name__,
            },
        category=DeprecationWarning,
        filename=func.func_code.co_filename,
        lineno=func.func_code.co_firstlineno + 1
        )
    return func(*args, **kwargs)

  return new_func
