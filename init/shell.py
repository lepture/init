# coding: utf-8

import os
from terminal.builtin import log
from subprocess import Popen, PIPE


def run(argv, cwd=None, input=None):
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
        log.error(stderr.decode())
        return None

    return stdout.decode()


class Git(object):
    """
    The interface of Git.
    """

    @staticmethod
    def origin(cwd=None):
        """
        Get the git origin url from a repo
        """

        ret = run('git remote -v', cwd=cwd)
        if not ret:
            return None

        lines = ret.splitlines()

        # remote named origin
        lines = filter(lambda o: o.strip().startswith('origin'), lines)
        if not lines:
            return None

        return lines[0].split()[1]

    @staticmethod
    def pull(remote='origin', branch='master', cwd=None):
        """
        Pull a git repo.
        """
        return run('git pull %s %s' % (remote, branch), cwd=cwd)

    @staticmethod
    def checkout(revision='HEAD', cwd=None):
        """
        Checkout the git repo to a revision.
        """
        return run('git checkout %s' % revision, cwd=cwd)

    @staticmethod
    def clone(url, dest, depth=50):
        """
        Clone a git repo.
        """
        return run(
            'git clone %s %s --recursive --depth %s' % (url, dest, depth)
        )

    @staticmethod
    def name():
        """
        Name in Git config.
        """
        name = run('git config --get user.name')
        return name.strip()

    @staticmethod
    def email():
        """
        Email in Git config.
        """
        email = run('git config --get user.email')
        return email.strip()
