#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python module that implements a few utilities used throughout our
code base to avoid duplication in multiple projects.

More information at http://github.com/gorakhargosh/mom
"""

from setuptools import setup

setup(
    name="mom",
    version="0.0.1",
    license="Apache Software License 2.0",
    url="http://github.com/gorakhargosh/mom",
    description="Python utility library.",
    long_description=__doc__,
    author="Yesudeep Mangalapilly",
    author_email="yesudeep@gmail.com",
    zip_safe=True,
    platforms="any",
    packages=["mom"],
    include_package_data=True,
    install_requires=[
        "PyCrypto >=2.3",
        "pyasn1 >=0.0.13b",
        # "simplejson",  # For python 2.5
    ],
    keywords=' '.join([
        "python",
        "utilities",
    ]),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha Development Status",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
