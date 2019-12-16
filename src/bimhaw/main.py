from invoke import task, Collection

import os
import os.path as osp

from bimhaw import CONFIG_DIR
import bimhaw.config as config
from bimhaw.profile import write_profile

## Top Level

@task
def link_shells(cx, force=False):

    force_str = ''
    if force:
        force_str = '-f'

    # run the link commands
    cx.run(f'ln -s -r {force_str} "$HOME/.bimhaw/shell_dotfiles/profile" "$HOME/.profile"')

    cx.run(f'ln -s -r {force_str} "$HOME/.bimhaw/shell_dotfiles/bash_profile" "$HOME/.bash_profile"')

    cx.run(f'ln -s -r {force_str} "$HOME/.bimhaw/shell_dotfiles/bash_logout" "$HOME/.bash_logout"')

    cx.run(f'ln -s -r {force_str} "$HOME/.bimhaw/shell_dotfiles/bashrc" "$HOME/.bashrc"')


## Profile

profile_ns = Collection()

def profile_gen(cx, name='bimhaw'):

    profile_dir = osp.join(CONFIG_DIR, 'profiles')

    write_profile(profile_dir, name)

profile_ns.add_task(task(profile_gen), name='gen')


@task(default=True)
def profile_load(cx, name='bimhaw'):

    # generate the profile
    profile_gen(cx, name=name)

    if name not in config.PROFILES:
        raise ValueError(f"Profile {name} not found")

    cx.run(f'ln -s -r -f -T "$HOME/.bimhaw/profiles/{name}" "$HOME/.bimhaw/active"')

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
tasks = [link_shells,]
for task in tasks:
    main_ns.add_task(task)


