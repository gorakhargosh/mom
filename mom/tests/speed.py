#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Timeit based speed reporter.
# Taken directly from the Python source code for timeit.

from __future__ import absolute_import

import os
import sys
import timeit

sys.path.insert(0, os.curdir)


def report(stmt, setup, number=0, verbose=0, precision=3,
           repeat=timeit.default_repeat, timer=timeit.default_timer):
  sys.stdout.write("%50s -- " % stmt)
  t = timeit.Timer(stmt, setup, timer)
  if number == 0:
    # determine number so that 0.2 <= total time < 2.0
    for i in range(1, 10):
      number = 10 ** i
      try:
        x = t.timeit(number)
      except Exception:
        t.print_exc()
        return 1
      if verbose:
        print("%d loops -> %.*g secs" % (number, precision, x))
      if x >= 0.2:
        break
  try:
    r = t.repeat(repeat, number)
  except Exception:
    t.print_exc()
    return 1
  best = min(r)
  if verbose:
    print("raw times:", " ".join(["%.*g" % (precision, x) for x in r]))
  sys.stdout.write("%d loops, " % number)
  usec = best * 1e6 / number
  if usec < 1000:
    print("best of %d: %.*g usec per loop" % (repeat, precision, usec))
  else:
    msec = usec / 1000
    if msec < 1000:
      print("best of %d: %.*g msec per loop" % (repeat, precision, msec))
    else:
      sec = msec / 1000
      print("best of %d: %.*g sec per loop" % (repeat, precision, sec))
