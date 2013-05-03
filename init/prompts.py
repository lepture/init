# coding: utf-8

# prompts for common tasks

import os
import re
from terminal import prompt
from . import git


def defaults():
    _, project = os.path.split(os.getcwd())
    username = os.environ.get('USER') or os.environ.get('USERNAME')

    repository = git.origin()
    if not repository:
        repository = 'git://github.com/%s/%s.git' % (username, project)

    author_name = git.name()
    author_email = git.email()
    return dict(
        project=project,
        username=username,
        repository=repository,
        author_name=author_name,
        author_email=author_email,
    )


def python():
    data = defaults()

    project = prompt('Project name', default=data['project'])
    description = prompt('Description', default='The best python module')
    version = prompt('Version', default='0.1.0')
    author_name = prompt('Author name', default=data['author_name'])
    author_email = prompt('Author email', default=data['author_email'])
    license = prompt('License', default='BSD3')
    return dict(
        project=project,
        description=description,
        version=version,
        author_name=author_name,
        author_email=author_email,
        license=license
    )


def nodejs():
    data = defaults()

    project = prompt('Project name', default=data['project'])
    description = prompt('Description', default='The best node module')
    version = prompt('Version', default='0.1.0')
    repository = prompt('Git repository', default=data['repository'])

    home = _parse_homepage(repository)
    homepage = prompt('Homepage', default=home)

    issues = prompt('Issue tracker', default='%/issues' % home)
    author_name = prompt('Author name', default=data['author_name'])
    author_email = prompt('Author email', default=data['author_email'])

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


def _parse_homepage(repository):
    home = re.sub('^git@', 'https://', repository)
    home = re.sub('^git:\/\/', 'https://', home)
    home = re.sub('\.git$', '', home)
    return home
