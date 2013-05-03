# coding: utf-8

import os

TEMPLATE_DIR = os.environ.get(
    'INIT_TEMPLATE', os.path.expanduser('~/.init-template')
)

import sys
import shutil
import datetime
from terminal import color, prompt, confirm
from terminal.builtin import log
from . import license, git, prompts
from .template import Template

try:
    import simplejson as json
except ImportError:
    import json

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


__all__ = ('install', 'init', 'templates')


def install(name):
    """
    Install or update a template from Git repo.
    """
    folder = os.path.join(TEMPLATE_DIR, name)
    if os.path.exists(folder):
        origin = git.origin(folder)
        if not origin:
            raise RuntimeError('%s has no origin remote' % name)
        log.info('git pull', color.cyan(origin))
        return git.pull(cwd=folder)
    url = _url(name)
    log.info('git clone', color.cyan(url))
    return git.clone(url, folder)


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
    if not os.path.exists(folder):
        install(name)

    log.info('loading', color.cyan(name))

    template = None
    for name in ['template.yml', 'template.yaml', 'template']:
        template = os.path.join(folder, name)
        if os.path.exists(template):
            break

    if not template:
        log.error('template not found.')
        return

    config = _get_config(template)

    if 'register' in config and os.path.exists(config['register']):
        q = confirm(
            'This is not an empty directory, do you want to rewrite it'
        )
        if not q:
            return sys.exit(2)

    # a blank line for seprating the logs and prompts
    print('')
    data = process_prompts(config)
    print('')

    # write from templates
    process_write(os.path.join(folder, 'root'), data)

    # create license
    if 'license' in data:
        process_license(data['license'], data)

    process_rename(config.get('rename', {}), data)

    footer = config.get('footer')
    if isinstance(footer, (list, tuple)):
        footer = '\n'.join(footer)

    if footer:
        print('\n%s\n' % footer)
    return


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


def process_prompts(config):
    data = {}

    if 'language' in config and hasattr(prompts, config['language']):
        fn = getattr(prompts, config['language'])
        data = fn()

    if 'prompt' not in config:
        return data

    defaults = prompts.defaults()
    questions = config['prompt']
    for key in questions:
        value = questions[key]
        default = None
        if isinstance(value, dict):
            message = value.get('message')
            default = value.get('default')
        else:
            message = value

        if default and '{{' in default:
            default = Template(default).render(**defaults)

        data[key] = prompt(message, default=default)

    return data


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
    dirs = os.listdir(filepath)
    return 'template.yml' in dirs or 'template.yaml' in dirs


def _get_config(template):
    f = open(template)
    config = yaml.load(f, _InitLoader)
    f.close()
    return config


class _InitLoader(Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.

    Gist from: https://gist.github.com/enaeseth/844388
    """

    def __init__(self, *args, **kwargs):
        Loader.__init__(self, *args, **kwargs)

        self.add_constructor(
            'tag:yaml.org,2002:map', type(self).construct_yaml_map
        )
        self.add_constructor(
            'tag:yaml.org,2002:omap', type(self).construct_yaml_map
        )

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None, None,
                'expected a mapping node, but found %s' % node.id,
                node.start_mark
            )

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError(
                    'while constructing a mapping',
                    node.start_mark,
                    'found unacceptable key (%s)' % exc,
                    key_node.start_mark
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping
