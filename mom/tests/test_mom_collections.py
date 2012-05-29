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

from __future__ import absolute_import

import unittest2

try:
  import queue as Queue
except ImportError:
  import Queue

import threading

from mom import collections


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


class Test_AttributeDict(unittest2.TestCase):
  def test_behavior(self):
    d = collections.AttributeDict(something="foobar", another_thing="haha")
    self.assertEqual(d.something, "foobar")
    self.assertEqual(d.another_thing, "haha")

    d = collections.attrdict(something="foobar", another_thing="haha")
    self.assertEqual(d.something, "foobar")
    self.assertEqual(d.another_thing, "haha")

  def test_AttributeError_when_key_not_found(self):
    d = collections.AttributeDict(something="foobar", another_thing="haha")
    a = collections.attrdict(something="foobar", another_thing="haha")

    def foo_wrapper(d):
      return d.not_present

    self.assertRaises(AttributeError, foo_wrapper, d)
    self.assertRaises(AttributeError, foo_wrapper, a)

  def test_delattr(self):
    d = collections.AttributeDict(something="foobar", another_thing="haha")
    del d.another_thing
    self.assertDictEqual(d, dict(something="foobar"))
    del d["something"]
    self.assertDictEqual(d, dict())

  def test_getattr(self):
    d = collections.AttributeDict(something="foobar", another_thing="haha")
    d["oob"] = "blah"
    self.assertEqual(d.something, "foobar")
    self.assertEqual(d.oob, "blah")

  def test_setattr(self):
    d = collections.AttributeDict()
    d.something = "foobar"
    self.assertEqual(d.something, "foobar")

  def test_contains(self):
    d = collections.AttributeDict(something="foobar")
    self.assertTrue("something" in d)

  def test_subclass_attribute_shadows_dict_key(self):
    class Foobar(collections.AttributeDict):
      def __init__(self, *args, **kwargs):
        super(Foobar, self).__init__(*args, **kwargs)
        self.foo = 0

    d = Foobar(foo="something")
    self.assertEqual(d["foo"], 0)
    d.foo = 1
    self.assertNotEqual(d["foo"], 0)
    self.assertEqual(d.foo, 1)

  def test_items(self):
    d = collections.AttributeDict(a="a", b="b", c="c")
    another = collections.AttributeDict()
    for k, v in d.items():
      another[k] = v
    self.assertDictEqual(d, another)

  def test_keys_items_and_values(self):
    d = collections.AttributeDict(a="ah", b="bh", c="ch")
    self.assertEqual(set(d.keys()), set(["a", "b", "c"]))
    self.assertEqual(set(d.values()), set(["ah", "bh", "ch"]))
    self.assertEqual(set(d.items()),
                     set([("a", "ah"), ("b", "bh"), ("c", "ch")]))

  def test_get(self):
    d = collections.AttributeDict(a="ah")
    self.assertEqual(d.get("a"), "ah")
    self.assertEqual(d.get("b"), None)
    self.assertEqual(d.get("b", "foo"), "foo")

  def test_clear(self):
    d = collections.AttributeDict(a="ah", b="foo")
    d.clear()
    self.assertDictEqual(d, dict())

  def test_instance(self):
    d = collections.AttributeDict(a="foo")
    self.assertTrue(isinstance(d, collections.AttributeDict))
    self.assertTrue(isinstance(d, dict))

  def test_fromkeys(self):
    d = collections.AttributeDict(a="a", b="b", c="c")
    another = collections.AttributeDict.fromkeys(d, "Hmm")
    self.assertDictEqual(another, dict(a="Hmm", b="Hmm", c="Hmm"))

  def test_update(self):
    d = collections.AttributeDict(a="b")
    d.update(collections.AttributeDict(b="c"))
    self.assertDictEqual(d, dict(a="b", b="c"))

  def test_repr(self):
    d = collections.AttributeDict(a="b")
    self.assertEqual(repr(d), "AttributeDict(%s)" % repr(dict(a="b")))


class TestSetQueue(unittest2.TestCase):
  def test_behavior(self):
    class QueuedEvent(object):
      def __init__(self, path):
        self.path = path

      @property
      def _key(self):
        return self.path

      def __eq__(self, other):
        return self._key == other._key

      def __ne__(self, other):
        return self._key != other._key

      def __hash__(self):
        return hash(self._key)

    foo = QueuedEvent("foo")
    bar = QueuedEvent("bar")
    event_list = [
      foo,
      foo,
      foo,
      foo,
      bar,
      bar,
      foo,
      foo,
      foo,
      bar,
      bar,
      bar,
      foo,
      foo,
      foo,
      foo,
      bar,
      bar,
      ]
    event_set = set(event_list)
    event_queue = collections.SetQueue()
    for event in event_list:
      event_queue.put(event)

    def event_consumer(in_queue):
      events = []
      while True:
        try:
          event = in_queue.get(block=True, timeout=0.2)
          events.append(event)
          in_queue.task_done()
        except Queue.Empty:
          break

      # Check set behavior.
      self.assertEqual(len(set(events)), len(events))
      self.assertEqual(set(events), event_set)

      # Check order
      self.assertEqual(events[0], foo)
      self.assertEqual(events[1], bar)

    consumer_thread = threading.Thread(target=event_consumer, args=(event_queue, ))
    consumer_thread.start()
    consumer_thread.join()
