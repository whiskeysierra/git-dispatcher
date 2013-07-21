#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import argparse
import git
import os
import shutil
import subprocess
import sys

from clint.textui.colored import yellow, green


# TODO usage/help/description
def parse():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()

    install = commands.add_parser('install')
    install.set_defaults(command='install')
    install.add_argument('version', nargs='?', default='master')

    update = commands.add_parser('update')
    update.set_defaults(command='update')
    update.add_argument('version', nargs='?', default='master')

    uninstall = commands.add_parser('uninstall')
    uninstall.set_defaults(command='uninstall')

    activate = commands.add_parser('activate')
    activate.set_defaults(command='activate')

    deactivate = commands.add_parser('deactivate')
    deactivate.set_defaults(command='deactivate')

    return parser.parse_args()


args = parse()

repo = git.Repo()
root = repo.working_dir
remote = 'git@github.com:whiskeysierra/git-hooks.git'
prefix = '.git-hooks'

local = os.path.join(root, prefix)
dispatcher = os.path.join(local, 'dispatcher.py')
manage = os.path.join(local, 'git-hooks.py')
hooks_directory = os.path.join(root, '.git', 'hooks')


def log(s):
    sys.stdout.write(s + ' ')
    sys.stdout.flush()


def log_result(r='done', color=green):
    sys.stdout.write('[%s]' % color(r) + '\n')


def relativize(path):
    return os.path.relpath(path, root)


def install():
    if os.path.exists(local):
        raise IOError("%s already exists" % prefix)

    log('Installing %s (%s) into %s' % (remote, args.version, prefix))
    repo.git.subtree('add', '--prefix', prefix, '--squash', remote, args.version)
    log_result()

    log("Adding alias 'hooks' to this repository")

    if subprocess.call([manage, 'state']) == 1:
        subprocess.call([manage, 'alias'])
        log_result()
    else:
        log_result('existed', color=yellow)

def update():
    if not os.path.exists(local):
        raise IOError("%s does not exists" % prefix)

    log("Updating %s with %s (%s)" % (prefix, remote, args.version))
    repo.git.subtree('pull', '--prefix', prefix, '--squash', remote, args.version)
    log_result()


def uninstall():
    if not os.path.exists(local):
        raise IOError("%s does not exists", prefix)

    log('Removing git-hooks from %s' % prefix)
    shutil.rmtree(local)
    log_result()

    log("Adding alias 'hooks' to this repository")

    if subprocess.call([manage, 'state']) == 0:
        subprocess.call([manage, 'unalias'])
        log_result()
    else:
        log_result('missing', color=yellow)


def activate():
    subprocess.call([manage, 'link'])


def deactivate():
    subprocess.call([manage, 'unlink'])


actions = {
    'install': install,
    'update': update,
    'uninstall': uninstall,
    'activate': activate,
    'deactivate': deactivate,
}


def unknown():
    raise RuntimeError("Unknown command '%s'" % args.command)


def on_error(message):
    sys.stderr.write(str(message) + '\n')


# see http://www.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3
try:
    action = actions.get(args.command, unknown)
    action()
except git.exc.GitCommandError, e:
    on_error(e.stderr)
    sys.exit(64)
except Exception, e:
    on_error(e)
    sys.exit(70)