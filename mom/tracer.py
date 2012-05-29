#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tracer.py: Tracing function calls using Python decorators.
#
# Written by Thomas Guest <tag@wordaligned.org>
# Please see http://wordaligned.org/articles/echo
#
# Place into the public domain.

""":synopsis: Echoes calls made to functions and methods in a module.
:module: mom.tracer

"Tracing" a function call means printing out the name of the function
and the values of its arguments before making the call (which is more
commonly referred to as "tracing", but Python already has a trace module).

For example, to trace calls made to functions in "my_module" do::

    from mom import tracer
    import my_module
    tracer.trace_module(my_module)

Or, for example, to trace calls made to functions in "my_module.my_class"
do::

    tracer.trace_class(my_module.my_class)

Alternatively, tracer.trace can be used to decorate functions. Calls to the
decorated function will be traced. Example::

    @tracer.trace
    def my_function(args):
        pass

.. autofunction:: is_classmethod
.. autofunction:: is_class_private_name
.. autofunction:: method_name
.. autofunction:: trace
.. autofunction:: trace_instancemethod
.. autofunction:: trace_class
.. autofunction:: trace_module

"""

from __future__ import absolute_import

import functools
import inspect
import sys


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


def name(item):
  """Return an item's name."""
  return item.__name__


def is_classmethod(instancemethod):
  """Determine if an instancemethod is a classmethod."""
  return instancemethod.im_self is not None


def is_class_private_name(member_name):
  """Determine if a name is a class private name."""
  # Exclude system defined names such as __init__, __add__ etc
  return member_name.startswith("__") and not member_name.endswith("__")


def method_name(method):
  """Return a method's name.

  This function returns the name the method is accessed by from
  outside the class (i.e. it prefixes "private" methods appropriately).
  """
  mname = name(method)
  if is_class_private_name(mname):
    mname = "_%s%s" % (name(method.im_class), mname)
  return mname


def format_arg_value(arg_val):
  """Return a string representing a (name, value) pair.

  >>> format_arg_value(("x", (1, 2, 3)))
  "x=(1, 2, 3)"
  """
  arg, val = arg_val
  return "%s=%r" % (arg, val)


def trace(func, write=sys.stdout.write):
  """Echo calls to a function.

  Returns a decorated version of the input function which "tracees" calls
  made to it by writing out the function's name and the arguments it was
  called with.
  """
  # Unpack function's arg count, arg names, arg defaults
  code = func.func_code
  argcount = code.co_argcount
  argnames = code.co_varnames[:argcount]
  fn_defaults = func.func_defaults or list()
  argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

  @functools.wraps(func)
  def wrapped(*v, **k):
    """Collect function arguments by chaining together positional,
defaulted, extra positional and keyword arguments."""
    positional = map(format_arg_value, zip(argnames, v))
    defaulted = [format_arg_value((a, argdefs[a]))
                 for a in argnames[len(v):] if a not in k]
    nameless = map(repr, v[argcount:])
    keyword = map(format_arg_value, k.items())
    args = positional + defaulted + nameless + keyword
    write("%s(%s)\n" % (name(func), ", ".join(args)))
    return func(*v, **k)

  return wrapped


def trace_instancemethod(klass, method, write=sys.stdout.write):
  """Change an instancemethod so that calls to it are traceed.

  Replacing a classmethod is a little more tricky.
  See: http://www.python.org/doc/current/ref/types.html
  """
  mname = method_name(method)
  never_trace = "__str__", "__repr__",  # Avoid recursion printing method calls
  if mname in never_trace:
    pass
  elif is_classmethod(method):
    setattr(klass, mname, classmethod(trace(method.im_func, write)))
  else:
    setattr(klass, mname, trace(method, write))


def trace_class(klass, write=sys.stdout.write):
  """Echo calls to class methods and static functions
  """
  for _, method in inspect.getmembers(klass, inspect.ismethod):
    trace_instancemethod(klass, method, write)
  for _, func in inspect.getmembers(klass, inspect.isfunction):
    setattr(klass, name(func), staticmethod(trace(func, write)))


def trace_module(mod, write=sys.stdout.write):
  """Echo calls to functions and methods in a module.
  """
  for fname, func in inspect.getmembers(mod, inspect.isfunction):
    setattr(mod, fname, trace(func, write))
  for _, klass in inspect.getmembers(mod, inspect.isclass):
    trace_class(klass, write)


if __name__ == "__main__":
  import doctest

  option_flags = doctest.ELLIPSIS
  doctest.testfile("traceexample.txt", optionflags=option_flags)
  doctest.testmod(optionflags=option_flags)
