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

"""
:module: mom.security.codec.pem
:synopsis: PEM/DER conversion utilities.

PEM/DER codec
-------------
.. autofunction:: der_to_pem
.. autofunction:: der_to_pem_certificate
.. autofunction:: der_to_pem_private_key
.. autofunction:: der_to_pem_private_rsa_key
.. autofunction:: der_to_pem_public_key
.. autofunction:: pem_to_der
.. autofunction:: pem_to_der_certificate
.. autofunction:: pem_to_der_private_key
.. autofunction:: pem_to_der_private_rsa_key
.. autofunction:: pem_to_der_public_key

Miscellaneous
-------------
.. autofunction:: cert_time_to_seconds
"""

from __future__ import absolute_import

import functools
import time

from mom import codec


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"

__all__ = [
    "cert_time_to_seconds",
    "der_to_pem",
    "der_to_pem_certificate",
    "der_to_pem_private_key",
    "der_to_pem_private_rsa_key",
    "der_to_pem_public_key",
    "pem_to_der",
    "pem_to_der_certificate",
    "pem_to_der_private_key",
    "pem_to_der_private_rsa_key",
    "pem_to_der_public_key",
    ]


CERT_PEM_HEADER = "-----BEGIN CERTIFICATE-----"
CERT_PEM_FOOTER = "-----END CERTIFICATE-----"

PRIVATE_KEY_PEM_HEADER = "-----BEGIN PRIVATE KEY-----"
PRIVATE_KEY_PEM_FOOTER = "-----END PRIVATE KEY-----"

PUBLIC_KEY_PEM_HEADER = "-----BEGIN PUBLIC KEY-----"
PUBLIC_KEY_PEM_FOOTER = "-----END PUBLIC KEY-----"

RSA_PRIVATE_KEY_PEM_HEADER = "-----BEGIN RSA PRIVATE KEY-----"
RSA_PRIVATE_KEY_PEM_FOOTER = "-----END RSA PRIVATE KEY-----"


def cert_time_to_seconds(cert_time):
  """
  Takes a date-time string in standard ASN1_print form
  ("MON DAY 24HOUR:MINUTE:SEC YEAR TIMEZONE") and return
  a Python time value in seconds past the epoch.

  :param cert_time:
      Time value in the certificate.
  :returns:
      Python time value.
  """
  return time.mktime(time.strptime(cert_time, "%b %d %H:%M:%S %Y GMT"))


def pem_to_der(pem_cert_string, pem_header, pem_footer):
  """
  Extracts the DER as a byte sequence out of an ASCII PEM formatted
  certificate or key.

  Taken from the Python SSL module.

  :param pem_cert_string:
      The PEM certificate or key string.
  :param pem_header:
      The PEM header to find.
  :param pem_footer:
      The PEM footer to find.
  """
  # Be a little lenient.
  pem_cert_string = pem_cert_string.strip()
  if not pem_cert_string.startswith(pem_header):
    raise ValueError("Invalid PEM encoding; must start with %s"
                     % pem_header)
  if not pem_cert_string.endswith(pem_footer):
    raise ValueError("Invalid PEM encoding; must end with %s"
                     % pem_footer)
  encoded = pem_cert_string[len(pem_header):-len(pem_footer)]
  return codec.base64_decode(encoded)


def der_to_pem(der_cert_bytes, pem_header, pem_footer):
  """
  Takes a certificate in binary DER format and returns the
  PEM version of it as a string.

  Taken from the Python SSL module.

  :param der_cert_bytes:
      A byte string of the DER.
  :param pem_header:
      The PEM header to use.
  :param pem_footer:
      The PEM footer to use.
  """
  # Does what base64.b64encode without the `altchars` argument does.
  import textwrap

  encoded = codec.base64_encode(der_cert_bytes)
  return (pem_header + "\n" +
          textwrap.fill(encoded, 64) + "\n" +
          pem_footer + "\n")


# Helper functions. Use these instead of using der_to_per and per_to_der.
pem_to_der_private_key = functools.partial(pem_to_der,
                                           pem_header=PRIVATE_KEY_PEM_HEADER,
                                           pem_footer=PRIVATE_KEY_PEM_FOOTER)
pem_to_der_private_rsa_key = functools.partial(pem_to_der,
                                               pem_header=RSA_PRIVATE_KEY_PEM_HEADER,
                                               pem_footer=RSA_PRIVATE_KEY_PEM_FOOTER)
pem_to_der_public_key = functools.partial(pem_to_der,
                                          pem_header=PUBLIC_KEY_PEM_HEADER,
                                          pem_footer=PUBLIC_KEY_PEM_FOOTER)
pem_to_der_certificate = functools.partial(pem_to_der,
                                           pem_header=CERT_PEM_HEADER,
                                           pem_footer=CERT_PEM_FOOTER)

der_to_pem_private_key = functools.partial(der_to_pem,
                                           pem_header=PRIVATE_KEY_PEM_HEADER,
                                           pem_footer=PRIVATE_KEY_PEM_FOOTER)
der_to_pem_private_rsa_key = functools.partial(der_to_pem,
                                               pem_header=RSA_PRIVATE_KEY_PEM_HEADER,
                                               pem_footer=RSA_PRIVATE_KEY_PEM_FOOTER)
der_to_pem_public_key = functools.partial(der_to_pem,
                                          pem_header=PUBLIC_KEY_PEM_HEADER,
                                          pem_footer=PUBLIC_KEY_PEM_FOOTER)
der_to_pem_certificate = functools.partial(der_to_pem,
                                           pem_header=CERT_PEM_HEADER,
                                           pem_footer=CERT_PEM_FOOTER)
