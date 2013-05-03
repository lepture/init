# coding: utf-8

import os
from terminal.builtin import log
from subprocess import Popen, PIPE


def shell(argv, cwd=None, input=None):
    """
    Run a shell command, get the response from stdout.
    """

    if not isinstance(argv, (list, tuple)):
        argv = argv.split()

    try:
        p = Popen(argv, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            log.error("Maybe you haven't installed", argv[0])
        else:
            log.error(e)
        return None

    stdout, stderr = p.communicate(input=input)
    if stderr:
        # log.error(stderr.decode())
        return None

    return stdout.decode()


def origin(cwd=None):
    """
    Get the git origin url from a repo
    """

    ret = shell('git remote -v', cwd=cwd)
    if not ret:
        return None

    lines = ret.splitlines()

    # remote named origin
    lines = filter(lambda o: o.strip().startswith('origin'), lines)
    if not lines:
        return None

    return lines[0].split()[1]


def pull(remote='origin', branch='master', cwd=None):
    """
    Pull a git repo.
    """
    return shell('git pull %s %s' % (remote, branch), cwd=cwd)


def checkout(revision='HEAD', cwd=None):
    """
    Checkout the git repo to a revision.
    """
    return shell('git checkout %s' % revision, cwd=cwd)


def clone(url, dest, depth=50):
    """
    Clone a git repo.
    """
    return shell(
        'git clone %s %s --recursive --depth %s' % (url, dest, depth)
    )


def name():
    """
    Name in Git config.
    """
    name = shell('git config --get user.name')
    return name.strip()


def email():
    """
    Email in Git config.
    """
    email = shell('git config --get user.email')
    return email.strip()
