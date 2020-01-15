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

@task
def current(cx):

    result = cx.run('readlink "$HOME/.bimhaw/active"', hide=True)

    profile_str = result.stdout.strip().split('/')[-1]
    print(profile_str)

## Profile

profile_ns = Collection()

def profile_gen(cx, name='bimhaw'):

    profile_dir = osp.join(CONFIG_DIR, 'profiles')

    # write out the main shell profile script files with configs in
    # them
    write_profile(profile_dir, name)

    # link the appropriate config files

    # TODO: currently we just link all of them since we don't have a
    # way to select them in the config yet, but we want to make the
    # right API for env variables in scripts
    cx.run(f'ln -f -s -r -T "$HOME/.bimhaw/lib" "{profile_dir}/lib"')

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


## Setups

# modules that get run once per environment (.e.g on new install of
# OS) such as installing packages or setting up directories etc.

setups_ns = Collection()

## Inits

# modules that get run per session but manually so

inits_ns = Collection()

## Bins

# executables that are callable from bimhaw. Can use to organize those
# scripts in the "misc" folder.

bin_ns = Collection()

## Check ins/outs

# scripts to run for different working sets "wsets" for when you
# arrive at a specific machine. Useful for keeping a large set of git
# repos in sync or a sneaker-net of updating your computer.

checkin_ns = Collection()
checkout_ns = Collection()



## Configs

# configurations, just able to show which ones are available


## Resources

# not configuration, but pure and utter data. For resources scripts in
# any other module might rely on




## Top level
main_ns = Collection()

# namespaces
main_ns.add_collection(profile_ns, name='profile')

# individual tasks
tasks = [link_shells, current,]
for task in tasks:
    main_ns.add_task(task)


