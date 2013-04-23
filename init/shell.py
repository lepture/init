# coding: utf-8

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
        lines = ret.splitlines()

        # remote named origin
        lines = filter(lambda o: o.strip().startswith('origin'), lines)
        if not lines:
            return None

        return lines[0].split()[1]

    @staticmethod
    def pull(cwd=None):
        pass

    @staticmethod
    def checkout(revision='HEAD', cwd=None):
        pass

    @staticmethod
    def clone(url, dest):
        pass
