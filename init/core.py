# coding: utf-8

import os
TEMPLATE_DIR = os.path.expanduser('~/.init-template')

import imp
import shutil
from terminal import color
from terminal.builtin import log
from .shell import Git
from .template import Template

try:
    import simplejson as json
except ImportError:
    import json


def install(name):
    """
    Install or update a template from Git repo.
    """
    folder = os.path.join(TEMPLATE_DIR, name)
    if os.path.exists(folder):
        origin = Git.origin(folder)
        if not origin:
            raise RuntimeError('%s has no origin remote' % name)
        return Git.pull(cwd=folder)
    url = _url(name)
    return Git.clone(url, folder)


def init(name):
    """
    The main interface for this program.

    Define a template yourself, the folder structure of a template::

        template.py
        config.json (optional)
        root/

    In your ``template.py``, define a ``prompt`` function to collect
    information::

        def main():
            # prompt for user, and get data from user
            # return data
    """
    folder = os.path.join(TEMPLATE_DIR, name)
    m = imp.load_source('main', os.path.join(folder, 'template.py'))
    data = m.main()

    # a blank line for seprating the logs and prompts
    print('')

    c = color.cyan
    rootdir = os.path.join(folder, 'root')

    log.info('rendering', c(folder))
    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            filepath = os.path.join(root, filename)
            dest = os.path.relpath(filepath, rootdir)
            log.verbose.info('processing', c(dest))
            t = Template(filepath=filepath)
            t.write(dest, **data)

    configfile = os.path.join(folder, 'config.json')
    if not os.path.exists(configfile):
        return

    f = open(configfile)
    config = json.load(f)
    f.close()

    renames = config.get('rename', {})
    for k, v in renames.items():
        t = Template(v)
        v = t.render(**data)
        if '{{' in v:
            log.error('error renaming', c(k), 'to', c(v))
        else:
            log.info('renaming', c(k), 'to', c(v))
            shutil.move(k, v)

    #TODO: other configs


def _url(name):
    if '/' in name:
        return 'https://github.com/%s' % name
    return 'https://github.com/init-template/%s' % name
