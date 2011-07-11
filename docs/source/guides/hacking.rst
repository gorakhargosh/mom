.. include:: ../global.rst.inc

.. _hacking:

Contributing
============
Welcome hackeratti! So you have got something you would like to see in
|project_name|? Whee. This document will help you get started.

Important URLs
--------------
|project_name| uses git_ to track code history and hosts its `code repository`_
at github_. The `issue tracker`_ is where you can file bug reports and request
features or enhancements to |project_name|.

Before you start
----------------
Ensure your system has the following programs and libraries installed before
beginning to hack:

1. Python_
2. git_
3. ssh

Setting up the Work Environment
-------------------------------
|project_name| makes extensive use of zc.buildout_ to set up its work
environment. You should get familiar with it.

Steps to setting up a clean environment:

1. Fork the `code repository`_ into your github_ account. Let us call you
   ``hackeratti``. That *is* your name innit? Replace ``hackeratti``
   with your own username below if it isn't.

2. Clone your fork and setup your environment::

    $ git clone --recursive git@github.com:hackeratti/mom.git
    $ cd mom
    $ python bootstrap.py --distribute
    $ bin/buildout

.. IMPORTANT:: Re-run ``bin/buildout`` every time you make a change to the
               ``buildout.cfg`` file.

That's it with the setup. Now you're ready to hack on |project_name|.

Enabling Continuous Integration
-------------------------------
The repository checkout contains a script called ``autobuild.sh``
which you should run prior to making changes. It will detect changes to
Python source code or restructuredText documentation files anywhere
in the directory tree and rebuild sphinx_ documentation, run all tests using
unittest2, and generate coverage_ reports.

Start it by issuing this command in the ``mom`` directory
checked out earlier::

    $ tools/autobuild.sh
    ...

Happy hacking!
