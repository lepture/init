# coding: utf-8

# prompts for common tasks

import os
import sys
import re
from terminal import prompt, confirm
from .shell import Git


def python():
    if os.path.exists('setup.py'):
        q = confirm(
            'This is not an empty directory, do you want to rewrite it'
        )
        if not q:
            return sys.exit(2)

    name = _parse_name()
    project = prompt('Project name', default=name)
    version = prompt('Version', default='0.1.0')
    author_name = prompt('Author name', default=Git.name())
    author_email = prompt('Author email', default=Git.email())
    license = prompt('License', default='BSD3')
    return dict(
        project=project,
        version=version,
        author_name=author_name,
        author_email=author_email,
        license=license
    )


def nodejs():
    if os.path.exists('package.json'):
        q = confirm(
            'This is not an empty directory, do you want to rewrite it'
        )
        if not q:
            return sys.exit(2)

    name = _parse_name()
    username = _parse_username()
    repo = Git.origin()
    if not repo:
        repo = 'git://github.com/%s/%s.git' % (username, name)

    project = prompt('Project name', default=name)
    description = prompt('Description', default=name)
    version = prompt('Version', default='0.1.0')
    repository = prompt('Git repository', default=repo)

    home = _parse_homepage(repository)
    homepage = prompt('Homepage', default=home)

    issues = prompt('Issue tracker', default='%/issues' % home)
    author_name = prompt('Author name', default=Git.name())
    author_email = prompt('Author email', default=Git.email())

    license = prompt('License', default='MIT')
    return dict(
        name=project,
        description=description,
        version=version,
        repository=repository,
        homepage=homepage,
        issues=issues,
        author_name=author_name,
        author_email=author_email,
        license=license
    )


def _parse_name():
    _, name = os.path.split(os.getcwd())
    return name


def _parse_username():
    return os.environ.get('USER') or os.environ.get('USERNAME')


def _parse_homepage(repository):
    home = re.sub('^git@', 'https://', repository)
    home = re.sub('^git:\/\/', 'https://', home)
    home = re.sub('\.git$', '', home)
    return home
