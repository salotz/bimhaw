from invoke import task, Collection

import os
import os.path as osp
from pathlib import Path

from . import (
    CONFIG_DIR,
    LIB_DIRNAME,
    SHELL_DOTFILES_DIRNAME,
    PROFILES_DIRNAME
)

import bimhaw.config as config
from .profile import write_profile

def mod_ignored(filename):

    if filename.endswith('~'):
        return True

## Top Level

@task
def link_shells(cx, force=False):

    force_str = ''
    if force:
        force_str = '-f'

    # run the link commands
    cx.run(f'ln -s -r {force_str} "{CONFIG_DIR}/{SHELL_DOTFILES_DIRNAME}/profile" "$HOME/.profile"')

    cx.run(f'ln -s -r {force_str} "{CONFIG_DIR}/{SHELL_DOTFILES_DIRNAME}/bash_profile" "$HOME/.bash_profile"')

    cx.run(f'ln -s -r {force_str} "{CONFIG_DIR}/{SHELL_DOTFILES_DIRNAME}/bash_logout" "$HOME/.bash_logout"')

    cx.run(f'ln -s -r {force_str} "{CONFIG_DIR}/{SHELL_DOTFILES_DIRNAME}/bashrc" "$HOME/.bashrc"')

@task
def current(cx):

    result = cx.run(f'readlink "{CONFIG_DIR}/active"', hide=True)

    profile_str = result.stdout.strip().split('/')[-1]
    print(profile_str)

## Profile

profile_ns = Collection()

def profile_gen(cx, name='bimhaw'):

    profile_dir = osp.join(CONFIG_DIR, PROFILES_DIRNAME)

    # write out the main shell profile script files with configs in
    # them
    write_profile(profile_dir, name)

    # link the appropriate config files

    # TODO: currently we just link all of them since we don't have a
    # way to select them in the config yet, but we want to make the
    # right API for env variables in scripts
    cx.run(f'ln -f -s -r -T "{CONFIG_DIR}/{LIB_DIRNAME}" "{profile_dir}/{name}/lib"')

profile_ns.add_task(task(profile_gen), name='gen')


@task(default=True)
def profile_load(cx, name='bimhaw'):

    # generate the profile
    profile_gen(cx, name=name)

    if name not in config.PROFILES:
        raise ValueError(f"Profile {name} not found")

    cx.run(f'ln -s -r -f -T "{CONFIG_DIR}/profiles/{name}" "{CONFIG_DIR}/active"')

profile_ns.add_task(profile_load, name='load')

@task
def profile_ls(cx):

    print('\n'.join(config.PROFILES))

profile_ns.add_task(profile_ls, name='ls')

## Top level
main_ns = Collection()

# namespaces
main_ns.add_collection(profile_ns, name='profile')

# individual tasks
tasks = [link_shells, current]
for task in tasks:
    main_ns.add_task(task)


