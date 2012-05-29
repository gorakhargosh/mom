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

""":synopsis: Common collections.
:module: mom.

Queues
------
.. autoclass:: SetQueue
.. autoclass:: AttributeDict
.. autoclass:: attrdict

"""

from __future__ import absolute_import

try:
  import queue
except ImportError:
  import Queue as queue


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"



class SetQueue(queue.Queue):
  """
  Thread-safe implementation of an ordered set queue, which coalesces
  duplicate items into a single item if the older occurrence has not yet been
  read and maintains the order of items in the queue.

  Ordered set queues are useful when implementing data structures like
  event buses or event queues where duplicate events need to be coalesced
  into a single event. An example use case is the inotify API in the Linux
  kernel which shares the same behavior.

  Queued items must be immutable and hashable so that they can be used as
  dictionary keys or added to sets. Items must have only read-only properties
  and must implement the :meth:`__hash__`, :meth:`__eq__`, and :meth:`__ne__`
  methods to be hashable.

  :author: Yesudeep Manglapilly <yesudeep@gmail.com>
  :author: Lukáš Lalinský <lalinsky@gmail.com>

  An example item class implementation follows::

      class QueuedItem(object):
          def __init__(self, a, b):
              self._a = a
              self._b = b

          @property
          def a(self):
              return self._a

          @property
          def b(self):
              return self._b

          def _key(self):
              return (self._a, self._b)

          def __eq__(self, item):
              return self._key() == item._key()

          def __ne__(self, item):
              return self._key() != item._key()

          def __hash__(self):
              return hash(self._key())

  .. NOTE:
      This ordered set queue leverages locking already present in the
      :class:`queue.Queue` class redefining only internal primitives.
      The order of items is maintained because the internal queue is
      not replaced. An internal set is used merely to check for the
      existence of an item in the queue.
  """

  def _init(self, maxsize):
    queue.Queue._init(self, maxsize)
    self._set_of_items = set()

  def _put(self, item):
    if item not in self._set_of_items:
      queue.Queue._put(self, item)
      self._set_of_items.add(item)

  def _get(self):
    item = queue.Queue._get(self)
    self._set_of_items.remove(item)
    return item


class AttributeDict(dict):
  """
  A dictionary with attribute-style access.
  It maps attribute access to the real dictionary.

  Subclass properties will override dictionary keys.

  :author: Alice Zoë Bevan–McGregor
  :license: MIT License.
  """

  def __init__(self, *args, **kw):
    dict.__init__(self, *args, **kw)

  def __repr__(self):
    return "%s(%s)" % (self.__class__.__name__,
                       super(AttributeDict, self).__repr__())

  def __delattr__(self, name):
    del self[name]

  def __getattr__(self, name):
    """
    Subclass properties will override dictionary keys.
    """
    try:
      return self[name]
    except KeyError:
      raise AttributeError("attribute %r not found" % name)

  def __setattr__(self, name, value):
    """
    Subclass properties will override dictionary keys.
    """
    self[name] = value


# Alias
attrdict = AttributeDict
