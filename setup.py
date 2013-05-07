#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from email.utils import parseaddr
install_requires = ['terminal', 'PyYaml']
try:
    from collections import OrderedDict
except ImportError:
    install_requires.append('ordereddict')

info = imp.load_source('info', 'init/info.py')
author, author_email = parseaddr(info.AUTHOR)

setup(
    name=info.NAME,
    version=info.VERSION,
    author=author,
    author_email=author_email,
    url=info.REPOSITORY,
    packages=['init'],
    description='init the package directory structure',
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    scripts=['scripts/init'],
    install_requires=install_requires,
    include_package_data=True,
)
