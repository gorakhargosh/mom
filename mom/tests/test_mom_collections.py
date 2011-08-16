#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


import unittest2

try:
    from queue import Empty as QueueEmpty
except ImportError:
    from Queue import Empty as QueueEmpty

from threading import Thread
from mom.collections import SetQueue, AttributeDict, attrdict

class Test_AttributeDict(unittest2.TestCase):
    def test_behavior(self):
        d = AttributeDict(something="foobar", another_thing="haha")
        self.assertEqual(d.something, "foobar")
        self.assertEqual(d.another_thing, "haha")

        d = attrdict(something="foobar", another_thing="haha")
        self.assertEqual(d.something, "foobar")
        self.assertEqual(d.another_thing, "haha")

    def test_KeyError_when_key_not_found(self):
        d = AttributeDict(something="foobar", another_thing="haha")
        a = attrdict(something="foobar", another_thing="haha")
        def foo_wrapper(d):
            return d.not_present
        self.assertRaises(KeyError, foo_wrapper, d)
        self.assertRaises(KeyError, foo_wrapper, a)


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

        foo = QueuedEvent('foo')
        bar = QueuedEvent('bar')
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
        event_queue = SetQueue()
        for event in event_list:
            event_queue.put(event)

        def event_consumer(in_queue):
            events = []
            while True:
                try:
                    event = in_queue.get(block=True, timeout=0.2)
                    events.append(event)
                    in_queue.task_done()
                except QueueEmpty:
                    break

            # Check set behavior.
            self.assertEqual(len(set(events)), len(events))
            self.assertEqual(set(events), event_set)

            # Check order
            self.assertEqual(events[0], foo)
            self.assertEqual(events[1], bar)

        consumer_thread = Thread(target=event_consumer, args=(event_queue, ))
        consumer_thread.start()
        consumer_thread.join()
