#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Joe Gregorio
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""MIME-Type Parser

This module provides basic functions for handling mime-types. It can handle
matching mime-types against a list of media-ranges. See section 14.1 of the
HTTP specification [RFC 2616] for a complete explanation.

   http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.1

Contents:
 - parse_mime_type():   Parses a mime-type into its component parts.
 - parse_media_range(): Media-ranges are mime-types with wild-cards and a 'q'
                          quality parameter.
 - quality():           Determines the quality ('q') of a mime-type when
                          compared against a list of media-ranges.
 - quality_parsed():    Just like quality() except the second parameter must be
                          pre-parsed.
 - best_match():        Choose the mime-type with the highest quality ('q')
                          from a list of candidates.
"""
from mom._compat import EMPTY_BYTE, EQUAL_BYTE, FORWARD_SLASH_BYTE

from mom.builtins import b

__version__ = '0.1.3'
__author__ = 'Joe Gregorio'
__email__ = 'joe@bitworking.org'
__license__ = 'MIT License'
__credits__ = ''

SEMICOLON_BYTE = b(';')
ASTERISK_BYTE = b('*')

FULL_TYPE = b('*/*')


def parse_mime_type(mime_type):
  """Parses a mime-type into its component parts.

Carves up a mime-type and returns a tuple of the (type, subtype, params)
where 'params' is a dictionary of all the parameters for the media range.
For example, the media range b'application/xhtml;q=0.5' would get parsed
into:

  (b'application', b'xhtml', {'q': b'0.5'})
  """
  parts = mime_type.split(SEMICOLON_BYTE)
  params = dict([tuple([s.strip() for s in param.split(EQUAL_BYTE, 1)])\
                 for param in parts[1:]
  ])
  full_type = parts[0].strip()
  # Java URLConnection class sends an Accept header that includes a
  # single '*'. Turn it into a legal wildcard.
  if full_type == ASTERISK_BYTE:
    full_type = FULL_TYPE
  (type, subtype) = full_type.split(FORWARD_SLASH_BYTE)

  return type.strip(), subtype.strip(), params


def parse_media_range(range):
  """Parse a media-range into its component parts.

  Carves up a media range and returns a tuple of the (type, subtype,
  params) where 'params' is a dictionary of all the parameters for the media
  range.  For example, the media range 'application/*;q=0.5' would get parsed
  into:

     ('application', '*', {b'q', '0.5'})

  In addition this function also guarantees that there is a value for 'q'
  in the params dictionary, filling it in with a proper default if
  necessary.
  """
  (type, subtype, params) = parse_mime_type(range)
  if not params.has_key('q') or not params['q'] or\
     not float(params['q']) or float(params['q']) > 1\
  or float(params['q']) < 0:
    params['q'] = '1'

  return type, subtype, params


def fitness_and_quality_parsed(mime_type, parsed_ranges):
  """Find the best match for a mime-type amongst parsed media-ranges.

  Find the best match for a given mime-type against a list of media_ranges
  that have already been parsed by parse_media_range(). Returns a tuple of
  the fitness value and the value of the 'q' quality parameter of the best
  match, or (-1, 0) if no match was found. Just as for quality_parsed(),
  'parsed_ranges' must be a list of parsed media ranges.
  """
  best_fitness = -1
  best_fit_q = 0
  (target_type, target_subtype, target_params) =\
  parse_media_range(mime_type)
  for (type, subtype, params) in parsed_ranges:
    type_match = (type == target_type or
                  type == ASTERISK_BYTE or
                  target_type == ASTERISK_BYTE)
    subtype_match = (subtype == target_subtype or
                     subtype == ASTERISK_BYTE or
                     target_subtype == ASTERISK_BYTE)
    if type_match and subtype_match:
      param_matches = reduce(lambda x, y: x + y, [1 for (key, value) in\
                                                  target_params.iteritems() if
                                                  key != 'q' and\
                                                  params.has_key(
                                                    key) and value == params[
                                                                      key]], 0)
      fitness = (type == target_type) and 100 or 0
      fitness += (subtype == target_subtype) and 10 or 0
      fitness += param_matches
      if fitness > best_fitness:
        best_fitness = fitness
        best_fit_q = params['q']

  return best_fitness, float(best_fit_q)


def quality_parsed(mime_type, parsed_ranges):
  """Find the best match for a mime-type amongst parsed media-ranges.

  Find the best match for a given mime-type against a list of media_ranges
  that have already been parsed by parse_media_range(). Returns the 'q'
  quality parameter of the best match, 0 if no match was found. This function
  bahaves the same as quality() except that 'parsed_ranges' must be a list of
  parsed media ranges.
  """

  return fitness_and_quality_parsed(mime_type, parsed_ranges)[1]


def quality(mime_type, ranges):
  """Return the quality ('q') of a mime-type against a list of media-ranges.

  Returns the quality 'q' of a mime-type when compared against the
  media-ranges in ranges. For example:

  >>> quality(b'text/html',b'text/*;q=0.3, text/html;q=0.7,
                text/html;level=1, text/html;level=2;q=0.4, */*;q=0.5')
  0.7

  """
  parsed_ranges = [parse_media_range(r) for r in ranges.split(b(','))]

  return quality_parsed(mime_type, parsed_ranges)


def best_match(supported, header):
  """Return mime-type with the highest quality ('q') from list of candidates.

  Takes a list of supported mime-types and finds the best match for all the
  media-ranges listed in header. The value of header must be a string that
  conforms to the format of the HTTP Accept: header. The value of 'supported'
  is a list of mime-types. The list of supported mime-types should be sorted
  in order of increasing desirability, in case of a situation where there is
  a tie.

  >>> best_match([b'application/xbel+xml', b'text/xml'],
                 b'text/*;q=0.5,*/*; q=0.1')
  b'text/xml'
  """
  split_header = _filter_blank(header.split(b(',')))
  parsed_header = [parse_media_range(r) for r in split_header]
  weighted_matches = []
  pos = 0
  for mime_type in supported:
    weighted_matches.append((fitness_and_quality_parsed(mime_type,
                                                        parsed_header), pos,
                             mime_type))
    pos += 1
  weighted_matches.sort()

  return weighted_matches[-1][0][1] and weighted_matches[-1][2] or EMPTY_BYTE


def _filter_blank(i):
  for s in i:
    if s.strip():
      yield s
