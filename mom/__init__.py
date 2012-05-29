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

""":synopsis: Mother of all our Python projects.
:module: mom

How many times have you noticed a ``utils`` subpackage or module?
-----------------------------------------------------------------
Yeah. There is a lot of code duplication that occurs throughout
our Python-based projects and results in code that is harder
to maintain in the long term. Not to mention all the duplicate
test code and more maintenance.

Therefore, we have decided to move all those ``util`` modules and
subpackages to a central library, which we use throughout our projects.
If you have a ``utils`` module, chances are you're duplicating
and wasting effort whereas instead you could use tested code
provided by this library. If there's something not included in
this library and think it should, speak up.

.. automodule:: mom.builtins
.. automodule:: mom.collections
.. automodule:: mom.decorators
.. automodule:: mom.functional
.. automodule:: mom.itertools
.. automodule:: mom.math
.. automodule:: mom.mimeparse
.. automodule:: mom.string
"""

__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"
