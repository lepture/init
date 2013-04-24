# coding: utf-8

import os
TEMPLATE_DIR = os.path.expanduser('~/.init-template')


def install(name):
    folder = os.path.join(TEMPLATE_DIR, name)
    if os.path.exists(folder):
        return update(name)


def update(name):
    pass


def create(name):
    pass


def init(template_path, **kwargs):
    """
    The API for ``template.py``.

    The structure of an template::

        template.py
        root/
          ...
        rename.json

    When the template has collected everything it needs, ``template.py`` can
    call the ``init`` method::

        from init.core import init
        init(os.path.dirname(__file__), **data)
    """

    rootdir = os.path.join(template_path, 'root')
    os.walk(rootdir)
