# coding: utf-8

import os
from .template import Template

LICEDIR = os.path.join(os.path.dirname(__file__), 'licenses')


def read(name):
    """
    Read a builtin license.
    """
    if not name.endswith('.txt'):
        name = '%s.txt' % name

    filepath = os.path.join(LICEDIR, name.lower())

    if not os.path.exists(filepath):
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
    content = read(name)
    if not content:
        return None
    t = Template(content)
    return t.render(**kwargs)
