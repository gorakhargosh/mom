#!/usr/bin/env python
# -*- coding: utf-8 -*-


def group(sequence, chunk_size):
    """
    Splits a sequence into a list of sequences each of size specified by
    ``chunk_size``.

    :param sequence:
        The sequence to split.
    :param chunk_size:
        The chunk size.
    :returns:
        Generates a list of sequences each of size ``chunk_size``.
    """
    for i in xrange(0, len(sequence), chunk_size):
        yield sequence[i:i+chunk_size]
    #return [sequence[i:i+chunk_size]
    #        for i in xrange(0, len(sequence), chunk_size)]
