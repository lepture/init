# coding: utf-8

import os
from .template import Template

LICEDIR = os.path.join(os.path.dirname(__file__), 'licenses')

__all__ = ('read', 'licenses', 'parse')


def _find(name):
    if not name.endswith('.txt'):
        name = '%s.txt' % name

    filepath = os.path.join(LICEDIR, name.lower())

    if not os.path.exists(filepath):
        return None
    return filepath


def read(name):
    """
    Read a builtin license.
    """
    filepath = _find(name)
    if not filepath:
        return None
    with open(filepath) as f:
        return f.read()


def licenses():
    """
    List all builtin licenses.
    """
    files = os.listdir(LICEDIR)
    files = filter(lambda name: name.endswith('.txt'), files)
    return map(lambda name: name[:-4], files)


def parse(name, **kwargs):
    """
    Parse the license, fill data into the license.
    """
    filepath = _find(name)
    if not filepath:
        return None
    t = Template(filepath=filepath)
    return t.render(**kwargs)
