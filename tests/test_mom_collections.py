#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import with_statement
import unittest2

try:
    from queue import Empty as QueueEmpty
except ImportError:
    from Queue import Empty as QueueEmpty

from threading import Thread
from mom.collections import SetQueue


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
