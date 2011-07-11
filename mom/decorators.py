#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:module: pyoauth.decorators
:synopsis: Decorators used throughout the library.

.. autofunction:: deprecated
"""

from __future__ import absolute_import

import warnings
import functools


__all__ = [
    "deprecated",
]

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    ## Usage examples ##

    ::
        @deprecated
        def my_func():
            pass

        @other_decorators_must_be_upper
        @deprecated
        def my_func():
            pass
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        """
        Wrapper function.
        """
        warnings.warn_explicit(
            "Call to deprecated function %(funcname)s." % {
                'funcname': func.__name__,
            },
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func

