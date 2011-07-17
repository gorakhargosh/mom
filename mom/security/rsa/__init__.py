#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: mom.security.rsa
:synopsis: Factory functions for RSA public and private keys.

Encoded key parsing
-------------------
.. autofunction:: parse_private_key
.. autofunction:: parse_public_key
"""

from __future__ import absolute_import

__license__ = """\
The Apache Licence, Version 2.0

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

__author__ = ", ".join([
    "Yesudeep Mangalapilly",
])


from mom.security.codec import private_key_pem_decode, public_key_pem_decode

try:
    from mom.security.rsa.pycrypto import PrivateKey, PublicKey
except ImportError:
    PrivateKey = None
    PublicKey = None
    raise NotImplementedError("RSA implementation not found.")

__all__ = [
    "parse_private_key",
    "parse_public_key",
]

def parse_private_key(encoded_key, encoding="PEM"):
    """
    Parses a private key in the given format.

    :param encoded_key:
        The encoded key.
    :param encoding:
        The encoding used to encode the key. Default "PEM".
    """
    encoding = encoding.upper()
    if encoding == "PEM":
        key_info = private_key_pem_decode(encoded_key)
    else:
        raise NotImplementedError("Key encoding not supported.")
    key = PrivateKey(key_info, encoded_key, encoding)
    return key


def parse_public_key(encoded_key, encoding="PEM"):
    """
    Parses a public key in the given format.

    :param encoded_key:
        The encoded key.
    :param encoding:
        The encoding used to encode the key. Default "PEM".
    """
    encoding = encoding.upper()
    if encoding == "PEM":
        key_info = public_key_pem_decode(encoded_key)
    else:
        raise NotImplementedError("Key encoding not supported.")
    key = PublicKey(key_info, encoded_key, encoding)
    return key
