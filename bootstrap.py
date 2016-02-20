"""Bootstrap dotfiles

Usage:
bootstrap [--dry-run]

Options:
--dry-run    Only print actions

"""

import os
import sh
import docopt
import logging


class Environment(object):
    def __init__(self, dry_run=False):
        self._dry_run = dry_run
        self._log = logging.getLogger('dotfiles')
        self._log.addHandler(logging.StreamHandler())
        self._log.setLevel(logging.DEBUG)
        self._repo_dir = os.path.dirname(os.path.realpath(__file__))
        self._user_dir = os.path.expanduser("~")

    def _get_kwargs(self):
        return {'dry_run': self._dry_run,
                'log': self._log}

    def symlink(self, target, source):
        Symlink(target, source, **self._get_kwargs())()


class Action(object):
    def __init__(self, dry_run, log):
        self._dry_run = dry_run
        self._log = log

    def __call__(self):
        self.pre_exec()
        if not self._dry_run:
            self.exec()
        self.post_exec()

    def pre_exec(self):
        pass

    def exec(self):
        pass

    def post_exec(self):
        self._log.info('Done.')


class Symlink(Action):
    def __init__(self, target, source, *args, **kwargs):
        super(Symlink, self).__init__(*args, **kwargs)
        self._target = target
        self._source = source

    def pre_exec(self):
        self._log.info('Creating symlink {} -> {}'.format(
            self._target, self._source))

    def exec(self):
        if not os.path.lexists(self._target):
            os.symlink(self._source, self._target)


def main():
    args = docopt.docopt(__doc__)
    repo_dir = os.path.dirname(os.path.realpath(__file__))
    user_dir = os.path.expanduser("~")
    env = Environment(dry_run=args['--dry-run'])
    subdirs = (node for node in os.listdir(repo_dir)
           if os.path.isdir(node)
           if not node.startswith('.'))

    for subdir in subdirs:
        print("bootstraping {}-related dotfiles...".format(subdir))
        subdir_path = os.path.join(repo_dir, subdir)
        dotfiles = os.listdir(subdir_path)
        for dotfile in dotfiles:
            dotfile_path = os.path.join(subdir_path, dotfile)
            link = os.path.join(user_dir, ".{}".format(dotfile))
            env.symlink(target=link, source=dotfile_path)
    
if __name__ == '__main__':
    main()
