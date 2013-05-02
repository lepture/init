# coding: utf-8

import os

TEMPLATE_DIR = os.environ.get(
    'INIT_TEMPLATE', os.path.expanduser('~/.init-template')
)

import imp
import shutil
import datetime
from terminal import color
from terminal.builtin import log
from . import license
from .shell import Git
from .template import Template

try:
    import simplejson as json
except ImportError:
    import json


__all__ = ('install', 'init', 'templates')


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
    log.info('loading', color.cyan(name))

    folder = os.path.join(TEMPLATE_DIR, name)
    m = imp.load_source('template', os.path.join(folder, 'template.py'))

    # a blank line for seprating the logs and prompts
    print('')
    data = m.main()
    print('')

    # write from templates
    process_write(os.path.join(folder, 'root'), data)

    # create license
    if 'license' in data:
        process_license(data['license'], data)

    # process via config.json
    configfile = os.path.join(folder, 'config.json')
    if not os.path.exists(configfile):
        return

    f = open(configfile)
    config = json.load(f)
    f.close()

    process_rename(config.get('rename', {}), data)

    #TODO: chmod


def templates():
    ret = []
    for name in os.listdir(TEMPLATE_DIR):
        filepath = os.path.join(TEMPLATE_DIR, name)
        if not os.path.isdir(filepath):
            continue

        if _is_template(filepath):
            ret.append(name)
            continue

        for subname in os.listdir(filepath):
            subpath = os.path.join(filepath, subname)
            if not os.path.isdir(subpath):
                continue
            if _is_template(subpath):
                ret.append('%s/%s' % (name, subname))

    return ret


def process_write(rootdir, data):
    log.info('templates from', color.cyan(rootdir))

    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            filepath = os.path.join(root, filename)
            dest = os.path.relpath(filepath, rootdir)
            log.verbose.info('writing', color.cyan(dest))
            t = Template(filepath=filepath)
            t.write(dest, **data)


def process_license(name, data):
    ORIGIN_NAME = name
    log.info('license', color.cyan(ORIGIN_NAME))
    # reset the name
    name = name.lower()
    if name == 'bsd':
        name = 'bsd3'
    elif name == 'gpl':
        name = 'gpl3'

    if 'organization' not in data:
        username = os.environ.get('USER') or os.environ.get('USERNAME')
        user = data.get('user', username)
        if user:
            data['organization'] = user

    if 'year' not in data:
        data['year'] = str(datetime.datetime.utcnow().year)

    if 'project' not in data and 'name' in data:
        data['project'] = data['name']

    content = license.parse(name, **data)
    if not content:
        return log.warn('license not found', color.cyan(ORIGIN_NAME))
    f = open('LICENSE', 'w')
    f.write(content)
    f.close()


def process_rename(renames, data):
    if not renames:
        return

    c = color.cyan
    for k, v in renames.items():
        t = Template(v)
        v = t.render(**data)
        if '{{' in v:
            log.error('error renaming', c(k), 'to', c(v))
        elif os.path.exists(v):
            log.warn('rewriting', c(v))
            shutil.rmtree(v)
            shutil.move(k, v)
        else:
            log.info('renaming', c(k), 'to', c(v))
            shutil.move(k, v)


def _url(name):
    if '/' in name:
        return 'https://github.com/%s' % name
    return 'https://github.com/init-template/%s' % name


def _is_template(filepath):
    if not os.path.exists(os.path.join(filepath, 'template.py')):
        return False
    return os.path.exists(os.path.join(filepath, 'root'))
