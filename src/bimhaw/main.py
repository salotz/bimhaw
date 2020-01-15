from invoke import task, Collection

import os
import os.path as osp
from pathlib import Path

from bimhaw import CONFIG_DIR
import bimhaw.config as config
from bimhaw.profile import write_profile

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

@task
def ls(cx, name):

    bimhaw_p = Path(osp.expandvars("$BIMHAW_DIR"))

    mods = [mod for mod in os.listdir(bimhaw_p / f"lib/{name}")
              if not mod_ignored(mod)]

    print('\n'.join(mods))


## Setups

# modules that get run once per environment (.e.g on new install of
# OS) such as installing packages or setting up directories etc.



# @task()
# def setups_ls(cx):

#     setups = list_modules('setups')

#     print('\n'.join(setups))


# setups_ns = Collection()
# setups_ns.add_task(setups_ls, name='ls')
# setups_ns.add_task(setups_run, name='run')

# ## Inits

# # modules that get run per session but manually so

# inits_ns = Collection()
# inits_ns.add_task(inits_ls, name='ls')
# inits_ns.add_task(inits_run, name='run')

# ## Bins

# # executables that are callable from bimhaw. Can use to organize those
# # scripts in the "misc" folder.

# bins_ns = Collection()
# bins_ns.add_task(bin_ls, name='ls')
# bins_ns.add_task(bin_run, name='run')

# ## Check ins/outs

# # scripts to run for different working sets "wsets" for when you
# # arrive at a specific machine. Useful for keeping a large set of git
# # repos in sync or a sneaker-net of updating your computer.

# checkins_ns = Collection()
# checkins_ns.add_task(checkins_ls, name='ls')
# checkins_ns.add_task(checkins_run, name='run')

# checkouts_ns = Collection()
# checkouts_ns.add_task(checkouts_ls, name='ls')
# checkouts_ns.add_task(checkouts_run, name='run')


# ## Configs

# # configurations, just able to show which ones are availabl
# configs_ns = Collection()
# configs_ns.add_task(configs_ls, name='ls')
# configs_ns.add_task(configs_run, name='path')


# ## Resources

# # not configuration, but pure and utter data. For resources scripts in
# # any other module might rely on
# resources_ns = Collection()
# resources_ns.add_task(resources_ls, name='ls')
# resources_ns.add_task(resources_run, name='path')




## Top level
main_ns = Collection()

# namespaces
main_ns.add_collection(profile_ns, name='profile')
# main_ns.add_collection(setups_ns, name='setup')
# main_ns.add_collection(inits_ns, name='init')
# main_ns.add_collection(bins_ns, name='run')
# main_ns.add_collection(checkins_ns, name='checkin')
# main_ns.add_collection(checkouts_ns, name='checkout')
# main_ns.add_collection(configs_ns, name='profile')
# main_ns.add_collection(resources_ns, name='profile')

# individual tasks
tasks = [link_shells, current, ls]
for task in tasks:
    main_ns.add_task(task)


