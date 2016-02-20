"""Bootstrap dotfiles

Usage:
bootstrap [--dry-run]

Options:
--dry-run    Only print actions

"""

import os
import sh
import shlex
import docopt
import shutil
import logging
import pathlib
import subprocess


class Environment(object):
    def __init__(self, dry_run=False):
        self._dry_run = dry_run
        self._log = logging.getLogger('dotfiles')
        self._log.addHandler(logging.StreamHandler())
        self._log.setLevel(logging.DEBUG)
        self._repo_dir = pathlib.Path(__file__).resolve().parent
        self._user_dir = pathlib.Path(os.path.expanduser('~'))
        self._cwd = [self._repo_dir]

    def _get_kwargs(self):
        return {'env': self}

    def symlink(self, target, source):
        Symlink(target, source, **self._get_kwargs())()
        
    def symlink_in_userdir(self, source):
        target_name = '.{}'.format(source)
        target = self._user_dir / target_name
        self.symlink(target, self.get_relative_to_cwd(source))

    def mkdir(self, target):
        MakeDir(self._user_dir / target, **self._get_kwargs())()

    def pushd(self, dir):
        self._cwd.append(self.get_cwd() / dir)

    def popd(self):
        assert len(self._cwd) > 1
        self._cwd.pop()

    def get_cwd(self) -> pathlib.Path:
        return self._cwd[-1]

    def get_relative_to_user(self, path):
        return self._user_dir / path

    def get_relative_to_cwd(self, path):
        return self.get_cwd() / path

    def run_cmd(self, cmd):
        RunCmd(cmd, **self._get_kwargs())()


class Action(object):
    def __init__(self, env):
        self._dry_run = env._dry_run
        self._log = env._log
        self._env = env

    def __call__(self):
        self._log.info('')
        self.pre_exec()
        if not self._dry_run:
            self.exec()
        self.post_exec()

    def pre_exec(self):
        pass

    def exec(self):
        pass

    def post_exec(self):
        pass


class Symlink(Action):
    def __init__(self, target, source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target = target
        self._source = source

    def pre_exec(self):
        self._log.info('Creating symlink {} -> {}'.format(
            self._target, self._source))

    def exec(self):
        try:
            self._target.symlink_to(self._source)
        except FileExistsError as e:
            self._log.warning(e.strerror)


class MakeDir(Action):
    def __init__(self, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target = pathlib.Path(target)

    def pre_exec(self):
        self._log.info('Creating directory {}'.format(self._target))

    def exec(self):
        try:
            self._target.mkdir()
        except FileExistsError as e:
            self._log.warning(e.strerror)


class RunCmd(Action):
    def __init__(self, cmd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cmd = cmd

    def pre_exec(self):
        self._log.info('Running shell command: {}'.format(self._cmd))

    def exec(self):
        subprocess.check_call(shlex.split(self._cmd), cwd=str(self._env.get_cwd()))


def bootstrap_vim(env: Environment) -> None:
    env.pushd('vim')
    env.run_cmd('sudo apt-get install vim')
    env.symlink_in_userdir('vimrc')
    env.mkdir('.vim')
    for dir in ('backup', 'tmp', 'undodir'):
        env.mkdir(env.get_relative_to_user('.vim') / dir)
    env.symlink(target=env.get_relative_to_user('.vim/colors'), 
                source=env.get_relative_to_cwd('colors'))
    env.popd()


def bootstrap_zsh(env: Environment) -> None:
    pass


def bootstrap_bash(env: Environment) -> None:
    pass


def bootstrap_history_search(env: Environment) -> None:
    pass


def main():
    args = docopt.docopt(__doc__)
    repo_dir = os.path.dirname(os.path.realpath(__file__))
    user_dir = os.path.expanduser("~")
    env = Environment(dry_run=args['--dry-run'])

    bootstrap_vim(env)

    subdirs = (node for node in os.listdir(repo_dir)
           if os.path.isdir(node)
           if not node.startswith('.'))
    
    
if __name__ == '__main__':
    main()
