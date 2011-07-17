#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.security.hash
:synopsis: Convenient hashing functions.

SHA-1 digests
-------------
.. autofunction:: sha1_digest
.. autofunction:: sha1_hex_digest
.. autofunction:: sha1_base64_digest

MD5 digests
-----------
.. autofunction:: md5_digest
.. autofunction:: md5_hex_digest
.. autofunction:: md5_base64_digest

HMAC-SHA-1 digests
------------------
.. autofunction:: hmac_sha1_digest
.. autofunction:: hmac_sha1_base64_digest

"""

from __future__ import absolute_import

__license__ = """\
The Apache Licence, Version 2.0

Copyright (C) 2005 Trevor Perrin <trevp@trevp.net>
Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__ = "Trevor Perrin, Yesudeep Mangalapilly"


import hashlib
from mom.codec import base64_encode, hex_encode


def sha1_digest(*inputs):
    """
    Calculates a SHA-1 digest of a variable number of inputs.

    :param inputs:
        A variable number of inputs for which the digest will be calculated.
    :returns:
        A byte string containing the SHA-1 message digest.
    """
    hash_func = hashlib.sha1()
    for i in inputs:
        hash_func.update(i)
    return hash_func.digest()


def sha1_hex_digest(*inputs):
    """
    Calculates hexadecimal representation of the SHA-1 digest of a variable
    number of inputs.

    :param inputs:
        A variable number of inputs for which the digest will be calculated.
    :returns:
        Hexadecimal representation of the SHA-1 digest.
    """
    return hex_encode(sha1_digest(*inputs))


def sha1_base64_digest(*inputs):
    """
    Calculates Base-64-encoded SHA-1 digest of a variable
    number of inputs.

    :param inputs:
        A variable number of inputs for which the digest will be calculated.
    :returns:
        Base-64-encoded SHA-1 digest.
    """
    return base64_encode(sha1_digest(*inputs))


def md5_digest(*inputs):
    """
    Calculates a MD5 digest of a variable number of inputs.

    :param inputs:
        A variable number of inputs for which the digest will be calculated.
    :returns:
        A byte string containing the MD5 message digest.
    """
    hash_func = hashlib.md5()
    for i in inputs:
        hash_func.update(i)
    return hash_func.digest()


def md5_hex_digest(*inputs):
    """
    Calculates hexadecimal representation of the MD5 digest of a variable
    number of inputs.

    :param inputs:
        A variable number of inputs for which the digest will be calculated.
    :returns:
        Hexadecimal representation of the MD5 digest.
    """
    return hex_encode(md5_digest(*inputs))


def md5_base64_digest(*inputs):
    """
    Calculates Base-64-encoded MD5 digest of a variable
    number of inputs.

    :param inputs:
        A variable number of inputs for which the digest will be calculated.
    :returns:
        Base-64-encoded MD5 digest.
    """
    return base64_encode(md5_digest(*inputs))


def hmac_sha1_digest(key, data):
    """
    Calculates a HMAC SHA-1 digest.

    :param key:
        The key for the digest.
    :param data:
        The data for which the digest will be calculted.
    :returns:
        HMAC SHA-1 Digest.
    """
    import hmac

    return hmac.new(key, data, hashlib.sha1).digest()


def hmac_sha1_base64_digest(key, data):
    """
    Calculates a base64-encoded HMAC SHA-1 signature.

    :param key:
        The key for the signature.
    :param data:
        The data to be signed.
    :returns:
        Base64-encoded HMAC SHA-1 signature.
    """
    return base64_encode(hmac_sha1_digest(key, data))

