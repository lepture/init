Init: for a simple life
=======================

Init is a program to init a package folder structure.


Installation
------------

It is easy to install with pip::

    $ sudo pip install init

If you don't have pip, you can install it with easy_install::

    $ sudo easy_install init


How to Use
----------

Take an example of a python package, let's call it a ``fool``::

    $ mkdir fool
    $ init python

And answer the questions, you will everything you need for a python package.


Templates
---------

You can find all offical templates on `init-template@github`_.

.. _`init-template@github`: https://github.com/init-template

You can also use your own templates::

    $ init {github username}/{github repo}
